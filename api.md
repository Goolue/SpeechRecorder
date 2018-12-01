## raspberry to server:
**POSTs use Body, GETs use Payload

#### raspberry -> server:

| Method        | URL         | Body (json) example  					                    | Description                                                                      | Response example
| ------------- |:------------| -----: 							  			                    | ---: 		                                                                       | ---: 
|POST           | /text 	  | {"deviceId": 1, "text": "some text"}                            | send speech as text to server                                                    | "True"
|POST           | /log        | {"deviceId": 1, "text": "no mic found!", "severity": "ERROR"}	| remote logging for device                                                        | "True"
|POST           | /connect    | {"deviceId": 1}                             	                | notify server of device connection                                               | "True"

#### client -> server:

| Method        | URL         | Body (json) example  					                    | Description                                                                      | Response example
| ------------- |:------------| -----: 							  			                    | ---: 		                                                                       | ---: 
|DELETE         | /text 	  | {"deviceId": 1, "date": "2018-11-29 12:46:49.256393"}           | delete all text sent by a device on a specific date                              | "True"
|GET  			| /text       | deviceId=1, date=2018-11-29	    								| get all speech as text for a specific device at a specific date (concatenated)   | "a lot of speech"
|GET  			| /devices    | 								                    			| get a dictionary of deviceId -> last connection date                             | {1: "2018-11-29 12:46:49.256393"}

