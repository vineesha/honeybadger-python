import urllib2
import sys
import traceback
import json
class Honeybadger(object):
    def __init__(self, *args, **kwargs):
        # TODO: move into separate Configuration class
        self.config = {
            'api_key': '33a9b24f', # honeybadger python test API key
            'endpoint': 'https://api.honeybadger.io',
        }
        self.context = {}

    # TODO: move into separate Agent class for dispatching requests to the API
    def _send_notice(self, exc_class, exc_message, exc_traceback, context={}):
        request = urllib2.Request(url="{}/v1/notices/".format(self.config.get('endpoint', 'https://api.honeybadger.io')))

        request.add_header('X-Api-Key', self.config.get('api_key', None))
        request.add_header('Content-Type', 'application/json')
        request.add_header('Accept', 'application/json')

        # TODO: move into separate data collector class for building the data packet
        data = {
            'notifier': {
                'name': "Honeybadger for Python",
                'url': "https://github.com/honeybadger-io/honeybadger-python",
                'version': "1.0" # TODO: pull this from setuptools
            },
            'error': {
                'class': exc_class,
                'message': exc_message,
                'backtrace': [],
                'source': {}
            },
            'server': {}
        }

        formatted_tb = traceback.extract_tb(exc_traceback)

        for frame in reversed(formatted_tb):
            data['error']['backtrace'].append({'number': frame[1], 'file': frame[0], 'method': frame[2]})

        source_file = formatted_tb[-1][0]
        source_line = formatted_tb[-1][1]
        f = open(source_file, 'r')
        contents = f.readlines()

        for line in xrange(source_line-3, source_line+2):
            data['error']['source'][line+1] = contents[line]

        request.add_data(json.dumps(data))
        response = urllib2.urlopen(request)

        if response.getcode() != 201:
            print response.info()
            print response.getcode()
            print response.read()
            print "Oops!"

    def exception_hook(self, type, value, traceback):
        self._send_notice(type.__name__, value.message, traceback, context=self.context)

    def notify(self, exception=None, options={}, context={}):
        if exception is None:
            pass
            # TODO: handle user-specified options
        else:
            exc_type  = exception.__class__.__name__
            exc_value = exception.message

        merged_context = self.context
        merged_context.update(context)

        traceback = sys.exc_info()[2]
        self._send_notice(exc_type, exc_value, traceback, context=merged_context)

    def configure(self, **kwargs):
        pass

    def set_context(self, **kwargs):
        self.context.update(kwargs)

    def clear_context(self):
        self.context = {}

    def context(self, **kwargs):
        pass
