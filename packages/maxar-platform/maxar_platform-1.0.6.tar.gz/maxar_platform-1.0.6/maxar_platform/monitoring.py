"""
Provides
--------

Functions to maintain Monitors:

- create and update a monitor
- enable/disable a monitor
- get one or list many monitors
- see events that the monitor has matched

Reference
---------
https://developers.maxar.com/docs/monitoring/
"""

from posixpath import join
from typing import List, Union

from maxar_platform import BASE_URL
from maxar_platform.session import paginated_request, session

__all__ = (
    "create_monitor",
    "get_monitor",
    "disable_monitor",
    "enable_monitor",
    "update_monitor",
    "list_monitors",
    "list_monitor_events",
)

MONITORING_BASE = BASE_URL + "monitoring/v1/monitors"
MONITORING_MONITOR = join(MONITORING_BASE, ":id")
MONITORING_EVENTS = join(MONITORING_MONITOR, "events")
MONITORING_ENABLE = join(MONITORING_MONITOR, "enable")
MONITORING_DISABLE = join(MONITORING_MONITOR, "disable")


def list_monitors(
    limit=100,
    sort="desc",
    filter=None,
):
    """Fetch user's monitors

    Parameters
    ----------
    limit: int or None, default None
        Maximum number of orders to fetch, None means unlimited, default is 100.
    sort: str
        Sort order for order IDs, either 'asc' (ascending) or 'desc' (descending). Default is 'desc'.
    filter: str or iterable of strings
        Filter results using `field:value` syntax.
        Matches are case sensitive and will match if the value is found anywhere in the field: filtering on a value of `description:NV` will return `Las Vegas, NV` along with `DENVER CO` descriptions.
        Multiple filters can be passed but keys must be unique since filters will be logically ANDed.
        Example: 'description:denver' or ['name:denver', 'description:parking']

    Returns
    -------
    list
        monitor objects matching parameters"""

    params = {}

    if filter is not None:
        params["filter"] = filter

    return paginated_request("GET", MONITORING_BASE, "monitors", sort, limit, **params)


def get_monitor(monitor_id):
    """Fetch raw data about a monitor from an ID

    Parameters
    ----------
    monitor_id : str
        Monitor ID to fetch metadata for

    Returns
    -------
    dict
        API data for the given monitor"""

    url = MONITORING_MONITOR.replace(":id", monitor_id)
    r = session.get(url)
    return r.json()["data"]


def create_monitor(monitor_payload):
    """Create a new monitor

    Parameters
    ----------
    monitor_payload : dict
        Dictionary of monitor settings

    Returns
    -------
    dict
        Data for the monitor"""

    r = session.post(MONITORING_BASE, json=monitor_payload)
    return r.json()["data"]


def update_monitor(monitor_id, monitor_payload):
    """Update an existing monitor with new settings

    Parameters
    ----------
    monitor_id : str
        Monitor ID to fetch metadata for
    monitor_payload : dict
        Dictionary of updated fields for the existing monitor

    Returns
    -------
    dict
        Data for the updated monitor"""

    url = MONITORING_MONITOR.replace(":id", monitor_id)
    r = session.patch(url, json=monitor_payload)
    return r.json()["data"]


def list_monitor_events(monitor_id):
    """Fetch the events for a monitor from an ID

    Parameters
    ----------
    monitor_id : str
        monitor ID to fetch events for

    Returns
    -------
    list
        Matched events for the given monitor"""

    url = MONITORING_EVENTS.replace(":id", monitor_id)
    return paginated_request("GET", url, "events", sort="desc")


def disable_monitor(monitor_id):
    """Disable a monitor

    Parameters
    ----------
    monitor_id : str
        monitor ID to disable

    Returns
    -------"""

    url = MONITORING_DISABLE.replace(":id", monitor_id)
    r = session.post(url)


def enable_monitor(monitor_id):
    """Enable a monitor

    Parameters
    ----------
    monitor_id : str
        monitor ID to enable

    Returns
    -------"""

    url = MONITORING_ENABLE.replace(":id", monitor_id)
    r = session.post(url)
