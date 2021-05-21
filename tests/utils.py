from json import JSONDecodeError

from django.db import connection
from django.db.models.base import ModelBase
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


class MockedRequest(object):
    def __init__(self, data: dict = {}, query_params: dict = {}):
        self.META = dict()
        self.data = data
        self.query_params = query_params
