""" OGC access to imagery

Provides
--------
OGC access to imagery - as well as metadata search.

Importing `web_feature_service` returns a configured OWSLib instance ready for use.

Similarly, `wfs_cql_client` is also a configured instance configured for searching
without having to look up TypeNames and other layer specific settings.

See the `ogc` parent module for more information about the classes returned here.

Notes
-----

This image layer contains ALL the imagery available - to access an individual image in WMS,
use a CQL filter like "legacyId=1040010096284D00". The imagery layer can evaluate filters on
the image metadata in the same manner as WFS queries on the image footprints.

The source layer uses EPSG:4326 so beware that coordinate order should be lat,lon.


References
----------
https://developers.maxar.com/docs/streaming-imagery/guides/wms

"""

from posixpath import join

from maxar_platform import BASE_URL
from maxar_platform.ogc import WebCoverageService as ows_wcs
from maxar_platform.ogc import WebFeatureService as ows_wfs
from maxar_platform.ogc import WebMapService as ows_wms
from maxar_platform.ogc import WfsSearchClient

__all__ = ["WebMapService", "WebFeatureService", "WebCoverageService", "wfs_cql_client"]


STREAMING_URL = join(BASE_URL, "streaming/v1/ogc/wms")


def WebMapService(version="1.1.1"):
    return ows_wms(STREAMING_URL, version=version)


def WebFeatureService(version="1.1.0"):
    return ows_wfs(STREAMING_URL, version=version)


def WebCoverageService(version="2.0.1"):
    return ows_wcs(STREAMING_URL, version=version)


wfs_cql_client = WfsSearchClient(STREAMING_URL, "Maxar:FinishedFeature")

web_map_service = WebMapService()
web_feature_service = WebFeatureService()
web_coverage_service = WebCoverageService()
