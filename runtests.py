#!/usr/bin/env python
import sys

from django.conf import settings
from django import setup


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'comps',
        ),
        SITE_ID=1,
        SECRET_KEY='super-secret',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': (
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.request',
                    ),
                }
            },
        ],
        ROOT_URLCONF='comps.tests.urls',
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
    )


from django.test.utils import get_runner


def runtests():
    setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['comps', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
