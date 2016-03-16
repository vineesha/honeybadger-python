from contextlib import contextmanager
import threading

from .connection import send_notice
from .payload import create_payload
from .config import Configuration

class Honeybadger(object):
    def __init__(self):
        self.config = Configuration()
        self._context = {}
        self.thread_local = threading.local()
        self.thread_local.request = None

    def _send_notice(self, exception, exc_traceback=None, context={}):
        payload = create_payload(exception, exc_traceback, request=self.thread_local.request, config=self.config, context=context)
        send_notice(self.config, payload)

    def request(self, request):
        self.thread_local.request = request

    def exception_hook(self, type, value, exc_traceback):
        self._send_notice(value, exc_traceback, context=self._context)

    def notify(self, exception=None, error_class=None, error_message=None, context={}):
        if exception is None:
            exception = {
                'error_class': error_class,
                'error_message': error_message
            }

        merged_context = self._context
        merged_context.update(context)

        self._send_notice(exception, context=merged_context)

    def configure(self, **kwargs):
        self.config.set_config_from_dict(kwargs)

    def set_context(self, **kwargs):
        self._context.update(kwargs)

    def reset_context(self):
        self._context = {}

    @contextmanager
    def context(self, **kwargs):
        merged_context = self._context
        merged_context.update(kwargs)

        try:
            yield
        except Exception, e:
            self._send_notice(e, context=merged_context)
            raise
