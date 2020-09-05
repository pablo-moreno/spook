from typing import Type, Union

from django.db.models import Model, QuerySet, Case, When
from rest_framework.serializers import Serializer


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
