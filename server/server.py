from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def printer():
    print("called")
    return json.dumps(True)


@app.route('/text', methods=['POST'])
def text_get():
    print("data:", request.data)
    print(request.json["deviceId"])
    return json.dumps(True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
