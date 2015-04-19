import os
from django.utils.translation import ugettext_lazy as _

LANGUAGE_CODE = 'de-ch'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "webservice.tests.mock_webservice",
]

ROOT_URLCONF = 'webservice.tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'event_service.sqlite3'),
    }
}

LANGUAGES = (
    ('de', _('German')),
    ('en', _('English'))
)