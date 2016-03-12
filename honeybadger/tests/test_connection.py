import json
import logging
from nose.tools import eq_

from honeybadger.connection import send_notice
from honeybadger.config import Configuration

from .utils import setup_mock_urlopen

def test_connection_success():
    api_key = 'badgerbadgermushroom'
    payload = {'test': 'payload'}
    config = Configuration(api_key=api_key)

    def test_request(request):
        eq_(request.get_header('X-api-key'), api_key)
        eq_(request.get_full_url(), '{}/v1/notices/'.format(config.endpoint))
        eq_(request.get_data(), json.dumps(payload))

    setup_mock_urlopen(test_request)

    send_notice(config, payload)

# TODO: figure out how to test logging output
