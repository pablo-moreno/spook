from django.db import models
from rest_framework import serializers

from spook.resources import APIResource
from spook.validators import InputValidator
from tests.utils import MockedResponse

PRODUCTS = {
    'count': 2,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': 1,
            'name': 'Star Wars Collection',
        },
        {
            'id': 2,
            'name': 'The Lord Of The Rings Collection',
        },
    ]
}

CREATED_PRODUCT = {
    'id': 3,
    'name': 'The Elder Scrolls V',
}

UPDATED_PRODUCT = {
    'id': 3,
    'name': 'The Elder Scrolls V: Skyrim',
}


class Product(models.Model):
    name = models.CharField(max_length=48)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class ProductValidator(InputValidator):
    serializer_class = ProductSerializer


class ProductService(APIResource):
    api_url = 'http://external/api'
    validator = ProductValidator


def get_mocked_products(*args, **kwargs):
    return MockedResponse(data=PRODUCTS)


def retrieve_product(*args, **kwargs):
    return MockedResponse(data=PRODUCTS['results'][0])


def create_product(*args, **kwargs):
    return MockedResponse(data=CREATED_PRODUCT, status_code=201)


def update_product(*args, **kwargs):
    return MockedResponse(data=UPDATED_PRODUCT)


def server_error(*args, **kwargs):
    return MockedResponse(data='Internal Server Error', status_code=500)


def server_validation_error(*args, **kwargs):
    data = {
        'age': [
            'This field must be positive.',
        ]
    }

    return MockedResponse(data=data, status_code=400)


def server_permission_error(*args, **kwargs):
    return MockedResponse(data='You are not allowed to perform this action', status_code=403)
