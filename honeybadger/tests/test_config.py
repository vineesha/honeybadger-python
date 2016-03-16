import os
from nose.tools import raises

from honeybadger.config import Configuration

def test_12factor_overrides_defaults():
    os.environ['HONEYBADGER_ENVIRONMENT'] = 'staging'
    c = Configuration()
    assert c.environment == 'staging'

def test_args_overrides_defaults():
    c = Configuration(environment='staging')
    assert c.environment == 'staging'

def test_args_overrides_12factor():
    os.environ['HONEYBADGER_ENVIRONMENT'] = 'test'
    c = Configuration(environment='staging')
    assert c.environment == 'staging'

def test_config_var_types_are_accurate():
    os.environ['HONEYBADGER_PARAMS_FILTERS'] = 'password,password_confirm,user_email'
    os.environ['HONEYBADGER_TRACE_THRESHOLD'] = '2500'
    c = Configuration()
    assert c.params_filters == ['password', 'password_confirm', 'user_email']
    assert c.trace_threshold == 2500

@raises(AttributeError)
def test_can_only_set_valid_options():
    c = Configuration(foo='bar')
    print c.foo
