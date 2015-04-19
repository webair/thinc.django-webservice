#!/usr/bin/env python
import os

import sys
import django
from django.conf import settings
from django.test.utils import get_runner


os.environ['DJANGO_SETTINGS_MODULE'] = 'webservice.tests.test_settings'


def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(["webservice"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    runtests()

