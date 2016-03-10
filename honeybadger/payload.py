import sys
import traceback
import os
from datetime import datetime

import psutil

from .version import __version__

def filter_dict(data, filter_keys):
    for key in filter_keys:
        if data.has_key(key):
            data[key] = "[FILTERED]"
    return data

def error_payload(exception, exc_traceback, config):
    def _filename(name):
        return name.replace(config.project_root, '[PROJECT_ROOT]')

    tb = traceback.extract_tb(exc_traceback)

    payload = {
        'class': type(exception) is dict and exception['error_class'] or exception.__class.__name__,
        'message': type(exception) is dict and exception['error_message'] or exception.message,
        'backtrace': [dict(number=f[1], file=_filename(f[0]), method=f[2]) for f in reversed(tb)],
        'source': {}
    }

    begin_source_line = (tb[-1][1] - 3) >= 0 and tb[-1][1] - 3 or 0

    with open(tb[-1][0], 'r') as f:
        contents = f.readlines()

    end_source_line = (begin_source_line+5 <= len(contents)) and begin_source_line+5 or len(contents)
    payload['source'] = dict(zip(range(begin_source_line+1, end_source_line+1), contents[begin_source_line:end_source_line]))

    return payload

def server_payload(config):
    payload = {
        'project_root': config.project_root,
        'environment_name': config.environment,
        'hostname': config.hostname,
        'time': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        'pid': os.getpid(),
        'stats': {}
    }

    mem = psutil.virtual_memory()
    loadavg = os.getloadavg()

    free = float(s.free) / 1048576.0
    buffers = hasattr(s, 'buffers') and float(s.buffers) / 1048576.0 or 0.0
    cached = hasattr(s, 'cached') and float(s.cached) / 1048576.0 or 0.0
    total_free = free + buffers + cached


    payload['stats']['mem'] = {
        'total': float(s.total) / 1048576.0, # bytes -> megabytes
        'free': free,
        'buffers': buffers,
        'cached': cached,
        'total_free': total_free
    }

    payload['stats']['load'] = dict(zip(('one', 'five', 'fifteen'), loadavg))

    return payload

def django_request_payload(request, context, config):
    payload = {
        'url': request.build_absolute_uri(),
        'component': request.resolver_match.app_name,
        'action': request.resolver_match.func.__name__,
        'params': {},
        'session': {},
        'cgi_data': dict(request.META),
        'context': context
    }

    if hasattr(request, 'session'):
        payload['session'] = filter_dict(dict(request.session), config.params_filters)

    if request.method == 'POST':
        payload['params'] = filter_dict(dict(request.POST), config.params_filters)
    else:
        payload['params'] = filter_dict(dict(request.GET), config.params_filters)


    return payload

def flask_request_payload(request, context, config):
    return {
        'context': context
    }

def generic_request_payload(request, context, config):
    return {
        'context': context
    }

def create_payload(exception, exc_traceback=None, config=None, request=None, context={}):
    if exc_traceback is None:
        exc_traceback = sys.exc_info()[2]

    if request.__module__ == 'django.http.request':
        request_payload = django_request_payload
    else:
        # TODO: figure out Flask support
        request_payload = generic_request_payload

    return {
        'notifier': {
            'name': "Honeybadger for Python",
            'url': "https://github.com/honeybadger-io/honeybadger-python",
            'version': __version__
        },
        'error':  error_payload(exception, exc_traceback, config),
        'server': server_payload(config),
        'request': request_payload(request, context, config),
    }
