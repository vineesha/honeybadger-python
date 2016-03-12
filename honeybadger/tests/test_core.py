from honeybadger import honeybadger
from nose.tools import eq_
from mocker import Mocker, ANY

def test_set_context():
    honeybadger.set_context(foo='bar')
    eq_(honeybadger.context, dict(foo='bar'))
    honeybadger.set_context(bar='foo')
    eq_(honeybadger.context, dict(foo='bar', bar='foo'))

def test_notify_with_custom_params():
    def send_notice_wrapper(exception, exc_traceback=None, context={}):
        eq_(exception, dict(error_class='Exceptin', error_message='Test message.'))
        eq_(context, dict(foo='bar'))
        eq_(True, False)
        return None

    mocker = Mocker()
    mock_send_notice = mocker.replace(honeybadger._send_notice)
    mock_send_notice(ANY)
    mocker.call(send_notice_wrapper)
    mocker.replay()

    honeybadger.notify(error_class='Exception', error_message='Test message.', context={'foo': 'bar'})
