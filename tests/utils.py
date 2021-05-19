from json import JSONDecodeError

from django.db import connection
from django.db.models.base import ModelBase
from django.test import TestCase
from rest_framework.test import APITestCase


class MockedResponse(object):
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code
        self.content = data

    def json(self):
        if isinstance(self.data, str):
            raise JSONDecodeError

        return self.data


class ModelMixinTestCase(APITestCase):
    """
    Test Case for abstract mixin models.
    Subclass and set cls.mixin to your desired mixin.
    access your model using cls.model.

    All the credit to: https://stackoverflow.com/a/57586891
    """
    mixins = []
    models = []

    @classmethod
    def setUpClass(cls):
        for mixin in cls.mixins:
            model = ModelBase(
                "__Test" + mixin.__name__,
                (mixin, ),
                {'__module__': mixin.__module__}
            )

            # Use schema_editor to create schema
            with connection.schema_editor() as editor:
                editor.create_model(model)
            cls.models.append(model)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        with connection.schema_editor() as editor:
            for model in cls.models:
                editor.delete_model(model)

        connection.close()
