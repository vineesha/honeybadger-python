from contextlib import contextmanager

from .connection import send_notice
from .payload import create_payload
from .config import Configuration

class Honeybadger(object):
    def __init__(self, *args, **kwargs):
        self.config = Configuration()
        self.context = {}
        self.request = kwargs.get('request', None)

    def _send_notice(self, exception, exc_traceback=None, context={}):
        payload = create_payload(exception, exc_traceback, request=self.request, config=self.config, context=context)
        send_notice(self.config, payload)

    def exception_hook(self, type, value, exc_traceback):
        self._send_notice(value, exc_traceback, context=self.context)

    def notify(self, *args, **kwargs):
        if kwargs.get('exception', None) is None or len(args) == 0:
            exception = {
                'error_class': kwargs.get('error_class', None),
                'error_message': kwargs.get('error_message', None)
            }
        else:
            exception = kwargs.get('exception', args[0])

        merged_context = self.context
        merged_context.update(kwargs.get('context', {}))

        self._send_notice(exception, context=merged_context)

    def configure(self, **kwargs):
        self.config.set_config_from_dict(kwargs)

    def set_context(self, **kwargs):
        self.context.update(kwargs)

    def reset_context(self):
        self.context = {}

    @contextmanager
    def context(self, **kwargs):
        merged_context = self.context
        merged_context.update(kwargs)

        try:
            yield
        except Exception, e:
            self._send_notice(e, context=merged_context)
