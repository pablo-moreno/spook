from typing import Type

from rest_framework.serializers import Serializer


class InputValidator(object):
    serializer_class: Type[Serializer] = None

    def validate(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return data
