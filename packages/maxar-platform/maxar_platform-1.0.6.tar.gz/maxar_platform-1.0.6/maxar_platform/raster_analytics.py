"""
Provides
--------

Pre-configured access to Raster Analytics via Rasterio.

Note
----

Raster Analytics, while technically an API, is better understood as a virtual Cloud Optimized GeoTIFF
service that renders the tiles inside a virtual COG as they are requested by a client. Think of it as
instead of ordering a large image, you can instead order small bites of the image "a la carte". In essence,
every tile read operation is its own miniature order.

However, because every small tile is made to order, how you interact with the tiles becomes important.

This module provides a Rasterio DatasetReader that is configured with the correct settings to interact
with Raster Analytics. When you open or read from a virtual COG, the correct GDAL settings are temporarily
applied to receive the API response and then are reset. This means that the specific settings for reading
data from Raster Analytics will inadvertently apply to other GDAL operations you may be using, such as writing
an output image from the data.

Note: to return a window of X by Y pixels requires fetching enough tiles to cover the window. You are billed
based on tiles fetched, and for small windows this can result in data usages that are larger than the window
size requested in the function.

The COG_ENV constant contains the correct GDAL settings for Rasterio should you need to apply them to other
reader implementations. To build correctly formatted and escaped URLs, the `build_url` function may also be
useful when combined with other clients that can read GeoTIFFs.

Reference
---------
https://developers.maxar.com/docs/analytics/raster/guides/raster-analytics-overview
"""

import json
import os
from urllib.parse import quote

from maxar_platform import BASE_URL
from maxar_platform.exceptions import MissingDependency
from maxar_platform.session import NoSessionCredentials

try:
    import rasterio

    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False

__all__ = ["COG_ENV", "build_url", "open_image"]

# TODO make the URLs more configurable for things like dev"
API_BASE = BASE_URL + "analytics/v1/raster"


# TODO consider also having GDAL envvars (same but quoted booleans)
# check types between gdal and rasterio and shell
# check if gdal has its own env override
COG_ENV = {
    "GDAL_HTTP_MERGE_CONSECUTIVE_RANGES": False,
    "VSI_CACHE": True,
    "GDAL_HTTP_MULTIPLEX": True,
    "VRT_SHARED_SOURCE": 0,
    "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
    "GDAL_CACHEMAX": 512,  # size in MB
    "GDAL_NUM_THREADS": 16,
    "GDAL_HTTP_TIMEOUT": 600,
    "GTIFF_VIRTUAL_MEM_IO": "IF_ENOUGH_RAM",
    "VSI_CACHE_SIZE": 536870913,
    #'GDAL_INGESTED_BYTES_AT_OPEN': 1200000,
    "GDAL_BAND_BLOCK_CACHE": "HASHSET",
}
""" GDAL envvars optimized for reading virtual geotiffs.

    Note: these use Python formatting for Rasterio.Env, for example True instead of 'true' """


def set_credentials():
    """Sets the credentials for GDAL"""

    key = os.environ.get("MAXAR_API_KEY")

    if key:
        COG_ENV["GDAL_HTTP_HEADERS"] = f"Maxar-Api-Token:{key}"
    else:
        from maxar_platform.session import session

        try:
            token = session.oauth_session.token["access_token"]
            COG_ENV["GDAL_HTTP_HEADERS"] = f"Authorization: Bearer {token}"
        except KeyError:
            pass

    if "GDAL_HTTP_HEADERS" not in COG_ENV:
        raise NoSessionCredentials("No credentials found for authenticating with the API")


def build_url(script, function, collect_identifier, crs=None, **params):
    """Build a Raster Analytics URL

    Parameters
    ----------
    script : str
        Script name
    function: str
        Function name
    collect_identifier : str
        Catalog ID
    crs : str
        Coordinate reference system code. Ex: 'EPSG:4326'

    Keywords
    --------
    Additional keywords are passed as function parameters to the API

    Returns
    -------
    str
        Formatted and escaped URL for the image

    """

    params["collect_identifier"] = collect_identifier

    if crs:
        params["crs"] = crs

    param_list = []

    for k, v in params.items():
        v = json.dumps(v)
        v = f"{quote(v)}"
        param_list.append(f"&p={k}={v}")

    param_string = "".join(param_list)

    path = f"{API_BASE}/{script}/geotiff?function={function}{param_string}"
    return path


def open_image(pipeline, collect_identifier, crs=None, params={}, **kwargs):
    """Configure and return a Rasterio DatasetReader

    Parameters
    ----------
    pipeline : str
        Script and function name formatted like pipelines with a slash. Ex: 'ortho/pansharp_ortho'
    collect_identifier : str
        Catalog ID
    crs : str
        Coordinate reference system code. Ex: 'EPSG:4326'

    Keywords
    --------
    Additional keywords are passed as function parameters to the API

    Returns
    -------
    rasterio.DatasetReader

    """
    if not HAS_RASTERIO:
        raise MissingDependency("open_image() requires Rasterio")

    set_credentials()

    script, function = pipeline.split("/")
    path = "/vsicurl/" + build_url(script, function, collect_identifier, crs, **params)

    def ccg_wrapper(self, *args, **kwargs):
        with rasterio.Env(**COG_ENV) as env:
            return self.method_read(*args, **kwargs)

    with rasterio.Env(**COG_ENV) as env:
        dsr = rasterio.open(path, **kwargs)
        dsr.method_read = dsr.read
        dsr.read = ccg_wrapper.__get__(dsr)
        return dsr
