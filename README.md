# Django Spook

Library to interconnect multiple external HTTP APIs as Http Services

## Installation

```bash
pip install django-spook
```

## Usage

Declare a serializer class for your external service

```python
from rest_framework import serializers

class MyServiceSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
```

Declare a Http Service class

```python
from django_spook.services import HttpService

class MyService(HttpService):
    serializer_class = MyServiceSerializer
    api_url = 'https://my.external/api'
    
```

And you can instance MyService class and use the methods

```python
service = MyService()

service.list()

```