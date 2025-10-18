"""
Django settings for Ez_Learn project (configured to use the 'website' app).
"""

from pathlib import Path
import os
import razorpay

# ------------------------------------------
# Base directory
# ------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------
# Security
# ------------------------------------------
SECRET_KEY = 'django-insecure-vozk(zqnn=tutaaay=-n6z-z051pwedv$6k)n2g65j!*z4jen&'
DEBUG = True
ALLOWED_HOSTS = []

# ------------------------------------------
# Installed apps
# ------------------------------------------
INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your application(s)
    # If website/apps.py defines class WebsiteConfig, use 'website.apps.WebsiteConfig'
    # Otherwise you can use 'website'
    'website.apps.WebsiteConfig',
]

# ------------------------------------------
# Middleware
# ------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------
# URLs & WSGI
# ------------------------------------------
ROOT_URLCONF = 'Ez_Learn.urls'
WSGI_APPLICATION = 'Ez_Learn.wsgi.application'

# ------------------------------------------
# Templates
# ------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # add if you use project-level templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------------------
# Database (sqlite for dev)
# ------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------------------
# Password validators
# ------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------
# Internationalization
# ------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------
# Static & media
# ------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ------------------------------------------
# Default primary key field type
# ------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------
# Email (local dev credentials kept inline as requested)
# ------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jayanthchange@gmail.com'
EMAIL_HOST_PASSWORD = 'bhhwjofuqiuggsyp'
EMAIL_PORT = 587

# ------------------------------------------
# Razorpay keys (inline for local dev)
# ------------------------------------------
KEY_ID = "rzp_test_ALvDvnHKMbLQmU"
KEY_SECRET = "GkvGt6afXG8aiWKwUK6F3m9S"

# optional razorpay client instance
razorpay_client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

# ------------------------------------------
# Logging
# ------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {'handlers': ['console'], 'level': 'WARNING'},
}
