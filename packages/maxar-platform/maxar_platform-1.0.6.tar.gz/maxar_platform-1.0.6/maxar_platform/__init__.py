"""
Provides
--------

Streamlined access to these Maxar Geospatial Platform APIs:

- Authentication
- Discovery Catalog
- OGC Image streaming, vectors, and metadata
- Ordering
- Monitoring
- Tasking
- Raster Analytics

Coming soon:

- 3D Analytics
- Change Monitoring

Reference
---------

https://developers.maxar.com/
"""

__version__ = "1.0.6"

import os

BASE_URL = os.environ.get("MGP_BASE_URL") or "https://api.maxar.com/"
CLIENT_ID = os.environ.get("MAXAR_CLIENT_ID") or "mgp"
PACKAGE = "maxar_platform"
