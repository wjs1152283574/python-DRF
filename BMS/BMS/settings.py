"""
Django settings for BMS project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y9+4jmd__ol!gy2wxbgi^$pyu_b7xbtp^=ut3epxvkrla2@%pu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",  # 解决跨域问题的插件
    "channels",     # 注册channels  才可以使用websocket 协议
    'rest_framework',
    'apps.users',
    'apps.nav',
    'apps.addrbook'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'BMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'BMS.wsgi.application'   # 指定wsgi 
ASGI_APPLICATION = 'BMS.routing.application'   # 指定 websocket channel

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # 数据库产品
        "NAME": "bms",  # 数据库名 // cassoapi
        "HOST": "127.0.0.1",  # 主机地址，本机使用localhost，生产环境为实际主机ip
        "PORT": "3306",  # 端口
        "USER": "root",  # 用户名
        "PASSWORD": "WJS123456.",  # 密码  本地// WJS123456.   // 腾讯云 casso123
        "CHARSET": "utf-8",
        "COLLATION": "utf8_genaral_ci",
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/bms/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media").replace("\\", "/")
# 重载系统的用户，让自定义到User模型生效 ---引用Django自带的用户表
AUTH_USER_MODEL = "users.User"
# AUTH_PERMISIONS_MODEL = "users.Bms_Permission"

# 以下直接赋值放在settings.py里即可解决---解决跨域问题  pip install django-cors-headers

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = "*"

# CORS_ALLOW_METHODS = ("DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT", "VIEW")

# CORS_ALLOW_HEADERS = (
#     "XMLHttpRequest",
#     "X_FILENAME",
#     "accept-encoding",
#     "authorization",
#     "content-type",
#     "dnt",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
#     "Pragma",
# )



REST_FRAMEWORK = {
    # 分页---只需两行代码  1.指定分页器类 2.指定每页数量
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # 每页显示的个数
    "PAGE_SIZE": 20,
    # 配置jwt  在这里全局配置用户认证类  一般会在视图中区别对待，即在视图中定义认证类
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",   # 测试时启用  可以登录
        "rest_framework.authentication.SessionAuthentication", # 测试时启用  可以登录
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ),
    # 限速设置
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",  # 未登陆用户
        "rest_framework.throttling.UserRateThrottle",  # 登陆用户
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "30/minute",  # 每分钟可以请求两次
        "user": "50/minute",  # 每分钟可以请求五次
        "test_casso":"500/day",
    },
    # 权限类配置
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.AllowAny'
    ],
    # "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.AutoSchema",
    'DEFAULT_RENDERER_CLASSES': (  # 默认响应渲染类
        'rest_framework.renderers.JSONRenderer',  # json渲染器
        'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览API渲染器
    )
}

# 缓存配置
REST_FRAMEWORK_EXTENSIONS = {"DEFAULT_CACHE_RESPONSE_TIMEOUT": 60}  ## 单位s

# 有效期限
from datetime import datetime
from datetime import timedelta

JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": timedelta(days=7),
    "JWT_AUTH_HEADER_PREFIX": "JWT",  # JWT跟前端保持一致，比如“token”这里设置成JWT
}