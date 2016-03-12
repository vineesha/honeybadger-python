import os
import socket

class Configuration(object):
    VALID_OPTIONS = ['api_key', 'project_root', 'environment',
                    'hostname', 'endpoint', 'params_filters', 'trace_threshold']

    def __init__(self, *args, **kwargs):
        self.api_key = ''
        self.project_root = os.getcwd()
        self.environment = 'production'
        self.hostname = socket.gethostname()
        self.endpoint = 'https://api.honeybadger.io'
        self.params_filters = ['password', 'password_confirmation', 'credit_card']
        self.trace_threshold = 2000

        self.set_12factor_config()
        self.set_config_from_dict(kwargs)

    def set_12factor_config(self):
        for option in self.VALID_OPTIONS:
            key = 'HONEYBADGER_{}'.format(option.upper())
            setattr(self, option, os.environ.get(key, getattr(self, option)))

    def set_config_from_dict(self, config):
        for key, value in config.items():
            if key in self.VALID_OPTIONS:
                setattr(self, key, value)
