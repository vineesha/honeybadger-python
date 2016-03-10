"""
Name	Type	Default	Description
api_key	string		Required. The project's private API key.
project_root	string	`pwd`	The path to the project's executable code.
environment	string	production	The environment name of the application.
hostname	string	`hostname`	The hostname of the system.
endpoint	string	https://api.honeybadger.io	The base API. Sometimes this is broken up into host, port, ssl, etc. options. Whatever makes sense is fine. The host, port and protocol/scheme should be configurable in any case.
params_filters	array	["password", "password_confirmation", "credit_card"]	A list of keys whose values are replaced with "[FILTERED]" in sensitive data objects (like request parameters).
trace_threshold	integer	2000	The threshold in milliseconds which will cause a trace to be sent to Honeybadger.
"""
import os
import socket

class Configuration(object):
    VALID_OPTIONS = ['api_key', 'project_root', 'environment',
                    'hostname', 'endpoint', 'params_filters', 'trace_threshold']

    def __init__(self, *args, **kwargs):
        self.api_key = ''
        self.project_root = os.getpwd()
        self.enviroment = 'production'
        self.hostname = socket.gethostname()
        self.endpoint = 'https://api.honeybadger.io'
        self.params_filters = ['password', 'password_confirmation', 'credit_card']
        self.trace_threshold = 2000

        self.set_12factor_config()
        self.set_config_from_dict(kwargs)

    def set_12factor_config(self):
        for option in VALID_OPTIONS:
            key = 'HONEYBADGER_{}'.format(option.upper())
            setattr(self, option, os.environ.get(key, getattr(self, option)))

    def set_config_from_dict(self, config):
        for key, value in config.items():
            if key in VALID_OPTIONS:
                setattr(self, key, value)
