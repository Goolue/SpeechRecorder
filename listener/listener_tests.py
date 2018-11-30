import json
import logging
import unittest

from httmock import HTTMock, urlmatch
from requests import PreparedRequest
import config

from listener import listener_utils as listener

speech_txt = 'some text'
log_txt = 'cannot log this stuff'


@urlmatch(path="/text")
def mock_text(url, request: PreparedRequest):
    print("url:", url, "body", request.body)
    as_json = json.loads(request.body)
    if as_json['text'] == speech_txt and as_json['deviceId'] == config.device_id:
        return json.dumps(True)
    return json.dumps(False)


@urlmatch(path="/connect")
def mock_connect(url, request: PreparedRequest):
    print("url:", url, "body", request.body)
    as_json = json.loads(request.body)
    if as_json['deviceId'] == config.device_id:
        return json.dumps(True)
    return json.dumps(False)


@urlmatch(path="/log")
def mock_log(url, request: PreparedRequest):
    print("url:", url, "body", request.body)
    as_json = json.loads(request.body)
    if as_json['deviceId'] == config.device_id and as_json['text'] == log_txt and as_json['severity'] == logging.ERROR:
        return json.dumps(True)
    return json.dumps(False)


class TestTextListener(unittest.TestCase):
    def test_send_text(self):
        with HTTMock(mock_text):
            res = listener.send_text_to_server(speech_txt)
            self.assertTrue(res)


class TestConnectListener(unittest.TestCase):
    def test_connect(self):
        with HTTMock(mock_connect):
            res = listener.connect_to_server()
            self.assertTrue(res)


class TestLogListener(unittest.TestCase):
    def test_log(self):
        with HTTMock(mock_log):
            res = listener.log(log_txt, logging.ERROR)
            self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
