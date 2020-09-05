from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.response import Response
from .services import HttpService


class HttpServiceMixin(object):
    service: 'HttpService' = None

    def get_service(self):
        if not self.service:
            raise Exception('You have to specify the service property or override .get_service() function')

        return self.service


class HttpServiceListView(ListAPIView, HttpServiceMixin):
    def list(self, request, *args, **kwargs):
        service = self.get_service()
        params = request.query_params
        response = service.list(**params)

        return Response(data=response.queryset.data, status=response.status)


class HttpServiceRetrieveView(RetrieveAPIView, HttpServiceMixin):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        service = self.get_service()
        params = request.query_params
        response = service.retrieve(pk, **params)

        return Response(data=response.queryset.data, status=response.status)


class HttpServiceCreateView(CreateAPIView, HttpServiceMixin):
    def create(self, request, *args, **kwargs):
        service = self.get_service()
        response = service.post(data=request.data, query=request.query_params)

        return Response(data=response.queryset.data, status=response.status)


class HttpServicePutView(UpdateAPIView, HttpServiceMixin):
    def update(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        service = self.get_service()
        response = service.put(pk=pk, data=request.data, query=request.query_params)

        return Response(data=response.queryset.data, status=response.status)


class HttpServiceDestroyView(DestroyAPIView, HttpServiceMixin):
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get(self.lookup_field)
        service = self.get_service()
        response = service.delete(pk=pk, query=request.query_params)

        return Response(data=response.queryset.data, status=response.status)


class HttpServiceRetrieveUpdateView(HttpServiceRetrieveView, HttpServicePutView):
    pass


class HttpServiceRetrieveUpdateDestroyView(HttpServiceRetrieveUpdateView, HttpServiceDestroyView):
    pass


class HttpServiceListCreateView(HttpServiceListView, HttpServiceCreateView):
    pass
