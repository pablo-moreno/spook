# Django Spook

![PyPI](https://img.shields.io/pypi/v/spook?style=flat-square)
[![codecov](https://codecov.io/gh/pablo-moreno/spook/branch/master/graph/badge.svg?token=6ZAHAHZG7Z)](https://codecov.io/gh/pablo-moreno/spook/)

Library to interconnect multiple external HTTP APIs as Http Services

## Installation

```bash
pip install spook
```

## Usage

Declare your internal model

```python
class MyModel(models.Model):
    name = models.CharField(max_length=16)
    age = models.IntegerField(default=0)
```

Declare a serializer class for your external service

```python
from rest_framework import serializers

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ('name', 'age', )
```

Declare a Http Service class and its manager.

```python
from spook.resources import APIResource
from spook.managers import DatabaseDataManager

class MyManager(DatabaseDataManager):
    model = MyModel
    serializer = MyModelSerializer

class MyResource(APIResource):
    api_url = 'https://my.external/api'
    manager = MyManager
```

And you can instance MyService class and use the methods

```python
resource = MyResource()

response = resource.list()
data = response.queryset
queryset = data.get_queryset()
```
