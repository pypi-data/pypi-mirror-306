"""
Provides
--------

Functions for working with the Order API to:

- Validate, estimate cost, and place an order to a pipeline
- Get one or list multiple placed orders
- Cancel an order (if supported by the pipeline)
- Get order events to check progress

There are no formal objects for orders and order settings, an order "object" is a Python dictionary.

References
----------
https://developers.maxar.com/docs/ordering/


"""

from posixpath import join
from typing import List, Union

from maxar_platform import BASE_URL
from maxar_platform.session import paginated_request, session

__all__ = (
    "submit_order",
    "validate_order",
    "estimate_order_usage",
    "get_order",
    "get_order_events",
    "cancel_order",
    "list_orders",
)

API_BASE = join(BASE_URL, "ordering/v1")
ORDERING_ORDERS = join(API_BASE, "orders")
ORDERING_ORDER = join(ORDERING_ORDERS, ":id")
ORDERING_ORDER_EVENTS = join(ORDERING_ORDER, "events")
ORDERING_ORDER_CANCEL = join(ORDERING_ORDER, "cancel")
ORDERING_PIPELINES = join(API_BASE, "pipelines")
ORDERING_PIPELINE_ORDER = join(ORDERING_PIPELINES, ":namespace/:name/order")
ORDERING_PIPELINE_VALIDATE = join(ORDERING_PIPELINES, ":namespace/:name/validate")
ORDERING_PIPELINE_ESTIMATE = join(ORDERING_PIPELINES, ":namespace/:name/estimate")


def list_orders(
    limit=100,
    sort="desc",
    filter=None,
):
    """Fetch user's orders

    Parameters
    ----------
    limit: int or None, default None
        Maximum number of orders to fetch, None means unlimited, default is 100.
    sort: str
        Sort order for order IDs, either 'asc' (ascending) or 'desc' (descending). Default is 'desc'.
    filter: str or iterable of strings
        Filter results that match values contained in the given key separated by a colon.
        Matches are not exact: filtering on a value of `pet:cat` will return `cat` along with `caterpillar` pets.
        Multiple filters can be passed but keys must be unique since filters will be logically ANDed.
        Example: 'product_id:1234' or ['pet:cat', 'color:black']

    Returns
    -------
    list
        Order objects matching parameters"""

    return paginated_request("GET", ORDERING_ORDERS, "orders", sort, limit, filter=filter)


def get_order(order_id):
    """Fetch raw data about an Order from an ID

    Parameters
    ----------
    order_id : str
        Order ID to fetch metadata for

    Returns
    -------
    dict
        API data for the given Order"""

    url = ORDERING_ORDER.replace(":id", order_id)
    r = session.get(url)
    return r.json()["data"]


def get_order_events(order_id):
    """Fetch event data from an Order from an ID

    Parameters
    ----------
    order_id : str
        Order ID to fetch metadata for

    Returns
    -------
    list
        Status events for the given Order as it completes different steps in the ordering process
    """

    url = ORDERING_ORDER_EVENTS.replace(":id", order_id)

    return paginated_request("GET", url, "events")


def cancel_order(order_id):
    """Cancel an order from an ID, if supported

    Parameters
    ----------
    order_id : str
        Order ID to cancel

    Returns
    -------

    Note
    ----

    Not all pipelines support cancellation. Orders may not be cancellable after they have reached
    certain points in processing. See the pipeline's documentation for more information.
    """

    url = ORDERING_ORDER_CANCEL.replace(":id", order_id)
    r = session.post(url)


def submit_order(pipeline, order):
    """Send a request to the Order API

    Parameters
    ----------
    pipeline : str
        Pipeline name, in the form `namespace/name`. Ex: "imagery/analysis-ready"
    order: dict
        Order object, see pipeline docs or snippets for examples.

    Returns
    -------
    dict
        API response data for the Order"""
    order_url = ORDERING_PIPELINE_ORDER.replace(":namespace/:name", pipeline)
    r = session.post(order_url, json=order)
    return r.json()["data"]


def validate_order(pipeline, order):
    """Validate a request to the Order API

    Parameters
    ----------
    pipeline : str
        Pipeline name, in the form `namespace/name`. Ex: "imagery/analysis-ready"
    order: dict
        Order object, see pipeline docs or snippets for examples.

    Returns
    -------
    dict
        API response data for the Order if it were placed"""
    order_url = ORDERING_PIPELINE_VALIDATE.replace(":namespace/:name", pipeline)
    r = session.post(order_url, json=order)
    return r.json()["data"]


def estimate_order_usage(pipeline, order):
    """Estimate the order cost

    Parameters
    ----------
    pipeline : str
        Pipeline name, in the form `namespace/name`. Ex: "imagery/analysis-ready"
    order: dict
        Order object, see pipeline docs or snippets for examples.

    Returns
    -------
    dict
        Usage estimates for the given Order"""
    order_url = ORDERING_PIPELINE_ESTIMATE.replace(":namespace/:name", pipeline)
    r = session.post(order_url, json=order)
    return r.json()["data"]
