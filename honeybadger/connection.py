import logging
import urllib2
import json

logger = logging.getLogger(__name__)

def send_notice(config, payload):
    request = urllib2.Request(url="{}/v1/notices/".format(config.endpoint))

    if not config.api_key:
        logger.error("Honeybadger API key missing from configuration: cannot report errors.")
        return

    request.add_header('X-Api-Key', config.api_key)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')

    request.add_data(json.dumps(payload)) # request.add_data(str(payload))
    response = urllib2.urlopen(request)

    status = response.getcode()
    if status != 201:
        logger.error("Received error response [{}] from Honeybadger API.".format(status))
