import json
import logging
from nose.tools import eq_
from mock import patch

from honeybadger.connection import send_notice
from honeybadger.config import Configuration

def test_connection_success():
    api_key = 'badgerbadgermushroom'
    payload = {'test': 'payload'}
    config = Configuration(api_key=api_key)

    with patch('six.moves.urllib.request.urlopen') as request_mock:
        send_notice(config, payload)

        assert request_mock.called == True
        ((request_object,), mock_kwargs) = request_mock.call_args
        eq_(request_object.get_header('X-api-key'), api_key)
        eq_(request_object.get_full_url(), '{}/v1/notices/'.format(config.endpoint))
        eq_(request_object.data, json.dumps(payload))

# TODO: figure out how to test logging output
