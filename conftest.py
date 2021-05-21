import os
import django
from django.conf import settings


APP_DIR = os.path.abspath(os.path.dirname(__file__))


SETTINGS_DICT = {
    "BASE_DIR": APP_DIR,
    "INSTALLED_APPS": (
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "rest_framework",
        "spook.apps.SpookConfig",
        "tests",
    ),
    "SECRET_KEY": "spook secret",
    # Test cases will override this liberally.
    "ROOT_URLCONF": "",
    "DATABASES": {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
    },
    "MIDDLEWARE": (
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ),
    "SITE_ID": 1,
    "DEFAULT_AUTO_FIELD": "django.db.models.AutoField",
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "OPTIONS": {
                "context_processors": [
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ],
    "REST_FRAMEWORK": {
        "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.BasicAuthentication",
        ),
        "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
        "DEFAULT_FILTER_BACKENDS": [
            "rest_framework.filters.OrderingFilter",
        ],
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 20,
    },
}


def pytest_configure():
    settings.configure(**SETTINGS_DICT)
    django.setup()
