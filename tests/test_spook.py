from django.db import models
from unittest.mock import patch
from spook.services import HttpService, DatabaseDataManager
from rest_framework import serializers

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


class Product(models.Model):
    name = models.CharField(max_length=48)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class ProductManager(DatabaseDataManager):
    model = Product
    serializer = ProductSerializer


class ProductService(HttpService):
    api_url = 'http://external/api'
    manager = ProductManager


def get_mocked_products(*args, **kwargs):
    return MockedResponse(
        data=PRODUCTS,
    )


def retrieve_product(*args, **kwargs):
    return MockedResponse(
        data=PRODUCTS[0],
    )


class TestHttpService(ModelMixinTestCase):
    mixins = [Product, ]

    def setUp(self):
        self.product_service = ProductService()

    @patch('requests.get', get_mocked_products)
    def test_list_products(self):
        response = self.product_service.list()
        assert response.status == 200
        queryset = response.queryset
        data = queryset.data
        assert data[0]['name'] == 'Star Wars Collection'

    @patch('requests.get', get_mocked_products)
    def test_persistance(self):
        response = self.product_service.list()
        assert response.status == 200
        queryset = response.queryset
        queryset.persist()
        assert Product.objects.count() == 2

    @patch('requests.get', retrieve_product)
    def test_retrieve_product(self):
        response = self.product_service.retrieve('1')
        assert response.status == 200
        data = response.queryset.data
        assert data['name'] == 'Star Wars Collection'
