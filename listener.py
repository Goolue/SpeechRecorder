import sys

import config
import speech_recognition as sr
from speech_recognition import Microphone


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
        print("text is:", txt)
        # TODO send to server here
    except sr.UnknownValueError:  # happens if the detected phrase is empty (= silence) or cannot be detected
        print("Unknown value")
    except sr.RequestError:
        print("Request error")


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
        raise Exception("No microphone can be found!")

    print("listening!\npress Enter to stop.")
    # stop_listening is a function that when called stops the background listening
    stop_listening = sr.Recognizer().listen_in_background(mic, callback=listening_callback,
                                                          phrase_time_limit=config.recognizer_phrase_time_limit)
    # wait for an input line. this is done tp prevent the script from exiting.
    # on the actual Raspberry pi device, this will most likely not happen because the device will not be connected to a
    # screen or keyboard.
    for _ in sys.stdin:
        print("stopping recording and speech recognition!")
    stop_listening(wait_for_stop=False)


listen_continuously()

print("Bye bye!")
