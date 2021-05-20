from unittest.mock import patch

from tests.mocks import *
from spook.views import *
from rest_framework.test import APITestCase


class ListCreateProductResourceView(APIResourceListCreateView):
    resource = ProductResource
    serializer_class = ProductSerializer

    def get_token(self, request):
        return ""


class RetrieveUpdateDestroyProductResourceView(APIResourceRetrieveUpdateDestroyView):
    resource = ProductResource
    serializer_class = ProductSerializer

    def get_token(self, request):
        return ""


class TestAPIResourceViews(APITestCase):
    @patch("spook.resources.requests.get", get_mocked_products)
    def test_list_view_products(self):
        view = ListCreateProductResourceView()
        response = view.list(MockedRequest())
        assert response.status_code == 200
        assert response.data == PRODUCTS

    @patch("spook.resources.requests.get", retrieve_product)
    def test_retrieve_view_products(self):
        view = RetrieveUpdateDestroyProductResourceView()
        response = view.get(MockedRequest(), pk=1)
        assert response.status_code == 200
        assert response.data == PRODUCTS["results"][0]

    @patch("spook.resources.requests.post", create_product)
    def test_create_view_product(self):
        view = ListCreateProductResourceView()
        response = view.create(MockedRequest(data={"name": "The Elder Scrolls V"}))
        assert response.status_code == 201
        assert response.data == CREATED_PRODUCT

    @patch("spook.resources.requests.put", update_product)
    def test_update_view_product(self):
        view = RetrieveUpdateDestroyProductResourceView()
        response = view.update(
            MockedRequest(data={"name": "The Elder Scrolls V: Skyrim"}), pk=3
        )
        assert response.status_code == 200
        assert response.data == UPDATED_PRODUCT

    @patch("spook.resources.requests.delete", delete_product)
    def test_delete_view_product(self):
        view = RetrieveUpdateDestroyProductResourceView()
        response = view.destroy(MockedRequest(), pk=3)
        assert response.status_code == 204
