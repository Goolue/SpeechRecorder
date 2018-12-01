import sys
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///speach.sqlite3'
db = SQLAlchemy(app)

class Speach(db.Model):
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
    returnedText = Speach.query.filter(Speach.device_id.like(device_id),Speach.date.contains(req_date)).text()
    return returnedText

@app.route('/text', methods=['POST'])
def text_post():
    print("text_post")
    print("headers", request.headers)
    print("json:", request.json)  # has right values! use this!
    data = Speach(device_id=request.get_json(force=True)["deviceId"],date=datetime.now().isoformat(),text=request.get_json(force=True)["text"])
    db.session.add(data)
    db.session.commit()
    return json.dumps(True)

@app.route('/text', methods=['DELETE'])
def text_delete():
    print("text_delete")
    device_id = request.headers["deviceId"]
    req_date = request.headers["date"]
    Speach.query.filter(Speach.device_id.like(device_id),Speach.date.contains(req_date)).delete()
    db.session.commit()
    return json.dumps(True)


@app.route('/devices', methods=['GET'])
def devices_get():
    print("devices_get")
    returnedText = Speach.query().order_by(desc('date')) ##TODO: need to fix query
    return returnedText

@app.route('/log', methods=['POST'])
def log_post():
    print("log_post")
    print(request.json["deviceId"])
    print("Log Level[%s]: device ID - %s, %s." %(request.json["severity"], request.json["deviceId"],request.json["text"]))
    return json.dumps(True)




@app.route('/connect', methods=['POST'])
def connect():
    print("connect")
    print(request.json["deviceId"])

    return json.dumps(True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    db.create_all()
