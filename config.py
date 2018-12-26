connect_to_server = True  # True -> send connection msg to server
is_test = False

mic_name = 'Microsoft LifeCam VX-800: USB Audio (hw:1,0)'  # name of microphone to be used
# mic_name = 'HDA Intel PCH: ALC3223 Analog (hw:1,0)'  # name of microphone to be used

recognizer_lang = 'he'  # speech language to use
recognizer_phrase_time_limit = 10  # maximum number of seconds a sentence can be
noise_adjustment_time = 3

# server parameter configs
server_url = 'http://132.72.23.63'
# server_url = 'http://192.168.1.6'
server_port = '3002'
# server_port = '5000'
device_id = 0
user_name = 'Oded'

listener_log_file = 'listener.log'
