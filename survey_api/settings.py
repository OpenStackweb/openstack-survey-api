"""
 * Copyright 2019 OpenStack Foundation
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

import os
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'survey_api.reports',
    'graphene_django',
    'django_filters',
    'corsheaders',
]

GRAPHENE = {
    'SCHEMA': 'survey_api.schema.schema'
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'survey_api.authentication.TokenValidationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'survey_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'survey_api/reports/templates')],
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


WSGI_APPLICATION = 'survey_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_API_ENGINE"),
        'NAME': os.getenv("DB_API_NAME"),
        'USER': os.getenv("DB_API_USER"),
        'PASSWORD': os.getenv("DB_API_PASSWORD"),
        'HOST': os.getenv("DB_API_HOST"),
        'PORT': os.getenv("DB_API_PORT"),
    },
    'openstack_db': {
        'ENGINE': os.getenv("DB_OPENSTACK_ENGINE"),
        'NAME': os.getenv("DB_OPENSTACK_NAME"),
        'USER': os.getenv("DB_OPENSTACK_USER"),
        'PASSWORD': os.getenv("DB_OPENSTACK_PASSWORD"),
        'HOST': os.getenv("DB_OPENSTACK_HOST"),
        'PORT': os.getenv("DB_OPENSTACK_PORT"),
    }
}

DATABASE_ROUTERS = ['survey_api.db_router.DBRouter']


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
            'console': {
                # exact format is not important, this is the minimum information
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            },
     },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(BASE_DIR, "web.log"),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True


# OAUTH
RS_CLIENT_ID = os.getenv("RS_CLIENT_ID")
RS_CLIENT_SECRET = os.getenv("RS_CLIENT_SECRET")