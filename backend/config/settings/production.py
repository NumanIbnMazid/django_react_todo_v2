import django_on_heroku
from config.settings.common import *

SECRET_KEY = env("SECRET_KEY", default=None)

DEBUG = False

ALLOWED_HOSTS = [os.environ.get("PRODUCTION_HOST")]

ROOT_URLCONF = 'config.production_urls'

APP_BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
REACT_APP_DIR = APP_BASE_DIR / 'frontend'

""" *** Database Configuration *** """
try:
    DATABASES = {
        'default': env.db(),
    }
except Exception as E:
    print("Exception ::=> ", E)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': PosixPath_BASE_DIR / 'db.sqlite3',
        }
    }
    
print("******* CONNECTED DATABASES::=> ", DATABASES)

INSTALLED_APPS.extend(["whitenoise.runserver_nostatic"])

# Must insert after SecurityMiddleware, which is first in settings/common.py
if not "whitenoise.middleware.WhiteNoiseMiddleware" in MIDDLEWARE:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

TEMPLATES[0]["DIRS"] = [os.path.join(REACT_APP_DIR, "frontend", "build")]

STATICFILES_DIRS = [
    os.path.join(REACT_APP_DIR, 'build', 'static')
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(PosixPath_BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(PosixPath_BASE_DIR, 'media/')

STATIC_URL = "/static/"
MEDIA_URL = '/media/'

WHITENOISE_ROOT = os.path.join(REACT_APP_DIR, "frontend", "build", "root")


# Activate Django - Heroku.
django_on_heroku.settings(locals())
# del DATABASES['default']['OPTIONS']['sslmode']
# This is new
options = DATABASES['default'].get('OPTIONS', {})
options.pop('sslmode', None)
