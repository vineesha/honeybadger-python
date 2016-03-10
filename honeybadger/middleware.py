from .core import Honeybadger

class DjangoHoneybadgerMiddleware(object):
    def process_request(self, request):
        request.honeybadger = Honeybadger(request=request)

        from django.conf import settings
        config_kwargs = dict([(k.lower(), v) for k, v in getattr(settings, 'HONEYBADGER', {}).items()])
        request.honeybadger.configure(**config_kwargs)

        return None

    def process_exception(self, request, exception):
        request.honeybadger.notify(exception)
        return None

# TODO: finish Flask support
class FlaskHoneybadgerMiddleware(object):
    def __init__(self, app, **kwargs):
        raise NotImplemented
        # return app
