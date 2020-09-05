import requests
from django.db.models import QuerySet, Case, When, Model
from typing import Union, Any, Type

from rest_framework.serializers import Serializer

from . import settings
from .utils import get_model_slug


class DataManager(object):
    primary_key_field_name: str = 'pk'
    model: Type[Model] = None
    serializer: Type[Serializer] = None

    def __init__(self, data):
        self.data = data
        assert self.serializer is not None, 'You need to specify the serializer property'
        assert self.model is not None, 'You need to specify the model property'

    def get_model(self) -> Type[Model]:
        if not self.model:
            raise Exception('You need to override .get_model() method or provide a default model.')

        return self.model

    def get_serializer_class(self) -> Type[Serializer]:
        if not self.serializer:
            raise Exception('You need to override .get_serializer() method or provide a default serializer.')

        return self.serializer

    def get_queryset(self, exact_order=True, as_pk_list=False) -> Union[list, QuerySet]:
        raise NotImplementedError

    def filter(self, fn):
        return filter(fn, self.data)

    def persist(self):
        raise NotImplementedError


class DatabaseDataManager(DataManager):
    def get_queryset(self, exact_order=True, as_pk_list=False) -> Union[list, QuerySet]:
        """
            Returns the queryset given the received data
        """
        pks = [item[self.primary_key_field_name] for item in self.data]

        if as_pk_list:
            return pks

        q = {
            f'{self.primary_key_field_name}__in': pks
        }
        results = self.get_model().objects.filter(**q)

        if exact_order:
            order = Case(*[
                When(**{self.primary_key_field_name: pk, 'then': pos})
                for pos, pk in enumerate(pks)
            ])
            results = results.order_by(order)

        return results

    def save(self, data):
        serialized = self.serializer(data=data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

    def persist(self):
        is_list = isinstance(self.data, list)

        if is_list:
            for item in self.data:
                self.save(data=item)
        else:
            self.save(data=self.data)


class ProxyResponse(object):
    def __init__(self, queryset, status):
        self.queryset = queryset
        self.status = status


class HttpService(object):
    """
        Http Service class to perform requests to an external API, fetch the results, validate them in
        the database and simplify the translation into a local queryset.
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
        :return:
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
        :param params: Aditional query params
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
