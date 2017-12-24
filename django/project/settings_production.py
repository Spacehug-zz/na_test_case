import os

BASE_URL = '127.0.0.1:8000'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'na_testcase',
        'USER': 'na_testcase',
        'PASSWORD': 'iHaeX5Iete',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMINS = (
    ('Lapshin Dmitri', 'spacehug.o0@gmail.com'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
             'level': 'ERROR',
             'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'propagate': True,
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
        },
    },
}