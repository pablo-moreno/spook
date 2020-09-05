from django.db import models
from rest_framework.test import APITestCase
from unittest.mock import patch
from spook.services import HttpService
from rest_framework import serializers
from .utils import MockedResponse


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


class Product(models.Model):
    name = models.CharField(max_length=48)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=48)


class ProductService(HttpService):
    api_url = 'http://external/api'
    model = Product
    serializer_class = ProductSerializer


def get_mocked_products(*args, **kwargs):
    return MockedResponse(
        data=PRODUCTS,
    )


def retrieve_product(*args, **kwargs):
    return MockedResponse(
        data=PRODUCTS[0],
    )


class TestItWorks(APITestCase):
    def setUp(self):
        self.product_service = ProductService()

    @patch('requests.get', get_mocked_products)
    def test_list_products(self):
        response = self.product_service.list()
        assert response.status == 200
        data = response.dataset.data
        assert data[0]['name'] == 'Star Wars Collection'

    @patch('requests.get', retrieve_product)
    def test_retrieve_product(self):
        response = self.product_service.retrieve('1')
        assert response.status == 200
        data = response.dataset.data
        assert data['name'] == 'Star Wars Collection'
