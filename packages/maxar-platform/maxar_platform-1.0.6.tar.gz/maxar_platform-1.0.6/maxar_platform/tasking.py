"""
Provides
--------

Functions for managing tasking requests:

- Validate, quote the cost of, and submit a tasking request
- Get one or list multiple taskings
- Cancel an tasking request

Reference
---------
https://developers.maxar.com/docs/tasking/

"""

from posixpath import join
from typing import List, Union

from maxar_platform import BASE_URL
from maxar_platform.session import paginated_request, session

__all__ = (
    "submit_tasking",
    "validate_tasking",
    "quote_tasking",
    "get_tasking",
    "cancel_tasking",
    "list_taskings",
)

TASKING_BASE = join(BASE_URL, "tasking/v1/tasking")
TASKING_QUOTE = join(TASKING_BASE, "quote")
TASKING_TASKING = join(TASKING_BASE, ":id")
TASKING_CANCEL = join(TASKING_TASKING, "cancel")


def list_taskings(
    limit=100,
    sort="desc",
    filter=None,
):
    """Fetch user's taskings

    Parameters
    ----------
    limit: int or None, default None
        Maximum number of taskings to fetch, None means unlimited, default is 100.
    sort: str
        Sort tasking for tasking IDs, either 'asc' (ascending) or 'desc' (descending). Default is 'desc'.
    filter: str or iterable of strings
        Filter results that match values contained in the given key separated by a colon.
        Matches are not exact: filtering on a value of `pet:cat` will return `cat` along with `caterpillar` pets.
        Multiple filters can be passed but keys must be unique since filters will be logically ANDed.
        Example: 'product_id:1234' or ['pet:cat', 'color:black']

    Returns
    -------
    list
        Tasking objects matching parameters"""

    params = {}

    if filter is not None:
        params["filter"] = filter

    return paginated_request("GET", TASKING_BASE, "taskings", sort, limit, **params)


def get_tasking(tasking_id):
    """Fetch a Tasking object from an ID

    Parameters
    ----------
    tasking_id : str
        Tasking ID to fetch metadata for

    Returns
    -------
    dict
        API data for the given tasking"""

    url = TASKING_TASKING.replace(":id", tasking_id)
    r = session.get(url)
    return r.json()["data"]


def cancel_tasking(tasking_id, reason=None):
    """Cancel a tasking request from an ID

    Parameters
    ----------
    tasking_id : str
        Tasking ID to cancel
    reason : str, optional
        Optional opportunity to record why the tasking request was cancelled for visibility to other users


    Returns
    -------"""

    data = {}

    if reason:
        data["reason"] = reason

    url = TASKING_CANCEL.replace(":id", tasking_id)
    r = session.post(url, json=data)


def submit_tasking(tasking):
    """Send a request to the Tasking API

    Parameters
    ----------
    payload : dict
        Tasking API request payload

    Returns
    -------
    dict
        API response data for the given Order"""
    r = session.post(TASKING_BASE, json=tasking)
    return r.json()["data"]


def quote_tasking(tasking):
    """Quote a tasking request (does not submit)

    Parameters
    ----------
    payload : dict
        Tasking API request payload

    Returns
    -------
    dict
        Quotation for the cost of collecting imagery for the given tasking parameters"""
    r = session.post(TASKING_QUOTE, json=tasking)
    return r.json()["data"]


def validate_tasking(tasking):
    """Validate a request to the Tasking API

    Parameters
    ----------
    payload : dict
        Tasking API request payload

    Returns
    -------
    dict
        Tasking object whose settings are all valid"""

    params = {"validation_only": "true"}
    r = session.post(TASKING_BASE, params=params, json=tasking)
    return r.json()["data"]
