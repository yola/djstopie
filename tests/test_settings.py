DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'fake_secret'
ROOT_URLCONF = 'tests.urls'

UNSUPPORTED_URL = '/unsupported-browser'

LAST_SUPPORTED_MODE = 9
LAST_SUPPORTED_BROWSER = 9


DATABASES = {}

INSTALLED_APPS = ()

STATIC_ROOT = 'tests.urls'
STATIC_URL = '/fake_static_url/'

MEDIA_URL = '/media/'

WHITELISTED_URL_PATHS = ('/js', '/i18n')
