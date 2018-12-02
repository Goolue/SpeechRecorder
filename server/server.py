import sys
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///speech.db'
db = SQLAlchemy(app)

class Speech(db.Model):
   device_id = db.Column(db.Integer, primary_key = True)
   date = db.Column(db.DateTime, primary_key = True)
   text = db.Column(db.Text)



@app.route('/', methods=['GET'])
def printer():
    print("called")
    return json.dumps('Server is listening...')


@app.route('/text', methods=['GET'])
def text_get():
    print("text_get")
    device_id = request.headers["deviceId"]
    req_date = request.headers["date"]
    returnedText = Speech.query.filter(Speech.device_id.like(device_id), Speech.date.contains(req_date)).all()
    texts = map(lambda speech: speech.text, returnedText)
    res = ''
    for s in texts:
        res += s + '\n'
    return json.dumps(res)


@app.route('/text', methods=['POST'])
def text_post():
    print("text_post")
    print("headers", request.headers)
    print("json:", request.json)  # has right values! use this!
    data = Speech(device_id=request.get_json(force=True)["deviceId"],date=datetime.now(), text=request.get_json(force=True)["text"])
    db.session.add(data)
    db.session.commit()
    return json.dumps(True)


@app.route('/text', methods=['DELETE'])
def text_delete():
    print("text_delete")
    device_id = request.headers["deviceId"]
    req_date = request.headers["date"]
    returnedText = Speech.query.filter(Speech.device_id.like(device_id), Speech.date.contains(req_date))
    returnedText.delete(synchronize_session='fetch')
    db.session.commit()
    return json.dumps(True)


@app.route('/devices', methods=['GET'])
def devices_get():
    print("devices_get")
    returnedText = db.session.query(Speech.device_id, func.max(Speech.date)).filter().group_by(Speech.device_id).all()
    devices = {res[0]: str(res[1]) for res in returnedText}
    return json.dumps(devices)


@app.route('/log', methods=['POST'])
def log_post():
    print("log_post")
    print(request.json["deviceId"])
    text_ = "Log Level[%s]: device ID - %s, %s." % (request.json["severity"], request.json["deviceId"], request.json["text"])
    print(text_)
    file = open('mic.log','a')
    file.writelines([text_])
    file.close()
    return json.dumps(True)



@app.route('/connect', methods=['POST'])
def connect():
    print("connect")
    print(request.json["deviceId"])
    text_ = "Log Level[INFO]: device ID - %s, connected." % (request.json["deviceId"])
    print(text_)
    file = open('mic.log', 'a')
    file.writelines([text_])
    file.close()
    return json.dumps(True)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')
