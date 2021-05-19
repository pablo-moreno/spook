import pytest
from unittest.mock import patch

from rest_framework.exceptions import ValidationError

from spook.utils import get_model_slug
from tests.utils import ModelMixinTestCase
from tests.mocks import *


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
        assert data['results'][0]['name'] == PRODUCTS['results'][0].get('name')

    @patch('spook.resources.requests.get', retrieve_product)
    def test_retrieve_product(self):
        response = self.product_service.retrieve('1')
        assert response.status == 200
        data = response.data
        assert data['name'] == PRODUCTS['results'][0].get('name')

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

    @patch('spook.resources.requests.delete', delete_product)
    def test_delete_product(self):
        response = self.product_service.delete('3')
        assert response.status == 204
        assert response.data == ''

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

    @patch('spook.resources.requests.get', server_error)
    def test_server_error(self):
        response = self.product_service.list()
        assert response.status == 500
        assert response.data == 'Internal Server Error'

    @patch('spook.resources.requests.post', server_validation_error)
    def test_server_validation_error(self):
        response = self.product_service.create({'name': 'Pablo', 'age': -2})
        assert response.status == 400
        assert response.data.get('age')[0] == 'This field must be positive.'

    @patch('spook.resources.requests.post', server_permission_error)
    def test_server_permissions_error(self):
        response = self.product_service.create({'name': 'Pablo', 'age': -2})
        assert response.status == 403
        assert response.data == 'You are not allowed to perform this action'
