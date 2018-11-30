import sys
from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def printer():
    print("called")
    return json.dumps(True)


@app.route('/text', methods=['POST'])
def text_post():
    print("text")
    print("headers", request.headers)
    print("data:", request.data)  # looks like binary
    print("json:", request.json)  # has right values! use this!
    print(request.json["deviceId"])
    return json.dumps(True)


@app.route('/connect', methods=['POST'])
def connect():
    print("connect")
    print("headers", request.headers)
    print("data:", request.data)  # looks like binary
    print("json:", request.json)  # has right values! use this!
    print(request.json["deviceId"])
    return json.dumps(True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
