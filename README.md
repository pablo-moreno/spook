# Django Spook

![PyPI](https://img.shields.io/pypi/v/spook?style=flat-square)
[![codecov](https://codecov.io/gh/pablo-moreno/spook/branch/master/graph/badge.svg?token=6ZAHAHZG7Z)](https://codecov.io/gh/pablo-moreno/spook/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Library to interconnect multiple external HTTP APIs as Http Services

## Installation

```bash
pip install spook
```

## Usage

Declare a serializer class for your input validation

```python
from rest_framework import serializers

class MySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    
    class Meta:
        fields = ('name', 'age', )
```

Declare an InputValidator

```python
from spook.validators import InputValidator


class MyResourceInputValidator(InputValidator):
    serializer_class = MySerializer
```


Declare an API Resource class.

```python
from spook.resources import APIResource


class MyResource(APIResource):
    api_url = 'https://my.external/api'
    validator = MyResourceInputValidator
```

Now you can instance MyResource class and use the methods

```python
resource = MyResource()

# List resources
resource.list()

# Retrieve a single resource
resource.retrieve(pk=1)

# Create resource
resource.create({'name': 'Pablo', 'age': 28})

# Update resource
resource.update(pk=1, data={'name': 'Pablo Moreno'})

# Delete resource
resource.delete(pk=1)
```

There are also some views available

```python
from spook.views import (
    APIResourceRetrieveView, APIResourceListView, APIResourceCreateView, APIResourcePutView,
    APIResourceRetrieveUpdateView, APIResourceRetrieveUpdateDestroyView, APIResourceListCreateView,
)


class ListCreateProductResourceView(APIResourceListCreateView):
    resource = ProductResource

    def get_token(self, request):
        return ''  # Wee need to override get_token()


class RetrieveUpdateDestroyProductResourceView(APIResourceRetrieveUpdateDestroyView):
    resource = ProductResource

    def get_token(self, request):
        return ''
```
