"""
Type annotations for amp service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amp/type_defs/)

Usage::

    ```python
    from mypy_boto3_amp.type_defs import AlertManagerDefinitionStatusTypeDef

    data: AlertManagerDefinitionStatusTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AlertManagerDefinitionStatusCodeType,
    LoggingConfigurationStatusCodeType,
    RuleGroupsNamespaceStatusCodeType,
    ScraperStatusCodeType,
    WorkspaceStatusCodeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AlertManagerDefinitionStatusTypeDef",
    "AmpConfigurationTypeDef",
    "BlobTypeDef",
    "ResponseMetadataTypeDef",
    "CreateLoggingConfigurationRequestRequestTypeDef",
    "LoggingConfigurationStatusTypeDef",
    "RuleGroupsNamespaceStatusTypeDef",
    "ScraperStatusTypeDef",
    "CreateWorkspaceRequestRequestTypeDef",
    "WorkspaceStatusTypeDef",
    "DeleteAlertManagerDefinitionRequestRequestTypeDef",
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    "DeleteRuleGroupsNamespaceRequestRequestTypeDef",
    "DeleteScraperRequestRequestTypeDef",
    "DeleteWorkspaceRequestRequestTypeDef",
    "DescribeAlertManagerDefinitionRequestRequestTypeDef",
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    "DescribeRuleGroupsNamespaceRequestRequestTypeDef",
    "DescribeScraperRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeWorkspaceRequestRequestTypeDef",
    "EksConfigurationOutputTypeDef",
    "EksConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ListRuleGroupsNamespacesRequestRequestTypeDef",
    "ListScrapersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWorkspacesRequestRequestTypeDef",
    "ScrapeConfigurationOutputTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    "UpdateWorkspaceAliasRequestRequestTypeDef",
    "AlertManagerDefinitionDescriptionTypeDef",
    "DestinationTypeDef",
    "CreateAlertManagerDefinitionRequestRequestTypeDef",
    "CreateRuleGroupsNamespaceRequestRequestTypeDef",
    "PutAlertManagerDefinitionRequestRequestTypeDef",
    "PutRuleGroupsNamespaceRequestRequestTypeDef",
    "ScrapeConfigurationTypeDef",
    "CreateAlertManagerDefinitionResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDefaultScraperConfigurationResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutAlertManagerDefinitionResponseTypeDef",
    "CreateLoggingConfigurationResponseTypeDef",
    "LoggingConfigurationMetadataTypeDef",
    "UpdateLoggingConfigurationResponseTypeDef",
    "CreateRuleGroupsNamespaceResponseTypeDef",
    "PutRuleGroupsNamespaceResponseTypeDef",
    "RuleGroupsNamespaceDescriptionTypeDef",
    "RuleGroupsNamespaceSummaryTypeDef",
    "CreateScraperResponseTypeDef",
    "DeleteScraperResponseTypeDef",
    "UpdateScraperResponseTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "WorkspaceDescriptionTypeDef",
    "WorkspaceSummaryTypeDef",
    "DescribeScraperRequestScraperActiveWaitTypeDef",
    "DescribeScraperRequestScraperDeletedWaitTypeDef",
    "DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef",
    "DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef",
    "SourceOutputTypeDef",
    "EksConfigurationUnionTypeDef",
    "ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef",
    "ListScrapersRequestListScrapersPaginateTypeDef",
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    "DescribeAlertManagerDefinitionResponseTypeDef",
    "UpdateScraperRequestRequestTypeDef",
    "DescribeLoggingConfigurationResponseTypeDef",
    "DescribeRuleGroupsNamespaceResponseTypeDef",
    "ListRuleGroupsNamespacesResponseTypeDef",
    "DescribeWorkspaceResponseTypeDef",
    "ListWorkspacesResponseTypeDef",
    "ScraperDescriptionTypeDef",
    "ScraperSummaryTypeDef",
    "SourceTypeDef",
    "DescribeScraperResponseTypeDef",
    "ListScrapersResponseTypeDef",
    "CreateScraperRequestRequestTypeDef",
)

AlertManagerDefinitionStatusTypeDef = TypedDict(
    "AlertManagerDefinitionStatusTypeDef",
    {
        "statusCode": AlertManagerDefinitionStatusCodeType,
        "statusReason": NotRequired[str],
    },
)
AmpConfigurationTypeDef = TypedDict(
    "AmpConfigurationTypeDef",
    {
        "workspaceArn": str,
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
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
CreateLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "CreateLoggingConfigurationRequestRequestTypeDef",
    {
        "logGroupArn": str,
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)
LoggingConfigurationStatusTypeDef = TypedDict(
    "LoggingConfigurationStatusTypeDef",
    {
        "statusCode": LoggingConfigurationStatusCodeType,
        "statusReason": NotRequired[str],
    },
)
RuleGroupsNamespaceStatusTypeDef = TypedDict(
    "RuleGroupsNamespaceStatusTypeDef",
    {
        "statusCode": RuleGroupsNamespaceStatusCodeType,
        "statusReason": NotRequired[str],
    },
)
ScraperStatusTypeDef = TypedDict(
    "ScraperStatusTypeDef",
    {
        "statusCode": ScraperStatusCodeType,
    },
)
CreateWorkspaceRequestRequestTypeDef = TypedDict(
    "CreateWorkspaceRequestRequestTypeDef",
    {
        "alias": NotRequired[str],
        "clientToken": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
WorkspaceStatusTypeDef = TypedDict(
    "WorkspaceStatusTypeDef",
    {
        "statusCode": WorkspaceStatusCodeType,
    },
)
DeleteAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteAlertManagerDefinitionRequestRequestTypeDef",
    {
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    {
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "DeleteRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "name": str,
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteScraperRequestRequestTypeDef = TypedDict(
    "DeleteScraperRequestRequestTypeDef",
    {
        "scraperId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteWorkspaceRequestRequestTypeDef = TypedDict(
    "DeleteWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)
DescribeAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeAlertManagerDefinitionRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
DescribeLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
DescribeRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "DescribeRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "name": str,
        "workspaceId": str,
    },
)
DescribeScraperRequestRequestTypeDef = TypedDict(
    "DescribeScraperRequestRequestTypeDef",
    {
        "scraperId": str,
    },
)
WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": NotRequired[int],
        "MaxAttempts": NotRequired[int],
    },
)
DescribeWorkspaceRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)
EksConfigurationOutputTypeDef = TypedDict(
    "EksConfigurationOutputTypeDef",
    {
        "clusterArn": str,
        "subnetIds": List[str],
        "securityGroupIds": NotRequired[List[str]],
    },
)
EksConfigurationTypeDef = TypedDict(
    "EksConfigurationTypeDef",
    {
        "clusterArn": str,
        "subnetIds": Sequence[str],
        "securityGroupIds": NotRequired[Sequence[str]],
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ListRuleGroupsNamespacesRequestRequestTypeDef = TypedDict(
    "ListRuleGroupsNamespacesRequestRequestTypeDef",
    {
        "workspaceId": str,
        "maxResults": NotRequired[int],
        "name": NotRequired[str],
        "nextToken": NotRequired[str],
    },
)
ListScrapersRequestRequestTypeDef = TypedDict(
    "ListScrapersRequestRequestTypeDef",
    {
        "filters": NotRequired[Mapping[str, Sequence[str]]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
ListWorkspacesRequestRequestTypeDef = TypedDict(
    "ListWorkspacesRequestRequestTypeDef",
    {
        "alias": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ScrapeConfigurationOutputTypeDef = TypedDict(
    "ScrapeConfigurationOutputTypeDef",
    {
        "configurationBlob": NotRequired[bytes],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
UpdateLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    {
        "logGroupArn": str,
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)
UpdateWorkspaceAliasRequestRequestTypeDef = TypedDict(
    "UpdateWorkspaceAliasRequestRequestTypeDef",
    {
        "workspaceId": str,
        "alias": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)
AlertManagerDefinitionDescriptionTypeDef = TypedDict(
    "AlertManagerDefinitionDescriptionTypeDef",
    {
        "createdAt": datetime,
        "data": bytes,
        "modifiedAt": datetime,
        "status": AlertManagerDefinitionStatusTypeDef,
    },
)
DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "ampConfiguration": NotRequired[AmpConfigurationTypeDef],
    },
)
CreateAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "CreateAlertManagerDefinitionRequestRequestTypeDef",
    {
        "data": BlobTypeDef,
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)
CreateRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "CreateRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "data": BlobTypeDef,
        "name": str,
        "workspaceId": str,
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
PutAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "PutAlertManagerDefinitionRequestRequestTypeDef",
    {
        "data": BlobTypeDef,
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)
PutRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "PutRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "data": BlobTypeDef,
        "name": str,
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)
ScrapeConfigurationTypeDef = TypedDict(
    "ScrapeConfigurationTypeDef",
    {
        "configurationBlob": NotRequired[BlobTypeDef],
    },
)
CreateAlertManagerDefinitionResponseTypeDef = TypedDict(
    "CreateAlertManagerDefinitionResponseTypeDef",
    {
        "status": AlertManagerDefinitionStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDefaultScraperConfigurationResponseTypeDef = TypedDict(
    "GetDefaultScraperConfigurationResponseTypeDef",
    {
        "configuration": bytes,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutAlertManagerDefinitionResponseTypeDef = TypedDict(
    "PutAlertManagerDefinitionResponseTypeDef",
    {
        "status": AlertManagerDefinitionStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateLoggingConfigurationResponseTypeDef = TypedDict(
    "CreateLoggingConfigurationResponseTypeDef",
    {
        "status": LoggingConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
LoggingConfigurationMetadataTypeDef = TypedDict(
    "LoggingConfigurationMetadataTypeDef",
    {
        "createdAt": datetime,
        "logGroupArn": str,
        "modifiedAt": datetime,
        "status": LoggingConfigurationStatusTypeDef,
        "workspace": str,
    },
)
UpdateLoggingConfigurationResponseTypeDef = TypedDict(
    "UpdateLoggingConfigurationResponseTypeDef",
    {
        "status": LoggingConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateRuleGroupsNamespaceResponseTypeDef = TypedDict(
    "CreateRuleGroupsNamespaceResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutRuleGroupsNamespaceResponseTypeDef = TypedDict(
    "PutRuleGroupsNamespaceResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RuleGroupsNamespaceDescriptionTypeDef = TypedDict(
    "RuleGroupsNamespaceDescriptionTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "data": bytes,
        "modifiedAt": datetime,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "tags": NotRequired[Dict[str, str]],
    },
)
RuleGroupsNamespaceSummaryTypeDef = TypedDict(
    "RuleGroupsNamespaceSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateScraperResponseTypeDef = TypedDict(
    "CreateScraperResponseTypeDef",
    {
        "arn": str,
        "scraperId": str,
        "status": ScraperStatusTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteScraperResponseTypeDef = TypedDict(
    "DeleteScraperResponseTypeDef",
    {
        "scraperId": str,
        "status": ScraperStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateScraperResponseTypeDef = TypedDict(
    "UpdateScraperResponseTypeDef",
    {
        "arn": str,
        "scraperId": str,
        "status": ScraperStatusTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateWorkspaceResponseTypeDef = TypedDict(
    "CreateWorkspaceResponseTypeDef",
    {
        "arn": str,
        "kmsKeyArn": str,
        "status": WorkspaceStatusTypeDef,
        "tags": Dict[str, str],
        "workspaceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
WorkspaceDescriptionTypeDef = TypedDict(
    "WorkspaceDescriptionTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "status": WorkspaceStatusTypeDef,
        "workspaceId": str,
        "alias": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "prometheusEndpoint": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
WorkspaceSummaryTypeDef = TypedDict(
    "WorkspaceSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "status": WorkspaceStatusTypeDef,
        "workspaceId": str,
        "alias": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
DescribeScraperRequestScraperActiveWaitTypeDef = TypedDict(
    "DescribeScraperRequestScraperActiveWaitTypeDef",
    {
        "scraperId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
DescribeScraperRequestScraperDeletedWaitTypeDef = TypedDict(
    "DescribeScraperRequestScraperDeletedWaitTypeDef",
    {
        "scraperId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef = TypedDict(
    "DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef",
    {
        "workspaceId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef = TypedDict(
    "DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef",
    {
        "workspaceId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
SourceOutputTypeDef = TypedDict(
    "SourceOutputTypeDef",
    {
        "eksConfiguration": NotRequired[EksConfigurationOutputTypeDef],
    },
)
EksConfigurationUnionTypeDef = Union[EksConfigurationTypeDef, EksConfigurationOutputTypeDef]
ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef = TypedDict(
    "ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef",
    {
        "workspaceId": str,
        "name": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListScrapersRequestListScrapersPaginateTypeDef = TypedDict(
    "ListScrapersRequestListScrapersPaginateTypeDef",
    {
        "filters": NotRequired[Mapping[str, Sequence[str]]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListWorkspacesRequestListWorkspacesPaginateTypeDef = TypedDict(
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    {
        "alias": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeAlertManagerDefinitionResponseTypeDef = TypedDict(
    "DescribeAlertManagerDefinitionResponseTypeDef",
    {
        "alertManagerDefinition": AlertManagerDefinitionDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateScraperRequestRequestTypeDef = TypedDict(
    "UpdateScraperRequestRequestTypeDef",
    {
        "scraperId": str,
        "alias": NotRequired[str],
        "clientToken": NotRequired[str],
        "destination": NotRequired[DestinationTypeDef],
        "scrapeConfiguration": NotRequired[ScrapeConfigurationTypeDef],
    },
)
DescribeLoggingConfigurationResponseTypeDef = TypedDict(
    "DescribeLoggingConfigurationResponseTypeDef",
    {
        "loggingConfiguration": LoggingConfigurationMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeRuleGroupsNamespaceResponseTypeDef = TypedDict(
    "DescribeRuleGroupsNamespaceResponseTypeDef",
    {
        "ruleGroupsNamespace": RuleGroupsNamespaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListRuleGroupsNamespacesResponseTypeDef = TypedDict(
    "ListRuleGroupsNamespacesResponseTypeDef",
    {
        "ruleGroupsNamespaces": List[RuleGroupsNamespaceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
DescribeWorkspaceResponseTypeDef = TypedDict(
    "DescribeWorkspaceResponseTypeDef",
    {
        "workspace": WorkspaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListWorkspacesResponseTypeDef = TypedDict(
    "ListWorkspacesResponseTypeDef",
    {
        "workspaces": List[WorkspaceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
ScraperDescriptionTypeDef = TypedDict(
    "ScraperDescriptionTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "destination": DestinationTypeDef,
        "lastModifiedAt": datetime,
        "roleArn": str,
        "scrapeConfiguration": ScrapeConfigurationOutputTypeDef,
        "scraperId": str,
        "source": SourceOutputTypeDef,
        "status": ScraperStatusTypeDef,
        "alias": NotRequired[str],
        "statusReason": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
ScraperSummaryTypeDef = TypedDict(
    "ScraperSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "destination": DestinationTypeDef,
        "lastModifiedAt": datetime,
        "roleArn": str,
        "scraperId": str,
        "source": SourceOutputTypeDef,
        "status": ScraperStatusTypeDef,
        "alias": NotRequired[str],
        "statusReason": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
SourceTypeDef = TypedDict(
    "SourceTypeDef",
    {
        "eksConfiguration": NotRequired[EksConfigurationUnionTypeDef],
    },
)
DescribeScraperResponseTypeDef = TypedDict(
    "DescribeScraperResponseTypeDef",
    {
        "scraper": ScraperDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListScrapersResponseTypeDef = TypedDict(
    "ListScrapersResponseTypeDef",
    {
        "scrapers": List[ScraperSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
CreateScraperRequestRequestTypeDef = TypedDict(
    "CreateScraperRequestRequestTypeDef",
    {
        "destination": DestinationTypeDef,
        "scrapeConfiguration": ScrapeConfigurationTypeDef,
        "source": SourceTypeDef,
        "alias": NotRequired[str],
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
