import os

from setuptools import setup
from pip.req import parse_requirements

module_dir = os.path.dirname(os.path.realpath(__file__))
pip_requirements = parse_requirements(os.path.join(module_dir, "requirements.txt"), session=False)
requirements = [str(ir.req) for ir in pip_requirements]
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-thinc-webservice',
    version='0.0.2',
    packages=['webservice'],
    include_package_data=True,
    license='MIT License',
    description='Adds i18n and delta support for models to django-rest-framework',
    long_description=README,
    url='https://github.com/webair/thinc.django.webservice',
    author='Chris Weber',
    author_email='chrisr.weber@gmail.com',
    install_requires=[
        'djangorestframework >= 3.1.1',
        'Django >= 1.8',
        'pytz >= 2014.10',
        'django-grappelli >= 2.6.4'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    test_suite="runtests.runtests",
)