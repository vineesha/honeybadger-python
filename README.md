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

Once set up, all `HttpRequest` objects will have an instance of honeybadger as `request.honeybadger`. See below for public API details.
### All set!

That's it! For additional configuration options, keep reading.

## Configuring with Environment Variables (12-factor style)

All of Honeybadger's configuration options can be set via environment variables with the `HONEYBADGER` prefix. For example, the `api_key` option can be set via the `HONEYBADGER_API_KEY` environment variable.

## Configuration Options

## Public Methods

### `honeybadger.set_context`: Set global context data

This method allows you to send additional information to the Honeybadger API to assist in debugging. This method sets global context data and is additive  - eg. every time you call it, it adds to the existing set unless you call `reset_context`, documented below.

#### Examples:

```python
# From a Django view
def my_view(request):
  request.honeybadger.set_context(user_id=request.user.id)

# In plain Python
from honeybadger import honeybadger
honeybadger.set_context(my_data='my_value')
```

### `honeybadger.reset_context`: Clear global context data

This method clears the global context dictionary.

#### Examples:

```python
# From a Django view
def my_view(request):
  request.honeybadger.clear_context()

# in Plain Python
from honeybadger import honeybadger
honeybadger.clear_context()
```

### `honeybadger.context`: Python context manager interface

What if you don't want to set global context data? You can use Python context managers to set case-specific contextual information.

#### Examples:

```python
# from a Django view
def my_view(request):
  with request.honeybadger.context(user_email=request.POST.get('user_email', None)):
    form = UserForm(request.POST)
    ...
```

### `honeybadger.configure`: Specify additional configuration options

Allows you to configure honeybadger within your code. Accepts any of the above-listed configuration options as keyword arguments.

#### Example:

```python
honeybadger.configure(api_key='myapikey', project_root='/home/dave/crywolf-django')
```

### `honeybadger.notify`: Send an error notice to Honeybadger

In cases where you'd like to manually send error notices to Honeybadger, this is what you're looking for. You can either pass it an exception as the first argument, or an `error_class`/`error_message` pair of keyword arguments. You can also pass it a custom context dictionary which will get merged with the global context.

#### Examples:

```python
# with an exception
mydict = dict(a=1)
try:
  print mydict['b']
except KeyError, exc:
  honeybadger.notify(exc, context={'foo': 'bar'})

# with custom arguments
honeybadger.notify(error_class='ValueError', error_message='Something bad happened!')
```
