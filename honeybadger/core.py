import urllib2

class Honeybadger(object):
    def __init__(self, *args, **kwargs):
        self.api_key = '33a9b24f' # honeybadger python test API key
        self.context = {}

    def exception_hook(self, type, value, traceback):
        pass
        

    def notify(self, text):
        request = urllib2.Request(url="https://api.honeybadger.io/v1/notices/")

        request.add_header('X-Api-Key', self.api_key)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Accept', 'application/json')

        req = urllib2.urlopen(request)

    def configure(self, *args, **kwargs):
        pass

    def set_context(self, *args, **kwargs):
        pass

    def clear_context(self):
        self.context = {}

    def context(self, *args, **kwargs):
        pass
