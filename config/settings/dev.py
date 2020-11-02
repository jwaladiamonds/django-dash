from .default import *
from django.contrib import messages


INSTALLED_APPS += [
    'crispy_forms',
    'sorl.thumbnail',
    'accounts',
    'dashboard',
    'core',
]

GMAIL_USER = "Django Verifier"
GMAIL_SECRET = env('GMAIL_SECRET', default='')
GMAIL_SCOPES = env.list('GMAIL_SCOPES', default=[])
GMAIL_REDIRECT = env('GMAIL_REDIRECT', default='')

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'en-in'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = False

STATIC_HOST = env('DJANGO_STATIC_HOST', default='')
STATIC_URL = STATIC_HOST + '/static/'
STATIC_ROOT = BASE_DIR.parent / 'assets/static'

MEDIA_HOST = env('DJANGO_MEDIA_HOST', default='')
MEDIA_URL = MEDIA_HOST + '/assets/'
MEDIA_ROOT = BASE_DIR.parent / 'assets'

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
