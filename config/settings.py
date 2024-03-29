"""
Django settings for odn_api project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET", 'django-insecure-6r4^nn51n*u*%k^mpw)wb-u%e0h$+&4ilp5!cn3w0i+j@34s9#')


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
# DEBUG = True

ALLOWED_HOSTS = ["*"]

# ALLOWED_HOSTS = [
#     '.api.odn-it.com',
#     '.odn-it.com',
#     '127.0.0.1',
#     'localhost',
#     '.elasticbeanstalk.com',
# ]


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    "rest_framework_gis",
    'corsheaders',
    'drf_spectacular',
]

PROJECT_APPS = [
    'device.apps.DeviceConfig',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# GOOGLE_API_KEY = 'AIzaSyABG3cnsrqJjy7S-lgwhkoPZCKvMdGQcC4'


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            "HOST": os.environ.get("HOST"),
            "NAME": os.environ.get("NAME"),
            "USER": os.environ.get("USER"),
            "PASSWORD": os.environ.get("PASSWORD"),
            "PORT": os.environ.get("PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": 'django.contrib.gis.db.backends.postgis',
            "HOST": os.environ.get("RDS_HOST"),
            "NAME": os.environ.get("RDS_NAME"),
            "USER": os.environ.get("RDS_USER"),
            "PASSWORD": os.environ.get("RDS_PASSWORD"),
            "PORT": os.environ.get("RDS_PORT"),
        }

    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators


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
CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:8000', 'http://localhost:3000',
#                          'http://odndashboard.s3-website.ap-northeast-2.amazonaws.com']
CORS_ALLOW_CREDENTIALS = True

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# GDAL_LIBRARY_PATH = '/opt/homebrew/Cellar/gdal/3.5.2_1/lib/libgdal.dylib'
# GEOS_LIBRARY_PATH = '/opt/homebrew/opt/geos/lib/libgeos_c.dylib'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [os.path.join(BASE_DIR, "device", "static"), ]

WSGI_APPLICATION = 'config.wsgi.application'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'PAGE_SIZE': 10
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'ODN REST API Document',
    'DESCRIPTION': " 안녕하세요 이곳은 ODN REST API 문서 페이지 입니다 :)<br/><br/><a href='http://api.odn-it.com/devices/'>스마트부표 REST API 바로가기 😚</a>",
    'CONTACT': {'name': 'doc2kim', 'email': 'doc2kim@naver.com'},
    'SWAGGER_UI_SETTINGS': {
        'dom_id': '#swagger-ui',  # required(default)
        'layout': 'BaseLayout',  # required(default)
        # API를 클릭할때 마다 SwaggerUI의 url이 변경. (특정 API url 공유시 유용하기때문에 True설정을 사용합)
        'deepLinking': True,
        # True 이면 SwaggerUI상 Authorize에 입력된 정보가 새로고침을 하더라도 초기화되지 않음.
        'persistAuthorization': True,
        # True이면 API의 urlId 값을 노출합니다. 대체로 DRF api name둘과 일치하기때문에 api를 찾을때 유용.
        'displayOperationId': True,
        'filter': True,  # True 이면 Swagger UI에서 'Filter by Tag' 검색이 가능
    },
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Swagger UI 버전을 조절.
    'SWAGGER_UI_DIST': '//unpkg.com/swagger-ui-dist@3.38.0',
}
