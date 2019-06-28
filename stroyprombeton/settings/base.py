"""
Django settings for stroyprombeton project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import socket
from datetime import datetime

import sentry_sdk
from django.utils.translation import ugettext_lazy as _
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'my_cool_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# setting from docker example: https://github.com/satyrius/paid/
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',')]

# Enable in frame loading for Ya.Metric
# https://docs.djangoproject.com/es/1.10/ref/clickjacking/
# https://yandex.ru/support/metrika/general/counter-webvisor.xml#download-page
X_FRAME_OPTIONS = 'ALLOW-FROM http://webvisor.com'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'django_user_agents',
    'debug_toolbar',
    'mptt',
    'widget_tweaks',
    'sorl.thumbnail',
    'cachalot',
    'generic_admin',
    'django.contrib.admin',
    'django_select2',
    'images',
    'refarm_redirects',
    'pages',
    'search',
    'catalog',
    'ecommerce',
    'refarm_test_utils',
    'wkhtmltopdf',
    'stroyprombeton',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'refarm_redirects.middleware.RedirectAllMiddleware',
]

ROOT_URLCONF = 'stroyprombeton.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ecommerce.context_processors.cart',
                'stroyprombeton.context_processors.site_info',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'stroyprombeton.wsgi.application'

# Password validation
# https://goo.gl/KVqbnH
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
# https://goo.gl/HD4atG
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('ru', _('Russian')),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'stroyprombeton/locale')]
FORMAT_MODULE_PATH = [
    'stroyprombeton.formats',
]

# Static files (CSS, JavaScript, Images)
# https://goo.gl/HTQqfF
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'front_build'),
    ASSETS_DIR,
]

# Need for debug_toolbar
INTERNAL_IPS = (
    '127.0.0.1',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# to activate django connections pool for persistent connections.
# https://docs.djangoproject.com/en/1.11/ref/databases/#persistent-connections
CONN_MAX_AGE = None

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': os.environ['POSTGRES_DB'],
       'USER': os.environ['POSTGRES_USER'],
       'PASSWORD': os.environ['POSTGRES_PASSWORD'],
       'HOST': os.environ['POSTGRES_URL'],
       'PORT': '5432',
   }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

TEST_RUNNER = 'refarm_test_utils.runners.RefarmTestRunner'
# address for selenium-based tests
# host name doesn't resolve at CI, so we have to use host address
LIVESERVER_HOST = socket.gethostbyname(socket.gethostname())

# Is required for Docker container
WKHTMLTOPDF_CMD = 'xvfb-run wkhtmltopdf'

# 60 days in seconds
CACHED_TIME = 60 * (24 * 60 * 60)

# -------- SITE DATA -------- #
PROTOCOL = 'https' if os.environ.get('HTTPS', '') else 'http'
BASE_URL = f'{PROTOCOL}://www.stroyprombeton.ru'

SHOP = {
    'id': '69886',
    'scid': '64788',
    'success_url': BASE_URL + '/order-success/',
    'fail_url': BASE_URL + '/',
    'cps_phone': '+78126481380',
    'cps_email': 'info@stroyprombeton.ru',
}

PAYMENT_OPTIONS = (
    ('cash', 'Наличные'),
    ('cashless', 'Безналичные и денежные переводы')
)

PRODUCT_MODEL = 'stroyprombeton.Product'
CART_ID = 'cart'

SITE_CREATED = datetime(2013, 1, 1)

PLACEHOLDER_IMAGE = 'images/common/image-thumb.png'
PLACEHOLDER_ALT = 'Логотип компании СтройПромБетон'

SEARCH_SEE_ALL_LABEL = 'Смотреть все результаты'

SITE_ID = 1
SITE_DOMAIN_NAME = 'www.stroyprombeton.ru'

USE_CELERY = False

# Email configs
# It is fake-pass. Correct pass will be created on `docker-compose up` stage from `docker/.env`
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.yandex.ru')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'mailer@stroyprombeton.ru')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'so_secret_pass')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 465)
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'mailer@stroyprombeton.ru')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', True)
EMAIL_RECIPIENTS = os.environ.get(
    'EMAIL_RECIPIENTS',
    'info@stroyprombeton.ru,info2@stroyprombeton.ru'
).split(',')

EMAIL_SUBJECTS = {
    'order': 'Stroyprombeton | Новый заказ',
    'backcall': 'Stroyprombeton | Заказ обратного звонка',
}

# Used mostly in breadcrumbs to generate URL for catalog's root.
CATEGORY_TREE_URL = 'category_tree'

# Shop dict contains information about shop:
# emails, phones, API-integrations.
SITE_INFO = {
    'email': 'info@stroyprombeton.ru',
    'phone': {
        'moscow_1': '8 (499) 322-31-98',
        'moscow_1_url': 'tel:+74993223198',
        'spb_1': '8 (812) 648-13-80',
        'spb_1_url': 'tel:+78126481380'
    },
}


def get_robots_content():
    with open(os.path.join(TEMPLATE_DIR, 'robots.txt')) as robots_file:
        return robots_file.read()

CUSTOM_PAGES = {
    'category-tree': {
        'slug': 'gbi',
        'title': 'Каталог товаров',
        'name': 'Все категории',
        'menu_title': 'Каталог',
    },
    'client-feedbacks': {
        'slug': 'client-feedbacks',
        'name': 'Отзывы',
    },
    'index': {
        'slug': '',
        'title': (
            'Завод ЖБИ «СТК Модуль» | Производство ЖБИ в Санкт-Петербурге,'
            ' железобетонные изделия СПб'
        ),
        'name': 'Завод железобетонных изделий «СТК Модуль»',
        'menu_title': 'Главная',
    },
    'news': {
        'slug': 'news',
        'name': 'Новости компании',
        'title': 'Завод ЖБИ «СТК Модуль»',
        'menu_title': 'Новости компании'
    },
    'order': {
        'slug': 'order',
        'title': 'Корзина Интернет-магазин СТК Модуль',
        'name': 'Оформление заказа',
    },
    'order-price': {
        'slug': 'order-price',
        'title': 'Оформление запроса на прайс ЖБИ',
        'name': 'Оформление запроса на прайс ЖБИ',
        'keywords': 'прайс лист жби',
        'description': 'Оформить заявку на прайслист ЖБИ завода СТК Модуль',
    },
    'order-success': {
        'slug': 'order-success',
        'title': 'Спасибо за Ваш заказ',
        'name': 'Заказ принят',
    },
    'regions': {
        'slug': 'regions',
        'name': 'Регионы, в которые поставлялась продукция СТК Модуль',
    },
    'search': {
        'slug': 'search',
        'title': 'Результаты поиска',
        'name': 'Результаты поиска',
    },
    'sitemap': {
        'slug': 'sitemap',
        'h1': 'Карта сайта',
        'name': 'Карта сайта',
    },
    'order-drawing': {
        'slug': 'order-drawing',
        'name': 'Оформление запроса на изготовление по индивидуальным чертежам',
    },
    'robots': {
        'slug': 'robots.txt',
        'content': get_robots_content(),
    },
    'series': {
        'slug': 'series',
        'name': 'Серии',
    },
    'sections': {
        'slug': 'sections',
        'name': 'Типы изделий',
    },
}

# region-coordinates mapping
REGIONS = {
    'chukot-autonomous-area': 0,
    'zabaykalsky-territory': 1,
    'novosibirsk-region': 2,
    'tyumen-region': 3,
    'omsk-region': 4,
    'chelyabinsk-region': 5,
    'orenburg-region': 6,
    'ryazan-region': 7,
    'samara-region': 8,
    'astrakhan-region': 9,
    'republic-of-adygea': 10,
    'krasnodar-territory': 11,
    'kaliningrad-region': 12,
    'kursk-region': 13,
    'voronezh-region': 14,
    'yamalo-nenets-autonomous-area': 15,
    'arkhangelsk-region': 16,
    'nenets-autonomus-area': 17,
    'komi-republic': 18,
    'murmansk-region': 19,
    'republic-of-karelia': 20,
    'vologda-region': 21,
    'yaroslavl-region': 22,
    'ivanovo-region': 23,
    'nizhny-novgorod-region': 24,
    'republic-of-mordovia': 25,
    'kaluga-region': 26,
    'tula-region': 28,
    'pskov-region': 29,
    'saint-petersburg': 30,
    'leningrad-region': 31,
    'novgorod-region': 32,
    'tver-region': 33,
    'moscow': 34,
    'moscow-region': 35,
    'smolensk-region': 1000,
}

CATEGORY_GENT_NAMES = {  # gent - родительный падеж
    457: 'дорожного строительства',
    459: 'строительства энергетических объектов',
    456: 'общегражданского и промышленного строительства',
    458: 'строительства инженерных сетей',
}

ENV_TYPE = os.environ.get('ENV_TYPE', 'PROD')  # LOCAL | CI | PROD

# 'Prod' <-> 'Product #1 of Category #0 of Category #1' = 0.17
# About trigram similarity: https://goo.gl/uYFcxN
TRIGRAM_MIN_SIMILARITY = 0.15

TAGS_URL_DELIMITER = '-or-'
TAG_GROUPS_URL_DELIMITER = '-and-'

TAGS_TITLE_DELIMITER = ' или '
TAG_GROUPS_TITLE_DELIMITER = ' и '

BRAND_TAG_GROUP_NAME = 'Производитель'

# max tags in one tag group on category page
TAGS_UI_LIMIT = 20

# Number of pagination neighbors shown for page.
# If PAGINATION_NEIGHBORS = 4 and number of a page = 5,
# then will be shown neighbors by number: 3, 4, 6, 7
PAGINATION_NEIGHBORS = 10
CATEGORY_STEP_MULTIPLIERS = [12, 15, 24, 25, 48, 50, 60, 100]
OPTIONS_ORDERING = ['code', 'product__name', 'mark']
PRODUCT_SIBLINGS_COUNT = 10

SERIES_MATRIX_COLUMNS_COUNT = 4

# we wait se#567 to remove it
CATEGORY_SORTING_OPTIONS = {}

SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN and not DEBUG:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            CeleryIntegration(),
            DjangoIntegration(),
        ],
    )
