from listener import listener_utils as utils
import config

if config.connect_to_server:
    utils.connect_to_server()
utils.listen_continuously()

print("Bye bye!")
