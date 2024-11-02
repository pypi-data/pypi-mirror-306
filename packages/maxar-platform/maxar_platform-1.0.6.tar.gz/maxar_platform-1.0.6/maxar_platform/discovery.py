""" Discovery API

Discovery is Maxar's data catalog. Since it implements STAC API, this SDK uses `pystac_client` for access.

For search, open a catalog or subcatalog to get a STAC client.


    from maxar_platform.discovery import open_catalog
    open_catalog() # returns the root catalog, or pass a subcatalog name like "imagery"
    results = stac_api_client.search(...)


Reference
---------
https://developers.maxar.com/docs/discovery/

https://pystac-client.readthedocs.io/en/latest/usage.html#itemsearch

"""

import json
import logging
import sys
from copy import deepcopy
from posixpath import join

from pystac_client import Client
from pystac_client.exceptions import APIError
from pystac_client.stac_api_io import StacApiIO

from maxar_platform import BASE_URL
from maxar_platform.session import session

# PyGeoFilter uses Lark 0.12 which will throw deprecation warnings in Py 3.11 or newer
# See https://github.com/geopython/pygeofilter/issues/98
# Once Discovery allows cql2-text in POSTs we can remove PyGeoFilter

from pygeofilter.backends.cql2_json import to_cql2  # isort:skip
from pygeofilter.parsers.cql2_text import parse as cql2_parse  # isort:skip

logger = logging.getLogger(__name__)

from typing import Any, Dict, Optional

DISCOVERY_URL = join(BASE_URL, "discovery/v1/")
DISCOVERY_CATALOG = join(DISCOVERY_URL, "catalogs/:subCatalogId")

__all__ = ["stac_api_client", "open_catalog"]


class MaxarStacApiIO(StacApiIO):

    area_based_calc = False

    def request(
        self,
        href: str,
        method: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Makes a request to an http endpoint

        Args:
            href (str): The request URL
            method (Optional[str], optional): The http method to use, 'GET' or 'POST'.
              Defaults to None, which will result in 'GET' being used.
            headers (Optional[Dict[str, str]], optional): Additional headers to include
                in request. Defaults to None.
            parameters (Optional[Dict[str, Any]], optional): parameters to send with
                request. Defaults to None.

        Raises:
            APIError: raised if the server returns an error response

        Return:
            str: The decoded response from the endpoint

        Note:
            This follows the default StacApiIO call but uses the SDK's session object. It also converts
            cql2 text queries to json since the Discovery API currently doesn't accept text queries in
            POST queries.
        """
        if method == "POST":
            if parameters.get("filter-lang") == "cql2-text":
                ast = cql2_parse(parameters["filter"])
                parameters["filter"] = json.loads(to_cql2(ast))
                parameters["filter-lang"] = "cql2-json"
            if self.area_based_calc and parameters:
                if "bbox" in parameters or "intersects" in parameters:
                    parameters.update({"area-based-calc": True})
            resp = session.post(url=href, headers=headers, json=parameters)
        else:
            params = deepcopy(parameters) or {}
            if self.area_based_calc and parameters:
                if "bbox" in parameters or "intersects" in parameters:
                    params.update({"area-based-calc": 1})
            resp = session.get(url=href, headers=headers, params=params)
        try:
            return resp.content.decode("utf-8")
        except Exception as err:
            raise APIError(str(err))


def open_catalog(catalog=None):
    """Open a pystac_client connection to a Discovery catalog

    Parameters
    ----------
    catalog : str, default None
        Catalog or subcatalog name to open, i.e. "imagery". If omitted the root catalog is used.

    Returns
    -------
    pystac_client.Client
        A Client object, configured to use Maxar authentication and area-based calculations

    Reference
    ---------
    https://pystac-client.readthedocs.io/en/latest/api.html#collection-client"""

    if not catalog:
        url = DISCOVERY_URL
    else:
        url = DISCOVERY_CATALOG.replace(":subCatalogId", catalog)

    client = Client.open(url, stac_io=MaxarStacApiIO())

    def abc_getter(self):
        return self._stac_io.area_based_calc

    def abc_setter(self, val):
        if type(val) is not bool:
            raise ValueError("Value must be a boolean")
        self._stac_io.area_based_calc = val

    setattr(
        client.__class__,
        "area_based_calc",
        property(abc_getter, abc_setter, doc="Return metadata with area-based calculations"),
    )

    return client


stac_api_client = open_catalog()
""" A pre-configured `pystac-client` instance ready to search the root catalog.


    Attributes
    ----------
    area_based_calc : Bool
        Toggles area-based calculations, default is False

    Reference
    ---------
    https://pystac-client.readthedocs.io/en/latest/api.html#collection-client """


# This is handy for certain searches
CATID_TO_COLLECTION = {
    "1010": "qb01",
    "1020": "wv01",
    "1030": "wv02",
    "1040": "wv03-vnir",
    "104A": "wv03-swir",
    "1050": "ge01",
    "1060": "ik02",
}
