"""
Provides
--------
OGC access to MGP images, footprints, and seamlines. For searching imagery, a streamlined
client that works similar to `pystac-client` is included as an alternative to using WFS
GetFeature calls.

References
----------
https://developers.maxar.com/docs/streaming-imagery/
https://developers.maxar.com/docs/streaming-basemap/

"""

from owslib import util
from owslib.etree import ParseError, etree

from maxar_platform.session import session

__all__ = [
    "WebMapService",
    "WebFeatureService",
    "WebCoverageService",
    "WfsSearchClient",
    "FeatureSearch",
    "flip_axis_order",
]


def flip_axis_order(bbox):
    """Flips a bbox from x,y to y,x and vice versa

    Parameters
    ----------
    bbox: list or tuple
        A bounding box

    Returns
    -------
    list
        A flipped bounding box
    """
    return [bbox[1], bbox[0], bbox[3], bbox[2], *bbox[4:]]


def open_MGP_URL(url_base, data=None, method="Get", *args, **kwargs):
    """An MGP URL opener using maxar_platform.session

    Used to patch OWSLib's opener.

    See owslib.util.OpenURL
    """

    rkwargs = {}
    headers = {}
    method = method.split("}")[-1]

    if method.lower() == "post":
        try:
            etree.fromstring(data)
            headers["Content-Type"] = "text/xml"
        except (ParseError, UnicodeEncodeError):
            pass

        rkwargs["data"] = data

    elif method.lower() == "get":
        rkwargs["params"] = data

    else:
        raise ValueError("Unknown method ('%s'), expected 'get' or 'post'" % method)

    req = session.request(method.upper(), url_base, headers=headers, **rkwargs)

    if req.status_code in [400, 401]:
        raise util.ServiceException(req.text)

    if req.status_code in [404, 500, 502, 503, 504]:  # add more if needed
        req.raise_for_status()

    # check for service exceptions without the http header set
    if "Content-Type" in req.headers and req.headers["Content-Type"] in [
        "text/xml",
        "application/xml",
        "application/vnd.ogc.se_xml",
    ]:
        # just in case 400 headers were not set, going to have to read the xml to see if it's an exception report.
        se_tree = etree.fromstring(req.content)

        # to handle the variety of namespaces and terms across services
        # and versions, especially for "legacy" responses like WMS 1.3.0
        possible_errors = [
            "{http://www.opengis.net/ows}Exception",
            "{http://www.opengis.net/ows/1.1}Exception",
            "{http://www.opengis.net/ogc}ServiceException",
            "ServiceException",
        ]

        for possible_error in possible_errors:
            serviceException = se_tree.find(possible_error)
            if serviceException is not None:
                # and we need to deal with some message nesting
                raise util.ServiceException(
                    "\n".join([t.strip() for t in serviceException.itertext() if t.strip()])
                )

    return util.ResponseWrapper(req)


util.openURL = open_MGP_URL

from owslib.wcs import WebCoverageService
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService


class WfsSearchClient:
    """A search client for WFS

    This provides a similar interface to `pystac_client` as used by the SDK for Discovery
    """

    def __init__(self, base_url, default_typename=None):
        self.base_url = base_url
        self.default_typename = default_typename

    def typename_to_id(self, typename):
        typename = typename.lower()
        if typename.endswith("finishedfeature"):
            return "legacyIdentifier"
        if "seamline" in typename:
            return "catid"
        else:
            raise NotImplementedError(
                f"The layer {typename} does not contain features tied to catalog IDs"
            )

    def search(
        self,
        query,
        typename=None,
        bbox=None,
        bbox_xy=None,
        limit=200,
        max_items=None,
        **parameters,
    ):
        """Initialize a search

        Parameters
        ----------
        query: str
            CQL query
        typename: str
            Typename to search. This should already be defined on the class but can be changed if needed.
        bbox: list or tuple
            Bounding box. Since the WFS layers are in EPSG:4326, the bounding box must follow the defined coordinate
            order of longitude, latitude.
        bbox_xy: list or tuple
            Bounding box in latitude, longitude order for convenience
        max_items:
            Maximum number of results to fetch

        Keywords
        --------
        Additional keywords are passed through to the WFS GetFeature call as parameters

        Notes
        -----
        While this functions similarly to `pystac-client`, the results are in GeoJSON. `pystac-client` returns
        STAC Items either as PySTAC objects or serialized as dictionaries.

        Returns
        -------
        FeatureSearch
            The class that executes searches
        """

        typename = self.default_typename or typename

        if typename is None:
            raise ValueError(
                "No typename was provided and this search client does not have a default typename to use instead"
            )

        parameter_keys = [key.lower() for key in parameters.keys()]
        if "startindex" in parameter_keys:
            raise NotImplementedError(
                'This search client does not support fetching arbitrary ranges with "startIndex"'
            )

        params = {
            "service": "WFS",
            "request": "GetFeature",
            "typeName": typename,
            "outputFormat": "json",
        }

        if bbox_xy is not None:
            if type(bbox) is str:
                coords = bbox_xy.split(",")
                bbox_xy = [float(c) for c in coords[:4]].extend(coords[4:])
            bbox = flip_axis_order(bbox_xy)

        if bbox is not None:
            if type(bbox) is not str:
                coords = [str(c) for c in bbox]
                bbox = ",".join(coords)
            if query:
                query = query + f"AND (bbox(featureGeometry,{bbox}))"
            else:
                params["bbox"] = bbox

        if query:
            params["cql_filter"] = query
        params.update(parameters)

        return FeatureSearch(self.base_url, params, limit, max_items)

    def find(self, cat_id, typename=None):
        """Find a feature by Catalog ID

        The field name that stores the Catalog ID can vary so this function is
        configured to use the correct field name.

        Parameters
        ----------
        cat_id: str
            Catalog ID of the image
        typename: str
            Typename to search, this will be already defined by the class but can be changed

        """

        typename = self.default_typename or typename
        id_field = self.typename_to_id(typename)
        result = self.search(f"{id_field}='{cat_id}'", typename)
        return list(result.features())


class FeatureSearch:
    """Executes the search and can return results in several formats

    Parameters
    ----------
    base_url: str
        WFS base URL
    params: dict
        WFS search parameters
    page_size: int, optional
        Number of records to fetch when paginating, defaults to 200
    max_items: int
        Total number of records to fetch
    """

    def __init__(self, base_url, params, limit=200, max_items=None):
        self.base_url = base_url
        self.params = params
        self.page_size = limit
        self.max_items = max_items

    def features(self):
        """Generator returning individual GeoJSON Features

        Yields
        ------
        Feature"""

        for page in self.pages():
            for feature in page["features"]:
                yield feature

    def pages(self):
        """Generator returning paginated fetches as GeoJSON FeatureCollections

        Yields
        ------
        FeatureCollection
        """
        for page in self._fetch_pages():
            yield page

    def feature_collection(self):
        """Return search results as single FeatureCollection

        Yields
        ------
        FeatureCollection"""

        return {"type": "FeatureCollection", "features": list(self.features)}

    def _fetch_pages(self):
        """Generator of pages of features as GeoJSON

        Yields
        ------
        FeatureCollection
        """
        current_page = 1
        total_pages = self.max_items // self.page_size if self.max_items else None
        remainder = self.max_items % self.page_size if self.max_items else None
        done = False
        while not done:
            is_last_page = total_pages == current_page
            self.params.update(
                {
                    "startindex": (current_page - 1) * self.page_size,
                    "count": self.page_size,
                }
            )
            r = session.get(self.base_url, params=self.params)
            fc = r.json()
            if not is_last_page:
                yield fc
            else:
                yield {
                    "type": "FeatureCollection",
                    "features": fc["features"][:remainder],
                }
            current_page += 1
            has_more = len(fc["features"]) == self.page_size
            empty_last_page = remainder == 0 and current_page + 1 == total_pages
            done = is_last_page or empty_last_page or not has_more
