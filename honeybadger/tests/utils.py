from contextlib import contextmanager
from mock import patch

@contextmanager
def mock_urlopen(func, status=201):
    with patch('six.moves.urllib.request.urlopen') as request_mock:
        yield request_mock
        ((request_object,), mock_kwargs) = request_mock.call_args
        func(request_object)
