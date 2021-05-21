import os
import django
from django.conf import settings


APP_DIR = os.path.abspath(os.path.dirname(__file__))


SETTINGS_DICT = {
    "BASE_DIR": APP_DIR,
    "INSTALLED_APPS": (
        "spook",
    ),
    "SECRET_KEY": "spook secret",
    "DATABASES": {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
    },
    "DEFAULT_AUTO_FIELD": "django.db.models.AutoField",
}


def pytest_configure():
    settings.configure(**SETTINGS_DICT)
    django.setup()
