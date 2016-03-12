from mocker import Mocker
from mocker import ANY

def setup_mock_urlopen(func, status=201):
    def func_wrap(request):
        func(request)
        return get_mock_response(status)

    mocker = Mocker()
    urlopen = mocker.replace('urllib2.urlopen')
    urlopen(ANY)
    mocker.call(func_wrap)
    mocker.replay()

def get_mock_response(status=201):
    m = Mocker()
    response = m.mock()
    response.getcode()
    m.result(status)
    m.replay()
    return response
