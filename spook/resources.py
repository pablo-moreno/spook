import enum
from json import JSONDecodeError

import requests
from typing import Union, Any, Type

from spook import settings
from spook.exceptions import *
from spook.pagination import BasePagination, DefaultPagination
from spook.responses import APIResourceResponse
from spook.validators import InputValidator


class APIResource(object):
    """
    API resource class to perform requests to an external API.
    """

    api_url: str = settings.EXTERNAL_API_URL
    authorization_header: str = settings.AUTHORIZATION_HEADER
    authorization_header_name: str = settings.AUTHORIZATION_HEADER_NAME
    pagination_class: Type[BasePagination] = DefaultPagination
    validator: Type[InputValidator] = None

    def __init__(
        self,
        token: str = None,
        http=requests,
        validator: Type[InputValidator] = None,
        context: dict = None,
    ):
        if context is None:
            context = {"request": None}

        self.token = token
        self.headers = {}
        self.http = http
        self.context = context

        if validator is not None:
            self.validator = validator

    def get_token(self) -> str:
        return self.token

    def get_api_url(self) -> str:
        if not self.api_url:
            raise Exception("You need to specify an api_url or override .get_api_url()")

        return self.api_url

    def get_url(self, *url_params) -> str:
        """
        Returns the url based on the url params
        """
        api_url = self.get_api_url()
        params = (api_url, *url_params)
        return "/".join([str(param) for param in params if param != ""])

    def get_pagination_class(self):
        return self.pagination_class

    def get_validator(self, action: str = None) -> InputValidator:
        return self.validator()

    def get_headers(self) -> dict:
        """
        Returns the headers to perform the request to the server
        """
        token = self.get_token()
        if token:
            headers = {
                self.authorization_header_name: f"{self.authorization_header} {token}",
                **self.headers,
            }
            return headers
        return self.headers

    def get_response_data(self, response) -> Union[dict, str]:
        try:
            response_data = response.json()
        except (JSONDecodeError, Exception) as e:
            response_data = response.content

        return response_data

    def map_response(
        self,
        data: Union[str, dict, list],
        action: str = "get",
        status: int = 200,
    ) -> Union[str, dict, list]:
        """
        Maps the response to a custom format
        """
        if status >= 400:
            return data

        if isinstance(data, str):
            return data

        return data

    def get_paginated_response(
        self, data: Union[str, dict, list]
    ) -> Union[str, dict, list]:
        pagination_class = self.get_pagination_class()

        if not pagination_class or isinstance(data, str):
            return data

        return pagination_class(
            data=data, context=self.context
        ).get_paginated_response()

    def validate(self, data: dict, action: str = None) -> dict:
        """
        Performs input validation
        """
        return self.get_validator(action=action).validate(data)

    def handle_server_errors(self, response, data: dict = None):
        """
        Error handling
        """
        pass

    def get(self, url: str, **params) -> APIResourceResponse:
        """
            Performs a GET request to a server URL
        :param url: The URL
        :param params: Additional query params
        :return: JSON response as a dict
        """
        response = self.http.get(url, headers=self.get_headers(), params=params)
        self.handle_server_errors(response)
        data = self.get_response_data(response)
        data = self.map_response(data, action="get", status=response.status_code)

        return APIResourceResponse(data=data, status=response.status_code)

    def list(self, **params) -> APIResourceResponse:
        """
            Retrieves a list of items
        :param params: Query params for the url
        :return: JSON response as a dict
        """
        url = self.get_url()

        response = self.http.get(url, headers=self.get_headers(), params=params)
        self.handle_server_errors(response)
        data = self.get_response_data(response)
        data = self.map_response(data, action="list", status=response.status_code)

        data = self.get_paginated_response(data)
        return APIResourceResponse(data=data, status=response.status_code)

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
        validated_data = self.validate(data, action="create")
        response = self.http.post(
            self.get_url(),
            data=validated_data,
            headers=self.get_headers(),
            params=query,
        )
        self.handle_server_errors(response, data=validated_data)
        data = self.get_response_data(response)
        data = self.map_response(data, action="create", status=response.status_code)

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
        self.validate(data, action="update")
        response = self.http.put(
            self.get_url(pk), json=data, headers=self.get_headers(), params=query
        )
        self.handle_server_errors(response, data=data)
        data = self.get_response_data(response)
        data = self.map_response(data, action="update", status=response.status_code)

        return APIResourceResponse(data=data, status=response.status_code)

    def patch(self, pk: Any, data: dict, query: dict = None) -> APIResourceResponse:
        """
            Performs a PATCH request to the server
        :param pk: Primary key of the object to update
        :param data: Updated data
        :param query: Query params
        :return: JSON response as a dict
        """
        self.validate(data, action="update")
        response = self.http.patch(
            self.get_url(pk), json=data, headers=self.get_headers(), params=query
        )
        self.handle_server_errors(response, data=data)
        data = self.get_response_data(response)
        data = self.map_response(
            data, action="partial_update", status=response.status_code
        )

        return APIResourceResponse(data=data, status=response.status_code)

    def update(
        self, pk: Any, data: dict, query: dict = None, partial: bool = False
    ) -> APIResourceResponse:
        if partial:
            return self.patch(pk=pk, data=data, query=query)

        return self.put(pk=pk, data=data, query=query)

    def delete(self, pk: Any, query: dict = None) -> APIResourceResponse:
        """
            Performs a DELETE request to the server
        :param pk: Primary key of the object to update
        :param query: Query params
        :return: JSON response as a dict
        """
        response = self.http.delete(
            self.get_url(pk), headers=self.get_headers(), params=query
        )
        self.handle_server_errors(response)
        data = self.get_response_data(response)
        data = self.map_response(data, action="delete", status=response.status_code)

        return APIResourceResponse(data=data, status=response.status_code)

    def destroy(self, pk: Any, query: dict = None) -> APIResourceResponse:
        return self.delete(pk=pk, query=query)
