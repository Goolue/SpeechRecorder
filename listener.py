import speech_recognition as sr
import sys
from speech_recognition import Microphone


def callback(recognizer: sr.Recognizer, audio):
    try:
        txt = recognizer.recognize_google(audio, language="he")
        print("text is:", txt)
    except sr.UnknownValueError:
        print("Unknown value")
    except sr.RequestError:
        print("Request error")


mics_lst = sr.Microphone.list_microphone_names()
for i, m in enumerate(mics_lst):
    if m == 'HDA Intel PCH: ALC3223 Analog (hw:1,0)':
        print(m, i)
        mic = Microphone(device_index=i)


recognizer = sr.Recognizer()
# mic = sr.Microphone()
#

# with mic as source:
#     print("adjusting ambient")
#     recognizer.adjust_for_ambient_noise(source, duration=5)
print("listening")
stop_listening = recognizer.listen_in_background(mic, callback=callback, phrase_time_limit=10)

for line in sys.stdin:
    print("stopping")

stop_listening(wait_for_stop=False)

print("Done")
#
# txt = recognizer.recognize_google(audio)
# #
# print("text is:", txt)