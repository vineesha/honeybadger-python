import json

from nose.tools import eq_, ok_
from nose.tools import raises

from .utils import mock_urlopen
from honeybadger import Honeybadger

def test_set_context():
    honeybadger = Honeybadger()
    honeybadger.set_context(foo='bar')
    eq_(honeybadger.thread_local.context, dict(foo='bar'))
    honeybadger.set_context(bar='foo')
    eq_(honeybadger.thread_local.context, dict(foo='bar', bar='foo'))


def test_notify_with_custom_params():
    def test_payload(request):
        payload = json.loads(request.data)
        eq_(payload['request']['context'], dict(foo='bar'))
        eq_(payload['error']['class'], 'Exception')
        eq_(payload['error']['message'], 'Test message.')

    hb = Honeybadger()

    with mock_urlopen(test_payload) as request_mock:
        hb.configure(api_key='aaa')
        hb.notify(error_class='Exception', error_message='Test message.', context={'foo': 'bar'})
        eq_(request_mock.call_count, 1)



def test_notify_with_exception():
    def test_payload(request):
        payload = json.loads(request.data)
        eq_(payload['error']['class'], 'ValueError')
        eq_(payload['error']['message'], 'Test value error.')

    hb = Honeybadger()

    with mock_urlopen(test_payload) as request_mock:
        hb.configure(api_key='aaa')
        hb.notify(ValueError('Test value error.'))
        eq_(request_mock.call_count, 1)

def test_notify_context_merging():
    def test_payload(request):
        payload = json.loads(request.data)
        eq_(payload['request']['context'], dict(foo='bar', bar='foo'))

    hb = Honeybadger()

    with mock_urlopen(test_payload) as request_mock:
        hb.configure(api_key='aaa')
        hb.set_context(foo='bar')
        hb.notify(error_class='Exception', error_message='Test.', context=dict(bar='foo'))
        eq_(request_mock.call_count, 1)
