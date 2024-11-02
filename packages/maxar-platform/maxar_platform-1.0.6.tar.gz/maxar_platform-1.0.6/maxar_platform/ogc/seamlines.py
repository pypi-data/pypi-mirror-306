""" WFS access to mosaic seamlines

Provides
--------
OGC access to mosaic seamlines - as well as metadata search through WFS.

Each feature represents an individual strip as it cut to fill the mosaic product

Importing `web_feature_service` returns a configured OWSLib instance ready for use.

Similarly, `wfs_cql_client` is also a configured instance configured for searching
without having to look up TypeNames and other layer specific settings.

See the `ogc` parent module for more information about the classes returned here.

Notes
-----

The source layer uses EPSG:4326 so beware that coordinate order should be lat,lon.


References
----------
https://developers.maxar.com/docs/streaming-basemap/guides/wfs

"""

from posixpath import join

from maxar_platform import BASE_URL
from maxar_platform.ogc import WebFeatureService as ows_wfs
from maxar_platform.ogc import WebMapService as ows_wms
from maxar_platform.ogc import WfsSearchClient

__all__ = ["WebMapService", "WebFeatureService", "wfs_cql_client"]


STREAMING_URL = join(BASE_URL, "basemaps/v1/seamlines/wms")


def WebFeatureService(version="1.1.0"):
    return ows_wfs(STREAMING_URL, version=version)


def WebMapService(version="1.3.0"):
    return ows_wms(STREAMING_URL, version=version)


wfs_cql_client = WfsSearchClient(STREAMING_URL)
web_feature_service = WebFeatureService()
web_map_service = WebMapService()
