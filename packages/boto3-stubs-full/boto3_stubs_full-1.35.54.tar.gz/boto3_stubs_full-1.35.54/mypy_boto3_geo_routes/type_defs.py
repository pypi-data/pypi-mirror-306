"""
Type annotations for geo-routes service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_geo_routes/type_defs/)

Usage::

    ```python
    from mypy_boto3_geo_routes.type_defs import IsolineAllowOptionsTypeDef

    data: IsolineAllowOptionsTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Sequence, Union

from .literals import (
    DayOfWeekType,
    GeometryFormatType,
    IsolineEngineTypeType,
    IsolineHazardousCargoTypeType,
    IsolineOptimizationObjectiveType,
    IsolineTravelModeType,
    IsolineTruckTypeType,
    IsolineZoneCategoryType,
    MatchingStrategyType,
    MeasurementSystemType,
    RoadSnapHazardousCargoTypeType,
    RoadSnapNoticeCodeType,
    RoadSnapTravelModeType,
    RouteDirectionType,
    RouteEngineTypeType,
    RouteFerryNoticeCodeType,
    RouteFerryTravelStepTypeType,
    RouteHazardousCargoTypeType,
    RouteLegAdditionalFeatureType,
    RouteLegTravelModeType,
    RouteLegTypeType,
    RouteMatrixErrorCodeType,
    RouteMatrixHazardousCargoTypeType,
    RouteMatrixTravelModeType,
    RouteMatrixTruckTypeType,
    RouteMatrixZoneCategoryType,
    RouteNoticeImpactType,
    RoutePedestrianNoticeCodeType,
    RoutePedestrianTravelStepTypeType,
    RouteResponseNoticeCodeType,
    RouteRoadTypeType,
    RouteSideOfStreetType,
    RouteSpanAdditionalFeatureType,
    RouteSpanCarAccessAttributeType,
    RouteSpanGateAttributeType,
    RouteSpanPedestrianAccessAttributeType,
    RouteSpanRailwayCrossingAttributeType,
    RouteSpanRoadAttributeType,
    RouteSpanScooterAccessAttributeType,
    RouteSpanTruckAccessAttributeType,
    RouteSteeringDirectionType,
    RouteTollPassValidityPeriodTypeType,
    RouteTollPaymentMethodType,
    RouteTravelModeType,
    RouteTravelStepTypeType,
    RouteTruckTypeType,
    RouteTurnIntensityType,
    RouteVehicleIncidentSeverityType,
    RouteVehicleIncidentTypeType,
    RouteVehicleNoticeCodeType,
    RouteVehicleTravelStepTypeType,
    RouteWeightConstraintTypeType,
    RouteZoneCategoryType,
    RoutingObjectiveType,
    SideOfStreetMatchingStrategyType,
    TrafficUsageType,
    WaypointOptimizationConstraintType,
    WaypointOptimizationHazardousCargoTypeType,
    WaypointOptimizationSequencingObjectiveType,
    WaypointOptimizationServiceTimeTreatmentType,
    WaypointOptimizationTravelModeType,
    WaypointOptimizationTruckTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "IsolineAllowOptionsTypeDef",
    "IsolineGranularityOptionsTypeDef",
    "IsolineThresholdsTypeDef",
    "IsolineTrafficOptionsTypeDef",
    "ResponseMetadataTypeDef",
    "RouteMatrixAllowOptionsTypeDef",
    "RouteMatrixExclusionOptionsTypeDef",
    "RouteMatrixTrafficOptionsTypeDef",
    "RouteMatrixEntryTypeDef",
    "RouteAllowOptionsTypeDef",
    "RouteExclusionOptionsTypeDef",
    "RouteTrafficOptionsTypeDef",
    "RouteResponseNoticeTypeDef",
    "CircleOutputTypeDef",
    "CircleTypeDef",
    "CorridorTypeDef",
    "PolylineCorridorTypeDef",
    "IsolineAvoidanceZoneCategoryTypeDef",
    "IsolineVehicleLicensePlateTypeDef",
    "IsolineConnectionGeometryTypeDef",
    "IsolineMatchingOptionsTypeDef",
    "IsolineSideOfStreetOptionsTypeDef",
    "IsolineShapeGeometryTypeDef",
    "IsolineTrailerOptionsTypeDef",
    "WeightPerAxleGroupTypeDef",
    "LocalizedStringTypeDef",
    "WaypointOptimizationExclusionOptionsTypeDef",
    "WaypointOptimizationOriginOptionsTypeDef",
    "WaypointOptimizationTrafficOptionsTypeDef",
    "WaypointOptimizationConnectionTypeDef",
    "WaypointOptimizationOptimizedWaypointTypeDef",
    "WaypointOptimizationTimeBreakdownTypeDef",
    "RoadSnapNoticeTypeDef",
    "RoadSnapSnappedGeometryTypeDef",
    "RoadSnapSnappedTracePointTypeDef",
    "RoadSnapTracePointTypeDef",
    "RoadSnapTrailerOptionsTypeDef",
    "RouteAvoidanceZoneCategoryTypeDef",
    "RouteVehicleLicensePlateTypeDef",
    "RouteMatchingOptionsTypeDef",
    "RouteSideOfStreetOptionsTypeDef",
    "RouteDriverScheduleIntervalTypeDef",
    "RouteEmissionTypeTypeDef",
    "RouteFerryAfterTravelStepTypeDef",
    "RouteFerryPlaceTypeDef",
    "RouteFerryBeforeTravelStepTypeDef",
    "RouteFerryNoticeTypeDef",
    "RouteFerryTravelStepTypeDef",
    "RouteFerryOverviewSummaryTypeDef",
    "RouteFerryTravelOnlySummaryTypeDef",
    "RouteLegGeometryTypeDef",
    "RouteNumberTypeDef",
    "RouteMatrixAutoCircleTypeDef",
    "RouteMatrixAvoidanceAreaGeometryTypeDef",
    "RouteMatrixAvoidanceZoneCategoryTypeDef",
    "RouteMatrixVehicleLicensePlateTypeDef",
    "RouteMatrixMatchingOptionsTypeDef",
    "RouteMatrixSideOfStreetOptionsTypeDef",
    "RouteMatrixTrailerOptionsTypeDef",
    "RouteNoticeDetailRangeTypeDef",
    "RoutePassThroughPlaceTypeDef",
    "RoutePedestrianPlaceTypeDef",
    "RoutePedestrianNoticeTypeDef",
    "RoutePedestrianOptionsTypeDef",
    "RoutePedestrianOverviewSummaryTypeDef",
    "RouteSpanDynamicSpeedDetailsTypeDef",
    "RouteSpanSpeedLimitDetailsTypeDef",
    "RoutePedestrianTravelOnlySummaryTypeDef",
    "RouteTollPassValidityPeriodTypeDef",
    "RouteTollPaymentSiteTypeDef",
    "RouteTollPriceValueRangeTypeDef",
    "RouteTransponderTypeDef",
    "RouteTollSystemTypeDef",
    "RouteTrailerOptionsTypeDef",
    "RouteVehiclePlaceTypeDef",
    "RouteVehicleIncidentTypeDef",
    "RouteZoneTypeDef",
    "RouteVehicleOverviewSummaryTypeDef",
    "RouteVehicleTravelOnlySummaryTypeDef",
    "RouteWeightConstraintTypeDef",
    "WaypointOptimizationAccessHoursEntryTypeDef",
    "WaypointOptimizationAvoidanceAreaGeometryTypeDef",
    "WaypointOptimizationSideOfStreetOptionsTypeDef",
    "WaypointOptimizationRestProfileTypeDef",
    "WaypointOptimizationFailedConstraintTypeDef",
    "WaypointOptimizationPedestrianOptionsTypeDef",
    "WaypointOptimizationRestCycleDurationsTypeDef",
    "WaypointOptimizationTrailerOptionsTypeDef",
    "CircleUnionTypeDef",
    "IsolineAvoidanceAreaGeometryTypeDef",
    "RouteAvoidanceAreaGeometryTypeDef",
    "IsolineCarOptionsTypeDef",
    "IsolineScooterOptionsTypeDef",
    "IsolineConnectionTypeDef",
    "IsolineDestinationOptionsTypeDef",
    "IsolineOriginOptionsTypeDef",
    "IsolineTruckOptionsTypeDef",
    "RouteContinueHighwayStepDetailsTypeDef",
    "RouteContinueStepDetailsTypeDef",
    "RouteEnterHighwayStepDetailsTypeDef",
    "RouteExitStepDetailsTypeDef",
    "RouteFerrySpanTypeDef",
    "RouteKeepStepDetailsTypeDef",
    "RouteRampStepDetailsTypeDef",
    "RouteRoundaboutEnterStepDetailsTypeDef",
    "RouteRoundaboutExitStepDetailsTypeDef",
    "RouteRoundaboutPassStepDetailsTypeDef",
    "RouteTurnStepDetailsTypeDef",
    "RouteUTurnStepDetailsTypeDef",
    "SnapToRoadsResponseTypeDef",
    "RoadSnapTruckOptionsTypeDef",
    "RouteCarOptionsTypeDef",
    "RouteScooterOptionsTypeDef",
    "RouteDestinationOptionsTypeDef",
    "RouteOriginOptionsTypeDef",
    "RouteWaypointTypeDef",
    "RouteDriverOptionsTypeDef",
    "RouteTollOptionsTypeDef",
    "RouteFerryArrivalTypeDef",
    "RouteFerryDepartureTypeDef",
    "RouteFerrySummaryTypeDef",
    "RouteMajorRoadLabelTypeDef",
    "RouteRoadTypeDef",
    "RouteSignpostLabelTypeDef",
    "RouteMatrixBoundaryGeometryOutputTypeDef",
    "RouteMatrixAvoidanceAreaTypeDef",
    "RouteMatrixCarOptionsTypeDef",
    "RouteMatrixScooterOptionsTypeDef",
    "RouteMatrixDestinationOptionsTypeDef",
    "RouteMatrixOriginOptionsTypeDef",
    "RouteMatrixTruckOptionsTypeDef",
    "RoutePassThroughWaypointTypeDef",
    "RoutePedestrianArrivalTypeDef",
    "RoutePedestrianDepartureTypeDef",
    "RoutePedestrianSpanTypeDef",
    "RouteVehicleSpanTypeDef",
    "RoutePedestrianSummaryTypeDef",
    "RouteTollPassTypeDef",
    "RouteTollPriceSummaryTypeDef",
    "RouteTollPriceTypeDef",
    "RouteTruckOptionsTypeDef",
    "RouteVehicleArrivalTypeDef",
    "RouteVehicleDepartureTypeDef",
    "RouteVehicleSummaryTypeDef",
    "RouteViolatedConstraintsTypeDef",
    "WaypointOptimizationAccessHoursTypeDef",
    "WaypointOptimizationAvoidanceAreaTypeDef",
    "WaypointOptimizationImpedingWaypointTypeDef",
    "WaypointOptimizationRestCyclesTypeDef",
    "WaypointOptimizationTruckOptionsTypeDef",
    "RouteMatrixBoundaryGeometryTypeDef",
    "IsolineAvoidanceAreaTypeDef",
    "RouteAvoidanceAreaTypeDef",
    "IsolineTypeDef",
    "IsolineTravelModeOptionsTypeDef",
    "RoadSnapTravelModeOptionsTypeDef",
    "RouteSignpostTypeDef",
    "RouteMatrixBoundaryOutputTypeDef",
    "RouteMatrixAvoidanceOptionsTypeDef",
    "RouteMatrixDestinationTypeDef",
    "RouteMatrixOriginTypeDef",
    "RouteMatrixTravelModeOptionsTypeDef",
    "RouteFerryLegDetailsTypeDef",
    "RouteTollSummaryTypeDef",
    "RouteTollRateTypeDef",
    "RouteTravelModeOptionsTypeDef",
    "RouteVehicleNoticeDetailTypeDef",
    "WaypointOptimizationDestinationOptionsTypeDef",
    "WaypointOptimizationWaypointTypeDef",
    "WaypointOptimizationAvoidanceOptionsTypeDef",
    "OptimizeWaypointsResponseTypeDef",
    "WaypointOptimizationDriverOptionsTypeDef",
    "WaypointOptimizationTravelModeOptionsTypeDef",
    "RouteMatrixBoundaryGeometryUnionTypeDef",
    "IsolineAvoidanceOptionsTypeDef",
    "RouteAvoidanceOptionsTypeDef",
    "CalculateIsolinesResponseTypeDef",
    "SnapToRoadsRequestRequestTypeDef",
    "RoutePedestrianTravelStepTypeDef",
    "RouteVehicleTravelStepTypeDef",
    "CalculateRouteMatrixResponseTypeDef",
    "RouteSummaryTypeDef",
    "RouteTollTypeDef",
    "RouteVehicleNoticeTypeDef",
    "OptimizeWaypointsRequestRequestTypeDef",
    "RouteMatrixBoundaryTypeDef",
    "CalculateIsolinesRequestRequestTypeDef",
    "CalculateRoutesRequestRequestTypeDef",
    "RoutePedestrianLegDetailsTypeDef",
    "RouteVehicleLegDetailsTypeDef",
    "CalculateRouteMatrixRequestRequestTypeDef",
    "RouteLegTypeDef",
    "RouteTypeDef",
    "CalculateRoutesResponseTypeDef",
)

IsolineAllowOptionsTypeDef = TypedDict(
    "IsolineAllowOptionsTypeDef",
    {
        "Hot": NotRequired[bool],
        "Hov": NotRequired[bool],
    },
)
IsolineGranularityOptionsTypeDef = TypedDict(
    "IsolineGranularityOptionsTypeDef",
    {
        "MaxPoints": NotRequired[int],
        "MaxResolution": NotRequired[int],
    },
)
IsolineThresholdsTypeDef = TypedDict(
    "IsolineThresholdsTypeDef",
    {
        "Distance": NotRequired[Sequence[int]],
        "Time": NotRequired[Sequence[int]],
    },
)
IsolineTrafficOptionsTypeDef = TypedDict(
    "IsolineTrafficOptionsTypeDef",
    {
        "FlowEventThresholdOverride": NotRequired[int],
        "Usage": NotRequired[TrafficUsageType],
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
RouteMatrixAllowOptionsTypeDef = TypedDict(
    "RouteMatrixAllowOptionsTypeDef",
    {
        "Hot": NotRequired[bool],
        "Hov": NotRequired[bool],
    },
)
RouteMatrixExclusionOptionsTypeDef = TypedDict(
    "RouteMatrixExclusionOptionsTypeDef",
    {
        "Countries": Sequence[str],
    },
)
RouteMatrixTrafficOptionsTypeDef = TypedDict(
    "RouteMatrixTrafficOptionsTypeDef",
    {
        "FlowEventThresholdOverride": NotRequired[int],
        "Usage": NotRequired[TrafficUsageType],
    },
)
RouteMatrixEntryTypeDef = TypedDict(
    "RouteMatrixEntryTypeDef",
    {
        "Distance": int,
        "Duration": int,
        "Error": NotRequired[RouteMatrixErrorCodeType],
    },
)
RouteAllowOptionsTypeDef = TypedDict(
    "RouteAllowOptionsTypeDef",
    {
        "Hot": NotRequired[bool],
        "Hov": NotRequired[bool],
    },
)
RouteExclusionOptionsTypeDef = TypedDict(
    "RouteExclusionOptionsTypeDef",
    {
        "Countries": Sequence[str],
    },
)
RouteTrafficOptionsTypeDef = TypedDict(
    "RouteTrafficOptionsTypeDef",
    {
        "FlowEventThresholdOverride": NotRequired[int],
        "Usage": NotRequired[TrafficUsageType],
    },
)
RouteResponseNoticeTypeDef = TypedDict(
    "RouteResponseNoticeTypeDef",
    {
        "Code": RouteResponseNoticeCodeType,
        "Impact": NotRequired[RouteNoticeImpactType],
    },
)
CircleOutputTypeDef = TypedDict(
    "CircleOutputTypeDef",
    {
        "Center": List[float],
        "Radius": float,
    },
)
CircleTypeDef = TypedDict(
    "CircleTypeDef",
    {
        "Center": Sequence[float],
        "Radius": float,
    },
)
CorridorTypeDef = TypedDict(
    "CorridorTypeDef",
    {
        "LineString": Sequence[Sequence[float]],
        "Radius": int,
    },
)
PolylineCorridorTypeDef = TypedDict(
    "PolylineCorridorTypeDef",
    {
        "Polyline": str,
        "Radius": int,
    },
)
IsolineAvoidanceZoneCategoryTypeDef = TypedDict(
    "IsolineAvoidanceZoneCategoryTypeDef",
    {
        "Category": NotRequired[IsolineZoneCategoryType],
    },
)
IsolineVehicleLicensePlateTypeDef = TypedDict(
    "IsolineVehicleLicensePlateTypeDef",
    {
        "LastCharacter": NotRequired[str],
    },
)
IsolineConnectionGeometryTypeDef = TypedDict(
    "IsolineConnectionGeometryTypeDef",
    {
        "LineString": NotRequired[List[List[float]]],
        "Polyline": NotRequired[str],
    },
)
IsolineMatchingOptionsTypeDef = TypedDict(
    "IsolineMatchingOptionsTypeDef",
    {
        "NameHint": NotRequired[str],
        "OnRoadThreshold": NotRequired[int],
        "Radius": NotRequired[int],
        "Strategy": NotRequired[MatchingStrategyType],
    },
)
IsolineSideOfStreetOptionsTypeDef = TypedDict(
    "IsolineSideOfStreetOptionsTypeDef",
    {
        "Position": Sequence[float],
        "UseWith": NotRequired[SideOfStreetMatchingStrategyType],
    },
)
IsolineShapeGeometryTypeDef = TypedDict(
    "IsolineShapeGeometryTypeDef",
    {
        "Polygon": NotRequired[List[List[List[float]]]],
        "PolylinePolygon": NotRequired[List[str]],
    },
)
IsolineTrailerOptionsTypeDef = TypedDict(
    "IsolineTrailerOptionsTypeDef",
    {
        "AxleCount": NotRequired[int],
        "TrailerCount": NotRequired[int],
    },
)
WeightPerAxleGroupTypeDef = TypedDict(
    "WeightPerAxleGroupTypeDef",
    {
        "Single": NotRequired[int],
        "Tandem": NotRequired[int],
        "Triple": NotRequired[int],
        "Quad": NotRequired[int],
        "Quint": NotRequired[int],
    },
)
LocalizedStringTypeDef = TypedDict(
    "LocalizedStringTypeDef",
    {
        "Value": str,
        "Language": NotRequired[str],
    },
)
WaypointOptimizationExclusionOptionsTypeDef = TypedDict(
    "WaypointOptimizationExclusionOptionsTypeDef",
    {
        "Countries": Sequence[str],
    },
)
WaypointOptimizationOriginOptionsTypeDef = TypedDict(
    "WaypointOptimizationOriginOptionsTypeDef",
    {
        "Id": NotRequired[str],
    },
)
WaypointOptimizationTrafficOptionsTypeDef = TypedDict(
    "WaypointOptimizationTrafficOptionsTypeDef",
    {
        "Usage": NotRequired[TrafficUsageType],
    },
)
WaypointOptimizationConnectionTypeDef = TypedDict(
    "WaypointOptimizationConnectionTypeDef",
    {
        "Distance": int,
        "From": str,
        "RestDuration": int,
        "To": str,
        "TravelDuration": int,
        "WaitDuration": int,
    },
)
WaypointOptimizationOptimizedWaypointTypeDef = TypedDict(
    "WaypointOptimizationOptimizedWaypointTypeDef",
    {
        "DepartureTime": str,
        "Id": str,
        "Position": List[float],
        "ArrivalTime": NotRequired[str],
    },
)
WaypointOptimizationTimeBreakdownTypeDef = TypedDict(
    "WaypointOptimizationTimeBreakdownTypeDef",
    {
        "RestDuration": int,
        "ServiceDuration": int,
        "TravelDuration": int,
        "WaitDuration": int,
    },
)
RoadSnapNoticeTypeDef = TypedDict(
    "RoadSnapNoticeTypeDef",
    {
        "Code": RoadSnapNoticeCodeType,
        "Title": str,
        "TracePointIndexes": List[int],
    },
)
RoadSnapSnappedGeometryTypeDef = TypedDict(
    "RoadSnapSnappedGeometryTypeDef",
    {
        "LineString": NotRequired[List[List[float]]],
        "Polyline": NotRequired[str],
    },
)
RoadSnapSnappedTracePointTypeDef = TypedDict(
    "RoadSnapSnappedTracePointTypeDef",
    {
        "Confidence": float,
        "OriginalPosition": List[float],
        "SnappedPosition": List[float],
    },
)
RoadSnapTracePointTypeDef = TypedDict(
    "RoadSnapTracePointTypeDef",
    {
        "Position": Sequence[float],
        "Heading": NotRequired[float],
        "Speed": NotRequired[float],
        "Timestamp": NotRequired[str],
    },
)
RoadSnapTrailerOptionsTypeDef = TypedDict(
    "RoadSnapTrailerOptionsTypeDef",
    {
        "TrailerCount": NotRequired[int],
    },
)
RouteAvoidanceZoneCategoryTypeDef = TypedDict(
    "RouteAvoidanceZoneCategoryTypeDef",
    {
        "Category": RouteZoneCategoryType,
    },
)
RouteVehicleLicensePlateTypeDef = TypedDict(
    "RouteVehicleLicensePlateTypeDef",
    {
        "LastCharacter": NotRequired[str],
    },
)
RouteMatchingOptionsTypeDef = TypedDict(
    "RouteMatchingOptionsTypeDef",
    {
        "NameHint": NotRequired[str],
        "OnRoadThreshold": NotRequired[int],
        "Radius": NotRequired[int],
        "Strategy": NotRequired[MatchingStrategyType],
    },
)
RouteSideOfStreetOptionsTypeDef = TypedDict(
    "RouteSideOfStreetOptionsTypeDef",
    {
        "Position": Sequence[float],
        "UseWith": NotRequired[SideOfStreetMatchingStrategyType],
    },
)
RouteDriverScheduleIntervalTypeDef = TypedDict(
    "RouteDriverScheduleIntervalTypeDef",
    {
        "DriveDuration": int,
        "RestDuration": int,
    },
)
RouteEmissionTypeTypeDef = TypedDict(
    "RouteEmissionTypeTypeDef",
    {
        "Type": str,
        "Co2EmissionClass": NotRequired[str],
    },
)
RouteFerryAfterTravelStepTypeDef = TypedDict(
    "RouteFerryAfterTravelStepTypeDef",
    {
        "Duration": int,
        "Type": Literal["Deboard"],
        "Instruction": NotRequired[str],
    },
)
RouteFerryPlaceTypeDef = TypedDict(
    "RouteFerryPlaceTypeDef",
    {
        "Position": List[float],
        "Name": NotRequired[str],
        "OriginalPosition": NotRequired[List[float]],
        "WaypointIndex": NotRequired[int],
    },
)
RouteFerryBeforeTravelStepTypeDef = TypedDict(
    "RouteFerryBeforeTravelStepTypeDef",
    {
        "Duration": int,
        "Type": Literal["Board"],
        "Instruction": NotRequired[str],
    },
)
RouteFerryNoticeTypeDef = TypedDict(
    "RouteFerryNoticeTypeDef",
    {
        "Code": RouteFerryNoticeCodeType,
        "Impact": NotRequired[RouteNoticeImpactType],
    },
)
RouteFerryTravelStepTypeDef = TypedDict(
    "RouteFerryTravelStepTypeDef",
    {
        "Duration": int,
        "Type": RouteFerryTravelStepTypeType,
        "Distance": NotRequired[int],
        "GeometryOffset": NotRequired[int],
        "Instruction": NotRequired[str],
    },
)
RouteFerryOverviewSummaryTypeDef = TypedDict(
    "RouteFerryOverviewSummaryTypeDef",
    {
        "Distance": int,
        "Duration": int,
    },
)
RouteFerryTravelOnlySummaryTypeDef = TypedDict(
    "RouteFerryTravelOnlySummaryTypeDef",
    {
        "Duration": int,
    },
)
RouteLegGeometryTypeDef = TypedDict(
    "RouteLegGeometryTypeDef",
    {
        "LineString": NotRequired[List[List[float]]],
        "Polyline": NotRequired[str],
    },
)
RouteNumberTypeDef = TypedDict(
    "RouteNumberTypeDef",
    {
        "Value": str,
        "Direction": NotRequired[RouteDirectionType],
        "Language": NotRequired[str],
    },
)
RouteMatrixAutoCircleTypeDef = TypedDict(
    "RouteMatrixAutoCircleTypeDef",
    {
        "Margin": NotRequired[int],
        "MaxRadius": NotRequired[int],
    },
)
RouteMatrixAvoidanceAreaGeometryTypeDef = TypedDict(
    "RouteMatrixAvoidanceAreaGeometryTypeDef",
    {
        "BoundingBox": NotRequired[Sequence[float]],
        "Polygon": NotRequired[Sequence[Sequence[Sequence[float]]]],
        "PolylinePolygon": NotRequired[Sequence[str]],
    },
)
RouteMatrixAvoidanceZoneCategoryTypeDef = TypedDict(
    "RouteMatrixAvoidanceZoneCategoryTypeDef",
    {
        "Category": NotRequired[RouteMatrixZoneCategoryType],
    },
)
RouteMatrixVehicleLicensePlateTypeDef = TypedDict(
    "RouteMatrixVehicleLicensePlateTypeDef",
    {
        "LastCharacter": NotRequired[str],
    },
)
RouteMatrixMatchingOptionsTypeDef = TypedDict(
    "RouteMatrixMatchingOptionsTypeDef",
    {
        "NameHint": NotRequired[str],
        "OnRoadThreshold": NotRequired[int],
        "Radius": NotRequired[int],
        "Strategy": NotRequired[MatchingStrategyType],
    },
)
RouteMatrixSideOfStreetOptionsTypeDef = TypedDict(
    "RouteMatrixSideOfStreetOptionsTypeDef",
    {
        "Position": Sequence[float],
        "UseWith": NotRequired[SideOfStreetMatchingStrategyType],
    },
)
RouteMatrixTrailerOptionsTypeDef = TypedDict(
    "RouteMatrixTrailerOptionsTypeDef",
    {
        "TrailerCount": NotRequired[int],
    },
)
RouteNoticeDetailRangeTypeDef = TypedDict(
    "RouteNoticeDetailRangeTypeDef",
    {
        "Min": NotRequired[int],
        "Max": NotRequired[int],
    },
)
RoutePassThroughPlaceTypeDef = TypedDict(
    "RoutePassThroughPlaceTypeDef",
    {
        "Position": List[float],
        "OriginalPosition": NotRequired[List[float]],
        "WaypointIndex": NotRequired[int],
    },
)
RoutePedestrianPlaceTypeDef = TypedDict(
    "RoutePedestrianPlaceTypeDef",
    {
        "Position": List[float],
        "Name": NotRequired[str],
        "OriginalPosition": NotRequired[List[float]],
        "SideOfStreet": NotRequired[RouteSideOfStreetType],
        "WaypointIndex": NotRequired[int],
    },
)
RoutePedestrianNoticeTypeDef = TypedDict(
    "RoutePedestrianNoticeTypeDef",
    {
        "Code": RoutePedestrianNoticeCodeType,
        "Impact": NotRequired[RouteNoticeImpactType],
    },
)
RoutePedestrianOptionsTypeDef = TypedDict(
    "RoutePedestrianOptionsTypeDef",
    {
        "Speed": NotRequired[float],
    },
)
RoutePedestrianOverviewSummaryTypeDef = TypedDict(
    "RoutePedestrianOverviewSummaryTypeDef",
    {
        "Distance": int,
        "Duration": int,
    },
)
RouteSpanDynamicSpeedDetailsTypeDef = TypedDict(
    "RouteSpanDynamicSpeedDetailsTypeDef",
    {
        "BestCaseSpeed": NotRequired[float],
        "TurnDuration": NotRequired[int],
        "TypicalSpeed": NotRequired[float],
    },
)
RouteSpanSpeedLimitDetailsTypeDef = TypedDict(
    "RouteSpanSpeedLimitDetailsTypeDef",
    {
        "MaxSpeed": NotRequired[float],
        "Unlimited": NotRequired[bool],
    },
)
RoutePedestrianTravelOnlySummaryTypeDef = TypedDict(
    "RoutePedestrianTravelOnlySummaryTypeDef",
    {
        "Duration": int,
    },
)
RouteTollPassValidityPeriodTypeDef = TypedDict(
    "RouteTollPassValidityPeriodTypeDef",
    {
        "Period": RouteTollPassValidityPeriodTypeType,
        "PeriodCount": NotRequired[int],
    },
)
RouteTollPaymentSiteTypeDef = TypedDict(
    "RouteTollPaymentSiteTypeDef",
    {
        "Position": List[float],
        "Name": NotRequired[str],
    },
)
RouteTollPriceValueRangeTypeDef = TypedDict(
    "RouteTollPriceValueRangeTypeDef",
    {
        "Min": float,
        "Max": float,
    },
)
RouteTransponderTypeDef = TypedDict(
    "RouteTransponderTypeDef",
    {
        "SystemName": NotRequired[str],
    },
)
RouteTollSystemTypeDef = TypedDict(
    "RouteTollSystemTypeDef",
    {
        "Name": NotRequired[str],
    },
)
RouteTrailerOptionsTypeDef = TypedDict(
    "RouteTrailerOptionsTypeDef",
    {
        "AxleCount": NotRequired[int],
        "TrailerCount": NotRequired[int],
    },
)
RouteVehiclePlaceTypeDef = TypedDict(
    "RouteVehiclePlaceTypeDef",
    {
        "Position": List[float],
        "Name": NotRequired[str],
        "OriginalPosition": NotRequired[List[float]],
        "SideOfStreet": NotRequired[RouteSideOfStreetType],
        "WaypointIndex": NotRequired[int],
    },
)
RouteVehicleIncidentTypeDef = TypedDict(
    "RouteVehicleIncidentTypeDef",
    {
        "Description": NotRequired[str],
        "EndTime": NotRequired[str],
        "Severity": NotRequired[RouteVehicleIncidentSeverityType],
        "StartTime": NotRequired[str],
        "Type": NotRequired[RouteVehicleIncidentTypeType],
    },
)
RouteZoneTypeDef = TypedDict(
    "RouteZoneTypeDef",
    {
        "Category": NotRequired[RouteZoneCategoryType],
        "Name": NotRequired[str],
    },
)
RouteVehicleOverviewSummaryTypeDef = TypedDict(
    "RouteVehicleOverviewSummaryTypeDef",
    {
        "Distance": int,
        "Duration": int,
        "BestCaseDuration": NotRequired[int],
        "TypicalDuration": NotRequired[int],
    },
)
RouteVehicleTravelOnlySummaryTypeDef = TypedDict(
    "RouteVehicleTravelOnlySummaryTypeDef",
    {
        "Duration": int,
        "BestCaseDuration": NotRequired[int],
        "TypicalDuration": NotRequired[int],
    },
)
RouteWeightConstraintTypeDef = TypedDict(
    "RouteWeightConstraintTypeDef",
    {
        "Type": RouteWeightConstraintTypeType,
        "Value": int,
    },
)
WaypointOptimizationAccessHoursEntryTypeDef = TypedDict(
    "WaypointOptimizationAccessHoursEntryTypeDef",
    {
        "DayOfWeek": DayOfWeekType,
        "TimeOfDay": str,
    },
)
WaypointOptimizationAvoidanceAreaGeometryTypeDef = TypedDict(
    "WaypointOptimizationAvoidanceAreaGeometryTypeDef",
    {
        "BoundingBox": NotRequired[Sequence[float]],
    },
)
WaypointOptimizationSideOfStreetOptionsTypeDef = TypedDict(
    "WaypointOptimizationSideOfStreetOptionsTypeDef",
    {
        "Position": Sequence[float],
        "UseWith": NotRequired[SideOfStreetMatchingStrategyType],
    },
)
WaypointOptimizationRestProfileTypeDef = TypedDict(
    "WaypointOptimizationRestProfileTypeDef",
    {
        "Profile": str,
    },
)
WaypointOptimizationFailedConstraintTypeDef = TypedDict(
    "WaypointOptimizationFailedConstraintTypeDef",
    {
        "Constraint": NotRequired[WaypointOptimizationConstraintType],
        "Reason": NotRequired[str],
    },
)
WaypointOptimizationPedestrianOptionsTypeDef = TypedDict(
    "WaypointOptimizationPedestrianOptionsTypeDef",
    {
        "Speed": NotRequired[float],
    },
)
WaypointOptimizationRestCycleDurationsTypeDef = TypedDict(
    "WaypointOptimizationRestCycleDurationsTypeDef",
    {
        "RestDuration": int,
        "WorkDuration": int,
    },
)
WaypointOptimizationTrailerOptionsTypeDef = TypedDict(
    "WaypointOptimizationTrailerOptionsTypeDef",
    {
        "TrailerCount": NotRequired[int],
    },
)
CircleUnionTypeDef = Union[CircleTypeDef, CircleOutputTypeDef]
IsolineAvoidanceAreaGeometryTypeDef = TypedDict(
    "IsolineAvoidanceAreaGeometryTypeDef",
    {
        "BoundingBox": NotRequired[Sequence[float]],
        "Corridor": NotRequired[CorridorTypeDef],
        "Polygon": NotRequired[Sequence[Sequence[Sequence[float]]]],
        "PolylineCorridor": NotRequired[PolylineCorridorTypeDef],
        "PolylinePolygon": NotRequired[Sequence[str]],
    },
)
RouteAvoidanceAreaGeometryTypeDef = TypedDict(
    "RouteAvoidanceAreaGeometryTypeDef",
    {
        "Corridor": NotRequired[CorridorTypeDef],
        "BoundingBox": NotRequired[Sequence[float]],
        "Polygon": NotRequired[Sequence[Sequence[Sequence[float]]]],
        "PolylineCorridor": NotRequired[PolylineCorridorTypeDef],
        "PolylinePolygon": NotRequired[Sequence[str]],
    },
)
IsolineCarOptionsTypeDef = TypedDict(
    "IsolineCarOptionsTypeDef",
    {
        "EngineType": NotRequired[IsolineEngineTypeType],
        "LicensePlate": NotRequired[IsolineVehicleLicensePlateTypeDef],
        "MaxSpeed": NotRequired[float],
        "Occupancy": NotRequired[int],
    },
)
IsolineScooterOptionsTypeDef = TypedDict(
    "IsolineScooterOptionsTypeDef",
    {
        "EngineType": NotRequired[IsolineEngineTypeType],
        "LicensePlate": NotRequired[IsolineVehicleLicensePlateTypeDef],
        "MaxSpeed": NotRequired[float],
        "Occupancy": NotRequired[int],
    },
)
IsolineConnectionTypeDef = TypedDict(
    "IsolineConnectionTypeDef",
    {
        "FromPolygonIndex": int,
        "Geometry": IsolineConnectionGeometryTypeDef,
        "ToPolygonIndex": int,
    },
)
IsolineDestinationOptionsTypeDef = TypedDict(
    "IsolineDestinationOptionsTypeDef",
    {
        "AvoidActionsForDistance": NotRequired[int],
        "Heading": NotRequired[float],
        "Matching": NotRequired[IsolineMatchingOptionsTypeDef],
        "SideOfStreet": NotRequired[IsolineSideOfStreetOptionsTypeDef],
    },
)
IsolineOriginOptionsTypeDef = TypedDict(
    "IsolineOriginOptionsTypeDef",
    {
        "AvoidActionsForDistance": NotRequired[int],
        "Heading": NotRequired[float],
        "Matching": NotRequired[IsolineMatchingOptionsTypeDef],
        "SideOfStreet": NotRequired[IsolineSideOfStreetOptionsTypeDef],
    },
)
IsolineTruckOptionsTypeDef = TypedDict(
    "IsolineTruckOptionsTypeDef",
    {
        "AxleCount": NotRequired[int],
        "EngineType": NotRequired[IsolineEngineTypeType],
        "GrossWeight": NotRequired[int],
        "HazardousCargos": NotRequired[Sequence[IsolineHazardousCargoTypeType]],
        "Height": NotRequired[int],
        "HeightAboveFirstAxle": NotRequired[int],
        "KpraLength": NotRequired[int],
        "Length": NotRequired[int],
        "LicensePlate": NotRequired[IsolineVehicleLicensePlateTypeDef],
        "MaxSpeed": NotRequired[float],
        "Occupancy": NotRequired[int],
        "PayloadCapacity": NotRequired[int],
        "TireCount": NotRequired[int],
        "Trailer": NotRequired[IsolineTrailerOptionsTypeDef],
        "TruckType": NotRequired[IsolineTruckTypeType],
        "TunnelRestrictionCode": NotRequired[str],
        "WeightPerAxle": NotRequired[int],
        "WeightPerAxleGroup": NotRequired[WeightPerAxleGroupTypeDef],
        "Width": NotRequired[int],
    },
)
RouteContinueHighwayStepDetailsTypeDef = TypedDict(
    "RouteContinueHighwayStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
        "TurnAngle": NotRequired[float],
        "TurnIntensity": NotRequired[RouteTurnIntensityType],
    },
)
RouteContinueStepDetailsTypeDef = TypedDict(
    "RouteContinueStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
    },
)
RouteEnterHighwayStepDetailsTypeDef = TypedDict(
    "RouteEnterHighwayStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
        "TurnAngle": NotRequired[float],
        "TurnIntensity": NotRequired[RouteTurnIntensityType],
    },
)
RouteExitStepDetailsTypeDef = TypedDict(
    "RouteExitStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "RelativeExit": NotRequired[int],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
        "TurnAngle": NotRequired[float],
        "TurnIntensity": NotRequired[RouteTurnIntensityType],
    },
)
RouteFerrySpanTypeDef = TypedDict(
    "RouteFerrySpanTypeDef",
    {
        "Country": NotRequired[str],
        "Distance": NotRequired[int],
        "Duration": NotRequired[int],
        "GeometryOffset": NotRequired[int],
        "Names": NotRequired[List[LocalizedStringTypeDef]],
        "Region": NotRequired[str],
    },
)
RouteKeepStepDetailsTypeDef = TypedDict(
    "RouteKeepStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
        "TurnAngle": NotRequired[float],
        "TurnIntensity": NotRequired[RouteTurnIntensityType],
    },
)
RouteRampStepDetailsTypeDef = TypedDict(
    "RouteRampStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
        "TurnAngle": NotRequired[float],
        "TurnIntensity": NotRequired[RouteTurnIntensityType],
    },
)
RouteRoundaboutEnterStepDetailsTypeDef = TypedDict(
    "RouteRoundaboutEnterStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
        "TurnAngle": NotRequired[float],
        "TurnIntensity": NotRequired[RouteTurnIntensityType],
    },
)
RouteRoundaboutExitStepDetailsTypeDef = TypedDict(
    "RouteRoundaboutExitStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "RelativeExit": NotRequired[int],
        "RoundaboutAngle": NotRequired[float],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
    },
)
RouteRoundaboutPassStepDetailsTypeDef = TypedDict(
    "RouteRoundaboutPassStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
        "TurnAngle": NotRequired[float],
        "TurnIntensity": NotRequired[RouteTurnIntensityType],
    },
)
RouteTurnStepDetailsTypeDef = TypedDict(
    "RouteTurnStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
        "TurnAngle": NotRequired[float],
        "TurnIntensity": NotRequired[RouteTurnIntensityType],
    },
)
RouteUTurnStepDetailsTypeDef = TypedDict(
    "RouteUTurnStepDetailsTypeDef",
    {
        "Intersection": List[LocalizedStringTypeDef],
        "SteeringDirection": NotRequired[RouteSteeringDirectionType],
        "TurnAngle": NotRequired[float],
        "TurnIntensity": NotRequired[RouteTurnIntensityType],
    },
)
SnapToRoadsResponseTypeDef = TypedDict(
    "SnapToRoadsResponseTypeDef",
    {
        "Notices": List[RoadSnapNoticeTypeDef],
        "PricingBucket": str,
        "SnappedGeometry": RoadSnapSnappedGeometryTypeDef,
        "SnappedGeometryFormat": GeometryFormatType,
        "SnappedTracePoints": List[RoadSnapSnappedTracePointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RoadSnapTruckOptionsTypeDef = TypedDict(
    "RoadSnapTruckOptionsTypeDef",
    {
        "GrossWeight": NotRequired[int],
        "HazardousCargos": NotRequired[Sequence[RoadSnapHazardousCargoTypeType]],
        "Height": NotRequired[int],
        "Length": NotRequired[int],
        "Trailer": NotRequired[RoadSnapTrailerOptionsTypeDef],
        "TunnelRestrictionCode": NotRequired[str],
        "Width": NotRequired[int],
    },
)
RouteCarOptionsTypeDef = TypedDict(
    "RouteCarOptionsTypeDef",
    {
        "EngineType": NotRequired[RouteEngineTypeType],
        "LicensePlate": NotRequired[RouteVehicleLicensePlateTypeDef],
        "MaxSpeed": NotRequired[float],
        "Occupancy": NotRequired[int],
    },
)
RouteScooterOptionsTypeDef = TypedDict(
    "RouteScooterOptionsTypeDef",
    {
        "EngineType": NotRequired[RouteEngineTypeType],
        "LicensePlate": NotRequired[RouteVehicleLicensePlateTypeDef],
        "MaxSpeed": NotRequired[float],
        "Occupancy": NotRequired[int],
    },
)
RouteDestinationOptionsTypeDef = TypedDict(
    "RouteDestinationOptionsTypeDef",
    {
        "AvoidActionsForDistance": NotRequired[int],
        "AvoidUTurns": NotRequired[bool],
        "Heading": NotRequired[float],
        "Matching": NotRequired[RouteMatchingOptionsTypeDef],
        "SideOfStreet": NotRequired[RouteSideOfStreetOptionsTypeDef],
        "StopDuration": NotRequired[int],
    },
)
RouteOriginOptionsTypeDef = TypedDict(
    "RouteOriginOptionsTypeDef",
    {
        "AvoidActionsForDistance": NotRequired[int],
        "AvoidUTurns": NotRequired[bool],
        "Heading": NotRequired[float],
        "Matching": NotRequired[RouteMatchingOptionsTypeDef],
        "SideOfStreet": NotRequired[RouteSideOfStreetOptionsTypeDef],
    },
)
RouteWaypointTypeDef = TypedDict(
    "RouteWaypointTypeDef",
    {
        "Position": Sequence[float],
        "AvoidActionsForDistance": NotRequired[int],
        "AvoidUTurns": NotRequired[bool],
        "Heading": NotRequired[float],
        "Matching": NotRequired[RouteMatchingOptionsTypeDef],
        "PassThrough": NotRequired[bool],
        "SideOfStreet": NotRequired[RouteSideOfStreetOptionsTypeDef],
        "StopDuration": NotRequired[int],
    },
)
RouteDriverOptionsTypeDef = TypedDict(
    "RouteDriverOptionsTypeDef",
    {
        "Schedule": NotRequired[Sequence[RouteDriverScheduleIntervalTypeDef]],
    },
)
RouteTollOptionsTypeDef = TypedDict(
    "RouteTollOptionsTypeDef",
    {
        "AllTransponders": NotRequired[bool],
        "AllVignettes": NotRequired[bool],
        "Currency": NotRequired[str],
        "EmissionType": NotRequired[RouteEmissionTypeTypeDef],
        "VehicleCategory": NotRequired[Literal["Minibus"]],
    },
)
RouteFerryArrivalTypeDef = TypedDict(
    "RouteFerryArrivalTypeDef",
    {
        "Place": RouteFerryPlaceTypeDef,
        "Time": NotRequired[str],
    },
)
RouteFerryDepartureTypeDef = TypedDict(
    "RouteFerryDepartureTypeDef",
    {
        "Place": RouteFerryPlaceTypeDef,
        "Time": NotRequired[str],
    },
)
RouteFerrySummaryTypeDef = TypedDict(
    "RouteFerrySummaryTypeDef",
    {
        "Overview": NotRequired[RouteFerryOverviewSummaryTypeDef],
        "TravelOnly": NotRequired[RouteFerryTravelOnlySummaryTypeDef],
    },
)
RouteMajorRoadLabelTypeDef = TypedDict(
    "RouteMajorRoadLabelTypeDef",
    {
        "RoadName": NotRequired[LocalizedStringTypeDef],
        "RouteNumber": NotRequired[RouteNumberTypeDef],
    },
)
RouteRoadTypeDef = TypedDict(
    "RouteRoadTypeDef",
    {
        "RoadName": List[LocalizedStringTypeDef],
        "RouteNumber": List[RouteNumberTypeDef],
        "Towards": List[LocalizedStringTypeDef],
        "Type": NotRequired[RouteRoadTypeType],
    },
)
RouteSignpostLabelTypeDef = TypedDict(
    "RouteSignpostLabelTypeDef",
    {
        "RouteNumber": NotRequired[RouteNumberTypeDef],
        "Text": NotRequired[LocalizedStringTypeDef],
    },
)
RouteMatrixBoundaryGeometryOutputTypeDef = TypedDict(
    "RouteMatrixBoundaryGeometryOutputTypeDef",
    {
        "AutoCircle": NotRequired[RouteMatrixAutoCircleTypeDef],
        "Circle": NotRequired[CircleOutputTypeDef],
        "BoundingBox": NotRequired[List[float]],
        "Polygon": NotRequired[List[List[List[float]]]],
    },
)
RouteMatrixAvoidanceAreaTypeDef = TypedDict(
    "RouteMatrixAvoidanceAreaTypeDef",
    {
        "Geometry": RouteMatrixAvoidanceAreaGeometryTypeDef,
    },
)
RouteMatrixCarOptionsTypeDef = TypedDict(
    "RouteMatrixCarOptionsTypeDef",
    {
        "LicensePlate": NotRequired[RouteMatrixVehicleLicensePlateTypeDef],
        "MaxSpeed": NotRequired[float],
        "Occupancy": NotRequired[int],
    },
)
RouteMatrixScooterOptionsTypeDef = TypedDict(
    "RouteMatrixScooterOptionsTypeDef",
    {
        "LicensePlate": NotRequired[RouteMatrixVehicleLicensePlateTypeDef],
        "MaxSpeed": NotRequired[float],
        "Occupancy": NotRequired[int],
    },
)
RouteMatrixDestinationOptionsTypeDef = TypedDict(
    "RouteMatrixDestinationOptionsTypeDef",
    {
        "AvoidActionsForDistance": NotRequired[int],
        "Heading": NotRequired[float],
        "Matching": NotRequired[RouteMatrixMatchingOptionsTypeDef],
        "SideOfStreet": NotRequired[RouteMatrixSideOfStreetOptionsTypeDef],
    },
)
RouteMatrixOriginOptionsTypeDef = TypedDict(
    "RouteMatrixOriginOptionsTypeDef",
    {
        "AvoidActionsForDistance": NotRequired[int],
        "Heading": NotRequired[float],
        "Matching": NotRequired[RouteMatrixMatchingOptionsTypeDef],
        "SideOfStreet": NotRequired[RouteMatrixSideOfStreetOptionsTypeDef],
    },
)
RouteMatrixTruckOptionsTypeDef = TypedDict(
    "RouteMatrixTruckOptionsTypeDef",
    {
        "AxleCount": NotRequired[int],
        "GrossWeight": NotRequired[int],
        "HazardousCargos": NotRequired[Sequence[RouteMatrixHazardousCargoTypeType]],
        "Height": NotRequired[int],
        "KpraLength": NotRequired[int],
        "Length": NotRequired[int],
        "LicensePlate": NotRequired[RouteMatrixVehicleLicensePlateTypeDef],
        "MaxSpeed": NotRequired[float],
        "Occupancy": NotRequired[int],
        "PayloadCapacity": NotRequired[int],
        "Trailer": NotRequired[RouteMatrixTrailerOptionsTypeDef],
        "TruckType": NotRequired[RouteMatrixTruckTypeType],
        "TunnelRestrictionCode": NotRequired[str],
        "WeightPerAxle": NotRequired[int],
        "WeightPerAxleGroup": NotRequired[WeightPerAxleGroupTypeDef],
        "Width": NotRequired[int],
    },
)
RoutePassThroughWaypointTypeDef = TypedDict(
    "RoutePassThroughWaypointTypeDef",
    {
        "Place": RoutePassThroughPlaceTypeDef,
        "GeometryOffset": NotRequired[int],
    },
)
RoutePedestrianArrivalTypeDef = TypedDict(
    "RoutePedestrianArrivalTypeDef",
    {
        "Place": RoutePedestrianPlaceTypeDef,
        "Time": NotRequired[str],
    },
)
RoutePedestrianDepartureTypeDef = TypedDict(
    "RoutePedestrianDepartureTypeDef",
    {
        "Place": RoutePedestrianPlaceTypeDef,
        "Time": NotRequired[str],
    },
)
RoutePedestrianSpanTypeDef = TypedDict(
    "RoutePedestrianSpanTypeDef",
    {
        "BestCaseDuration": NotRequired[int],
        "Country": NotRequired[str],
        "Distance": NotRequired[int],
        "Duration": NotRequired[int],
        "DynamicSpeed": NotRequired[RouteSpanDynamicSpeedDetailsTypeDef],
        "FunctionalClassification": NotRequired[int],
        "GeometryOffset": NotRequired[int],
        "Incidents": NotRequired[List[int]],
        "Names": NotRequired[List[LocalizedStringTypeDef]],
        "PedestrianAccess": NotRequired[List[RouteSpanPedestrianAccessAttributeType]],
        "Region": NotRequired[str],
        "RoadAttributes": NotRequired[List[RouteSpanRoadAttributeType]],
        "RouteNumbers": NotRequired[List[RouteNumberTypeDef]],
        "SpeedLimit": NotRequired[RouteSpanSpeedLimitDetailsTypeDef],
        "TypicalDuration": NotRequired[int],
    },
)
RouteVehicleSpanTypeDef = TypedDict(
    "RouteVehicleSpanTypeDef",
    {
        "BestCaseDuration": NotRequired[int],
        "CarAccess": NotRequired[List[RouteSpanCarAccessAttributeType]],
        "Country": NotRequired[str],
        "Distance": NotRequired[int],
        "Duration": NotRequired[int],
        "DynamicSpeed": NotRequired[RouteSpanDynamicSpeedDetailsTypeDef],
        "FunctionalClassification": NotRequired[int],
        "Gate": NotRequired[RouteSpanGateAttributeType],
        "GeometryOffset": NotRequired[int],
        "Incidents": NotRequired[List[int]],
        "Names": NotRequired[List[LocalizedStringTypeDef]],
        "Notices": NotRequired[List[int]],
        "RailwayCrossing": NotRequired[RouteSpanRailwayCrossingAttributeType],
        "Region": NotRequired[str],
        "RoadAttributes": NotRequired[List[RouteSpanRoadAttributeType]],
        "RouteNumbers": NotRequired[List[RouteNumberTypeDef]],
        "ScooterAccess": NotRequired[List[RouteSpanScooterAccessAttributeType]],
        "SpeedLimit": NotRequired[RouteSpanSpeedLimitDetailsTypeDef],
        "TollSystems": NotRequired[List[int]],
        "TruckAccess": NotRequired[List[RouteSpanTruckAccessAttributeType]],
        "TruckRoadTypes": NotRequired[List[int]],
        "TypicalDuration": NotRequired[int],
        "Zones": NotRequired[List[int]],
    },
)
RoutePedestrianSummaryTypeDef = TypedDict(
    "RoutePedestrianSummaryTypeDef",
    {
        "Overview": NotRequired[RoutePedestrianOverviewSummaryTypeDef],
        "TravelOnly": NotRequired[RoutePedestrianTravelOnlySummaryTypeDef],
    },
)
RouteTollPassTypeDef = TypedDict(
    "RouteTollPassTypeDef",
    {
        "IncludesReturnTrip": NotRequired[bool],
        "SeniorPass": NotRequired[bool],
        "TransferCount": NotRequired[int],
        "TripCount": NotRequired[int],
        "ValidityPeriod": NotRequired[RouteTollPassValidityPeriodTypeDef],
    },
)
RouteTollPriceSummaryTypeDef = TypedDict(
    "RouteTollPriceSummaryTypeDef",
    {
        "Currency": str,
        "Estimate": bool,
        "Range": bool,
        "Value": float,
        "RangeValue": NotRequired[RouteTollPriceValueRangeTypeDef],
    },
)
RouteTollPriceTypeDef = TypedDict(
    "RouteTollPriceTypeDef",
    {
        "Currency": str,
        "Estimate": bool,
        "Range": bool,
        "Value": float,
        "PerDuration": NotRequired[int],
        "RangeValue": NotRequired[RouteTollPriceValueRangeTypeDef],
    },
)
RouteTruckOptionsTypeDef = TypedDict(
    "RouteTruckOptionsTypeDef",
    {
        "AxleCount": NotRequired[int],
        "EngineType": NotRequired[RouteEngineTypeType],
        "GrossWeight": NotRequired[int],
        "HazardousCargos": NotRequired[Sequence[RouteHazardousCargoTypeType]],
        "Height": NotRequired[int],
        "HeightAboveFirstAxle": NotRequired[int],
        "KpraLength": NotRequired[int],
        "Length": NotRequired[int],
        "LicensePlate": NotRequired[RouteVehicleLicensePlateTypeDef],
        "MaxSpeed": NotRequired[float],
        "Occupancy": NotRequired[int],
        "PayloadCapacity": NotRequired[int],
        "TireCount": NotRequired[int],
        "Trailer": NotRequired[RouteTrailerOptionsTypeDef],
        "TruckType": NotRequired[RouteTruckTypeType],
        "TunnelRestrictionCode": NotRequired[str],
        "WeightPerAxle": NotRequired[int],
        "WeightPerAxleGroup": NotRequired[WeightPerAxleGroupTypeDef],
        "Width": NotRequired[int],
    },
)
RouteVehicleArrivalTypeDef = TypedDict(
    "RouteVehicleArrivalTypeDef",
    {
        "Place": RouteVehiclePlaceTypeDef,
        "Time": NotRequired[str],
    },
)
RouteVehicleDepartureTypeDef = TypedDict(
    "RouteVehicleDepartureTypeDef",
    {
        "Place": RouteVehiclePlaceTypeDef,
        "Time": NotRequired[str],
    },
)
RouteVehicleSummaryTypeDef = TypedDict(
    "RouteVehicleSummaryTypeDef",
    {
        "Overview": NotRequired[RouteVehicleOverviewSummaryTypeDef],
        "TravelOnly": NotRequired[RouteVehicleTravelOnlySummaryTypeDef],
    },
)
RouteViolatedConstraintsTypeDef = TypedDict(
    "RouteViolatedConstraintsTypeDef",
    {
        "HazardousCargos": List[RouteHazardousCargoTypeType],
        "AllHazardsRestricted": NotRequired[bool],
        "AxleCount": NotRequired[RouteNoticeDetailRangeTypeDef],
        "MaxHeight": NotRequired[int],
        "MaxKpraLength": NotRequired[int],
        "MaxLength": NotRequired[int],
        "MaxPayloadCapacity": NotRequired[int],
        "MaxWeight": NotRequired[RouteWeightConstraintTypeDef],
        "MaxWeightPerAxle": NotRequired[int],
        "MaxWeightPerAxleGroup": NotRequired[WeightPerAxleGroupTypeDef],
        "MaxWidth": NotRequired[int],
        "Occupancy": NotRequired[RouteNoticeDetailRangeTypeDef],
        "RestrictedTimes": NotRequired[str],
        "TimeDependent": NotRequired[bool],
        "TrailerCount": NotRequired[RouteNoticeDetailRangeTypeDef],
        "TravelMode": NotRequired[bool],
        "TruckRoadType": NotRequired[str],
        "TruckType": NotRequired[RouteTruckTypeType],
        "TunnelRestrictionCode": NotRequired[str],
    },
)
WaypointOptimizationAccessHoursTypeDef = TypedDict(
    "WaypointOptimizationAccessHoursTypeDef",
    {
        "From": WaypointOptimizationAccessHoursEntryTypeDef,
        "To": WaypointOptimizationAccessHoursEntryTypeDef,
    },
)
WaypointOptimizationAvoidanceAreaTypeDef = TypedDict(
    "WaypointOptimizationAvoidanceAreaTypeDef",
    {
        "Geometry": WaypointOptimizationAvoidanceAreaGeometryTypeDef,
    },
)
WaypointOptimizationImpedingWaypointTypeDef = TypedDict(
    "WaypointOptimizationImpedingWaypointTypeDef",
    {
        "FailedConstraints": List[WaypointOptimizationFailedConstraintTypeDef],
        "Id": str,
        "Position": List[float],
    },
)
WaypointOptimizationRestCyclesTypeDef = TypedDict(
    "WaypointOptimizationRestCyclesTypeDef",
    {
        "LongCycle": WaypointOptimizationRestCycleDurationsTypeDef,
        "ShortCycle": WaypointOptimizationRestCycleDurationsTypeDef,
    },
)
WaypointOptimizationTruckOptionsTypeDef = TypedDict(
    "WaypointOptimizationTruckOptionsTypeDef",
    {
        "GrossWeight": NotRequired[int],
        "HazardousCargos": NotRequired[Sequence[WaypointOptimizationHazardousCargoTypeType]],
        "Height": NotRequired[int],
        "Length": NotRequired[int],
        "Trailer": NotRequired[WaypointOptimizationTrailerOptionsTypeDef],
        "TruckType": NotRequired[WaypointOptimizationTruckTypeType],
        "TunnelRestrictionCode": NotRequired[str],
        "WeightPerAxle": NotRequired[int],
        "Width": NotRequired[int],
    },
)
RouteMatrixBoundaryGeometryTypeDef = TypedDict(
    "RouteMatrixBoundaryGeometryTypeDef",
    {
        "AutoCircle": NotRequired[RouteMatrixAutoCircleTypeDef],
        "Circle": NotRequired[CircleUnionTypeDef],
        "BoundingBox": NotRequired[Sequence[float]],
        "Polygon": NotRequired[Sequence[Sequence[Sequence[float]]]],
    },
)
IsolineAvoidanceAreaTypeDef = TypedDict(
    "IsolineAvoidanceAreaTypeDef",
    {
        "Geometry": IsolineAvoidanceAreaGeometryTypeDef,
        "Except": NotRequired[Sequence[IsolineAvoidanceAreaGeometryTypeDef]],
    },
)
RouteAvoidanceAreaTypeDef = TypedDict(
    "RouteAvoidanceAreaTypeDef",
    {
        "Geometry": RouteAvoidanceAreaGeometryTypeDef,
        "Except": NotRequired[Sequence[RouteAvoidanceAreaGeometryTypeDef]],
    },
)
IsolineTypeDef = TypedDict(
    "IsolineTypeDef",
    {
        "Connections": List[IsolineConnectionTypeDef],
        "Geometries": List[IsolineShapeGeometryTypeDef],
        "DistanceThreshold": NotRequired[int],
        "TimeThreshold": NotRequired[int],
    },
)
IsolineTravelModeOptionsTypeDef = TypedDict(
    "IsolineTravelModeOptionsTypeDef",
    {
        "Car": NotRequired[IsolineCarOptionsTypeDef],
        "Scooter": NotRequired[IsolineScooterOptionsTypeDef],
        "Truck": NotRequired[IsolineTruckOptionsTypeDef],
    },
)
RoadSnapTravelModeOptionsTypeDef = TypedDict(
    "RoadSnapTravelModeOptionsTypeDef",
    {
        "Truck": NotRequired[RoadSnapTruckOptionsTypeDef],
    },
)
RouteSignpostTypeDef = TypedDict(
    "RouteSignpostTypeDef",
    {
        "Labels": List[RouteSignpostLabelTypeDef],
    },
)
RouteMatrixBoundaryOutputTypeDef = TypedDict(
    "RouteMatrixBoundaryOutputTypeDef",
    {
        "Geometry": NotRequired[RouteMatrixBoundaryGeometryOutputTypeDef],
        "Unbounded": NotRequired[bool],
    },
)
RouteMatrixAvoidanceOptionsTypeDef = TypedDict(
    "RouteMatrixAvoidanceOptionsTypeDef",
    {
        "Areas": NotRequired[Sequence[RouteMatrixAvoidanceAreaTypeDef]],
        "CarShuttleTrains": NotRequired[bool],
        "ControlledAccessHighways": NotRequired[bool],
        "DirtRoads": NotRequired[bool],
        "Ferries": NotRequired[bool],
        "TollRoads": NotRequired[bool],
        "TollTransponders": NotRequired[bool],
        "TruckRoadTypes": NotRequired[Sequence[str]],
        "Tunnels": NotRequired[bool],
        "UTurns": NotRequired[bool],
        "ZoneCategories": NotRequired[Sequence[RouteMatrixAvoidanceZoneCategoryTypeDef]],
    },
)
RouteMatrixDestinationTypeDef = TypedDict(
    "RouteMatrixDestinationTypeDef",
    {
        "Position": Sequence[float],
        "Options": NotRequired[RouteMatrixDestinationOptionsTypeDef],
    },
)
RouteMatrixOriginTypeDef = TypedDict(
    "RouteMatrixOriginTypeDef",
    {
        "Position": Sequence[float],
        "Options": NotRequired[RouteMatrixOriginOptionsTypeDef],
    },
)
RouteMatrixTravelModeOptionsTypeDef = TypedDict(
    "RouteMatrixTravelModeOptionsTypeDef",
    {
        "Car": NotRequired[RouteMatrixCarOptionsTypeDef],
        "Scooter": NotRequired[RouteMatrixScooterOptionsTypeDef],
        "Truck": NotRequired[RouteMatrixTruckOptionsTypeDef],
    },
)
RouteFerryLegDetailsTypeDef = TypedDict(
    "RouteFerryLegDetailsTypeDef",
    {
        "AfterTravelSteps": List[RouteFerryAfterTravelStepTypeDef],
        "Arrival": RouteFerryArrivalTypeDef,
        "BeforeTravelSteps": List[RouteFerryBeforeTravelStepTypeDef],
        "Departure": RouteFerryDepartureTypeDef,
        "Notices": List[RouteFerryNoticeTypeDef],
        "PassThroughWaypoints": List[RoutePassThroughWaypointTypeDef],
        "Spans": List[RouteFerrySpanTypeDef],
        "TravelSteps": List[RouteFerryTravelStepTypeDef],
        "RouteName": NotRequired[str],
        "Summary": NotRequired[RouteFerrySummaryTypeDef],
    },
)
RouteTollSummaryTypeDef = TypedDict(
    "RouteTollSummaryTypeDef",
    {
        "Total": NotRequired[RouteTollPriceSummaryTypeDef],
    },
)
RouteTollRateTypeDef = TypedDict(
    "RouteTollRateTypeDef",
    {
        "Id": str,
        "LocalPrice": RouteTollPriceTypeDef,
        "Name": str,
        "PaymentMethods": List[RouteTollPaymentMethodType],
        "Transponders": List[RouteTransponderTypeDef],
        "ApplicableTimes": NotRequired[str],
        "ConvertedPrice": NotRequired[RouteTollPriceTypeDef],
        "Pass": NotRequired[RouteTollPassTypeDef],
    },
)
RouteTravelModeOptionsTypeDef = TypedDict(
    "RouteTravelModeOptionsTypeDef",
    {
        "Car": NotRequired[RouteCarOptionsTypeDef],
        "Pedestrian": NotRequired[RoutePedestrianOptionsTypeDef],
        "Scooter": NotRequired[RouteScooterOptionsTypeDef],
        "Truck": NotRequired[RouteTruckOptionsTypeDef],
    },
)
RouteVehicleNoticeDetailTypeDef = TypedDict(
    "RouteVehicleNoticeDetailTypeDef",
    {
        "Title": NotRequired[str],
        "ViolatedConstraints": NotRequired[RouteViolatedConstraintsTypeDef],
    },
)
WaypointOptimizationDestinationOptionsTypeDef = TypedDict(
    "WaypointOptimizationDestinationOptionsTypeDef",
    {
        "AccessHours": NotRequired[WaypointOptimizationAccessHoursTypeDef],
        "AppointmentTime": NotRequired[str],
        "Heading": NotRequired[float],
        "Id": NotRequired[str],
        "ServiceDuration": NotRequired[int],
        "SideOfStreet": NotRequired[WaypointOptimizationSideOfStreetOptionsTypeDef],
    },
)
WaypointOptimizationWaypointTypeDef = TypedDict(
    "WaypointOptimizationWaypointTypeDef",
    {
        "Position": Sequence[float],
        "AccessHours": NotRequired[WaypointOptimizationAccessHoursTypeDef],
        "AppointmentTime": NotRequired[str],
        "Before": NotRequired[Sequence[int]],
        "Heading": NotRequired[float],
        "Id": NotRequired[str],
        "ServiceDuration": NotRequired[int],
        "SideOfStreet": NotRequired[WaypointOptimizationSideOfStreetOptionsTypeDef],
    },
)
WaypointOptimizationAvoidanceOptionsTypeDef = TypedDict(
    "WaypointOptimizationAvoidanceOptionsTypeDef",
    {
        "Areas": NotRequired[Sequence[WaypointOptimizationAvoidanceAreaTypeDef]],
        "CarShuttleTrains": NotRequired[bool],
        "ControlledAccessHighways": NotRequired[bool],
        "DirtRoads": NotRequired[bool],
        "Ferries": NotRequired[bool],
        "TollRoads": NotRequired[bool],
        "Tunnels": NotRequired[bool],
        "UTurns": NotRequired[bool],
    },
)
OptimizeWaypointsResponseTypeDef = TypedDict(
    "OptimizeWaypointsResponseTypeDef",
    {
        "Connections": List[WaypointOptimizationConnectionTypeDef],
        "Distance": int,
        "Duration": int,
        "ImpedingWaypoints": List[WaypointOptimizationImpedingWaypointTypeDef],
        "OptimizedWaypoints": List[WaypointOptimizationOptimizedWaypointTypeDef],
        "PricingBucket": str,
        "TimeBreakdown": WaypointOptimizationTimeBreakdownTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
WaypointOptimizationDriverOptionsTypeDef = TypedDict(
    "WaypointOptimizationDriverOptionsTypeDef",
    {
        "RestCycles": NotRequired[WaypointOptimizationRestCyclesTypeDef],
        "RestProfile": NotRequired[WaypointOptimizationRestProfileTypeDef],
        "TreatServiceTimeAs": NotRequired[WaypointOptimizationServiceTimeTreatmentType],
    },
)
WaypointOptimizationTravelModeOptionsTypeDef = TypedDict(
    "WaypointOptimizationTravelModeOptionsTypeDef",
    {
        "Pedestrian": NotRequired[WaypointOptimizationPedestrianOptionsTypeDef],
        "Truck": NotRequired[WaypointOptimizationTruckOptionsTypeDef],
    },
)
RouteMatrixBoundaryGeometryUnionTypeDef = Union[
    RouteMatrixBoundaryGeometryTypeDef, RouteMatrixBoundaryGeometryOutputTypeDef
]
IsolineAvoidanceOptionsTypeDef = TypedDict(
    "IsolineAvoidanceOptionsTypeDef",
    {
        "Areas": NotRequired[Sequence[IsolineAvoidanceAreaTypeDef]],
        "CarShuttleTrains": NotRequired[bool],
        "ControlledAccessHighways": NotRequired[bool],
        "DirtRoads": NotRequired[bool],
        "Ferries": NotRequired[bool],
        "SeasonalClosure": NotRequired[bool],
        "TollRoads": NotRequired[bool],
        "TollTransponders": NotRequired[bool],
        "TruckRoadTypes": NotRequired[Sequence[str]],
        "Tunnels": NotRequired[bool],
        "UTurns": NotRequired[bool],
        "ZoneCategories": NotRequired[Sequence[IsolineAvoidanceZoneCategoryTypeDef]],
    },
)
RouteAvoidanceOptionsTypeDef = TypedDict(
    "RouteAvoidanceOptionsTypeDef",
    {
        "Areas": NotRequired[Sequence[RouteAvoidanceAreaTypeDef]],
        "CarShuttleTrains": NotRequired[bool],
        "ControlledAccessHighways": NotRequired[bool],
        "DirtRoads": NotRequired[bool],
        "Ferries": NotRequired[bool],
        "SeasonalClosure": NotRequired[bool],
        "TollRoads": NotRequired[bool],
        "TollTransponders": NotRequired[bool],
        "TruckRoadTypes": NotRequired[Sequence[str]],
        "Tunnels": NotRequired[bool],
        "UTurns": NotRequired[bool],
        "ZoneCategories": NotRequired[Sequence[RouteAvoidanceZoneCategoryTypeDef]],
    },
)
CalculateIsolinesResponseTypeDef = TypedDict(
    "CalculateIsolinesResponseTypeDef",
    {
        "ArrivalTime": str,
        "DepartureTime": str,
        "IsolineGeometryFormat": GeometryFormatType,
        "Isolines": List[IsolineTypeDef],
        "PricingBucket": str,
        "SnappedDestination": List[float],
        "SnappedOrigin": List[float],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SnapToRoadsRequestRequestTypeDef = TypedDict(
    "SnapToRoadsRequestRequestTypeDef",
    {
        "TracePoints": Sequence[RoadSnapTracePointTypeDef],
        "Key": NotRequired[str],
        "SnappedGeometryFormat": NotRequired[GeometryFormatType],
        "SnapRadius": NotRequired[int],
        "TravelMode": NotRequired[RoadSnapTravelModeType],
        "TravelModeOptions": NotRequired[RoadSnapTravelModeOptionsTypeDef],
    },
)
RoutePedestrianTravelStepTypeDef = TypedDict(
    "RoutePedestrianTravelStepTypeDef",
    {
        "Duration": int,
        "Type": RoutePedestrianTravelStepTypeType,
        "ContinueStepDetails": NotRequired[RouteContinueStepDetailsTypeDef],
        "CurrentRoad": NotRequired[RouteRoadTypeDef],
        "Distance": NotRequired[int],
        "ExitNumber": NotRequired[List[LocalizedStringTypeDef]],
        "GeometryOffset": NotRequired[int],
        "Instruction": NotRequired[str],
        "KeepStepDetails": NotRequired[RouteKeepStepDetailsTypeDef],
        "NextRoad": NotRequired[RouteRoadTypeDef],
        "RoundaboutEnterStepDetails": NotRequired[RouteRoundaboutEnterStepDetailsTypeDef],
        "RoundaboutExitStepDetails": NotRequired[RouteRoundaboutExitStepDetailsTypeDef],
        "RoundaboutPassStepDetails": NotRequired[RouteRoundaboutPassStepDetailsTypeDef],
        "Signpost": NotRequired[RouteSignpostTypeDef],
        "TurnStepDetails": NotRequired[RouteTurnStepDetailsTypeDef],
    },
)
RouteVehicleTravelStepTypeDef = TypedDict(
    "RouteVehicleTravelStepTypeDef",
    {
        "Duration": int,
        "Type": RouteVehicleTravelStepTypeType,
        "ContinueHighwayStepDetails": NotRequired[RouteContinueHighwayStepDetailsTypeDef],
        "ContinueStepDetails": NotRequired[RouteContinueStepDetailsTypeDef],
        "CurrentRoad": NotRequired[RouteRoadTypeDef],
        "Distance": NotRequired[int],
        "EnterHighwayStepDetails": NotRequired[RouteEnterHighwayStepDetailsTypeDef],
        "ExitNumber": NotRequired[List[LocalizedStringTypeDef]],
        "ExitStepDetails": NotRequired[RouteExitStepDetailsTypeDef],
        "GeometryOffset": NotRequired[int],
        "Instruction": NotRequired[str],
        "KeepStepDetails": NotRequired[RouteKeepStepDetailsTypeDef],
        "NextRoad": NotRequired[RouteRoadTypeDef],
        "RampStepDetails": NotRequired[RouteRampStepDetailsTypeDef],
        "RoundaboutEnterStepDetails": NotRequired[RouteRoundaboutEnterStepDetailsTypeDef],
        "RoundaboutExitStepDetails": NotRequired[RouteRoundaboutExitStepDetailsTypeDef],
        "RoundaboutPassStepDetails": NotRequired[RouteRoundaboutPassStepDetailsTypeDef],
        "Signpost": NotRequired[RouteSignpostTypeDef],
        "TurnStepDetails": NotRequired[RouteTurnStepDetailsTypeDef],
        "UTurnStepDetails": NotRequired[RouteUTurnStepDetailsTypeDef],
    },
)
CalculateRouteMatrixResponseTypeDef = TypedDict(
    "CalculateRouteMatrixResponseTypeDef",
    {
        "ErrorCount": int,
        "PricingBucket": str,
        "RouteMatrix": List[List[RouteMatrixEntryTypeDef]],
        "RoutingBoundary": RouteMatrixBoundaryOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RouteSummaryTypeDef = TypedDict(
    "RouteSummaryTypeDef",
    {
        "Distance": NotRequired[int],
        "Duration": NotRequired[int],
        "Tolls": NotRequired[RouteTollSummaryTypeDef],
    },
)
RouteTollTypeDef = TypedDict(
    "RouteTollTypeDef",
    {
        "PaymentSites": List[RouteTollPaymentSiteTypeDef],
        "Rates": List[RouteTollRateTypeDef],
        "Systems": List[int],
        "Country": NotRequired[str],
    },
)
RouteVehicleNoticeTypeDef = TypedDict(
    "RouteVehicleNoticeTypeDef",
    {
        "Code": RouteVehicleNoticeCodeType,
        "Details": List[RouteVehicleNoticeDetailTypeDef],
        "Impact": NotRequired[RouteNoticeImpactType],
    },
)
OptimizeWaypointsRequestRequestTypeDef = TypedDict(
    "OptimizeWaypointsRequestRequestTypeDef",
    {
        "Origin": Sequence[float],
        "Avoid": NotRequired[WaypointOptimizationAvoidanceOptionsTypeDef],
        "DepartureTime": NotRequired[str],
        "Destination": NotRequired[Sequence[float]],
        "DestinationOptions": NotRequired[WaypointOptimizationDestinationOptionsTypeDef],
        "Driver": NotRequired[WaypointOptimizationDriverOptionsTypeDef],
        "Exclude": NotRequired[WaypointOptimizationExclusionOptionsTypeDef],
        "Key": NotRequired[str],
        "OptimizeSequencingFor": NotRequired[WaypointOptimizationSequencingObjectiveType],
        "OriginOptions": NotRequired[WaypointOptimizationOriginOptionsTypeDef],
        "Traffic": NotRequired[WaypointOptimizationTrafficOptionsTypeDef],
        "TravelMode": NotRequired[WaypointOptimizationTravelModeType],
        "TravelModeOptions": NotRequired[WaypointOptimizationTravelModeOptionsTypeDef],
        "Waypoints": NotRequired[Sequence[WaypointOptimizationWaypointTypeDef]],
    },
)
RouteMatrixBoundaryTypeDef = TypedDict(
    "RouteMatrixBoundaryTypeDef",
    {
        "Geometry": NotRequired[RouteMatrixBoundaryGeometryUnionTypeDef],
        "Unbounded": NotRequired[bool],
    },
)
CalculateIsolinesRequestRequestTypeDef = TypedDict(
    "CalculateIsolinesRequestRequestTypeDef",
    {
        "Thresholds": IsolineThresholdsTypeDef,
        "Allow": NotRequired[IsolineAllowOptionsTypeDef],
        "ArrivalTime": NotRequired[str],
        "Avoid": NotRequired[IsolineAvoidanceOptionsTypeDef],
        "DepartNow": NotRequired[bool],
        "DepartureTime": NotRequired[str],
        "Destination": NotRequired[Sequence[float]],
        "DestinationOptions": NotRequired[IsolineDestinationOptionsTypeDef],
        "IsolineGeometryFormat": NotRequired[GeometryFormatType],
        "IsolineGranularity": NotRequired[IsolineGranularityOptionsTypeDef],
        "Key": NotRequired[str],
        "OptimizeIsolineFor": NotRequired[IsolineOptimizationObjectiveType],
        "OptimizeRoutingFor": NotRequired[RoutingObjectiveType],
        "Origin": NotRequired[Sequence[float]],
        "OriginOptions": NotRequired[IsolineOriginOptionsTypeDef],
        "Traffic": NotRequired[IsolineTrafficOptionsTypeDef],
        "TravelMode": NotRequired[IsolineTravelModeType],
        "TravelModeOptions": NotRequired[IsolineTravelModeOptionsTypeDef],
    },
)
CalculateRoutesRequestRequestTypeDef = TypedDict(
    "CalculateRoutesRequestRequestTypeDef",
    {
        "Destination": Sequence[float],
        "Origin": Sequence[float],
        "Allow": NotRequired[RouteAllowOptionsTypeDef],
        "ArrivalTime": NotRequired[str],
        "Avoid": NotRequired[RouteAvoidanceOptionsTypeDef],
        "DepartNow": NotRequired[bool],
        "DepartureTime": NotRequired[str],
        "DestinationOptions": NotRequired[RouteDestinationOptionsTypeDef],
        "Driver": NotRequired[RouteDriverOptionsTypeDef],
        "Exclude": NotRequired[RouteExclusionOptionsTypeDef],
        "InstructionsMeasurementSystem": NotRequired[MeasurementSystemType],
        "Key": NotRequired[str],
        "Languages": NotRequired[Sequence[str]],
        "LegAdditionalFeatures": NotRequired[Sequence[RouteLegAdditionalFeatureType]],
        "LegGeometryFormat": NotRequired[GeometryFormatType],
        "MaxAlternatives": NotRequired[int],
        "OptimizeRoutingFor": NotRequired[RoutingObjectiveType],
        "OriginOptions": NotRequired[RouteOriginOptionsTypeDef],
        "SpanAdditionalFeatures": NotRequired[Sequence[RouteSpanAdditionalFeatureType]],
        "Tolls": NotRequired[RouteTollOptionsTypeDef],
        "Traffic": NotRequired[RouteTrafficOptionsTypeDef],
        "TravelMode": NotRequired[RouteTravelModeType],
        "TravelModeOptions": NotRequired[RouteTravelModeOptionsTypeDef],
        "TravelStepType": NotRequired[RouteTravelStepTypeType],
        "Waypoints": NotRequired[Sequence[RouteWaypointTypeDef]],
    },
)
RoutePedestrianLegDetailsTypeDef = TypedDict(
    "RoutePedestrianLegDetailsTypeDef",
    {
        "Arrival": RoutePedestrianArrivalTypeDef,
        "Departure": RoutePedestrianDepartureTypeDef,
        "Notices": List[RoutePedestrianNoticeTypeDef],
        "PassThroughWaypoints": List[RoutePassThroughWaypointTypeDef],
        "Spans": List[RoutePedestrianSpanTypeDef],
        "TravelSteps": List[RoutePedestrianTravelStepTypeDef],
        "Summary": NotRequired[RoutePedestrianSummaryTypeDef],
    },
)
RouteVehicleLegDetailsTypeDef = TypedDict(
    "RouteVehicleLegDetailsTypeDef",
    {
        "Arrival": RouteVehicleArrivalTypeDef,
        "Departure": RouteVehicleDepartureTypeDef,
        "Incidents": List[RouteVehicleIncidentTypeDef],
        "Notices": List[RouteVehicleNoticeTypeDef],
        "PassThroughWaypoints": List[RoutePassThroughWaypointTypeDef],
        "Spans": List[RouteVehicleSpanTypeDef],
        "Tolls": List[RouteTollTypeDef],
        "TollSystems": List[RouteTollSystemTypeDef],
        "TravelSteps": List[RouteVehicleTravelStepTypeDef],
        "TruckRoadTypes": List[str],
        "Zones": List[RouteZoneTypeDef],
        "Summary": NotRequired[RouteVehicleSummaryTypeDef],
    },
)
CalculateRouteMatrixRequestRequestTypeDef = TypedDict(
    "CalculateRouteMatrixRequestRequestTypeDef",
    {
        "Destinations": Sequence[RouteMatrixDestinationTypeDef],
        "Origins": Sequence[RouteMatrixOriginTypeDef],
        "RoutingBoundary": RouteMatrixBoundaryTypeDef,
        "Allow": NotRequired[RouteMatrixAllowOptionsTypeDef],
        "Avoid": NotRequired[RouteMatrixAvoidanceOptionsTypeDef],
        "DepartNow": NotRequired[bool],
        "DepartureTime": NotRequired[str],
        "Exclude": NotRequired[RouteMatrixExclusionOptionsTypeDef],
        "Key": NotRequired[str],
        "OptimizeRoutingFor": NotRequired[RoutingObjectiveType],
        "Traffic": NotRequired[RouteMatrixTrafficOptionsTypeDef],
        "TravelMode": NotRequired[RouteMatrixTravelModeType],
        "TravelModeOptions": NotRequired[RouteMatrixTravelModeOptionsTypeDef],
    },
)
RouteLegTypeDef = TypedDict(
    "RouteLegTypeDef",
    {
        "Geometry": RouteLegGeometryTypeDef,
        "TravelMode": RouteLegTravelModeType,
        "Type": RouteLegTypeType,
        "FerryLegDetails": NotRequired[RouteFerryLegDetailsTypeDef],
        "Language": NotRequired[str],
        "PedestrianLegDetails": NotRequired[RoutePedestrianLegDetailsTypeDef],
        "VehicleLegDetails": NotRequired[RouteVehicleLegDetailsTypeDef],
    },
)
RouteTypeDef = TypedDict(
    "RouteTypeDef",
    {
        "Legs": List[RouteLegTypeDef],
        "MajorRoadLabels": List[RouteMajorRoadLabelTypeDef],
        "Summary": NotRequired[RouteSummaryTypeDef],
    },
)
CalculateRoutesResponseTypeDef = TypedDict(
    "CalculateRoutesResponseTypeDef",
    {
        "LegGeometryFormat": GeometryFormatType,
        "Notices": List[RouteResponseNoticeTypeDef],
        "PricingBucket": str,
        "Routes": List[RouteTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
