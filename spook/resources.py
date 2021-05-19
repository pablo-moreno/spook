from json import JSONDecodeError

import requests
from typing import Union, Any, Type

from spook import settings
from spook.pagination import BasePagination
from spook.responses import APIResourceResponse
from spook.validators import InputValidator


class APIResource(object):
    """
        API resource class to perform requests to an external API.
    """
    api_url: str = settings.EXTERNAL_API_URL
    authorization_header: str = settings.AUTHORIZATION_HEADER
    authorization_header_name: str = settings.AUTHORIZATION_HEADER_NAME
    pagination_class: Type[BasePagination] = None
    validator: Type[InputValidator] = None

    def __init__(self, token: str = None, http=requests):
        self.token = token
        self.headers = {}
        self.http = http

    def get_token(self) -> str:
        return self.token

    def set_token(self, token: str):
        self.token = token

    def get_url(self, *url_params) -> str:
        """
            Returns the url based on the url params
        """
        params = (self.api_url, *url_params)
        return '/'.join([str(param) for param in params if param != ''])

    def get_pagination_class(self):
        return self.pagination_class

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

    def get_response_data(self, response) -> Union[dict, str]:
        try:
            response_data = response.json()
        except (JSONDecodeError, Exception) as e:
            response_data = response.content

        data = self.map_response(response_data)

        return data

    def map_response(self, data: Union[str, dict, list], action='get') -> Union[str, dict, list]:
        """
            Maps the response to a custom format
        """
        if isinstance(data, str):
            return data

        return data

    def get_paginated_response(self, data: Union[dict, list]) -> Union[dict, list]:
        pagination_class = self.get_pagination_class()

        if not pagination_class:
            return data

        data = self.map_response(data)

        pagination_class = self.get_pagination_class()

        return pagination_class(data=data).get_paginated_response()

    def validate(self, data: dict) -> dict:
        """
            Performs input validation
        """
        return self.validator().validate(data)

    def get(self, url: str, **params) -> APIResourceResponse:
        """
            Performs a GET request to a server URL
        :param url: The URL
        :param params: Additional query params
        :return: JSON response as a dict
        """
        response = self.http.get(url, headers=self.get_headers(), params=params)
        data = self.get_response_data(response)
        data = self.map_response(data, action='get')

        return APIResourceResponse(data=data, status=response.status_code)

    def list(self, **params) -> APIResourceResponse:
        """
            Retrieves a list of items
        :param params: Query params for the url
        :return: JSON response as a dict
        """
        url = self.get_url()

        return self.get(url, **params)

    def retrieve(self, pk: Any, **params) -> APIResourceResponse:
        """
            Retrieves an item given its pk or uid
        :param pk: Unique ID of the item
        :param params: Extra query params
        :return: JSON response as a dict
        """
        url = self.get_url(pk)

        return self.get(url, **params)

    def post(self, data: dict, query: dict = None) -> APIResourceResponse:
        """
            Performs a POST request to the server
        :param data: Data attached
        :param query: Extra querystring as a dict
        :return: JSON response as a dict
        """
        validated_data = self.validate(data)
        response = self.http.post(self.get_url(), data=validated_data, headers=self.get_headers(), params=query)
        data = self.get_response_data(response)
        data = self.map_response(data, action='create')

        return APIResourceResponse(data=data, status=response.status_code)

    def create(self, data: dict, query: dict = None) -> APIResourceResponse:
        return self.post(data=data, query=query)

    def put(self, pk: Any, data: dict, query: dict = None) -> APIResourceResponse:
        """
            Performs a PUT request to the server
        :param pk: Primary key of the object to update
        :param data: Updated data
        :param query: Query params
        :return: JSON response as a dict
        """
        self.validate(data)
        response = self.http.put(self.get_url(pk), data=data, headers=self.get_headers(), params=query)
        data = self.get_response_data(response)
        data = self.map_response(data, action='update')

        return APIResourceResponse(data=data, status=response.status_code)

    def update(self, pk: Any, data: dict, query: dict = None) -> APIResourceResponse:
        return self.put(pk=pk, data=data, query=query)

    def delete(self, pk: Any, query: dict = None) -> APIResourceResponse:
        """
            Performs a DELETE request to the server
        :param pk: Primary key of the object to update
        :param query: Query params
        :return: JSON response as a dict
        """
        response = self.http.delete(self.get_url(pk), headers=self.get_headers(), params=query)
        data = self.get_response_data(response)
        data = self.map_response(data, action='delete')

        return APIResourceResponse(data=data, status=response.status_code)

    def destroy(self, pk: Any, query: dict = None) -> APIResourceResponse:
        return self.delete(pk=pk, query=query)
