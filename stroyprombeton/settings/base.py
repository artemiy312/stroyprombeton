"""
Django settings for stroyprombeton project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from datetime import datetime
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'my_cool_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# setting from docker example: https://github.com/satyrius/paid/
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',')]

# Application definition

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
    'mptt',
    'widget_tweaks',
    'sorl.thumbnail',
    'generic_admin',
    'django.contrib.admin',
    'images',
    'pages',
    'catalog',
    'ecommerce',
    'stroyprombeton',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

ROOT_URLCONF = 'stroyprombeton.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Static files (CSS, JavaScript, Images)
# https://goo.gl/HTQqfF
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'front/build'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASE_URL = 'postgres://user:pass@host/db_name'
DATABASES = {
    'default': dj_database_url.config(
        env='DATABASE_URL',
        default=DATABASE_URL
    )
}


# -------- SITE DATA -------- #
PAYMENT_OPTIONS = (('cash', 'Наличные'),
                   ('cashless', 'Безналичные и денежные переводы'))

PRODUCT_MODEL = 'stroyprombeton.Product'
CART_ID = 'cart'

BASE_URL = 'http://www.stroyprombeton.ru'
SITE_CREATED = datetime(2013, 1, 1)

PLACEHOLDER_IMAGE = 'images/common/image-thumb.png'
PLACEHOLDER_ALT = 'Логотип компании СтройПромБетон'

SEARCH_SEE_ALL_LABEL = 'Смотреть все результаты'

SITE_ID = 1
SITE_DOMAIN_NAME = 'www.stroyprombeton.ru'

# Email configs
# It is fake-pass. Correct pass will be created on `docker-compose up` stage from `docker/.env`
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'so_secret_pass')
EMAIL_HOST_USER = 'mailer@stroyprombeton.ru'
EMAIL_PORT = 587
EMAIL_RECIPIENT = 'info@stroyprombeton.ru'
EMAIL_SENDER = 'mailer@stroyprombeton.ru'
EMAIL_USE_TLS = True
SHOP_EMAIL = 'info@stroyprombeton.ru'

# Uncomment for http->https change
# os.environ['HTTPS'] = 'on'

EMAIL_SUBJECTS = {
    'order': 'Stroyprombeton | Новый заказ',
    'backcall': 'Stroyprombeton | Заказ обратного звонка',
}

# Used mostly in breadcrumbs to generate URL for catalog's root.
CATEGORY_TREE_URL = 'category_tree'

SITE_INFO = {
    'email': 'info@stroyprombeton.ru',
    'phone': {
        'moscow_1': '8 (499) 322-31-98',
        'moscow_1_url': '+74993223198',
        'spb_1': '8 (812) 648-13-80',
        'spb_1_url': '+78126481380'
    },
}

CUSTOM_PAGES = {
    'category_tree': {
        'slug': 'gbi',
        'title': 'Каталог товаров',
        'name': 'Все категории',
        'menu_title': 'Каталог',
    },
    'client_feedbacks': {
        'slug': 'client-feedbacks',
        'name': 'Отзывы',
    },
    'index': {
        'slug': '',
        'title': 'Завод ЖБИ «СТК-ПромБетон» | Производство ЖБИ в Санкт-Петербурге, железобетонные изделия СПб',
        'name': 'Завод железобетонных изделий «СТК-Промбетон»',
        'menu_title': 'Главная',
    },
    'news': {
        'slug': 'news',
        'name': 'Новости компании',
        'title': 'Завод ЖБИ «СТК-ПромБетон»',
        'menu_title': 'Новости компании'
    },
    'order': {
        'slug': 'order',
        'title': 'Корзина Интернет-магазин СТК-ПромБетон',
        'name': 'Оформление заказа',
    },
    'order-success': {
        'slug': 'order-success',
        'title': 'Спасибо за Ваш заказ',
        'name': 'Заказ принят',
    },
    'regions': {
        'slug': 'regions',
        'name': 'Регионы, в которые поставлялась продукция СТК-ПромБетон',
    },
    'search': {
        'slug': 'search',
        'title': 'Результаты поиска',
        'name': 'Результаты поиска',
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

PARTNERS = [
    {
        'url': 'http://xn----htbqgdmrio5g.xn--p1ai/?utm_source=STB_site&utm_medium=backlink&utm_campaign=backlink_traffic',
        'logo': 'images/partner-stkmodul-logo.png',
        'alt': 'СТК-Модуль',
    },
    {
        'url': 'http://stkm-energo.ru/?utm_source=STB_site&utm_medium=backlink&utm_campaign=backlink_traffic',
        'logo': 'images/partner-modulenergo-logo.png',
        'text': 'Модуль энерго',
        'alt': 'Монтаж и строительство энергообъектов',
    },
    {
        'url': 'http://www.stk-metal.ru/?utm_source=STB_site&utm_medium=backlink&utm_campaign=backlink_traffic',
        'logo': 'images/partner-stkmetall-logo.png',
        'text': 'СТК-Металл',
        'alt': 'Поставка металлоконструкций',
    },
]
