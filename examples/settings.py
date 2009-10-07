import os
BASE_DIR = '/'.join(os.path.dirname(__file__).split('/'))
DEBUG = True 
TEMPLATE_DEBUG = DEBUG
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
AUTHENTICATION_BACKENDS=('django.contrib.auth.backends.ModelBackend', )
SECRET_KEY = '#y56vo#ba@k_5m!bd92x=c)!@(kht6pe=d(*m@n0uo=%5i08ry'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
#    'django.template.loaders.app_directories.load_template_source',

)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.doc.XViewMiddleware',
)
ROOT_URLCONF = 'examples.urls'
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
) 

MIXL_PATHS = (
    os.path.join(BASE_DIR, 'css/test'),
    os.path.join(BASE_DIR, 'css/test_library'),
)
GOOGLE_MAPS_API_KEY = "ABQIAAAAw2dNrXRAho8P2gV49EZCExRR6xkh8qLGFJExz59sg03Me4T75BR62a_g73Wrpm6kk3vTzPLZHMlbaw"
DMIGRATIONS_DIR = os.path.join(BASE_DIR, 'migrations')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
TEMPLATE_DIRS = (
	os.path.join(BASE_DIR, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'mixl',
)

DEBUG = True 
TEMPLATE_DEBUG = DEBUG 
ADMINS = (
('admin', 'admin@admin.com'),
)
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'           
DATABASE_NAME = 'mixl_test'             
DATABASE_USER = ''         
DATABASE_PASSWORD = ''         
DATABASE_HOST = ''             
DATABASE_PORT = ''             
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
