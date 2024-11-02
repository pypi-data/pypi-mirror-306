"""
Provides
--------

Communication with the APIs through a single global `session` object using the Python
Requests library. The session object provides:

- Retries
- Error Handling
- wraps up API Key and Ouath2 sessions into a single session
- Uses API Keys preferentially if both authentication methods are configured
- Credentials are read from envvars only
- an interactive login form

If you must store credentials in a file, see the dotenv package and be careful not to
commit the file into source control!

Reference
---------
https://developers.maxar.com/docs/authentication/

"""

import html
import os
import sys
import time
from getpass import getpass
from platform import python_version, system

import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests.adapters import HTTPAdapter
from requests.models import PreparedRequest
from requests.packages.urllib3.util.retry import Retry
from requests_oauthlib import OAuth2Session

from maxar_platform import CLIENT_ID, PACKAGE
from maxar_platform.exceptions import (
    api_server_request_hook,
    bad_api_request_hook,
    missing_resource_hook,
    oversize_request_hook,
    unauth_request_hook,
)

try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata

__all__ = ("session", "MaxarSession", "paginated_request", "setenv", "unsetenv")


class NoSessionCredentials(Exception):
    """No credentials were found for this session"""

    pass


def setenv(api_key=None, username=None, password=None):
    """Set any of the three envvars used for authentication

    Keywords
    ----------
    api_key: str, optional
        API Key if used
    username: str, optional
        Username, use with `password`
    password: str, optional
        Password, use with `username`

    """
    if api_key:
        os.environ["MAXAR_API_KEY"] = api_key
    if username:
        os.environ["MAXAR_USERNAME"] = username
    if password:
        os.environ["MAXAR_PASSWORD"] = password


def unsetenv():
    """Unset all of the envvars used for authentication"""

    for key in ["MAXAR_API_KEY", "MAXAR_USERNAME", "MAXAR_PASSWORD"]:
        try:
            del os.environ[key]
        except KeyError:
            pass


# Timeout and Retry handling
# from https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/


MAXAR_API_TIMEOUT = os.environ.get(
    "MAXAR_API_TIMEOUT", 30
)  # seconds, this is high for big selects and dry run orders


class TimeoutHTTPAdapter(HTTPAdapter):
    """HTTP Adapter that adds in default timeouts

    Keywords
    --------
    timeout(numeric): seconds to wait before timing out

    """

    def __init__(self, *args, **kwargs):
        self.timeout = MAXAR_API_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def mount_adaptors(session):
    """Mount adaptors to a session for retries and update UA string

    Arguments
    ---------
    session: Requests session
    """

    retries = Retry(total=3, backoff_factor=5, status_forcelist=[429, 503, 504])
    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    session.mount("http://", TimeoutHTTPAdapter(max_retries=retries))
    version = metadata.version("maxar_platform")
    session.headers.update(
        {
            "User-Agent": f"{PACKAGE}/maxar_platform {version} (Python {python_version()}/{system()})"
        }
    )
    return session


def paginated_request(method, url, key, sort="asc", limit=None, **params):
    """A paginated request wrapper

    Parameters
    ----------
    method: str
        Request method for requests to use, i.e. "get", "post", etc
    url: str
        URL of endpoint to fetch from
    key:
        Name of key in the response to find the returned objects. Usually this is just 'data'

    Keywords
    --------
    sort: str
        Sort order, either 'asc' or 'desc'
    limit: int
        Limit of number of objects total objects to fetch

    Returns
    -------
    list of objects
        The objects from all the paginated requests are returned as a single list
    """
    params["sort"] = sort
    for k in list(params.keys()):
        if not params[k]:
            del params[k]
    response = session.request(method, url, params=params).json()
    things = response["data"][key].copy()
    while response.get("next_page_token"):
        params["starting_after"] = response["next_page_token"]
        response = session.request(method, url, params=params).json()
        things.extend(response["data"][key])
        if limit:
            if len(things) > limit:
                return things[:limit]
    return things


def add_session_hooks(session):
    """
    Add hooks for session object, and return it.
    Note: Order of Hooks is important.
    """
    session.hooks["response"] = [
        # Generic 400 errors
        bad_api_request_hook,
        # 413 errors
        oversize_request_hook,
        # 403 errors
        unauth_request_hook,
        # 404 errors
        missing_resource_hook,
        # non-200 errors
        api_server_request_hook,
    ]

    return session


def MaxarKeySession(key):
    """A requests.session that uses API Keys for authentication

    Parameters
    ----------
    key: str
        An API key

    """

    key_header = {"MAXAR-API-KEY": key}
    key_param = {"maxar_api_key": key}

    def sign_url(url):
        req = PreparedRequest()
        req.prepare_url(url, key_param)
        return req.url

    session = requests.Session()
    session.headers.update(key_header)
    session = mount_adaptors(session)
    session.sign_url = sign_url
    session.key = key
    return add_session_hooks(session)


AUTH_URL = "https://account.maxar.com/auth/realms/mds/protocol/openid-connect/token"


def MaxarOauthSession(username, password, auth_url=AUTH_URL):
    """A requests_oauthlib.session that uses OAuth

    Parameters
    ----------
    username: str
        Username
    password: str
        Password
    auth_url: str
        Authentication URL
    """

    def save_token(token):
        session.token = token

    session = OAuth2Session(
        client=LegacyApplicationClient(CLIENT_ID),
        auto_refresh_url=auth_url,
        auto_refresh_kwargs={"client_id": CLIENT_ID},
        token_updater=save_token,
    )

    session.fetch_token(auth_url, username=username, password=password, client_id=CLIENT_ID)

    session = mount_adaptors(session)
    return add_session_hooks(session)


class NullKeySession:
    """A placeholder object for KeySession when no credentials are found

    This provides nice error messages and is also false-y

    """

    def __getattribute__(self, name):
        msg = "The API key session was explicitly called but no key was found in the `MAXAR_API_KEY` envvar.\n"
        msg = (
            msg
            + "If you are in an interactive session, call `session.login` to temporarily set an API key."
        )
        raise NoSessionCredentials(msg)

    def __bool__(self):
        return False


class NullOauthSession:
    """A placeholder object for OauthSession when no credentials are found

    This provides nice error messages and is also false-y

    """

    def __getattribute__(self, name):
        msg = "The Oauth session was explicitly called but no credentials were found in the `MAXAR_USERNAME` and `MAXAR_PASSWORD` envvars.\n"
        msg = (
            msg
            + "If you are in an interactive session, call `session.login` to temporarily set your credentials."
        )
        raise NoSessionCredentials(msg)

    def __bool__(self):
        return False


class MaxarSession:
    """A Session wrapper that provides a single point of entry

    If available, will try to use a Key session first.

    To use this object to use a specific authentication, the key and OAuth sessions are available under the
    key_session and oauth_session attributes.

    This module provides an initalized instance under the name 'session'
    """

    def __init__(self):
        self.key_session = NullKeySession()
        self.oauth_session = NullOauthSession()
        key = os.environ.get("MAXAR_API_KEY")
        if key:
            self.key_session = MaxarKeySession(key)
        user = os.environ.get("MAXAR_USERNAME")
        password = os.environ.get("MAXAR_PASSWORD")
        if user and password:
            self.oauth_session = MaxarOauthSession(user, password)

    def __getattr__(self, name):
        # call the key session
        key_session = object.__getattribute__(self, "key_session")
        if name == "key_session" and key_session:
            return key_session
        if name == "key_session" and not key_session:
            raise NoSessionCredentials('No API key set - use the envvar "MAXAR_API_KEY"')
        if key_session and name != "oauth_session":
            return key_session.__getattribute__(name)
        # otherwise try the oauth session
        oauth_session = object.__getattribute__(self, "oauth_session")
        if name == "sign_url":
            raise NoSessionCredentials(
                "To sign URLs you must have API Key credentials configured first"
            )
        if name == "oauth_session" and oauth_session:
            return oauth_session
        if name == "oauth_session" and not oauth_session:
            raise NoSessionCredentials(
                'No Oauth credentials set - use the envvars "MAXAR_USERNAME" and "MAXAR_PASSWORD"'
            )
        if oauth_session:
            return oauth_session.__getattribute__(name)
        raise NoSessionCredentials(
            'No credentials are set in envvars "MAXAR_API_KEY", "MAXAR_USERNAME", and "MAXAR_PASSWORD".\n You can use "session.login" in an interactive session'
        )

    def reload(self):
        """Reloads the underlying sessions, for instance if envvars have changed"""
        self.__init__()

    def login(self):
        """An interactive login for terminal or notebook use when envvars are not configured"""
        if sys.stdin.isatty() or hasattr(sys, "ps1"):
            print(
                "Log in with a username/password and/or an API key.\nCredentials are not saved - use envvars to store them."
            )
            username = input("Username or <enter> to skip: ")
            password = getpass("Password or <enter> to skip: ")
            api_key = getpass("API key or <enter> to skip: ")
            setenv(api_key=api_key, username=username, password=password)
            self.reload()
        else:
            raise NotImplemented(
                '"session.login()" is for interactive prompts only. For scripts set envvars to supply credentials.'
            )

    def __str__(self):
        try:
            key = self.key_session.headers["MAXAR-API-KEY"][:7]
            key_text = f" (Key session using {key}... available)"
        except:
            key_text = ""
        try:
            token = self.oauth_session.token
            oauth_text = " (OAuth session available)"
        except:
            oauth_text = ""
        if key_text == "" and oauth_text == "":
            key_text = " (No credentials configured)"
        return f"<MaxarSession{key_text}{oauth_text}>"

    def __repr__(self):
        return str(self)

    def _repr_html_(self):
        return "<pre>" + html.escape(str(self)) + "</pre>"

    def _repr_pretty_(self, p, cycle):
        p.text(str(self))


# create an instance for easy use, note this is not a true singleton
session = MaxarSession()
""" A session instance, ready to use """
