import logging
import urllib2
import json

logger = logging.getLogger(__name__)

def send_notice(config, payload):
    request = urllib2.Request(url="{}/v1/notices/".format(config.get('endpoint', 'https://api.honeybadger.io')))

    if not config.has_key('api_key') or config['api_key'] is None:
        logger.error("Honeybadger API key missing from configuration: cannot report errors.")

    request.add_header('X-Api-Key', config.get('api_key', None))
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')

    request.add_data(json.dumps(payload)) # request.add_data(str(payload))
    response = urllib2.urlopen(request)

    if response.getcode() != 201:
        logger.error("Received error response [{}] from Honeybadger API.".format(response.getcode()))
