import requests
from django.db.models import Model
from rest_framework.serializers import Serializer
from typing import Union, Any, Type

from . import settings
from .managers import DataManager
from .responses import ProxyResponse
from .utils import get_model_slug


class HttpService(object):
    """
        Http Service class to perform requests to an external API.
    """
    manager: Type[DataManager] = None
    api_url: str = settings.EXTERNAL_API_URL
    authorization_header: str = settings.AUTHORIZATION_HEADER
    authorization_header_name: str = settings.AUTHORIZATION_HEADER_NAME

    def __init__(self):
        self.token = None
        self.headers = dict()
        self.http = requests

    def get_token(self) -> str:
        return self.token

    def set_token(self, token: str):
        self.token = token

    def get_manager_class(self) -> Type[DataManager]:
        if not self.manager:
            raise Exception('You need to override .get_manager_class() method or '
                            'provide a default manager_class.')

        return self.manager

    def get_serializer_class(self) -> Type[Serializer]:
        return self.get_manager_class().serializer

    def get_model(self) -> Type[Model]:
        return self.get_manager_class().model

    def get_url(self, *url_params) -> str:
        """
            Returns the url based on the url params
        """
        params = (self.api_url, get_model_slug(self.get_model()), *url_params)
        return '/'.join([str(param) for param in params if param != ''])

    def get_headers(self) -> dict:
        """
            Returns the headers to perform the request to the server
        """
        token = self.get_token()
        if token:
            headers = {
                self.authorization_header_name: f'{self.authorization_header} {token}',
                **self.headers,
            }
            return headers
        return self.headers

    def get_response_data(self, response):
        if response.status_code not in range(200, 400):
            raise Exception(f'Error {response.status_code}')

        data, is_list = self.map_response(response.json())

        serializer = self.get_serializer_class()
        results = serializer(data=data, many=is_list)
        results.is_valid(raise_exception=True)

        return data

    def map_response(self, data: Union[dict, list]) -> (Union[dict, list], bool):
        """
            Maps the response to a custom format
        """
        is_list = isinstance(data, list)
        return data, is_list

    def list(self, **params) -> ProxyResponse:
        """
            Retrieves a list of items
        :param params: Query params for the url
        :return: JSON response as a dict
        """
        url = self.get_url()

        return self.get(url, **params)

    def retrieve(self, pk: Any, **params) -> ProxyResponse:
        """
            Retrieves an item given its pk or uid
        :param pk: Unique ID of the item
        :param params: Extra query params
        :return: JSON response as a dict
        """
        url = self.get_url(pk)

        return self.get(url, **params)

    def get(self, url: str, **params) -> ProxyResponse:
        """
            Performs a GET request to a server URL
        :param url: The URL
        :param params: Additional query params
        :return: JSON response as a dict
        """
        response = self.http.get(url, headers=self.get_headers(), params=params)
        data = self.get_response_data(response)
        manager = self.get_manager_class()
        queryset = manager(data=data)

        return ProxyResponse(queryset=queryset, status=response.status_code)

    def post(self, data: dict, query: dict = None) -> ProxyResponse:
        """
            Performs a POST request to the server
        :param data: Data attached
        :param query: Extra querystring as a dict
        :return: JSON response as a dict
        """
        response = self.http.post(self.get_url(), data=data, headers=self.get_headers(), params=query)
        data = self.get_response_data(response)
        manager = self.get_manager_class()
        queryset = manager(data=data)

        return ProxyResponse(queryset=queryset, status=response.status_code)

    def create(self, data: dict, query: dict = None) -> ProxyResponse:
        return self.post(data=data, query=query)

    def put(self, pk: Any, data: dict, query: dict = None) -> ProxyResponse:
        """
            Performs a PUT request to the server
        :param pk: Primary key of the object to update
        :param data: Updated data
        :param query: Query params
        :return: JSON response as a dict
        """
        response = self.http.put(self.get_url(pk), data=data, headers=self.get_headers(), params=query)
        data = self.get_response_data(response)
        manager = self.get_manager_class()
        queryset = manager(data=data)

        return ProxyResponse(queryset=queryset, status=response.status_code)

    def update(self, pk: Any, data: dict, query: dict = None) -> ProxyResponse:
        return self.put(pk=pk, data=data, query=query)

    def delete(self, pk: Any, query: dict = None) -> ProxyResponse:
        """
            Performs a DELETE request to the server
        :param pk: Primary key of the object to update
        :param query: Query params
        :return: JSON response as a dict
        """
        response = self.http.delete(self.get_url(pk), headers=self.get_headers(), params=query)
        data = self.get_response_data(response)
        manager = self.get_manager_class()
        queryset = manager(data=data)

        return ProxyResponse(queryset=queryset, status=response.status_code)

    def destroy(self, pk: Any, query: dict = None) -> ProxyResponse:
        return self.delete(pk=pk, query=query)
