from django.conf import settings

EXTERNAL_API_URL = getattr(settings, 'SPOOK_API_URL', '')
AUTHORIZATION_HEADER_NAME = getattr(settings, 'SPOOK_AUTHORIZATION_HEADER_NAME', 'Authorization')
AUTHORIZATION_HEADER = getattr(settings, 'SPOOK_AUTHORIZATION_HEADER', 'Bearer')
