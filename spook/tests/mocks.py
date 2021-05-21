from rest_framework import serializers

from spook.resources import APIResource
from spook.validators import InputValidator
from spook.tests.utils import MockedResponse


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    class Meta:
        fields = ["id", "name"]


class ProductValidator(InputValidator):
    serializer_class = ProductSerializer


class ProductResource(APIResource):
    api_url = "http://example.com/api/1.0/products/"
    validator = ProductValidator

    def get_token(self) -> str:
        return "my-awesome-token"


PRODUCTS = {
    "count": 2,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": 1,
            "name": "Star Wars Collection",
        },
        {
            "id": 2,
            "name": "The Lord Of The Rings Collection",
        },
    ],
}

CREATED_PRODUCT = {
    "id": 3,
    "name": "The Elder Scrolls V",
}

UPDATED_PRODUCT = {
    "id": 3,
    "name": "The Elder Scrolls V: Skyrim",
}


def get_mocked_products(*args, **kwargs):
    return MockedResponse(data=PRODUCTS)


def retrieve_product(*args, **kwargs):
    return MockedResponse(data=PRODUCTS["results"][0])


def create_product(*args, **kwargs):
    return MockedResponse(data=CREATED_PRODUCT, status_code=201)


def update_product(*args, **kwargs):
    return MockedResponse(data=UPDATED_PRODUCT)


def delete_product(*args, **kwargs):
    return MockedResponse(data="", status_code=204)


def server_error(*args, **kwargs):
    return MockedResponse(data="Internal Server Error", status_code=500)


def server_validation_error(*args, **kwargs):
    data = {
        "price": [
            "Invalid field name.",
        ]
    }

    return MockedResponse(data=data, status_code=400)


def server_permission_error(*args, **kwargs):
    return MockedResponse(
        data="You are not allowed to perform this action", status_code=403
    )
