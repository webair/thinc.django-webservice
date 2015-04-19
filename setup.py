import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-thinc-webservice',
    version='0.1',
    packages=['webservice'],
    include_package_data=True,
    license='MIT License',  # example license
    description='Adds i18n and delta support for models to django-rest-framework',
    long_description=README,
    url='https://github.com/webair/thinc.django.webservice',
    author='Chris Weber',
    author_email='chrisr.weber@gmail.com',
    install_requires=[
    	'djangorestframework >= 3.1.1',
        'Django >= 1.8',
        'pytz >= 2014.10',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    test_suite = "runtests.runtests",
)