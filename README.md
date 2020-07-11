# Django Spook

Library to interconnect multiple external HTTP APIs as Http Services

## Installation

```bash
pip install django-spook
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

Declare a Http Service class

```python
from spook.services import HttpService

class MyService(HttpService):
    model = MyModel
    serializer_class = MyModelSerializer
    api_url = 'https://my.external/api'
```

And you can instance MyService class and use the methods

```python
service = MyService()

response = service.list()
data = response.data_set.data
service.get_queryset(data=data)
```