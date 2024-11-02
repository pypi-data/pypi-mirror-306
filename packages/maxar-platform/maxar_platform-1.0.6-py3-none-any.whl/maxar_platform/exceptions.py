""" SDK Exceptions """

from datetime import datetime

__all__ = [
    "MissingDependency",
    "APIServerException",
    "BadAPIRequest",
    "MissingAPIResource",
    "OversizeRequestException",
    "UnAuthorizedException",
]

#########
# General Errors
#########


class MissingDependency(Exception):
    """A dependency required for this functionality has not been installed"""

    pass


#########
# API Errors
#########


class APIServerException(Exception):
    """The API service encountered an error"""

    def __init__(self, msg, *args, **kwargs):
        msg = f"{msg} ({datetime.now()})"
        super().__init__(msg, *args, **kwargs)


class BadAPIRequest(Exception):
    """The API request sent was incorrectly formatted"""

    pass


class MissingAPIResource(Exception):
    """An API request returned a 404"""

    pass


class OversizeRequestException(Exception):
    """The API request sent was incorrectly formatted"""

    pass


class UnAuthorizedException(Exception):
    """The API request's credentials were rejected"""

    pass


########
# Hook functions for Request.Session.hooks
########


def messenger(request):
    try:
        payload = request.json()
        message = payload.get("message")
        messages = payload.get("error", {}).get("error_messages")
        if messages:
            messages = "; ".join(messages)
        return message or messages or request.text
    except:
        return request.text


def oversize_request_hook(r, *args, **kwargs):
    """
    Hook for handling oversize request errors from API.
    """
    if r.status_code == 413 and "Request Entity Too Large" in r.json()["message"]:
        raise OversizeRequestException(f"{messenger(r)}, Reduce size of attributes and try again.")

    return r


def bad_api_request_hook(r, *args, **kwargs):
    """
    Hook for handling 400 errors from API.
    """
    if r.status_code == 400:
        raise BadAPIRequest(messenger(r))
    return r


def unauth_request_hook(r, *args, **kwargs):
    """
    Hook for handling 401 errors from API.
    """
    if r.status_code in [401, 403]:
        raise UnAuthorizedException(
            f"Server responded with {r.status_code} '{messenger(r)}', check your credentials and try again."
        )

    return r


def missing_resource_hook(r, *args, **kwargs):
    if r.status_code == 404:
        raise MissingAPIResource(messenger(r))

    return r


def api_server_request_hook(r, *args, **kwargs):
    """
    Hook for handling non-20X errors from API.
    """
    if not r.ok:
        raise APIServerException(messenger(r))

    return r
