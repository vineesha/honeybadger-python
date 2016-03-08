from setuptools import setup
import honeybadger

setup(
    name='honeybadger',
    version=honeybadger.__version__,
    description='Send Python and Django errors to Honeybadger',
    url='https://github.com/honeybadger-io/honeybadger-python',
    author='Dave Sullivan',
    author_email='dave@davesullivan.ca',
    license='MIT',
    packages=['honeybadger'],
    zip_safe=False
)
