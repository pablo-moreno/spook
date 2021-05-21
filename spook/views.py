from typing import Type

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from .resources import APIResource
from .validators import InputValidator


class APIResourceMixin(object):
    resource: Type[APIResource] = None

    def get_token(self, request):
        raise NotImplementedError

    def get_resource(self):
        if not self.resource:
            raise Exception(
                "You have to specify the service property or override .get_resource() function"
            )

        return self.resource

    def get_validator(self):
        serializer = self.get_serializer_class()

        class Validator(InputValidator):
            serializer_class = serializer

        return Validator


class APIResourceListView(ListAPIView, APIResourceMixin):
    def list(self, request, *args, **kwargs):
        resource = self.get_resource()
        token = self.get_token(request)
        params = request.query_params
        serializer = self.get_serializer_class()
        context = {
            "request": request,
        }
        response = resource(
            token=token, validator=self.get_validator(), context=context
        ).list(**params)

        return Response(data=response.data, status=response.status)


class APIResourceRetrieveView(RetrieveAPIView, APIResourceMixin):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        resource = self.get_resource()
        token = self.get_token(request)
        params = request.query_params
        context = {
            "request": request,
        }
        response = resource(
            token=token, validator=self.get_validator(), context=context
        ).retrieve(pk, **params)

        return Response(data=response.data, status=response.status)


class APIResourceCreateView(CreateAPIView, APIResourceMixin):
    def create(self, request, *args, **kwargs):
        resource = self.get_resource()
        token = self.get_token(request)
        context = {
            "request": request,
        }
        response = resource(
            token=token, validator=self.get_validator(), context=context
        ).create(data=request.data, query=request.query_params)

        return Response(data=response.data, status=response.status)


class APIResourcePutView(UpdateAPIView, APIResourceMixin):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        pk = kwargs.get(self.lookup_field)
        resource = self.get_resource()
        token = self.get_token(request)
        context = {
            "request": request,
        }
        response = resource(
            token=token, validator=self.get_validator(), context=context
        ).update(pk=pk, data=request.data, query=request.query_params, partial=partial)

        return Response(data=response.data, status=response.status)


class APIResourceDestroyView(DestroyAPIView, APIResourceMixin):
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        resource = self.get_resource()
        token = self.get_token(request)
        context = {
            "request": request,
        }
        response = resource(
            token=token, validator=self.get_validator(), context=context
        ).delete(pk=pk, query=request.query_params)

        return Response(data=response.data, status=response.status)


class APIResourceRetrieveUpdateView(APIResourceRetrieveView, APIResourcePutView):
    pass


class APIResourceRetrieveUpdateDestroyView(
    APIResourceRetrieveUpdateView, APIResourceDestroyView
):
    pass


class APIResourceListCreateView(APIResourceListView, APIResourceCreateView):
    pass
