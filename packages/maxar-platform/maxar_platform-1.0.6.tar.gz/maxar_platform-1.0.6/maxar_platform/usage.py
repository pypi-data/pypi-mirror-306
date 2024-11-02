"""
Provides
--------

Usage information for the user making the requests.

Reference
---------
https://developers.maxar.com/docs/usage/

"""

from posixpath import join

from maxar_platform import BASE_URL
from maxar_platform.exceptions import APIServerException
from maxar_platform.session import session

__all__ = ["get_usage", "usage_is_allowed"]


USAGE_URL = join(BASE_URL, "usage/v1/")
USAGE_OVERVIEW = join(USAGE_URL, "activation/overview")
USAGE_ALLOWED = join(USAGE_URL, "allowed")


def get_usage():
    """Get usage information for the user making the request

    Returns
    -------
    KeyDict
        Key as Python dictionary with special `str` and `repr` methods to mask keys from accidental display.

    """

    return session.oauth_session.get(USAGE_OVERVIEW).json()


def usage_is_allowed():
    """Check if usage is allowed for the requesting user


    Returns
    -------
    Boolean
        True if the user is allowed usage.
    """
    try:
        session.oauth_session.get(USAGE_ALLOWED)
        return True
    except APIServerException:
        return False
