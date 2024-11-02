""" WFS access to 'footprints'

Provides
--------
OGC access to image footprints as well as metadata search through WFS.

See the `ogc` parent module for more information about the classes returned here.

Notes
-----
Footprints covers both the bounds of individual strips and mosaic products.

They are served from the TypeName 'Maxar:FinishedFeature' which is not obvious.

For seamlines within a mosaic, use `maxar_platform.ogc.seamlines`

The source layer uses EPSG:4326 so beware that coordinate order should be lat,lon.

References
----------
https://developers.maxar.com/docs/streaming-imagery/guides/wfs

"""

from posixpath import join

from maxar_platform import BASE_URL
from maxar_platform.ogc import WebFeatureService as ows_wfs
from maxar_platform.ogc import WfsSearchClient

__all__ = ["WebFeatureService", "web_feature_service", "wfs_cql_client"]

STREAMING_URL = join(BASE_URL, "streaming/v1/ogc/wms")


def WebFeatureService(version="1.1.0"):
    """Factory function to get an OWSLib WFS object

    Parameters
    ----------
    version : str
        WMS version, default is 1.1.0

    Returns
    -------
    maxar_platform.ogc.WebFeatureService"""

    return ows_wfs(STREAMING_URL, version=version)


wfs_cql_client = WfsSearchClient(STREAMING_URL, "Maxar:FinishedFeature")
""" A configured instance of WfsSearchClient """

web_feature_service = WebFeatureService()
""" A configured instance of OWSLib's WFS object, using WFS 1.10 """
