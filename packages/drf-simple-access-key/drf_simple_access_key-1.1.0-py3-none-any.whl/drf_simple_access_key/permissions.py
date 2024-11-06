from drf_simple_access_key.settings import simple_access_key_settings

__all__ = ["SimpleAccessKey"]


class SimpleAccessKey(object):
    """
    Allow access if a valid authorisation token was part of the request headers. The authorization
    data consists of a scheme ("Bearer" in this case) and the actual key. If no valid keys are
    configured in the application settings, this permission class will grant access.
    """

    def has_permission(self, request, view):
        """
        Grants permission if the given authorization key is within the configured allowed keys. Also grants
        permission if no allowed keys are configured.
        """
        settings = simple_access_key_settings()
        allowed_keys = settings.AUTHORIZATION_KEYS
        request_key = request.headers.get(settings.HTTP_AUTHORIZATION_HEADER)

        if not allowed_keys:
            return True

        try:
            key_schema, key = request_key.split(" ", maxsplit=1)
            key_schema, key = key_schema.strip().lower(), key.strip()

            return (
                key_schema == settings.HTTP_AUTHORIZATION_SCHEME and key in allowed_keys
            )
        except (
            AttributeError,
            ValueError,
        ):
            return False

    def has_object_permission(self, request, view, obj):
        """
        This permission class has no special implementation of per-object permissions, so the result
        will be the same as the `has_permission` method.
        """
        return self.has_permission(request, view)
