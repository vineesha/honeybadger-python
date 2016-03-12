from honeybadger.payload import error_payload
from honeybadger.payload import server_payload
from honeybadger.config import Configuration

from nose.tools import eq_
from mocker import Mocker, ANY
import os
# TODO: figure out how to run Django tests?

def setup_mock_traceback(line_no=5):
    mocker = Mocker()
    obj = mocker.replace('traceback.extract_tb')
    obj(ANY)

    path = os.path.dirname(__file__)
    tb_data = []
    for i in range(1, 3):
        tb_data.append((os.path.join(path, 'file_{}.py'.format(i)), line_no*i, 'method_{}'.format(i)))

    tb_data.append(('/fake/path/fake_file.py', 15, 'fake_method'))
    tb_data.append((os.path.join(path, 'payload_fixture.txt'), line_no, 'fixture_method'))

    mocker.result(tb_data)
    mocker.replay()

def test_error_payload_project_root_replacement():
    setup_mock_traceback()
    config = Configuration(project_root=os.path.dirname(__file__))
    payload = error_payload(dict(error_class='Exception', error_message='Test'), None, config)
    assert payload['backtrace'][0]['file'].startswith('[PROJECT_ROOT]')
    assert payload['backtrace'][1]['file'] == '/fake/path/fake_file.py'

def test_error_payload_source_line_top_of_file():
    setup_mock_traceback(line_no=1)
    config = Configuration()
    payload = error_payload(dict(error_class='Exception', error_message='Test'), None, config)
    expected = dict(zip(range(1, 6), ["Line {}\n".format(x) for x in range(1, 6)]))
    eq_(payload['source'], expected)

def test_error_payload_source_line_bottom_of_file():
    setup_mock_traceback(line_no=10)
    config = Configuration()
    payload = error_payload(dict(error_class='Exception', error_message='Test'), None, config)
    expected = dict(zip(range(6, 11), ["Line {}\n".format(x) for x in range(6, 11)]))
    eq_(payload['source'], expected)

def test_error_payload_source_line_midfile():
    setup_mock_traceback(line_no=5)
    config = Configuration()
    payload = error_payload(dict(error_class='Exception', error_message='Test'), None, config)
    expected = dict(zip(range(3, 8), ["Line {}\n".format(x) for x in range(3, 8)]))
    eq_(payload['source'], expected)

def test_server_payload():
    config = Configuration(project_root=os.path.dirname(__file__), environment='test', hostname='test.local')
    payload = server_payload(config)

    eq_(payload['project_root'], os.path.dirname(__file__))
    eq_(payload['environment_name'], 'test')
    eq_(payload['hostname'], 'test.local')
    eq_(payload['pid'], os.getpid())
    assert type(payload['stats']['mem']['total']) == float
    assert type(payload['stats']['mem']['free']) == float
