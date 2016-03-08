import sys
import traceback

from .version import __version__

def error_payload(exception, exc_traceback):
    tb = traceback.extract_tb(exc_traceback)

    payload = {
        'class': exception.__class__.__name__,
        'message': exception.message,
        'backtrace': [dict(number=f[1], file=f[0], method=f[2]) for f in reversed(tb)],
        'source': {}
    }

    begin_source_line = (tb[-1][1] - 3) >= 0 and tb[-1][1] - 3 or 0

    with open(tb[-1][0], 'r') as f:
        contents = f.readlines()

    end_source_line = (begin_source_line+5 <= len(contents)) and begin_source_line+5 or len(contents)
    payload['source'] = dict(zip(range(begin_source_line+1, end_source_line+1), contents[begin_source_line:end_source_line]))

    return payload

def server_payload():
    return {}

def request_payload(request, context):
    return {
        'context': context
    }

def create_payload(exception, exc_traceback=None, request=None, context={}):
    if exc_traceback is None:
        exc_traceback = sys.exc_info()[2]

    return {
        'notifier': {
            'name': "Honeybadger for Python",
            'url': "https://github.com/honeybadger-io/honeybadger-python",
            'version': __version__
        },
        'error':  error_payload(exception, exc_traceback),
        'server': server_payload(),
        'request': request_payload(request, context),
    }
