from setuptools import setup
import honeybadger

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='honeybadger',
    version=honeybadger.__version__,
    description='Send Python and Django errors to Honeybadger',
    long_description=readme(),
    url='https://github.com/honeybadger-io/honeybadger-python',
    author='Dave Sullivan',
    author_email='dave@davesullivan.ca',
    license='MIT',
    packages=['honeybadger'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Monitoring'
    ],
    install_requires=[
        'psutil'
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'mocker']
)
