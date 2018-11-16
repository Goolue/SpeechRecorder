import sys

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
        txt = recognizer.recognize_google(audio, language="he")
        print("text is:", txt)
        # TODO send to server here
    except sr.UnknownValueError:  # happens if the detected phrase is empty (= silence) or cannot be detected
        print("Unknown value")
    except sr.RequestError:
        print("Request error")


mics_lst = sr.Microphone.list_microphone_names()
mic = None
for i, m in enumerate(mics_lst):
    # TODO: change this str to be configurable
    if m == 'HDA Intel PCH: ALC3223 Analog (hw:1,0)':
        print(m, i)
        mic = Microphone(device_index=i)

if mic is None:
    raise Exception("No microphone can be found!")

print("listening")
# stop_listening is a function that when called stops the background listening
stop_listening = sr.Recognizer().listen_in_background(mic, callback=listening_callback, phrase_time_limit=10)

# wait for an input line. this is done tp prevent the script from exiting
for line in sys.stdin:
    print("stopping")

stop_listening(wait_for_stop=False)

print("Exiting!")
