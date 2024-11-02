"""
Type annotations for geo-places service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_places/type_defs/)

Usage::

    ```python
    from mypy_boto3_geo_places.type_defs import AccessPointTypeDef

    data: AccessPointTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Sequence

from .literals import (
    AutocompleteFilterPlaceTypeType,
    GeocodeAdditionalFeatureType,
    GeocodeFilterPlaceTypeType,
    GeocodeIntendedUseType,
    GetPlaceAdditionalFeatureType,
    GetPlaceIntendedUseType,
    PlaceTypeType,
    PostalCodeModeType,
    PostalCodeTypeType,
    QueryTypeType,
    RecordTypeCodeType,
    ReverseGeocodeAdditionalFeatureType,
    ReverseGeocodeFilterPlaceTypeType,
    ReverseGeocodeIntendedUseType,
    SearchNearbyAdditionalFeatureType,
    SearchNearbyIntendedUseType,
    SearchTextAdditionalFeatureType,
    SearchTextIntendedUseType,
    SuggestAdditionalFeatureType,
    SuggestResultItemTypeType,
    TypePlacementType,
    ZipClassificationCodeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessPointTypeDef",
    "CategoryTypeDef",
    "AddressComponentMatchScoresTypeDef",
    "PhonemeTranscriptionTypeDef",
    "CountryTypeDef",
    "RegionTypeDef",
    "StreetComponentsTypeDef",
    "SubRegionTypeDef",
    "HighlightTypeDef",
    "FilterCircleTypeDef",
    "ResponseMetadataTypeDef",
    "BusinessChainTypeDef",
    "FoodTypeTypeDef",
    "GeocodeFilterTypeDef",
    "GeocodeQueryComponentsTypeDef",
    "TimeZoneTypeDef",
    "GetPlaceRequestRequestTypeDef",
    "OpeningHoursComponentsTypeDef",
    "UspsZipPlus4TypeDef",
    "UspsZipTypeDef",
    "QueryRefinementTypeDef",
    "ReverseGeocodeFilterTypeDef",
    "SearchNearbyFilterTypeDef",
    "SuggestQueryResultTypeDef",
    "AccessRestrictionTypeDef",
    "ContactDetailsTypeDef",
    "ComponentMatchScoresTypeDef",
    "AddressComponentPhonemesTypeDef",
    "AddressTypeDef",
    "CountryHighlightsTypeDef",
    "RegionHighlightsTypeDef",
    "SubRegionHighlightsTypeDef",
    "SuggestAddressHighlightsTypeDef",
    "AutocompleteFilterTypeDef",
    "SearchTextFilterTypeDef",
    "SuggestFilterTypeDef",
    "GeocodeRequestRequestTypeDef",
    "OpeningHoursTypeDef",
    "PostalCodeDetailsTypeDef",
    "ReverseGeocodeRequestRequestTypeDef",
    "SearchNearbyRequestRequestTypeDef",
    "ContactsTypeDef",
    "MatchScoreDetailsTypeDef",
    "PhonemeDetailsTypeDef",
    "AutocompleteAddressHighlightsTypeDef",
    "SuggestHighlightsTypeDef",
    "AutocompleteRequestRequestTypeDef",
    "SearchTextRequestRequestTypeDef",
    "SuggestRequestRequestTypeDef",
    "ReverseGeocodeResultItemTypeDef",
    "GeocodeResultItemTypeDef",
    "GetPlaceResponseTypeDef",
    "SearchNearbyResultItemTypeDef",
    "SearchTextResultItemTypeDef",
    "SuggestPlaceResultTypeDef",
    "AutocompleteHighlightsTypeDef",
    "ReverseGeocodeResponseTypeDef",
    "GeocodeResponseTypeDef",
    "SearchNearbyResponseTypeDef",
    "SearchTextResponseTypeDef",
    "SuggestResultItemTypeDef",
    "AutocompleteResultItemTypeDef",
    "SuggestResponseTypeDef",
    "AutocompleteResponseTypeDef",
)

AccessPointTypeDef = TypedDict(
    "AccessPointTypeDef",
    {
        "Position": NotRequired[List[float]],
    },
)
CategoryTypeDef = TypedDict(
    "CategoryTypeDef",
    {
        "Id": str,
        "Name": str,
        "LocalizedName": NotRequired[str],
        "Primary": NotRequired[bool],
    },
)
AddressComponentMatchScoresTypeDef = TypedDict(
    "AddressComponentMatchScoresTypeDef",
    {
        "Country": NotRequired[float],
        "Region": NotRequired[float],
        "SubRegion": NotRequired[float],
        "Locality": NotRequired[float],
        "District": NotRequired[float],
        "SubDistrict": NotRequired[float],
        "PostalCode": NotRequired[float],
        "Block": NotRequired[float],
        "SubBlock": NotRequired[float],
        "Intersection": NotRequired[List[float]],
        "AddressNumber": NotRequired[float],
        "Building": NotRequired[float],
    },
)
PhonemeTranscriptionTypeDef = TypedDict(
    "PhonemeTranscriptionTypeDef",
    {
        "Value": NotRequired[str],
        "Language": NotRequired[str],
        "Preferred": NotRequired[bool],
    },
)
CountryTypeDef = TypedDict(
    "CountryTypeDef",
    {
        "Code2": NotRequired[str],
        "Code3": NotRequired[str],
        "Name": NotRequired[str],
    },
)
RegionTypeDef = TypedDict(
    "RegionTypeDef",
    {
        "Code": NotRequired[str],
        "Name": NotRequired[str],
    },
)
StreetComponentsTypeDef = TypedDict(
    "StreetComponentsTypeDef",
    {
        "BaseName": NotRequired[str],
        "Type": NotRequired[str],
        "TypePlacement": NotRequired[TypePlacementType],
        "TypeSeparator": NotRequired[str],
        "Prefix": NotRequired[str],
        "Suffix": NotRequired[str],
        "Direction": NotRequired[str],
        "Language": NotRequired[str],
    },
)
SubRegionTypeDef = TypedDict(
    "SubRegionTypeDef",
    {
        "Code": NotRequired[str],
        "Name": NotRequired[str],
    },
)
HighlightTypeDef = TypedDict(
    "HighlightTypeDef",
    {
        "StartIndex": NotRequired[int],
        "EndIndex": NotRequired[int],
        "Value": NotRequired[str],
    },
)
FilterCircleTypeDef = TypedDict(
    "FilterCircleTypeDef",
    {
        "Center": Sequence[float],
        "Radius": int,
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
BusinessChainTypeDef = TypedDict(
    "BusinessChainTypeDef",
    {
        "Name": NotRequired[str],
        "Id": NotRequired[str],
    },
)
FoodTypeTypeDef = TypedDict(
    "FoodTypeTypeDef",
    {
        "LocalizedName": str,
        "Id": NotRequired[str],
        "Primary": NotRequired[bool],
    },
)
GeocodeFilterTypeDef = TypedDict(
    "GeocodeFilterTypeDef",
    {
        "IncludeCountries": NotRequired[Sequence[str]],
        "IncludePlaceTypes": NotRequired[Sequence[GeocodeFilterPlaceTypeType]],
    },
)
GeocodeQueryComponentsTypeDef = TypedDict(
    "GeocodeQueryComponentsTypeDef",
    {
        "Country": NotRequired[str],
        "Region": NotRequired[str],
        "SubRegion": NotRequired[str],
        "Locality": NotRequired[str],
        "District": NotRequired[str],
        "Street": NotRequired[str],
        "AddressNumber": NotRequired[str],
        "PostalCode": NotRequired[str],
    },
)
TimeZoneTypeDef = TypedDict(
    "TimeZoneTypeDef",
    {
        "Name": str,
        "Offset": NotRequired[str],
        "OffsetSeconds": NotRequired[int],
    },
)
GetPlaceRequestRequestTypeDef = TypedDict(
    "GetPlaceRequestRequestTypeDef",
    {
        "PlaceId": str,
        "AdditionalFeatures": NotRequired[Sequence[GetPlaceAdditionalFeatureType]],
        "Language": NotRequired[str],
        "PoliticalView": NotRequired[str],
        "IntendedUse": NotRequired[GetPlaceIntendedUseType],
        "Key": NotRequired[str],
    },
)
OpeningHoursComponentsTypeDef = TypedDict(
    "OpeningHoursComponentsTypeDef",
    {
        "OpenTime": NotRequired[str],
        "OpenDuration": NotRequired[str],
        "Recurrence": NotRequired[str],
    },
)
UspsZipPlus4TypeDef = TypedDict(
    "UspsZipPlus4TypeDef",
    {
        "RecordTypeCode": NotRequired[RecordTypeCodeType],
    },
)
UspsZipTypeDef = TypedDict(
    "UspsZipTypeDef",
    {
        "ZipClassificationCode": NotRequired[ZipClassificationCodeType],
    },
)
QueryRefinementTypeDef = TypedDict(
    "QueryRefinementTypeDef",
    {
        "RefinedTerm": str,
        "OriginalTerm": str,
        "StartIndex": int,
        "EndIndex": int,
    },
)
ReverseGeocodeFilterTypeDef = TypedDict(
    "ReverseGeocodeFilterTypeDef",
    {
        "IncludePlaceTypes": NotRequired[Sequence[ReverseGeocodeFilterPlaceTypeType]],
    },
)
SearchNearbyFilterTypeDef = TypedDict(
    "SearchNearbyFilterTypeDef",
    {
        "BoundingBox": NotRequired[Sequence[float]],
        "IncludeCountries": NotRequired[Sequence[str]],
        "IncludeCategories": NotRequired[Sequence[str]],
        "ExcludeCategories": NotRequired[Sequence[str]],
        "IncludeBusinessChains": NotRequired[Sequence[str]],
        "ExcludeBusinessChains": NotRequired[Sequence[str]],
        "IncludeFoodTypes": NotRequired[Sequence[str]],
        "ExcludeFoodTypes": NotRequired[Sequence[str]],
    },
)
SuggestQueryResultTypeDef = TypedDict(
    "SuggestQueryResultTypeDef",
    {
        "QueryId": NotRequired[str],
        "QueryType": NotRequired[QueryTypeType],
    },
)
AccessRestrictionTypeDef = TypedDict(
    "AccessRestrictionTypeDef",
    {
        "Restricted": NotRequired[bool],
        "Categories": NotRequired[List[CategoryTypeDef]],
    },
)
ContactDetailsTypeDef = TypedDict(
    "ContactDetailsTypeDef",
    {
        "Label": NotRequired[str],
        "Value": NotRequired[str],
        "Categories": NotRequired[List[CategoryTypeDef]],
    },
)
ComponentMatchScoresTypeDef = TypedDict(
    "ComponentMatchScoresTypeDef",
    {
        "Title": NotRequired[float],
        "Address": NotRequired[AddressComponentMatchScoresTypeDef],
    },
)
AddressComponentPhonemesTypeDef = TypedDict(
    "AddressComponentPhonemesTypeDef",
    {
        "Country": NotRequired[List[PhonemeTranscriptionTypeDef]],
        "Region": NotRequired[List[PhonemeTranscriptionTypeDef]],
        "SubRegion": NotRequired[List[PhonemeTranscriptionTypeDef]],
        "Locality": NotRequired[List[PhonemeTranscriptionTypeDef]],
        "District": NotRequired[List[PhonemeTranscriptionTypeDef]],
        "SubDistrict": NotRequired[List[PhonemeTranscriptionTypeDef]],
        "Block": NotRequired[List[PhonemeTranscriptionTypeDef]],
        "SubBlock": NotRequired[List[PhonemeTranscriptionTypeDef]],
        "Street": NotRequired[List[PhonemeTranscriptionTypeDef]],
    },
)
AddressTypeDef = TypedDict(
    "AddressTypeDef",
    {
        "Label": NotRequired[str],
        "Country": NotRequired[CountryTypeDef],
        "Region": NotRequired[RegionTypeDef],
        "SubRegion": NotRequired[SubRegionTypeDef],
        "Locality": NotRequired[str],
        "District": NotRequired[str],
        "SubDistrict": NotRequired[str],
        "PostalCode": NotRequired[str],
        "Block": NotRequired[str],
        "SubBlock": NotRequired[str],
        "Intersection": NotRequired[List[str]],
        "Street": NotRequired[str],
        "StreetComponents": NotRequired[List[StreetComponentsTypeDef]],
        "AddressNumber": NotRequired[str],
        "Building": NotRequired[str],
    },
)
CountryHighlightsTypeDef = TypedDict(
    "CountryHighlightsTypeDef",
    {
        "Code": NotRequired[List[HighlightTypeDef]],
        "Name": NotRequired[List[HighlightTypeDef]],
    },
)
RegionHighlightsTypeDef = TypedDict(
    "RegionHighlightsTypeDef",
    {
        "Code": NotRequired[List[HighlightTypeDef]],
        "Name": NotRequired[List[HighlightTypeDef]],
    },
)
SubRegionHighlightsTypeDef = TypedDict(
    "SubRegionHighlightsTypeDef",
    {
        "Code": NotRequired[List[HighlightTypeDef]],
        "Name": NotRequired[List[HighlightTypeDef]],
    },
)
SuggestAddressHighlightsTypeDef = TypedDict(
    "SuggestAddressHighlightsTypeDef",
    {
        "Label": NotRequired[List[HighlightTypeDef]],
    },
)
AutocompleteFilterTypeDef = TypedDict(
    "AutocompleteFilterTypeDef",
    {
        "BoundingBox": NotRequired[Sequence[float]],
        "Circle": NotRequired[FilterCircleTypeDef],
        "IncludeCountries": NotRequired[Sequence[str]],
        "IncludePlaceTypes": NotRequired[Sequence[AutocompleteFilterPlaceTypeType]],
    },
)
SearchTextFilterTypeDef = TypedDict(
    "SearchTextFilterTypeDef",
    {
        "BoundingBox": NotRequired[Sequence[float]],
        "Circle": NotRequired[FilterCircleTypeDef],
        "IncludeCountries": NotRequired[Sequence[str]],
    },
)
SuggestFilterTypeDef = TypedDict(
    "SuggestFilterTypeDef",
    {
        "BoundingBox": NotRequired[Sequence[float]],
        "Circle": NotRequired[FilterCircleTypeDef],
        "IncludeCountries": NotRequired[Sequence[str]],
    },
)
GeocodeRequestRequestTypeDef = TypedDict(
    "GeocodeRequestRequestTypeDef",
    {
        "QueryText": NotRequired[str],
        "QueryComponents": NotRequired[GeocodeQueryComponentsTypeDef],
        "MaxResults": NotRequired[int],
        "BiasPosition": NotRequired[Sequence[float]],
        "Filter": NotRequired[GeocodeFilterTypeDef],
        "AdditionalFeatures": NotRequired[Sequence[GeocodeAdditionalFeatureType]],
        "Language": NotRequired[str],
        "PoliticalView": NotRequired[str],
        "IntendedUse": NotRequired[GeocodeIntendedUseType],
        "Key": NotRequired[str],
    },
)
OpeningHoursTypeDef = TypedDict(
    "OpeningHoursTypeDef",
    {
        "Display": NotRequired[List[str]],
        "OpenNow": NotRequired[bool],
        "Components": NotRequired[List[OpeningHoursComponentsTypeDef]],
        "Categories": NotRequired[List[CategoryTypeDef]],
    },
)
PostalCodeDetailsTypeDef = TypedDict(
    "PostalCodeDetailsTypeDef",
    {
        "PostalCode": NotRequired[str],
        "PostalAuthority": NotRequired[Literal["Usps"]],
        "PostalCodeType": NotRequired[PostalCodeTypeType],
        "UspsZip": NotRequired[UspsZipTypeDef],
        "UspsZipPlus4": NotRequired[UspsZipPlus4TypeDef],
    },
)
ReverseGeocodeRequestRequestTypeDef = TypedDict(
    "ReverseGeocodeRequestRequestTypeDef",
    {
        "QueryPosition": Sequence[float],
        "QueryRadius": NotRequired[int],
        "MaxResults": NotRequired[int],
        "Filter": NotRequired[ReverseGeocodeFilterTypeDef],
        "AdditionalFeatures": NotRequired[Sequence[ReverseGeocodeAdditionalFeatureType]],
        "Language": NotRequired[str],
        "PoliticalView": NotRequired[str],
        "IntendedUse": NotRequired[ReverseGeocodeIntendedUseType],
        "Key": NotRequired[str],
    },
)
SearchNearbyRequestRequestTypeDef = TypedDict(
    "SearchNearbyRequestRequestTypeDef",
    {
        "QueryPosition": Sequence[float],
        "QueryRadius": NotRequired[int],
        "MaxResults": NotRequired[int],
        "Filter": NotRequired[SearchNearbyFilterTypeDef],
        "AdditionalFeatures": NotRequired[Sequence[SearchNearbyAdditionalFeatureType]],
        "Language": NotRequired[str],
        "PoliticalView": NotRequired[str],
        "IntendedUse": NotRequired[SearchNearbyIntendedUseType],
        "NextToken": NotRequired[str],
        "Key": NotRequired[str],
    },
)
ContactsTypeDef = TypedDict(
    "ContactsTypeDef",
    {
        "Phones": NotRequired[List[ContactDetailsTypeDef]],
        "Faxes": NotRequired[List[ContactDetailsTypeDef]],
        "Websites": NotRequired[List[ContactDetailsTypeDef]],
        "Emails": NotRequired[List[ContactDetailsTypeDef]],
    },
)
MatchScoreDetailsTypeDef = TypedDict(
    "MatchScoreDetailsTypeDef",
    {
        "Overall": NotRequired[float],
        "Components": NotRequired[ComponentMatchScoresTypeDef],
    },
)
PhonemeDetailsTypeDef = TypedDict(
    "PhonemeDetailsTypeDef",
    {
        "Title": NotRequired[List[PhonemeTranscriptionTypeDef]],
        "Address": NotRequired[AddressComponentPhonemesTypeDef],
    },
)
AutocompleteAddressHighlightsTypeDef = TypedDict(
    "AutocompleteAddressHighlightsTypeDef",
    {
        "Label": NotRequired[List[HighlightTypeDef]],
        "Country": NotRequired[CountryHighlightsTypeDef],
        "Region": NotRequired[RegionHighlightsTypeDef],
        "SubRegion": NotRequired[SubRegionHighlightsTypeDef],
        "Locality": NotRequired[List[HighlightTypeDef]],
        "District": NotRequired[List[HighlightTypeDef]],
        "SubDistrict": NotRequired[List[HighlightTypeDef]],
        "Street": NotRequired[List[HighlightTypeDef]],
        "Block": NotRequired[List[HighlightTypeDef]],
        "SubBlock": NotRequired[List[HighlightTypeDef]],
        "Intersection": NotRequired[List[List[HighlightTypeDef]]],
        "PostalCode": NotRequired[List[HighlightTypeDef]],
        "AddressNumber": NotRequired[List[HighlightTypeDef]],
        "Building": NotRequired[List[HighlightTypeDef]],
    },
)
SuggestHighlightsTypeDef = TypedDict(
    "SuggestHighlightsTypeDef",
    {
        "Title": NotRequired[List[HighlightTypeDef]],
        "Address": NotRequired[SuggestAddressHighlightsTypeDef],
    },
)
AutocompleteRequestRequestTypeDef = TypedDict(
    "AutocompleteRequestRequestTypeDef",
    {
        "QueryText": str,
        "MaxResults": NotRequired[int],
        "BiasPosition": NotRequired[Sequence[float]],
        "Filter": NotRequired[AutocompleteFilterTypeDef],
        "PostalCodeMode": NotRequired[PostalCodeModeType],
        "AdditionalFeatures": NotRequired[Sequence[Literal["Core"]]],
        "Language": NotRequired[str],
        "PoliticalView": NotRequired[str],
        "IntendedUse": NotRequired[Literal["SingleUse"]],
        "Key": NotRequired[str],
    },
)
SearchTextRequestRequestTypeDef = TypedDict(
    "SearchTextRequestRequestTypeDef",
    {
        "QueryText": NotRequired[str],
        "QueryId": NotRequired[str],
        "MaxResults": NotRequired[int],
        "BiasPosition": NotRequired[Sequence[float]],
        "Filter": NotRequired[SearchTextFilterTypeDef],
        "AdditionalFeatures": NotRequired[Sequence[SearchTextAdditionalFeatureType]],
        "Language": NotRequired[str],
        "PoliticalView": NotRequired[str],
        "IntendedUse": NotRequired[SearchTextIntendedUseType],
        "NextToken": NotRequired[str],
        "Key": NotRequired[str],
    },
)
SuggestRequestRequestTypeDef = TypedDict(
    "SuggestRequestRequestTypeDef",
    {
        "QueryText": str,
        "MaxResults": NotRequired[int],
        "MaxQueryRefinements": NotRequired[int],
        "BiasPosition": NotRequired[Sequence[float]],
        "Filter": NotRequired[SuggestFilterTypeDef],
        "AdditionalFeatures": NotRequired[Sequence[SuggestAdditionalFeatureType]],
        "Language": NotRequired[str],
        "PoliticalView": NotRequired[str],
        "IntendedUse": NotRequired[Literal["SingleUse"]],
        "Key": NotRequired[str],
    },
)
ReverseGeocodeResultItemTypeDef = TypedDict(
    "ReverseGeocodeResultItemTypeDef",
    {
        "PlaceId": str,
        "PlaceType": PlaceTypeType,
        "Title": str,
        "Address": NotRequired[AddressTypeDef],
        "AddressNumberCorrected": NotRequired[bool],
        "PostalCodeDetails": NotRequired[List[PostalCodeDetailsTypeDef]],
        "Position": NotRequired[List[float]],
        "Distance": NotRequired[int],
        "MapView": NotRequired[List[float]],
        "Categories": NotRequired[List[CategoryTypeDef]],
        "FoodTypes": NotRequired[List[FoodTypeTypeDef]],
        "AccessPoints": NotRequired[List[AccessPointTypeDef]],
        "TimeZone": NotRequired[TimeZoneTypeDef],
        "PoliticalView": NotRequired[str],
    },
)
GeocodeResultItemTypeDef = TypedDict(
    "GeocodeResultItemTypeDef",
    {
        "PlaceId": str,
        "PlaceType": PlaceTypeType,
        "Title": str,
        "Address": NotRequired[AddressTypeDef],
        "AddressNumberCorrected": NotRequired[bool],
        "PostalCodeDetails": NotRequired[List[PostalCodeDetailsTypeDef]],
        "Position": NotRequired[List[float]],
        "Distance": NotRequired[int],
        "MapView": NotRequired[List[float]],
        "Categories": NotRequired[List[CategoryTypeDef]],
        "FoodTypes": NotRequired[List[FoodTypeTypeDef]],
        "AccessPoints": NotRequired[List[AccessPointTypeDef]],
        "TimeZone": NotRequired[TimeZoneTypeDef],
        "PoliticalView": NotRequired[str],
        "MatchScores": NotRequired[MatchScoreDetailsTypeDef],
    },
)
GetPlaceResponseTypeDef = TypedDict(
    "GetPlaceResponseTypeDef",
    {
        "PlaceId": str,
        "PlaceType": PlaceTypeType,
        "Title": str,
        "PricingBucket": str,
        "Address": AddressTypeDef,
        "AddressNumberCorrected": bool,
        "PostalCodeDetails": List[PostalCodeDetailsTypeDef],
        "Position": List[float],
        "MapView": List[float],
        "Categories": List[CategoryTypeDef],
        "FoodTypes": List[FoodTypeTypeDef],
        "BusinessChains": List[BusinessChainTypeDef],
        "Contacts": ContactsTypeDef,
        "OpeningHours": List[OpeningHoursTypeDef],
        "AccessPoints": List[AccessPointTypeDef],
        "AccessRestrictions": List[AccessRestrictionTypeDef],
        "TimeZone": TimeZoneTypeDef,
        "PoliticalView": str,
        "Phonemes": PhonemeDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SearchNearbyResultItemTypeDef = TypedDict(
    "SearchNearbyResultItemTypeDef",
    {
        "PlaceId": str,
        "PlaceType": PlaceTypeType,
        "Title": str,
        "Address": NotRequired[AddressTypeDef],
        "AddressNumberCorrected": NotRequired[bool],
        "Position": NotRequired[List[float]],
        "Distance": NotRequired[int],
        "MapView": NotRequired[List[float]],
        "Categories": NotRequired[List[CategoryTypeDef]],
        "FoodTypes": NotRequired[List[FoodTypeTypeDef]],
        "BusinessChains": NotRequired[List[BusinessChainTypeDef]],
        "Contacts": NotRequired[ContactsTypeDef],
        "OpeningHours": NotRequired[List[OpeningHoursTypeDef]],
        "AccessPoints": NotRequired[List[AccessPointTypeDef]],
        "AccessRestrictions": NotRequired[List[AccessRestrictionTypeDef]],
        "TimeZone": NotRequired[TimeZoneTypeDef],
        "PoliticalView": NotRequired[str],
        "Phonemes": NotRequired[PhonemeDetailsTypeDef],
    },
)
SearchTextResultItemTypeDef = TypedDict(
    "SearchTextResultItemTypeDef",
    {
        "PlaceId": str,
        "PlaceType": PlaceTypeType,
        "Title": str,
        "Address": NotRequired[AddressTypeDef],
        "AddressNumberCorrected": NotRequired[bool],
        "Position": NotRequired[List[float]],
        "Distance": NotRequired[int],
        "MapView": NotRequired[List[float]],
        "Categories": NotRequired[List[CategoryTypeDef]],
        "FoodTypes": NotRequired[List[FoodTypeTypeDef]],
        "BusinessChains": NotRequired[List[BusinessChainTypeDef]],
        "Contacts": NotRequired[ContactsTypeDef],
        "OpeningHours": NotRequired[List[OpeningHoursTypeDef]],
        "AccessPoints": NotRequired[List[AccessPointTypeDef]],
        "AccessRestrictions": NotRequired[List[AccessRestrictionTypeDef]],
        "TimeZone": NotRequired[TimeZoneTypeDef],
        "PoliticalView": NotRequired[str],
        "Phonemes": NotRequired[PhonemeDetailsTypeDef],
    },
)
SuggestPlaceResultTypeDef = TypedDict(
    "SuggestPlaceResultTypeDef",
    {
        "PlaceId": NotRequired[str],
        "PlaceType": NotRequired[PlaceTypeType],
        "Address": NotRequired[AddressTypeDef],
        "Position": NotRequired[List[float]],
        "Distance": NotRequired[int],
        "MapView": NotRequired[List[float]],
        "Categories": NotRequired[List[CategoryTypeDef]],
        "FoodTypes": NotRequired[List[FoodTypeTypeDef]],
        "BusinessChains": NotRequired[List[BusinessChainTypeDef]],
        "AccessPoints": NotRequired[List[AccessPointTypeDef]],
        "AccessRestrictions": NotRequired[List[AccessRestrictionTypeDef]],
        "TimeZone": NotRequired[TimeZoneTypeDef],
        "PoliticalView": NotRequired[str],
        "Phonemes": NotRequired[PhonemeDetailsTypeDef],
    },
)
AutocompleteHighlightsTypeDef = TypedDict(
    "AutocompleteHighlightsTypeDef",
    {
        "Title": NotRequired[List[HighlightTypeDef]],
        "Address": NotRequired[AutocompleteAddressHighlightsTypeDef],
    },
)
ReverseGeocodeResponseTypeDef = TypedDict(
    "ReverseGeocodeResponseTypeDef",
    {
        "PricingBucket": str,
        "ResultItems": List[ReverseGeocodeResultItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GeocodeResponseTypeDef = TypedDict(
    "GeocodeResponseTypeDef",
    {
        "PricingBucket": str,
        "ResultItems": List[GeocodeResultItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SearchNearbyResponseTypeDef = TypedDict(
    "SearchNearbyResponseTypeDef",
    {
        "PricingBucket": str,
        "ResultItems": List[SearchNearbyResultItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SearchTextResponseTypeDef = TypedDict(
    "SearchTextResponseTypeDef",
    {
        "PricingBucket": str,
        "ResultItems": List[SearchTextResultItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SuggestResultItemTypeDef = TypedDict(
    "SuggestResultItemTypeDef",
    {
        "Title": str,
        "SuggestResultItemType": SuggestResultItemTypeType,
        "Place": NotRequired[SuggestPlaceResultTypeDef],
        "Query": NotRequired[SuggestQueryResultTypeDef],
        "Highlights": NotRequired[SuggestHighlightsTypeDef],
    },
)
AutocompleteResultItemTypeDef = TypedDict(
    "AutocompleteResultItemTypeDef",
    {
        "PlaceId": str,
        "PlaceType": PlaceTypeType,
        "Title": str,
        "Address": NotRequired[AddressTypeDef],
        "Distance": NotRequired[int],
        "Language": NotRequired[str],
        "PoliticalView": NotRequired[str],
        "Highlights": NotRequired[AutocompleteHighlightsTypeDef],
    },
)
SuggestResponseTypeDef = TypedDict(
    "SuggestResponseTypeDef",
    {
        "PricingBucket": str,
        "ResultItems": List[SuggestResultItemTypeDef],
        "QueryRefinements": List[QueryRefinementTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AutocompleteResponseTypeDef = TypedDict(
    "AutocompleteResponseTypeDef",
    {
        "PricingBucket": str,
        "ResultItems": List[AutocompleteResultItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
