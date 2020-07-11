from django.conf import settings

EXTERNAL_API_URL = getattr('SPOOK_API_URL', settings, '')
AUTHORIZATION_HEADER_NAME = getattr('SPOOK_AUTHORIZATION_HEADER_NAME', settings, 'Authorization')
AUTHORIZATION_HEADER = getattr('SPOOK_AUTHORIZATION_HEADER', settings, 'Bearer')
