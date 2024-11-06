from django.conf import settings
from rest_framework.settings import APISettings

__all__ = ["simple_access_key_settings"]


SIMPLE_ACCESS_KEY_SETTINGS = {
    "HTTP_AUTHORIZATION_HEADER": "x-authorization",
    "HTTP_AUTHORIZATION_SCHEME": "bearer",
    "AUTHORIZATION_KEYS": [],
}


def simple_access_key_settings():
    return APISettings(
        user_settings=getattr(settings, "SIMPLE_ACCESS_KEY_SETTINGS", {}),
        defaults=SIMPLE_ACCESS_KEY_SETTINGS,
    )
