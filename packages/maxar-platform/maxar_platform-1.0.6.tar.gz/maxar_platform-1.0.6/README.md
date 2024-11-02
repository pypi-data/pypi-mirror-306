# maxar-platform

A Python SDK for working with [Maxar Geospatial Platform](https://pro.maxar.com/)

Version: 1.0.6

## Introduction

`maxar-platform` provides wrappers around the MGP APIs with a focus on simplicity and productivity. It wraps popular and proven Python geospatial packages whenever possible, but also offers a core HTTP session object to use as a basis for more custom functionality.

### APIs supported:

#### Discovery

Discovery is Maxar's catalog API. `maxar_platform` extends `pystac-client` to provide STAC search to the user.

#### Streaming APIs (OGC)

[`owslib`](https://owslib.readthedocs.io/en/latest/) methods are available for OGC access to imagery and image footprint OGC endpoints. In addition, `maxar-platform` provides a search client with a similar interface to the Discovery module that queries the images available from these endpoints

#### Ordering, Monitoring, and Tasking APIs

These endpoints can be accessed through matching modules and functions.

#### Raster Analytics

Open any image available in Raster Analytics with `rasterio` as if the image was a Cloud Optimized Geotiff. Pixel data is generated on-the-fly.

#### Authentication

An underlying `session` object handles authentication and communication with the APIs. Also included is a module for managing API Keys.

## Installation

`pip install maxar-platform`

To use the Raster Analytics module, you will also need to install [`rasterio`](https://rasterio.readthedocs.io/en/stable/).

## Documentation

See the [MGP Developer Site](https://developers.maxar.com/docs/developer-tools/python-sdk)
