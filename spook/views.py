from typing import Type

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.response import Response
from .resources import APIResource


class APIResourceMixin(object):
    resource: Type[APIResource] = None

    def get_resource(self):
        if not self.resource:
            raise Exception('You have to specify the service property or override .get_service() function')

        return self.resource


class APIResourceListView(ListAPIView, APIResourceMixin):
    def list(self, request, *args, **kwargs):
        resource = self.get_resource()
        params = request.query_params
        response = resource().list(**params)

        return Response(data=response.data, status=response.status)


class APIResourceRetrieveView(RetrieveAPIView, APIResourceMixin):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        resource = self.get_resource()
        params = request.query_params
        response = resource().retrieve(pk, **params)

        return Response(data=response.data, status=response.status)


class APIResourceCreateView(CreateAPIView, APIResourceMixin):
    def create(self, request, *args, **kwargs):
        resource = self.get_resource()
        response = resource().post(data=request.data, query=request.query_params)

        return Response(data=response.data, status=response.status)


class APIResourcePutView(UpdateAPIView, APIResourceMixin):
    def update(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        resource = self.get_resource()
        response = resource().put(pk=pk, data=request.data, query=request.query_params)

        return Response(data=response.data, status=response.status)


class APIResourceDestroyView(DestroyAPIView, APIResourceMixin):
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        resource = self.get_resource()
        response = resource().delete(pk=pk, query=request.query_params)

        return Response(data=response.data, status=response.status)


class APIResourceRetrieveUpdateView(APIResourceRetrieveView, APIResourcePutView):
    pass


class APIResourceRetrieveUpdateDestroyView(APIResourceRetrieveUpdateView, APIResourceDestroyView):
    pass


class APIResourceListCreateView(APIResourceListView, APIResourceCreateView):
    pass
