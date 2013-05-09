from django.conf import global_settings
from django.utils.http import http_date

import sys
import os
from time import time

from path import path
import dj_database_url

PROJECT_ROOT = path(__file__).abspath().dirname().dirname()
sys.path.insert(0, PROJECT_ROOT / 'libs')
sys.path.insert(0, PROJECT_ROOT / 'apps')

if os.environ.get('DEVELOPMENT'):
    DEBUG = True
else:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['jwpevans.herokuapp.com']

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

# Serving static files.
#Amazon S3 storage settings.
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
#Queries to AWS don't need to be authenicated. They are public!
AWS_QUERYSTRING_AUTH = False
# The browsers won't request the static files for max_age seconds.
# Further reading here. http://developer.yahoo.com/performance/rules.html#expires for more details.
# Based on https://github.com/kylemacfarlane/django-cuddlybuddly-storage-s3/issues/8
# Currently set to 5 mintues
max_age = 60 * 5
# Sets the header in our static files. Expires X seconds (and cache) for X seconds. X is the max_age variable.
AWS_HEADERS = {
    'x-amz-acl': 'public-read',
    'Expires': http_date(time() + max_age),
    'Cache-Control': 'public, max-age=' + str(max_age),
    'Access-Control-Allow-Origin': '*'}

#Storage Backend
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#Causes collect static to automatically put files to s3
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' if DEBUG else 'utils.storage.CachedS3BotoStorage'

COMPRESS_STORAGE = STATICFILES_STORAGE
#Changes the URL structure of the cache from /CACHE/ to /
COMPRESS_OUTPUT_DIR = ''
#The new CDN base URL and update the URLs to the files in your templates which you want to compres
COMPRESS_URL = os.environ.get('AWS_URL')

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT / 'public/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT / 'public/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/' if DEBUG else COMPRESS_URL

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT / 'static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
# Needed for Grappelli
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

#TODO: Remove this?

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT / 'templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # 3rd party apps
    'south',
    'django_extensions',
    'compressor',
    'disqus',
    'gunicorn',
    # Project specific apps go here
    'blog',
    'landing',
    'utils',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + ()

STATICFILES_FINDERS = global_settings.STATICFILES_FINDERS + (
    'compressor.finders.CompressorFinder',
)


# Third-party app settings

# django-compressor
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']

# django-disqus
DISQUS_API_KEY = os.environ.get('DISQUS_API_KEY')
DISQUS_WEBSITE_SHORTNAME = 'jwpevans'

