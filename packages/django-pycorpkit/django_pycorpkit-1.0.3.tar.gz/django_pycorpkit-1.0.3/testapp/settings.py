import json
import os
import secrets
from datetime import timedelta
from os.path import join

from testapp.perms.apps.perm_groups import BRANCH_ADMIN, DEPARTMENT_ADMIN, ORGANISATION_ADMIN, PROFILE_ADMIN


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_bool_env(env_var, default=False):
    """
    Retrieve a boolean value from an environment variable.

    This function fetches the value of an environment variable and attempts to
    parse it as a boolean. If the environment variable is not set, the provided
    default value is returned. The function only accepts `True` or `False` as
    valid boolean values.
    """
    val = os.getenv(env_var)
    if val is None:
        return default

    try:
        p = json.loads(val.lower())
        if not isinstance(p, bool):
            raise ValueError("Invalid boolean config: {}".format(val))
        return p
    except (ValueError, json.JSONDecodeError):
        raise ValueError("Invalid boolean config: {}".format(val))


INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third party apps
    "rest_framework",  # utilities for rest apis
    "django_filters",  # for filtering rest endpoints
    "django_rest_passwordreset",  # for password reset functionality
    "rest_framework_simplejwt",  # jwt web tokens
    # custom apps
    "pycorpkit.common",
    "pycorpkit.accountx",
    "pycorpkit.org_structure",
)

# https://docs.djangoproject.com/en/2.0/topics/http/middleware/
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "pycorpkit.common.utils.middleware.OrganisationIDMiddleware",
)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")
ROOT_URLCONF = "testapp.urls"
SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pycorpkit_test_db',
        'USER': 'pycorpkit_user',
        'PASSWORD': 'pycorpkit',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# General
APPEND_SLASH = False
TIME_ZONE = "Africa/Nairobi"

LANGUAGE_CODE = "en-us"
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
USE_L10N = True
USE_TZ = True

PERMISSIONS_PATH = "testapp.perms"

SITE_ID = 1
APP_NAME = "PyCorpKit"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

USE_S3 = os.getenv("USE_S3") == "TRUE"

MEDIA_ROOT = join(os.path.dirname(BASE_DIR), "media")
MEDIA_URL = "/media/"

STATIC_ROOT = join(os.path.dirname(BASE_DIR), "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [join(os.path.dirname(BASE_DIR), "static")]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Set DEBUG to False as a default for safety
# https://docs.djangoproject.com/en/dev/ref/settings/#debug

DEBUG = get_bool_env("DJANGO_DEBUG", True)

# Password Validation
# https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
    },
]

# Custom user app
AUTH_USER_MODEL = "accountx.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "pycorpkit.common.paginator.ImprovedPagination",
    "PAGE_SIZE": int(
        os.getenv(
            "DJANGO_PAGINATION_LIMIT",
            40,
        )
    ),
    "EXCEPTION_HANDLER": "pycorpkit.common.utils.exception_handler.custom_exception_handler",
    "DATETIME_FORMAT": "iso-8601",
    "DATE_FORMAT": "iso-8601",
    "TIME_FORMAT": "iso-8601",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "pycorpkit.accountx.permissions.enforce.EnforceDRFViewPermission",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_MODEL_SERIALIZER_CLASS": (
        "rest_framework.serializers.HyperlinkedModelSerializer",
        "rest_framework.serializers.ModelSerializer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
        "pycorpkit.common.filters.base.OrganisationFilterBackend",
    ),
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'pycorpkit.common.utils.phone_backend.PhoneModelBackend',
]

# email settings
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "admin@propertysync360.co.ke")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=3600),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}

# Password `reset strategy
# time in hours about how long the password reset token is active (Default: 24) # noqa
DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 1
DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomNumberTokenGenerator"
}
DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomNumberTokenGenerator",
    "OPTIONS": {"min_number": 1500, "max_number": 9999},
}

# User verification code apply on user register
VERIFICATION_CODE_LENGTH = os.getenv("VERIFICATION_CODE_LENGTH", 6)
VERIFICATION_CODE_CHARS = os.getenv("VERIFICATION_CODE_CHARS", "123456789")
VERIFICATION_CODE_DAYS_EXPIRY = os.getenv("VERIFICATION_CODE_DAYS_EXPIRY", 3)
INVITE_CODE_DAYS_EXPIRY = os.getenv("VERIFICATION_CODE_DAYS_EXPIRY", 7)

CLIENT_DOMAIN = os.getenv("CLIENT_DOMAIN", "http://localhost:3000")

# celery settings
CELERY_BROKER_URL = os.getenv("BROKER_URL", "amqp://guest:guest@localhost:5672/")
CELERY_RESULT_BACKEND = "rpc://"
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_RESULT_EXPIRES = int(os.getenv("CELERY_TASK_RESULT_EXPIRES", 300))
CELERY_TIMEZONE = TIME_ZONE
CELERY_DEFAULT_QUEUE = os.getenv("CELERY_QUEUE", "ratiba_queue")
CELERY_DEFAULT_EXCHANGE = CELERY_DEFAULT_QUEUE
CELERY_DEFAULT_ROUTING_KEY = CELERY_DEFAULT_QUEUE
SOFT_TIME_DELAY = 60 * 5

DEFAULT_ROLES = {
    "Organisation Admin": ORGANISATION_ADMIN,
    "Branch Admin": BRANCH_ADMIN,
    "Department Admin": DEPARTMENT_ADMIN,
    "User": PROFILE_ADMIN,
}
