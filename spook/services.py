import re
import requests
from . import settings
from django.db.models import QuerySet, Case, When
from typing import Union, Any


class PersistanceMixin(object):
    def save(self):
        is_list = isinstance(self.data, list)

        if is_list:
            for item in self.data:
                self.serializer(data=item).save()
        else:
            self.serializer(data=self.data).save()


class BaseHttpDataSet(PersistanceMixin):
    def __init__(self, data, serializer):
        self.data = data
        self.serializer = serializer


class HttpDataSet(BaseHttpDataSet, PersistanceMixin):
    pass


class ProxyResponse(object):
    def __init__(self, data_set, status):
        self.data_set = data_set
        self.status = status


class HttpService(object):
    """
        Http Service class to perform requests to an external API, fetch the results, validate them in
        the database and simplify the translation into a local queryset.
    """
    model = None
    serializer_class = None
    api_url: str = settings.EXTERNAL_API_URL
    authorization_header: str = settings.AUTHORIZATION_HEADER
    authorization_header_name: str = settings.AUTHORIZATION_HEADER_NAME
    primary_key_field_name: str = 'pk'

    def __init__(self):
        self.token = None
        self.headers = dict()
        self.http = requests

    def get_token(self) -> str:
        return self.token

    def set_token(self, token: str):
        self.token = token

    def get_serializer_class(self):
        if not self.model:
            raise Exception('You need to override .get_serializer_class() method or '
                            'provide a default serializer_class.')

        return self.serializer_class

    def set_serializer_class(self, serializer_class):
        self.serializer_class = serializer_class

    def get_model(self):
        if not self.model:
            raise Exception('You need to override .get_model() method or provide a default model.')

        return self.model

    def pluralize(self, text: str) -> str:
        """
            Pluralizes a word depending on the last letter of the word
        """
        return f'{text}ies' if text[-1] == 'y' else f'{text}s'

    def get_model_slug(self) -> str:
        """
            Returns the model slug
        """
        slug = re.sub('(?<=.)([A-Z]+)', '-\\1', self.get_model().__name__).lower()
        return self.pluralize(slug)

    def get_url(self, *url_params) -> str:
        """
            Returns the url based on the url params
        """
        params = (self.api_url, self.get_model_slug(), *url_params)
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

    def serialize(self, instance, many=False):
        """
            Returns the serialized data given the model instance
        """
        serializer = self.get_serializer_class()
        serialized = serializer(instance, many=many)
        serialized.is_valid(raise_exception=True)

        return serialized.validated_data

    def deserialize(self, data, many=False) -> Union[dict, list, QuerySet]:
        """
            Returns the deserialized data given the data
        """
        serializer = self.get_serializer_class()
        return serializer(data=data, many=many).validated_data

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

    def get_queryset(self, data: list, exact_order=True, as_pk_list=False) -> Union[list, QuerySet]:
        """
            Returns the queryset given the received data
        """
        pks = [item[self.primary_key_field_name] for item in data]

        if as_pk_list:
            return pks

        q = {
            f'{self.primary_key_field_name}__in': pks
        }
        results = self.get_model().objects.filter(**q)

        if exact_order:
            order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)])
            results = results.order_by(order)

        return results

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
        http_queryset = HttpDataSet(data=data, serializer=self.get_serializer_class())

        return ProxyResponse(data_set=http_queryset, status=response.status_code)

    def post(self, data: dict, query: dict = None) -> ProxyResponse:
        """
            Performs a POST request to the server
        :param data: Data attached
        :param query: Extra querystring as a dict
        :return: JSON response as a dict
        """
        response = self.http.post(self.get_url(), data=data, headers=self.get_headers(), params=query)
        data = self.get_response_data(response)
        http_queryset = HttpDataSet(data=data, serializer=self.get_serializer_class())

        return ProxyResponse(data_set=http_queryset, status=response.status_code)

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
        http_queryset = HttpDataSet(data=data, serializer=self.get_serializer_class())

        return ProxyResponse(data_set=http_queryset, status=response.status_code)

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
        http_queryset = HttpDataSet(data=data, serializer=self.get_serializer_class())

        return ProxyResponse(data_set=http_queryset, status=response.status_code)

    def destroy(self, pk: Any, query: dict = None) -> ProxyResponse:
        return self.delete(pk=pk, query=query)
