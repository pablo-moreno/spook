import pytest
from django.db import models
from unittest.mock import patch

from rest_framework.exceptions import ValidationError

from spook.resources import APIResource
from rest_framework import serializers

from spook.validators import InputValidator
from spook.utils import pluralize, get_model_slug
from .utils import MockedResponse, ModelMixinTestCase


PRODUCTS = [
    {
        'id': 1,
        'name': 'Star Wars Collection',
    },
    {
        'id': 2,
        'name': 'The Lord Of The Rings Collection',
    },
]

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
    return MockedResponse(
        data=PRODUCTS,
    )


def retrieve_product(*args, **kwargs):
    return MockedResponse(
        data=PRODUCTS[0],
    )


def create_product(*args, **kwargs):
    return MockedResponse(
        data=CREATED_PRODUCT,
        status_code=201,
    )


def update_product(*args, **kwargs):
    return MockedResponse(
        data=UPDATED_PRODUCT,
    )


class TestAPIResource(ModelMixinTestCase):
    mixins = [Product, ]

    def setUp(self):
        self.product_service = ProductService()

    def test_get_model_slug(self):
        assert get_model_slug(Product) == 'products'

    @patch('spook.resources.requests.get', get_mocked_products)
    def test_list_products(self):
        response = self.product_service.list()
        assert response.status == 200
        data = response.data
        assert data[0]['name'] == PRODUCTS[0].get('name')

    @patch('spook.resources.requests.get', retrieve_product)
    def test_retrieve_product(self):
        response = self.product_service.retrieve('1')
        assert response.status == 200
        data = response.data
        assert data['name'] == PRODUCTS[0].get('name')

    @patch('spook.resources.requests.post', create_product)
    def test_create_product(self):
        response = self.product_service.create(CREATED_PRODUCT)
        assert response.status == 201
        data = response.data
        assert data['name'] == CREATED_PRODUCT.get('name')

    @patch('spook.resources.requests.put', update_product)
    def test_update_product(self):
        response = self.product_service.update('3', UPDATED_PRODUCT)
        assert response.status == 200
        data = response.data
        assert data['name'] == UPDATED_PRODUCT.get('name')

    @patch('spook.resources.requests.post', create_product)
    def test_create_invalid_input(self):
        with pytest.raises(ValidationError):
            self.product_service.create({
                'wrong': 'input'
            })

    @patch('spook.resources.requests.put', update_product)
    def test_update_invalid_input(self):
        with pytest.raises(ValidationError):
            self.product_service.update(3, {
                'wrong': 'input'
            })
