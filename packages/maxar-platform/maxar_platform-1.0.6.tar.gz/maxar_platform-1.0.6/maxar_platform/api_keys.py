"""
API keys are an alternative to OAuth2 authentication.

They are more compact than OAuth2 bearer tokens which makes them easier to send as URL parameters.

Unlike bearer tokens which expire in two hours, API keys have a default 6 month lifespan. It is also possible to
set the expiration date as short as needed. API keys can not be renewed or extended, once they expire a new one must
be created.

API keys have the same roles and scopes as your account but can not be used on any of the administrative endpoints:

- Admin API
- API Key Service
- Oauth2 Authentication

API Key dictionaries use a custom representations that mask out the API key string when they are displayed/printed.

    >>> key = generate_key("my key")
    >>> print(key)

    {'id': '5431dd15-3efe-418a-b04d-acdca3a4d281',
     'name': 'my key',
     'description': '',
     'api_key': '*******',
     'last_modified_date': '2023-07-20 19:44:07',
     'created_date': '2023-07-20 19:44:07',
     'expiration_date': '2024-03-12 18:33:23'}

The `api_key` value is not otherwise masked, be careful with:

    >>> print(key['api_key'])
    <your key will print out!>


Reference
---------

https://developers.maxar.com/docs/authentication/guides/api-key

"""

import pprint
from posixpath import join

import pendulum

from maxar_platform import BASE_URL
from maxar_platform.exceptions import MissingAPIResource
from maxar_platform.session import session

__all__ = ["generate_key", "list_keys", "delete_key", "get_key"]


KEYS_URL = join(BASE_URL, "api-key/api/v2/api-key")
KEYS_KEY = join(KEYS_URL, "id/:id")


def generate_key(name="", description="", expiration=None, lifespan=None):
    """Generate a new API key

    Keywords
    ----------
    name: str, optional
        Name of key, while optional highly recommended.
    description: str, optional
        Description of key.
    expiration: datelike object
        Expiration date. Can be Date or Datetime objects, or strings of dates in common formats. Maximum lifespan is 6 months.
    lifespan: int
        Lifespan of keys in days if you don't want to compute an expiration date.

    Returns
    -------
    KeyDict
        Key as Python dictionary with special `str` and `repr` methods to mask keys from accidental display.

    """

    expires_format = "YYYY-MM-DD HH:mm:ss"

    payload = {"name": name, "description": description}

    if expiration and lifespan:
        raise ValueError("Tokens can be given an `expiration` OR a `lifespan`, not both")

    if expiration:
        expires = pendulum.parse(expiration)
        payload["expiration_date"] = expires.format(expires_format)

    if lifespan:
        expires = pendulum.now().add(days=lifespan)
        payload["expiration_date"] = expires.format(expires_format)

    return KeyDict(session.oauth_session.post(KEYS_URL, json=payload).json())


def list_keys():
    """List keys associated with your user

    Returns
    -------
    list of KeyDict
        All of user's keys, including expired ones

    """
    return [KeyDict(k) for k in session.oauth_session.get(KEYS_URL).json()]


def delete_key(key_or_id):
    """Delete an API key

    Parameters
    ----------
    key: KeyDict or str
        Either a key dictionary, or a key's ID string

    Returns
    -------
    None

    Note
    ----
    A key's ID is the 'id' value, not the 'api_key' value that is used for authentication.


    """
    if isinstance(key_or_id, dict):
        key_id = key_or_id["id"]
    else:
        key_id = key_or_id
    url = KEYS_KEY.replace(":id", key_id)
    try:
        session.oauth_session.delete(url)
    except MissingAPIResource:
        raise MissingAPIResource(f"API Key with ID {key_id} was not found")


def get_key(**kwargs):
    """Get a key

    Keywords
    ----------
    id: str, optional
    name: str, optional
    description: str, optional
    api_key: str, optional

    Returns
    -------
    KeyDict
        The first key found matching the supplied keyword arguments.

    Note
    ----
    You can match to any ONE of the KeyDict fields, however in most cases you would use ID or name.
    Matching is exact, there is no support for wildcards or other regex magic at this time.

    """
    if len(kwargs) > 1:
        raise ValueError("API keys can only be retrieved on a single property")
    for k, v in kwargs.items():
        for key in list_keys():
            if key[k] == v:
                return KeyDict(key)
    raise MissingAPIResource(f"API Key with {k} `{v}` was not found")


class KeyDict(dict):
    """A dictionary class for keys that masks the key value when printed or displayed"""

    def __str__(self):
        masked = self.copy()
        masked["api_key"] = "**************"
        return pprint.pformat(masked, sort_dicts=False)

    def __repr__(self):
        masked = self.copy()
        masked["api_key"] = "*******"
        return str(masked)
