DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'fake_secret'
ROOT_URLCONF = ''

COMPATIBILITY_URL = 'compatibility-mode'
UNSUPPORTED_URL = 'unsupported-browser'

COMPATIBILITY_MODE_BROWSERS = ('7','8')
UNSUPPORTED_BROWSERS = ('6','7','8')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tests/integration_tests.db'
    }
}

INSTALLED_APPS = ()

STATIC_ROOT = 'tests.urls'
STATIC_URL = '/fake_static_url/'
