import pytest
from unittest.mock import patch

from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from spook.utils import get_model_slug
from spook.tests.mocks import *


class TestAPIResource(APITestCase):
    mixins = []

    def setUp(self):
        self.product_service = ProductResource()

    def test_get_model_slug(self):
        class Product:
            pass

        class Inventory(object):
            pass

        assert get_model_slug(Product) == "products"
        assert get_model_slug(Inventory) == "inventories"

    def test_raises_resource_api_url_not_provided(self):
        class MyResource(APIResource):
            pass

        e = None
        with pytest.raises(Exception) as e:
            MyResource().list()
        assert e is not None

    @patch("spook.resources.requests.get", get_mocked_products)
    def test_raises_resource_token_not_provided(self):
        class MyResource(APIResource):
            api_url = "http://example.com/api/1.0/products/"

        response = MyResource().list()
        assert response.status == 200
        data = response.data
        assert data["results"][0]["name"] == PRODUCTS["results"][0].get("name")

    @patch("spook.resources.requests.get", get_mocked_products)
    def test_list_products(self):
        response = self.product_service.list()
        assert response.status == 200
        data = response.data
        assert data["results"][0]["name"] == PRODUCTS["results"][0].get("name")

    @patch("spook.resources.requests.get", retrieve_product)
    def test_retrieve_product(self):
        response = self.product_service.retrieve("1")
        assert response.status == 200
        data = response.data
        assert data["name"] == PRODUCTS["results"][0].get("name")

    @patch("spook.resources.requests.post", create_product)
    def test_create_product(self):
        response = self.product_service.create(CREATED_PRODUCT)
        assert response.status == 201
        data = response.data
        assert data["name"] == CREATED_PRODUCT.get("name")

    @patch("spook.resources.requests.put", update_product)
    def test_update_product(self):
        response = self.product_service.update("3", UPDATED_PRODUCT)
        assert response.status == 200
        data = response.data
        assert data["name"] == UPDATED_PRODUCT.get("name")

    @patch("spook.resources.requests.patch", update_product)
    def test_partial_update_product(self):
        response = self.product_service.update("3", UPDATED_PRODUCT, partial=True)
        assert response.status == 200
        data = response.data
        assert data["name"] == UPDATED_PRODUCT.get("name")

    @patch("spook.resources.requests.delete", delete_product)
    def test_delete_product(self):
        response = self.product_service.destroy("3")
        assert response.status == 204
        assert response.data == ""

    @patch("spook.resources.requests.post", create_product)
    def test_create_invalid_input(self):
        e = None
        with pytest.raises(ValidationError) as e:
            self.product_service.create({"wrong": "input"})
        assert e is not None

    @patch("spook.resources.requests.put", update_product)
    def test_update_invalid_input(self):
        e = None
        with pytest.raises(ValidationError) as e:
            self.product_service.update(3, {"wrong": "input"})
        assert e is not None

    @patch("spook.resources.requests.get", server_error)
    def test_server_error(self):
        response = self.product_service.list()
        assert response.status == 500
        assert response.data == "Internal Server Error"

    @patch("spook.resources.requests.post", server_validation_error)
    def test_server_validation_error(self):
        response = self.product_service.create(
            {"name": "The Elder Scrolls V: Skyrim", "price": -2}
        )
        assert response.status == 400
        assert response.data.get("price")[0] == "Invalid field name."

    @patch("spook.resources.requests.post", server_permission_error)
    def test_server_permissions_error(self):
        response = self.product_service.create({"name": "The Elder Scrolls V: Skyrim"})
        assert response.status == 403
        assert response.data == "You are not allowed to perform this action"
