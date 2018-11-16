from flask import Flask
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def printer():
    print("called")
    return json.dumps(True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
