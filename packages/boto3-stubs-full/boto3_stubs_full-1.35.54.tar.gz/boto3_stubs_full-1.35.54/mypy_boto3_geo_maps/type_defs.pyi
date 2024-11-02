"""
Type annotations for geo-maps service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_maps/type_defs/)

Usage::

    ```python
    from mypy_boto3_geo_maps.type_defs import GetGlyphsRequestRequestTypeDef

    data: GetGlyphsRequestRequestTypeDef = ...
    ```
"""

import sys
from typing import Dict

from botocore.response import StreamingBody

from .literals import ColorSchemeType, MapStyleType, ScaleBarUnitType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "GetGlyphsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GetSpritesRequestRequestTypeDef",
    "GetStaticMapRequestRequestTypeDef",
    "GetStyleDescriptorRequestRequestTypeDef",
    "GetTileRequestRequestTypeDef",
    "GetGlyphsResponseTypeDef",
    "GetSpritesResponseTypeDef",
    "GetStaticMapResponseTypeDef",
    "GetStyleDescriptorResponseTypeDef",
    "GetTileResponseTypeDef",
)

GetGlyphsRequestRequestTypeDef = TypedDict(
    "GetGlyphsRequestRequestTypeDef",
    {
        "FontStack": str,
        "FontUnicodeRange": str,
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
GetSpritesRequestRequestTypeDef = TypedDict(
    "GetSpritesRequestRequestTypeDef",
    {
        "FileName": str,
        "Style": MapStyleType,
        "ColorScheme": ColorSchemeType,
        "Variant": Literal["Default"],
    },
)
GetStaticMapRequestRequestTypeDef = TypedDict(
    "GetStaticMapRequestRequestTypeDef",
    {
        "Height": int,
        "FileName": str,
        "Width": int,
        "BoundingBox": NotRequired[str],
        "BoundedPositions": NotRequired[str],
        "Center": NotRequired[str],
        "CompactOverlay": NotRequired[str],
        "GeoJsonOverlay": NotRequired[str],
        "Key": NotRequired[str],
        "Padding": NotRequired[int],
        "Radius": NotRequired[int],
        "ScaleBarUnit": NotRequired[ScaleBarUnitType],
        "Style": NotRequired[Literal["Satellite"]],
        "Zoom": NotRequired[float],
    },
)
GetStyleDescriptorRequestRequestTypeDef = TypedDict(
    "GetStyleDescriptorRequestRequestTypeDef",
    {
        "Style": MapStyleType,
        "ColorScheme": NotRequired[ColorSchemeType],
        "PoliticalView": NotRequired[str],
        "Key": NotRequired[str],
    },
)
GetTileRequestRequestTypeDef = TypedDict(
    "GetTileRequestRequestTypeDef",
    {
        "Tileset": str,
        "Z": str,
        "X": str,
        "Y": str,
        "Key": NotRequired[str],
    },
)
GetGlyphsResponseTypeDef = TypedDict(
    "GetGlyphsResponseTypeDef",
    {
        "Blob": StreamingBody,
        "ContentType": str,
        "CacheControl": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSpritesResponseTypeDef = TypedDict(
    "GetSpritesResponseTypeDef",
    {
        "Blob": StreamingBody,
        "ContentType": str,
        "CacheControl": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStaticMapResponseTypeDef = TypedDict(
    "GetStaticMapResponseTypeDef",
    {
        "Blob": StreamingBody,
        "ContentType": str,
        "CacheControl": str,
        "ETag": str,
        "PricingBucket": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStyleDescriptorResponseTypeDef = TypedDict(
    "GetStyleDescriptorResponseTypeDef",
    {
        "Blob": StreamingBody,
        "ContentType": str,
        "CacheControl": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTileResponseTypeDef = TypedDict(
    "GetTileResponseTypeDef",
    {
        "Blob": StreamingBody,
        "ContentType": str,
        "CacheControl": str,
        "ETag": str,
        "PricingBucket": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
