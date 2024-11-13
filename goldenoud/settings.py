"""
Django settings for goldenoud project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from django.contrib.messages import constants as messages
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fjwqbop2zf#x0!8trrx@*%mi#utuyj=pof&$n@id!qmbyme5(^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'True'

ALLOWED_HOSTS = [ 'www.glasgoud.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'accounts',
    'store',
    'carts',
    'orders',

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

ROOT_URLCONF = 'goldenoud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'goldenoud.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    'goldenoud/static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

# EMAIL CONFIGURATION
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'saeed.murray@gmail.com'
EMAIL_HOST_PASSWORD = 'xruebeiqgoujnxpq'
EMAIL_USE_TLS = 'True'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# In settings.py
STRIPE_SECRET_KEY = 'sk_test_51NGnZcLAob8kQ6E5Hdd1o0Frrc9VoRzaX2tF3HtLLyNX20eN23DDCTDtInng57YzdYEV53kCS8i1RKzmRACCQB1k00431wTZ5B'
STRIPE_PUBLIC_KEY = 'pk_test_51NGnZcLAob8kQ6E5ctOUo5ctkKxSWOV7IFrPrrQHcscwTnAAIXa8LbOgsVEnz8syhkDGJLdAng2kLABEzC3An40t00IEIIWqDU'



# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST_PASSWORD = 'xrue beiq gouj nxpq' or '4rshad02'

# to activate virtual environment
# source ./env/Scripts/activate

# to start new app named category
# py manage.py startapp category
# py manage.py startapp store

# add model to database
# py manage.py makemigrations
# py manage.py migrate

# to create superuser.
# py manage.py createsuperuser
# saeed.murray@gmail.com
# smurray
# arshad02

# to run server
# py manage.py runserver


# awsbean
# https://767397959529.signin.aws.amazon.com/console
# greatkart_user
# 4r$had0z

# ssh-key
# greatkart
# SHA256:bwqGjqzyTA7GZk7Z/KXjhyozRrXpEOTL+ZWjn+kCMFo smurray@C3601
# aws-eb  aws-eb.pub  id_rsa  id_rsa.pub


# password linode
# greatkartgreatkart
# *X2!HS)u3G#oyk
