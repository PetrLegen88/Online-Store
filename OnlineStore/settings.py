"""
Django settings for online_store project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from enum import IntEnum, Enum


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = 'photos/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l$&%3x+b405k=enn)_-ic*nw!8zc)ymnwg=1scv#7htr(u0mrk'

STRIPE_PUBLISHABLE_KEY = 'pk_test_51Mg4drEiikof21SXbcoMkl8qtrbrC6GlQdUBflY3VIdFywiYV4SQpxUnNAyXCw2dMaO8qYLl2tcZCFc8DK9pgNHM00c1j8M28p'
STRIPE_SECRET_KEY = 'sk_test_51Mg4drEiikof21SXITXFHUAUoU6ardPkxrTpGzsX01pJXTqFxqQJGWm6gu4IOFMSHMe6GCJeNhANqv00NZPWcHOM00DqgPU6Qb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customer',
    'accounts',
    'migration_fixer',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'online_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "customer/templates/"],
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

WSGI_APPLICATION = 'online_store.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


class Status(IntEnum):
    EMPTY = 1
    INCART = 2
    ONWAY = 3
    DELIVERED = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ProductType(Enum):
    CLASSIC = "CLASSIC"
    DELUXE = "DELUXE"
    PREMIUM = "PREMIUM"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PaymentMethods(Enum):
    PayPal = "PayPal"
    BankTransfer = "Bank Transfer"
    ApplePay = "Apple pay"
    GooglePay = "Google pay"
    CreditCard = "Credit card"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]