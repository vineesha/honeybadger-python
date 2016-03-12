from mocker import Mocker, ANY
import json
import logging
from nose.tools import eq_

from honeybadger.connection import send_notice
from honeybadger.config import Configuration

def get_mock_response(status=201):
    m = Mocker()
    response = m.mock()
    response.getcode()
    m.result(status)
    m.replay()
    return response

def test_connection_success():
    api_key = 'badgerbadgermushroom'
    payload = {'test': 'payload'}
    config = Configuration(api_key=api_key)

    def test_request(request):
        eq_(request.get_header('X-api-key'), api_key)
        eq_(request.get_full_url(), '{}/v1/notices/'.format(config.endpoint))
        eq_(request.get_data(), json.dumps(payload))
        return get_mock_response()

    mocker = Mocker()
    urlopen = mocker.replace('urllib2.urlopen')
    urlopen(ANY)
    mocker.call(test_request)
    mocker.replay()

    send_notice(config, payload)

# TODO: figure out how to test logging output
