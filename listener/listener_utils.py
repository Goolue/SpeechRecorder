import sys
import config
import speech_recognition as sr
from speech_recognition import Microphone
import requests
import logging


def setup_logger() -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG)
    log_handler = logging.FileHandler(config.listener_log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    logger_res = logging.getLogger()
    logger_res.addHandler(log_handler)
    return logger_res


server_url = config.server_url + ':' + config.server_port + '/'
logger = setup_logger()


def connect_to_server() -> bool:
    body = {"deviceId": config.device_id}
    try:
        res = requests.post(server_url + 'connect', json=body)
        return res.text == 'true'
    except Exception as e:
        logger.error("Could not connect to server {0}, {1}".format(server_url, e))
        exit(1)


def send_text_to_server(txt: str) -> bool:
    body = {"deviceId": config.device_id, "text": txt}
    try:
        log("trying to send text '" + txt + "' to server", remote=False)
        res = requests.post(server_url + 'text', json=body)
        return res.text == 'true'
    except Exception as e:
        print("text is:", txt)
        logger.error("Could not send text to server {0}, {1}".format(server_url, e))
        return False


def log(msg: str, level: int = logging.INFO, remote: bool = True) -> bool:
    print("logging msg:", msg)
    {
        logging.INFO: logger.info,
        logging.ERROR: logger.error
    }.get(level, print)(msg)
    if not remote:
        return True
    else:
        try:
            body = {"deviceId": config.device_id, "text": msg, "severity": level}
            res = requests.post(server_url + 'log', json=body)
            return res.text == 'true'
        except Exception as e:
            logger.error("Could not log msg {0} remotely to url: {1}. error is: {2}".format(msg, server_url, e))
            return False


def listening_callback(recognizer: sr.Recognizer, audio) -> None:
    """
    Callback to be called when a phrase was recorded
    :param recognizer: sr.Recognizer to be used
    :param audio: phrase as audio
    """

    try:
        # try to use Google speech recognition to extract the text.
        # the Google one works best (out of the free ones)
        txt = recognizer.recognize_google(audio, language=config.recognizer_lang)
        # print("text is:", txt)
        log("text is: {0}".format(txt), remote=False)
        send_text_to_server(txt)
    except sr.UnknownValueError:  # happens if the detected phrase is empty (= silence) or cannot be detected
        log("Unknown value", level=logging.ERROR, remote=False)
    except sr.RequestError:
        log("Request error", level=logging.ERROR)


def listen_continuously() -> None:
    """
    Listen for speech continuously, send each sentence to a speech-to-text converter, then send the text to the server.
    Sentences are detected by pauses in the speech.
    """

    # look for the microphone specified in config file
    mics_lst = sr.Microphone.list_microphone_names()
    mic = None
    for i, m in enumerate(mics_lst):
        if m == config.mic_name:
            mic = Microphone(device_index=i)
    if mic is None:
        msg = "No microphone can be found!"
        log(msg, level=logging.ERROR, remote=False)
        raise Exception(msg)

    recognizer = sr.Recognizer()
    print("adjusting")
    log("adjusting to noise for {0} sec".format(config.noise_adjustment_time), remote=False)
    with mic as source:
        recognizer.adjust_for_ambient_noise(duration=config.noise_adjustment_time, source=source)

    log("listening!\npress Enter to stop.", remote=False)
    # stop_listening is a function that when called stops the background listening
    stop_listening = recognizer.listen_in_background(mic, callback=listening_callback,
                                                     phrase_time_limit=config.recognizer_phrase_time_limit)
    # wait for an input line. this is done tp prevent the script from exiting.
    # on the actual Raspberry pi device, this will most likely not happen because the device will not be connected to a
    # screen or keyboard.
    for _ in sys.stdin:
        log("stopping recording and speech recognition!", remote=True)
    stop_listening(wait_for_stop=False)
