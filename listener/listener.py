import sys

from listener import listener_utils as utils
import config

if config.connect_to_server:
    utils.connect_to_server()
stop_listening = utils.listen_continuously()
# wait for an input line. this is done tp prevent the script from exiting.
# on the actual Raspberry pi device, this will most likely not happen because the device will not be connected to a
# screen or keyboard.
for _ in sys.stdin:
    utils.log("stopping recording and speech recognition!", remote=True)
stop_listening(False)

print("Bye bye!")
