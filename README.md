# Honeybadger for Python
When any uncaught exceptions occur, Honeybadger will send the data off to the Honeybadger server specified in your environment.

## Supported Versions

Tested with Django 1.9 and Python 2.7. Django integration is done via middleware and so it should work with almost any version.

## Getting Started

Honeybadger for Python works out of the box with Django with only a few configuration options required. The following is a basic setup - more advanced setup will be described later.

### Install Honeybadger

Install honeybadger with pip.

`$ pip install honeybadger`

### Plain Python

In a plain Python application, simply import honeybadger and configure it with your API key.

```python
from honeybadger import honeybadger
honeybadger.configure(api_key='myapikey')
```

### Django

In a Django application, add the Honeybadger Django middleware to your `MIDDLEWARE_CLASSES` config variable:

```python
MIDDLEWARE_CLASSES = (
  ...
  'honeybadger.middleware.DjangoHoneybadgerMiddleware'
)
```

You'll also need to add a new `HONEYBADGER` config variable to your `settings.py` to specify your API key:

```python
HONEYBADGER = {
  'API_KEY': 'myapikey'
}
```

### All set!

That's it! For additional configuration options, keep reading.
