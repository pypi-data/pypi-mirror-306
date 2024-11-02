"""
Type annotations for appsync service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appsync/type_defs/)

Usage::

    ```python
    from mypy_boto3_appsync.type_defs import CognitoUserPoolConfigTypeDef

    data: CognitoUserPoolConfigTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ApiCacheStatusType,
    ApiCacheTypeType,
    ApiCachingBehaviorType,
    AssociationStatusType,
    AuthenticationTypeType,
    CacheHealthMetricsConfigType,
    ConflictDetectionTypeType,
    ConflictHandlerTypeType,
    DataSourceIntrospectionStatusType,
    DataSourceLevelMetricsBehaviorType,
    DataSourceLevelMetricsConfigType,
    DataSourceTypeType,
    DefaultActionType,
    EventLogLevelType,
    FieldLogLevelType,
    GraphQLApiIntrospectionConfigType,
    GraphQLApiTypeType,
    GraphQLApiVisibilityType,
    MergeTypeType,
    OperationLevelMetricsConfigType,
    OutputTypeType,
    OwnershipType,
    ResolverKindType,
    ResolverLevelMetricsBehaviorType,
    ResolverLevelMetricsConfigType,
    SchemaStatusType,
    SourceApiAssociationStatusType,
    TypeDefinitionFormatType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CognitoUserPoolConfigTypeDef",
    "LambdaAuthorizerConfigTypeDef",
    "OpenIDConnectConfigTypeDef",
    "ApiAssociationTypeDef",
    "ApiCacheTypeDef",
    "ApiKeyTypeDef",
    "AppSyncRuntimeTypeDef",
    "AssociateApiRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SourceApiAssociationConfigTypeDef",
    "AuthModeTypeDef",
    "CognitoConfigTypeDef",
    "AwsIamConfigTypeDef",
    "BlobTypeDef",
    "CachingConfigOutputTypeDef",
    "CachingConfigTypeDef",
    "CodeErrorLocationTypeDef",
    "CreateApiCacheRequestRequestTypeDef",
    "CreateApiKeyRequestRequestTypeDef",
    "ElasticsearchDataSourceConfigTypeDef",
    "EventBridgeDataSourceConfigTypeDef",
    "LambdaDataSourceConfigTypeDef",
    "OpenSearchServiceDataSourceConfigTypeDef",
    "CreateDomainNameRequestRequestTypeDef",
    "DomainNameConfigTypeDef",
    "EnhancedMetricsConfigTypeDef",
    "LogConfigTypeDef",
    "UserPoolConfigTypeDef",
    "PipelineConfigTypeDef",
    "CreateTypeRequestRequestTypeDef",
    "TypeTypeDef",
    "DataSourceIntrospectionModelFieldTypeTypeDef",
    "DataSourceIntrospectionModelIndexTypeDef",
    "DeleteApiCacheRequestRequestTypeDef",
    "DeleteApiKeyRequestRequestTypeDef",
    "DeleteApiRequestRequestTypeDef",
    "DeleteChannelNamespaceRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteDomainNameRequestRequestTypeDef",
    "DeleteFunctionRequestRequestTypeDef",
    "DeleteGraphqlApiRequestRequestTypeDef",
    "DeleteResolverRequestRequestTypeDef",
    "DeleteTypeRequestRequestTypeDef",
    "DeltaSyncConfigTypeDef",
    "DisassociateApiRequestRequestTypeDef",
    "DisassociateMergedGraphqlApiRequestRequestTypeDef",
    "DisassociateSourceGraphqlApiRequestRequestTypeDef",
    "ErrorDetailTypeDef",
    "EvaluateMappingTemplateRequestRequestTypeDef",
    "EventLogConfigTypeDef",
    "FlushApiCacheRequestRequestTypeDef",
    "GetApiAssociationRequestRequestTypeDef",
    "GetApiCacheRequestRequestTypeDef",
    "GetApiRequestRequestTypeDef",
    "GetChannelNamespaceRequestRequestTypeDef",
    "GetDataSourceIntrospectionRequestRequestTypeDef",
    "GetDataSourceRequestRequestTypeDef",
    "GetDomainNameRequestRequestTypeDef",
    "GetFunctionRequestRequestTypeDef",
    "GetGraphqlApiEnvironmentVariablesRequestRequestTypeDef",
    "GetGraphqlApiRequestRequestTypeDef",
    "GetIntrospectionSchemaRequestRequestTypeDef",
    "GetResolverRequestRequestTypeDef",
    "GetSchemaCreationStatusRequestRequestTypeDef",
    "GetSourceApiAssociationRequestRequestTypeDef",
    "GetTypeRequestRequestTypeDef",
    "LambdaConflictHandlerConfigTypeDef",
    "PaginatorConfigTypeDef",
    "ListApiKeysRequestRequestTypeDef",
    "ListApisRequestRequestTypeDef",
    "ListChannelNamespacesRequestRequestTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListDomainNamesRequestRequestTypeDef",
    "ListFunctionsRequestRequestTypeDef",
    "ListGraphqlApisRequestRequestTypeDef",
    "ListResolversByFunctionRequestRequestTypeDef",
    "ListResolversRequestRequestTypeDef",
    "ListSourceApiAssociationsRequestRequestTypeDef",
    "SourceApiAssociationSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTypesByAssociationRequestRequestTypeDef",
    "ListTypesRequestRequestTypeDef",
    "PipelineConfigOutputTypeDef",
    "PutGraphqlApiEnvironmentVariablesRequestRequestTypeDef",
    "RdsDataApiConfigTypeDef",
    "RdsHttpEndpointConfigTypeDef",
    "StartSchemaMergeRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApiCacheRequestRequestTypeDef",
    "UpdateApiKeyRequestRequestTypeDef",
    "UpdateDomainNameRequestRequestTypeDef",
    "UpdateTypeRequestRequestTypeDef",
    "AdditionalAuthenticationProviderTypeDef",
    "EvaluateCodeRequestRequestTypeDef",
    "AssociateApiResponseTypeDef",
    "CreateApiCacheResponseTypeDef",
    "CreateApiKeyResponseTypeDef",
    "DisassociateMergedGraphqlApiResponseTypeDef",
    "DisassociateSourceGraphqlApiResponseTypeDef",
    "GetApiAssociationResponseTypeDef",
    "GetApiCacheResponseTypeDef",
    "GetGraphqlApiEnvironmentVariablesResponseTypeDef",
    "GetIntrospectionSchemaResponseTypeDef",
    "GetSchemaCreationStatusResponseTypeDef",
    "ListApiKeysResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutGraphqlApiEnvironmentVariablesResponseTypeDef",
    "StartDataSourceIntrospectionResponseTypeDef",
    "StartSchemaCreationResponseTypeDef",
    "StartSchemaMergeResponseTypeDef",
    "UpdateApiCacheResponseTypeDef",
    "UpdateApiKeyResponseTypeDef",
    "AssociateMergedGraphqlApiRequestRequestTypeDef",
    "AssociateSourceGraphqlApiRequestRequestTypeDef",
    "SourceApiAssociationTypeDef",
    "UpdateSourceApiAssociationRequestRequestTypeDef",
    "ChannelNamespaceTypeDef",
    "CreateChannelNamespaceRequestRequestTypeDef",
    "UpdateChannelNamespaceRequestRequestTypeDef",
    "AuthProviderTypeDef",
    "AuthorizationConfigTypeDef",
    "StartSchemaCreationRequestRequestTypeDef",
    "CodeErrorTypeDef",
    "CreateDomainNameResponseTypeDef",
    "GetDomainNameResponseTypeDef",
    "ListDomainNamesResponseTypeDef",
    "UpdateDomainNameResponseTypeDef",
    "CreateTypeResponseTypeDef",
    "GetTypeResponseTypeDef",
    "ListTypesByAssociationResponseTypeDef",
    "ListTypesResponseTypeDef",
    "UpdateTypeResponseTypeDef",
    "DataSourceIntrospectionModelFieldTypeDef",
    "DynamodbDataSourceConfigTypeDef",
    "EvaluateMappingTemplateResponseTypeDef",
    "SyncConfigTypeDef",
    "ListApiKeysRequestListApiKeysPaginateTypeDef",
    "ListApisRequestListApisPaginateTypeDef",
    "ListChannelNamespacesRequestListChannelNamespacesPaginateTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListDomainNamesRequestListDomainNamesPaginateTypeDef",
    "ListFunctionsRequestListFunctionsPaginateTypeDef",
    "ListGraphqlApisRequestListGraphqlApisPaginateTypeDef",
    "ListResolversByFunctionRequestListResolversByFunctionPaginateTypeDef",
    "ListResolversRequestListResolversPaginateTypeDef",
    "ListSourceApiAssociationsRequestListSourceApiAssociationsPaginateTypeDef",
    "ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef",
    "ListTypesRequestListTypesPaginateTypeDef",
    "ListSourceApiAssociationsResponseTypeDef",
    "StartDataSourceIntrospectionRequestRequestTypeDef",
    "RelationalDatabaseDataSourceConfigTypeDef",
    "CreateGraphqlApiRequestRequestTypeDef",
    "GraphqlApiTypeDef",
    "UpdateGraphqlApiRequestRequestTypeDef",
    "AssociateMergedGraphqlApiResponseTypeDef",
    "AssociateSourceGraphqlApiResponseTypeDef",
    "GetSourceApiAssociationResponseTypeDef",
    "UpdateSourceApiAssociationResponseTypeDef",
    "CreateChannelNamespaceResponseTypeDef",
    "GetChannelNamespaceResponseTypeDef",
    "ListChannelNamespacesResponseTypeDef",
    "UpdateChannelNamespaceResponseTypeDef",
    "EventConfigOutputTypeDef",
    "EventConfigTypeDef",
    "HttpDataSourceConfigTypeDef",
    "EvaluateCodeErrorDetailTypeDef",
    "DataSourceIntrospectionModelTypeDef",
    "CreateFunctionRequestRequestTypeDef",
    "CreateResolverRequestRequestTypeDef",
    "FunctionConfigurationTypeDef",
    "ResolverTypeDef",
    "UpdateFunctionRequestRequestTypeDef",
    "UpdateResolverRequestRequestTypeDef",
    "CreateGraphqlApiResponseTypeDef",
    "GetGraphqlApiResponseTypeDef",
    "ListGraphqlApisResponseTypeDef",
    "UpdateGraphqlApiResponseTypeDef",
    "ApiTypeDef",
    "CreateApiRequestRequestTypeDef",
    "UpdateApiRequestRequestTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "DataSourceTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "EvaluateCodeResponseTypeDef",
    "DataSourceIntrospectionResultTypeDef",
    "CreateFunctionResponseTypeDef",
    "GetFunctionResponseTypeDef",
    "ListFunctionsResponseTypeDef",
    "UpdateFunctionResponseTypeDef",
    "CreateResolverResponseTypeDef",
    "GetResolverResponseTypeDef",
    "ListResolversByFunctionResponseTypeDef",
    "ListResolversResponseTypeDef",
    "UpdateResolverResponseTypeDef",
    "CreateApiResponseTypeDef",
    "GetApiResponseTypeDef",
    "ListApisResponseTypeDef",
    "UpdateApiResponseTypeDef",
    "CreateDataSourceResponseTypeDef",
    "GetDataSourceResponseTypeDef",
    "ListDataSourcesResponseTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "GetDataSourceIntrospectionResponseTypeDef",
)

CognitoUserPoolConfigTypeDef = TypedDict(
    "CognitoUserPoolConfigTypeDef",
    {
        "userPoolId": str,
        "awsRegion": str,
        "appIdClientRegex": NotRequired[str],
    },
)
LambdaAuthorizerConfigTypeDef = TypedDict(
    "LambdaAuthorizerConfigTypeDef",
    {
        "authorizerUri": str,
        "authorizerResultTtlInSeconds": NotRequired[int],
        "identityValidationExpression": NotRequired[str],
    },
)
OpenIDConnectConfigTypeDef = TypedDict(
    "OpenIDConnectConfigTypeDef",
    {
        "issuer": str,
        "clientId": NotRequired[str],
        "iatTTL": NotRequired[int],
        "authTTL": NotRequired[int],
    },
)
ApiAssociationTypeDef = TypedDict(
    "ApiAssociationTypeDef",
    {
        "domainName": NotRequired[str],
        "apiId": NotRequired[str],
        "associationStatus": NotRequired[AssociationStatusType],
        "deploymentDetail": NotRequired[str],
    },
)
ApiCacheTypeDef = TypedDict(
    "ApiCacheTypeDef",
    {
        "ttl": NotRequired[int],
        "apiCachingBehavior": NotRequired[ApiCachingBehaviorType],
        "transitEncryptionEnabled": NotRequired[bool],
        "atRestEncryptionEnabled": NotRequired[bool],
        "type": NotRequired[ApiCacheTypeType],
        "status": NotRequired[ApiCacheStatusType],
        "healthMetricsConfig": NotRequired[CacheHealthMetricsConfigType],
    },
)
ApiKeyTypeDef = TypedDict(
    "ApiKeyTypeDef",
    {
        "id": NotRequired[str],
        "description": NotRequired[str],
        "expires": NotRequired[int],
        "deletes": NotRequired[int],
    },
)
AppSyncRuntimeTypeDef = TypedDict(
    "AppSyncRuntimeTypeDef",
    {
        "name": Literal["APPSYNC_JS"],
        "runtimeVersion": str,
    },
)
AssociateApiRequestRequestTypeDef = TypedDict(
    "AssociateApiRequestRequestTypeDef",
    {
        "domainName": str,
        "apiId": str,
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
SourceApiAssociationConfigTypeDef = TypedDict(
    "SourceApiAssociationConfigTypeDef",
    {
        "mergeType": NotRequired[MergeTypeType],
    },
)
AuthModeTypeDef = TypedDict(
    "AuthModeTypeDef",
    {
        "authType": AuthenticationTypeType,
    },
)
CognitoConfigTypeDef = TypedDict(
    "CognitoConfigTypeDef",
    {
        "userPoolId": str,
        "awsRegion": str,
        "appIdClientRegex": NotRequired[str],
    },
)
AwsIamConfigTypeDef = TypedDict(
    "AwsIamConfigTypeDef",
    {
        "signingRegion": NotRequired[str],
        "signingServiceName": NotRequired[str],
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
CachingConfigOutputTypeDef = TypedDict(
    "CachingConfigOutputTypeDef",
    {
        "ttl": int,
        "cachingKeys": NotRequired[List[str]],
    },
)
CachingConfigTypeDef = TypedDict(
    "CachingConfigTypeDef",
    {
        "ttl": int,
        "cachingKeys": NotRequired[Sequence[str]],
    },
)
CodeErrorLocationTypeDef = TypedDict(
    "CodeErrorLocationTypeDef",
    {
        "line": NotRequired[int],
        "column": NotRequired[int],
        "span": NotRequired[int],
    },
)
CreateApiCacheRequestRequestTypeDef = TypedDict(
    "CreateApiCacheRequestRequestTypeDef",
    {
        "apiId": str,
        "ttl": int,
        "apiCachingBehavior": ApiCachingBehaviorType,
        "type": ApiCacheTypeType,
        "transitEncryptionEnabled": NotRequired[bool],
        "atRestEncryptionEnabled": NotRequired[bool],
        "healthMetricsConfig": NotRequired[CacheHealthMetricsConfigType],
    },
)
CreateApiKeyRequestRequestTypeDef = TypedDict(
    "CreateApiKeyRequestRequestTypeDef",
    {
        "apiId": str,
        "description": NotRequired[str],
        "expires": NotRequired[int],
    },
)
ElasticsearchDataSourceConfigTypeDef = TypedDict(
    "ElasticsearchDataSourceConfigTypeDef",
    {
        "endpoint": str,
        "awsRegion": str,
    },
)
EventBridgeDataSourceConfigTypeDef = TypedDict(
    "EventBridgeDataSourceConfigTypeDef",
    {
        "eventBusArn": str,
    },
)
LambdaDataSourceConfigTypeDef = TypedDict(
    "LambdaDataSourceConfigTypeDef",
    {
        "lambdaFunctionArn": str,
    },
)
OpenSearchServiceDataSourceConfigTypeDef = TypedDict(
    "OpenSearchServiceDataSourceConfigTypeDef",
    {
        "endpoint": str,
        "awsRegion": str,
    },
)
CreateDomainNameRequestRequestTypeDef = TypedDict(
    "CreateDomainNameRequestRequestTypeDef",
    {
        "domainName": str,
        "certificateArn": str,
        "description": NotRequired[str],
    },
)
DomainNameConfigTypeDef = TypedDict(
    "DomainNameConfigTypeDef",
    {
        "domainName": NotRequired[str],
        "description": NotRequired[str],
        "certificateArn": NotRequired[str],
        "appsyncDomainName": NotRequired[str],
        "hostedZoneId": NotRequired[str],
    },
)
EnhancedMetricsConfigTypeDef = TypedDict(
    "EnhancedMetricsConfigTypeDef",
    {
        "resolverLevelMetricsBehavior": ResolverLevelMetricsBehaviorType,
        "dataSourceLevelMetricsBehavior": DataSourceLevelMetricsBehaviorType,
        "operationLevelMetricsConfig": OperationLevelMetricsConfigType,
    },
)
LogConfigTypeDef = TypedDict(
    "LogConfigTypeDef",
    {
        "fieldLogLevel": FieldLogLevelType,
        "cloudWatchLogsRoleArn": str,
        "excludeVerboseContent": NotRequired[bool],
    },
)
UserPoolConfigTypeDef = TypedDict(
    "UserPoolConfigTypeDef",
    {
        "userPoolId": str,
        "awsRegion": str,
        "defaultAction": DefaultActionType,
        "appIdClientRegex": NotRequired[str],
    },
)
PipelineConfigTypeDef = TypedDict(
    "PipelineConfigTypeDef",
    {
        "functions": NotRequired[Sequence[str]],
    },
)
CreateTypeRequestRequestTypeDef = TypedDict(
    "CreateTypeRequestRequestTypeDef",
    {
        "apiId": str,
        "definition": str,
        "format": TypeDefinitionFormatType,
    },
)
TypeTypeDef = TypedDict(
    "TypeTypeDef",
    {
        "name": NotRequired[str],
        "description": NotRequired[str],
        "arn": NotRequired[str],
        "definition": NotRequired[str],
        "format": NotRequired[TypeDefinitionFormatType],
    },
)
DataSourceIntrospectionModelFieldTypeTypeDef = TypedDict(
    "DataSourceIntrospectionModelFieldTypeTypeDef",
    {
        "kind": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[Dict[str, Any]],
        "values": NotRequired[List[str]],
    },
)
DataSourceIntrospectionModelIndexTypeDef = TypedDict(
    "DataSourceIntrospectionModelIndexTypeDef",
    {
        "name": NotRequired[str],
        "fields": NotRequired[List[str]],
    },
)
DeleteApiCacheRequestRequestTypeDef = TypedDict(
    "DeleteApiCacheRequestRequestTypeDef",
    {
        "apiId": str,
    },
)
DeleteApiKeyRequestRequestTypeDef = TypedDict(
    "DeleteApiKeyRequestRequestTypeDef",
    {
        "apiId": str,
        "id": str,
    },
)
DeleteApiRequestRequestTypeDef = TypedDict(
    "DeleteApiRequestRequestTypeDef",
    {
        "apiId": str,
    },
)
DeleteChannelNamespaceRequestRequestTypeDef = TypedDict(
    "DeleteChannelNamespaceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
    },
)
DeleteDataSourceRequestRequestTypeDef = TypedDict(
    "DeleteDataSourceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
    },
)
DeleteDomainNameRequestRequestTypeDef = TypedDict(
    "DeleteDomainNameRequestRequestTypeDef",
    {
        "domainName": str,
    },
)
DeleteFunctionRequestRequestTypeDef = TypedDict(
    "DeleteFunctionRequestRequestTypeDef",
    {
        "apiId": str,
        "functionId": str,
    },
)
DeleteGraphqlApiRequestRequestTypeDef = TypedDict(
    "DeleteGraphqlApiRequestRequestTypeDef",
    {
        "apiId": str,
    },
)
DeleteResolverRequestRequestTypeDef = TypedDict(
    "DeleteResolverRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "fieldName": str,
    },
)
DeleteTypeRequestRequestTypeDef = TypedDict(
    "DeleteTypeRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
    },
)
DeltaSyncConfigTypeDef = TypedDict(
    "DeltaSyncConfigTypeDef",
    {
        "baseTableTTL": NotRequired[int],
        "deltaSyncTableName": NotRequired[str],
        "deltaSyncTableTTL": NotRequired[int],
    },
)
DisassociateApiRequestRequestTypeDef = TypedDict(
    "DisassociateApiRequestRequestTypeDef",
    {
        "domainName": str,
    },
)
DisassociateMergedGraphqlApiRequestRequestTypeDef = TypedDict(
    "DisassociateMergedGraphqlApiRequestRequestTypeDef",
    {
        "sourceApiIdentifier": str,
        "associationId": str,
    },
)
DisassociateSourceGraphqlApiRequestRequestTypeDef = TypedDict(
    "DisassociateSourceGraphqlApiRequestRequestTypeDef",
    {
        "mergedApiIdentifier": str,
        "associationId": str,
    },
)
ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef",
    {
        "message": NotRequired[str],
    },
)
EvaluateMappingTemplateRequestRequestTypeDef = TypedDict(
    "EvaluateMappingTemplateRequestRequestTypeDef",
    {
        "template": str,
        "context": str,
    },
)
EventLogConfigTypeDef = TypedDict(
    "EventLogConfigTypeDef",
    {
        "logLevel": EventLogLevelType,
        "cloudWatchLogsRoleArn": str,
    },
)
FlushApiCacheRequestRequestTypeDef = TypedDict(
    "FlushApiCacheRequestRequestTypeDef",
    {
        "apiId": str,
    },
)
GetApiAssociationRequestRequestTypeDef = TypedDict(
    "GetApiAssociationRequestRequestTypeDef",
    {
        "domainName": str,
    },
)
GetApiCacheRequestRequestTypeDef = TypedDict(
    "GetApiCacheRequestRequestTypeDef",
    {
        "apiId": str,
    },
)
GetApiRequestRequestTypeDef = TypedDict(
    "GetApiRequestRequestTypeDef",
    {
        "apiId": str,
    },
)
GetChannelNamespaceRequestRequestTypeDef = TypedDict(
    "GetChannelNamespaceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
    },
)
GetDataSourceIntrospectionRequestRequestTypeDef = TypedDict(
    "GetDataSourceIntrospectionRequestRequestTypeDef",
    {
        "introspectionId": str,
        "includeModelsSDL": NotRequired[bool],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
GetDataSourceRequestRequestTypeDef = TypedDict(
    "GetDataSourceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
    },
)
GetDomainNameRequestRequestTypeDef = TypedDict(
    "GetDomainNameRequestRequestTypeDef",
    {
        "domainName": str,
    },
)
GetFunctionRequestRequestTypeDef = TypedDict(
    "GetFunctionRequestRequestTypeDef",
    {
        "apiId": str,
        "functionId": str,
    },
)
GetGraphqlApiEnvironmentVariablesRequestRequestTypeDef = TypedDict(
    "GetGraphqlApiEnvironmentVariablesRequestRequestTypeDef",
    {
        "apiId": str,
    },
)
GetGraphqlApiRequestRequestTypeDef = TypedDict(
    "GetGraphqlApiRequestRequestTypeDef",
    {
        "apiId": str,
    },
)
GetIntrospectionSchemaRequestRequestTypeDef = TypedDict(
    "GetIntrospectionSchemaRequestRequestTypeDef",
    {
        "apiId": str,
        "format": OutputTypeType,
        "includeDirectives": NotRequired[bool],
    },
)
GetResolverRequestRequestTypeDef = TypedDict(
    "GetResolverRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "fieldName": str,
    },
)
GetSchemaCreationStatusRequestRequestTypeDef = TypedDict(
    "GetSchemaCreationStatusRequestRequestTypeDef",
    {
        "apiId": str,
    },
)
GetSourceApiAssociationRequestRequestTypeDef = TypedDict(
    "GetSourceApiAssociationRequestRequestTypeDef",
    {
        "mergedApiIdentifier": str,
        "associationId": str,
    },
)
GetTypeRequestRequestTypeDef = TypedDict(
    "GetTypeRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "format": TypeDefinitionFormatType,
    },
)
LambdaConflictHandlerConfigTypeDef = TypedDict(
    "LambdaConflictHandlerConfigTypeDef",
    {
        "lambdaConflictHandlerArn": NotRequired[str],
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
ListApiKeysRequestRequestTypeDef = TypedDict(
    "ListApiKeysRequestRequestTypeDef",
    {
        "apiId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListApisRequestRequestTypeDef = TypedDict(
    "ListApisRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListChannelNamespacesRequestRequestTypeDef = TypedDict(
    "ListChannelNamespacesRequestRequestTypeDef",
    {
        "apiId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListDataSourcesRequestRequestTypeDef = TypedDict(
    "ListDataSourcesRequestRequestTypeDef",
    {
        "apiId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListDomainNamesRequestRequestTypeDef = TypedDict(
    "ListDomainNamesRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListFunctionsRequestRequestTypeDef = TypedDict(
    "ListFunctionsRequestRequestTypeDef",
    {
        "apiId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListGraphqlApisRequestRequestTypeDef = TypedDict(
    "ListGraphqlApisRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "apiType": NotRequired[GraphQLApiTypeType],
        "owner": NotRequired[OwnershipType],
    },
)
ListResolversByFunctionRequestRequestTypeDef = TypedDict(
    "ListResolversByFunctionRequestRequestTypeDef",
    {
        "apiId": str,
        "functionId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListResolversRequestRequestTypeDef = TypedDict(
    "ListResolversRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListSourceApiAssociationsRequestRequestTypeDef = TypedDict(
    "ListSourceApiAssociationsRequestRequestTypeDef",
    {
        "apiId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
SourceApiAssociationSummaryTypeDef = TypedDict(
    "SourceApiAssociationSummaryTypeDef",
    {
        "associationId": NotRequired[str],
        "associationArn": NotRequired[str],
        "sourceApiId": NotRequired[str],
        "sourceApiArn": NotRequired[str],
        "mergedApiId": NotRequired[str],
        "mergedApiArn": NotRequired[str],
        "description": NotRequired[str],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
ListTypesByAssociationRequestRequestTypeDef = TypedDict(
    "ListTypesByAssociationRequestRequestTypeDef",
    {
        "mergedApiIdentifier": str,
        "associationId": str,
        "format": TypeDefinitionFormatType,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListTypesRequestRequestTypeDef = TypedDict(
    "ListTypesRequestRequestTypeDef",
    {
        "apiId": str,
        "format": TypeDefinitionFormatType,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
PipelineConfigOutputTypeDef = TypedDict(
    "PipelineConfigOutputTypeDef",
    {
        "functions": NotRequired[List[str]],
    },
)
PutGraphqlApiEnvironmentVariablesRequestRequestTypeDef = TypedDict(
    "PutGraphqlApiEnvironmentVariablesRequestRequestTypeDef",
    {
        "apiId": str,
        "environmentVariables": Mapping[str, str],
    },
)
RdsDataApiConfigTypeDef = TypedDict(
    "RdsDataApiConfigTypeDef",
    {
        "resourceArn": str,
        "secretArn": str,
        "databaseName": str,
    },
)
RdsHttpEndpointConfigTypeDef = TypedDict(
    "RdsHttpEndpointConfigTypeDef",
    {
        "awsRegion": NotRequired[str],
        "dbClusterIdentifier": NotRequired[str],
        "databaseName": NotRequired[str],
        "schema": NotRequired[str],
        "awsSecretStoreArn": NotRequired[str],
    },
)
StartSchemaMergeRequestRequestTypeDef = TypedDict(
    "StartSchemaMergeRequestRequestTypeDef",
    {
        "associationId": str,
        "mergedApiIdentifier": str,
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
UpdateApiCacheRequestRequestTypeDef = TypedDict(
    "UpdateApiCacheRequestRequestTypeDef",
    {
        "apiId": str,
        "ttl": int,
        "apiCachingBehavior": ApiCachingBehaviorType,
        "type": ApiCacheTypeType,
        "healthMetricsConfig": NotRequired[CacheHealthMetricsConfigType],
    },
)
UpdateApiKeyRequestRequestTypeDef = TypedDict(
    "UpdateApiKeyRequestRequestTypeDef",
    {
        "apiId": str,
        "id": str,
        "description": NotRequired[str],
        "expires": NotRequired[int],
    },
)
UpdateDomainNameRequestRequestTypeDef = TypedDict(
    "UpdateDomainNameRequestRequestTypeDef",
    {
        "domainName": str,
        "description": NotRequired[str],
    },
)
UpdateTypeRequestRequestTypeDef = TypedDict(
    "UpdateTypeRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "format": TypeDefinitionFormatType,
        "definition": NotRequired[str],
    },
)
AdditionalAuthenticationProviderTypeDef = TypedDict(
    "AdditionalAuthenticationProviderTypeDef",
    {
        "authenticationType": NotRequired[AuthenticationTypeType],
        "openIDConnectConfig": NotRequired[OpenIDConnectConfigTypeDef],
        "userPoolConfig": NotRequired[CognitoUserPoolConfigTypeDef],
        "lambdaAuthorizerConfig": NotRequired[LambdaAuthorizerConfigTypeDef],
    },
)
EvaluateCodeRequestRequestTypeDef = TypedDict(
    "EvaluateCodeRequestRequestTypeDef",
    {
        "runtime": AppSyncRuntimeTypeDef,
        "code": str,
        "context": str,
        "function": NotRequired[str],
    },
)
AssociateApiResponseTypeDef = TypedDict(
    "AssociateApiResponseTypeDef",
    {
        "apiAssociation": ApiAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateApiCacheResponseTypeDef = TypedDict(
    "CreateApiCacheResponseTypeDef",
    {
        "apiCache": ApiCacheTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateApiKeyResponseTypeDef = TypedDict(
    "CreateApiKeyResponseTypeDef",
    {
        "apiKey": ApiKeyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DisassociateMergedGraphqlApiResponseTypeDef = TypedDict(
    "DisassociateMergedGraphqlApiResponseTypeDef",
    {
        "sourceApiAssociationStatus": SourceApiAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DisassociateSourceGraphqlApiResponseTypeDef = TypedDict(
    "DisassociateSourceGraphqlApiResponseTypeDef",
    {
        "sourceApiAssociationStatus": SourceApiAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetApiAssociationResponseTypeDef = TypedDict(
    "GetApiAssociationResponseTypeDef",
    {
        "apiAssociation": ApiAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetApiCacheResponseTypeDef = TypedDict(
    "GetApiCacheResponseTypeDef",
    {
        "apiCache": ApiCacheTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGraphqlApiEnvironmentVariablesResponseTypeDef = TypedDict(
    "GetGraphqlApiEnvironmentVariablesResponseTypeDef",
    {
        "environmentVariables": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetIntrospectionSchemaResponseTypeDef = TypedDict(
    "GetIntrospectionSchemaResponseTypeDef",
    {
        "schema": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSchemaCreationStatusResponseTypeDef = TypedDict(
    "GetSchemaCreationStatusResponseTypeDef",
    {
        "status": SchemaStatusType,
        "details": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListApiKeysResponseTypeDef = TypedDict(
    "ListApiKeysResponseTypeDef",
    {
        "apiKeys": List[ApiKeyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutGraphqlApiEnvironmentVariablesResponseTypeDef = TypedDict(
    "PutGraphqlApiEnvironmentVariablesResponseTypeDef",
    {
        "environmentVariables": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartDataSourceIntrospectionResponseTypeDef = TypedDict(
    "StartDataSourceIntrospectionResponseTypeDef",
    {
        "introspectionId": str,
        "introspectionStatus": DataSourceIntrospectionStatusType,
        "introspectionStatusDetail": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartSchemaCreationResponseTypeDef = TypedDict(
    "StartSchemaCreationResponseTypeDef",
    {
        "status": SchemaStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartSchemaMergeResponseTypeDef = TypedDict(
    "StartSchemaMergeResponseTypeDef",
    {
        "sourceApiAssociationStatus": SourceApiAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateApiCacheResponseTypeDef = TypedDict(
    "UpdateApiCacheResponseTypeDef",
    {
        "apiCache": ApiCacheTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateApiKeyResponseTypeDef = TypedDict(
    "UpdateApiKeyResponseTypeDef",
    {
        "apiKey": ApiKeyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AssociateMergedGraphqlApiRequestRequestTypeDef = TypedDict(
    "AssociateMergedGraphqlApiRequestRequestTypeDef",
    {
        "sourceApiIdentifier": str,
        "mergedApiIdentifier": str,
        "description": NotRequired[str],
        "sourceApiAssociationConfig": NotRequired[SourceApiAssociationConfigTypeDef],
    },
)
AssociateSourceGraphqlApiRequestRequestTypeDef = TypedDict(
    "AssociateSourceGraphqlApiRequestRequestTypeDef",
    {
        "mergedApiIdentifier": str,
        "sourceApiIdentifier": str,
        "description": NotRequired[str],
        "sourceApiAssociationConfig": NotRequired[SourceApiAssociationConfigTypeDef],
    },
)
SourceApiAssociationTypeDef = TypedDict(
    "SourceApiAssociationTypeDef",
    {
        "associationId": NotRequired[str],
        "associationArn": NotRequired[str],
        "sourceApiId": NotRequired[str],
        "sourceApiArn": NotRequired[str],
        "mergedApiArn": NotRequired[str],
        "mergedApiId": NotRequired[str],
        "description": NotRequired[str],
        "sourceApiAssociationConfig": NotRequired[SourceApiAssociationConfigTypeDef],
        "sourceApiAssociationStatus": NotRequired[SourceApiAssociationStatusType],
        "sourceApiAssociationStatusDetail": NotRequired[str],
        "lastSuccessfulMergeDate": NotRequired[datetime],
    },
)
UpdateSourceApiAssociationRequestRequestTypeDef = TypedDict(
    "UpdateSourceApiAssociationRequestRequestTypeDef",
    {
        "associationId": str,
        "mergedApiIdentifier": str,
        "description": NotRequired[str],
        "sourceApiAssociationConfig": NotRequired[SourceApiAssociationConfigTypeDef],
    },
)
ChannelNamespaceTypeDef = TypedDict(
    "ChannelNamespaceTypeDef",
    {
        "apiId": NotRequired[str],
        "name": NotRequired[str],
        "subscribeAuthModes": NotRequired[List[AuthModeTypeDef]],
        "publishAuthModes": NotRequired[List[AuthModeTypeDef]],
        "codeHandlers": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "channelNamespaceArn": NotRequired[str],
        "created": NotRequired[datetime],
        "lastModified": NotRequired[datetime],
    },
)
CreateChannelNamespaceRequestRequestTypeDef = TypedDict(
    "CreateChannelNamespaceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "subscribeAuthModes": NotRequired[Sequence[AuthModeTypeDef]],
        "publishAuthModes": NotRequired[Sequence[AuthModeTypeDef]],
        "codeHandlers": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateChannelNamespaceRequestRequestTypeDef = TypedDict(
    "UpdateChannelNamespaceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "subscribeAuthModes": NotRequired[Sequence[AuthModeTypeDef]],
        "publishAuthModes": NotRequired[Sequence[AuthModeTypeDef]],
        "codeHandlers": NotRequired[str],
    },
)
AuthProviderTypeDef = TypedDict(
    "AuthProviderTypeDef",
    {
        "authType": AuthenticationTypeType,
        "cognitoConfig": NotRequired[CognitoConfigTypeDef],
        "openIDConnectConfig": NotRequired[OpenIDConnectConfigTypeDef],
        "lambdaAuthorizerConfig": NotRequired[LambdaAuthorizerConfigTypeDef],
    },
)
AuthorizationConfigTypeDef = TypedDict(
    "AuthorizationConfigTypeDef",
    {
        "authorizationType": Literal["AWS_IAM"],
        "awsIamConfig": NotRequired[AwsIamConfigTypeDef],
    },
)
StartSchemaCreationRequestRequestTypeDef = TypedDict(
    "StartSchemaCreationRequestRequestTypeDef",
    {
        "apiId": str,
        "definition": BlobTypeDef,
    },
)
CodeErrorTypeDef = TypedDict(
    "CodeErrorTypeDef",
    {
        "errorType": NotRequired[str],
        "value": NotRequired[str],
        "location": NotRequired[CodeErrorLocationTypeDef],
    },
)
CreateDomainNameResponseTypeDef = TypedDict(
    "CreateDomainNameResponseTypeDef",
    {
        "domainNameConfig": DomainNameConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDomainNameResponseTypeDef = TypedDict(
    "GetDomainNameResponseTypeDef",
    {
        "domainNameConfig": DomainNameConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDomainNamesResponseTypeDef = TypedDict(
    "ListDomainNamesResponseTypeDef",
    {
        "domainNameConfigs": List[DomainNameConfigTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
UpdateDomainNameResponseTypeDef = TypedDict(
    "UpdateDomainNameResponseTypeDef",
    {
        "domainNameConfig": DomainNameConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateTypeResponseTypeDef = TypedDict(
    "CreateTypeResponseTypeDef",
    {
        "type": TypeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTypeResponseTypeDef = TypedDict(
    "GetTypeResponseTypeDef",
    {
        "type": TypeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTypesByAssociationResponseTypeDef = TypedDict(
    "ListTypesByAssociationResponseTypeDef",
    {
        "types": List[TypeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
ListTypesResponseTypeDef = TypedDict(
    "ListTypesResponseTypeDef",
    {
        "types": List[TypeTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
UpdateTypeResponseTypeDef = TypedDict(
    "UpdateTypeResponseTypeDef",
    {
        "type": TypeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataSourceIntrospectionModelFieldTypeDef = TypedDict(
    "DataSourceIntrospectionModelFieldTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[DataSourceIntrospectionModelFieldTypeTypeDef],
        "length": NotRequired[int],
    },
)
DynamodbDataSourceConfigTypeDef = TypedDict(
    "DynamodbDataSourceConfigTypeDef",
    {
        "tableName": str,
        "awsRegion": str,
        "useCallerCredentials": NotRequired[bool],
        "deltaSyncConfig": NotRequired[DeltaSyncConfigTypeDef],
        "versioned": NotRequired[bool],
    },
)
EvaluateMappingTemplateResponseTypeDef = TypedDict(
    "EvaluateMappingTemplateResponseTypeDef",
    {
        "evaluationResult": str,
        "error": ErrorDetailTypeDef,
        "logs": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SyncConfigTypeDef = TypedDict(
    "SyncConfigTypeDef",
    {
        "conflictHandler": NotRequired[ConflictHandlerTypeType],
        "conflictDetection": NotRequired[ConflictDetectionTypeType],
        "lambdaConflictHandlerConfig": NotRequired[LambdaConflictHandlerConfigTypeDef],
    },
)
ListApiKeysRequestListApiKeysPaginateTypeDef = TypedDict(
    "ListApiKeysRequestListApiKeysPaginateTypeDef",
    {
        "apiId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListApisRequestListApisPaginateTypeDef = TypedDict(
    "ListApisRequestListApisPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListChannelNamespacesRequestListChannelNamespacesPaginateTypeDef = TypedDict(
    "ListChannelNamespacesRequestListChannelNamespacesPaginateTypeDef",
    {
        "apiId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListDataSourcesRequestListDataSourcesPaginateTypeDef = TypedDict(
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    {
        "apiId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListDomainNamesRequestListDomainNamesPaginateTypeDef = TypedDict(
    "ListDomainNamesRequestListDomainNamesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFunctionsRequestListFunctionsPaginateTypeDef = TypedDict(
    "ListFunctionsRequestListFunctionsPaginateTypeDef",
    {
        "apiId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListGraphqlApisRequestListGraphqlApisPaginateTypeDef = TypedDict(
    "ListGraphqlApisRequestListGraphqlApisPaginateTypeDef",
    {
        "apiType": NotRequired[GraphQLApiTypeType],
        "owner": NotRequired[OwnershipType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListResolversByFunctionRequestListResolversByFunctionPaginateTypeDef = TypedDict(
    "ListResolversByFunctionRequestListResolversByFunctionPaginateTypeDef",
    {
        "apiId": str,
        "functionId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListResolversRequestListResolversPaginateTypeDef = TypedDict(
    "ListResolversRequestListResolversPaginateTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSourceApiAssociationsRequestListSourceApiAssociationsPaginateTypeDef = TypedDict(
    "ListSourceApiAssociationsRequestListSourceApiAssociationsPaginateTypeDef",
    {
        "apiId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef = TypedDict(
    "ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef",
    {
        "mergedApiIdentifier": str,
        "associationId": str,
        "format": TypeDefinitionFormatType,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTypesRequestListTypesPaginateTypeDef = TypedDict(
    "ListTypesRequestListTypesPaginateTypeDef",
    {
        "apiId": str,
        "format": TypeDefinitionFormatType,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSourceApiAssociationsResponseTypeDef = TypedDict(
    "ListSourceApiAssociationsResponseTypeDef",
    {
        "sourceApiAssociationSummaries": List[SourceApiAssociationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
StartDataSourceIntrospectionRequestRequestTypeDef = TypedDict(
    "StartDataSourceIntrospectionRequestRequestTypeDef",
    {
        "rdsDataApiConfig": NotRequired[RdsDataApiConfigTypeDef],
    },
)
RelationalDatabaseDataSourceConfigTypeDef = TypedDict(
    "RelationalDatabaseDataSourceConfigTypeDef",
    {
        "relationalDatabaseSourceType": NotRequired[Literal["RDS_HTTP_ENDPOINT"]],
        "rdsHttpEndpointConfig": NotRequired[RdsHttpEndpointConfigTypeDef],
    },
)
CreateGraphqlApiRequestRequestTypeDef = TypedDict(
    "CreateGraphqlApiRequestRequestTypeDef",
    {
        "name": str,
        "authenticationType": AuthenticationTypeType,
        "logConfig": NotRequired[LogConfigTypeDef],
        "userPoolConfig": NotRequired[UserPoolConfigTypeDef],
        "openIDConnectConfig": NotRequired[OpenIDConnectConfigTypeDef],
        "tags": NotRequired[Mapping[str, str]],
        "additionalAuthenticationProviders": NotRequired[
            Sequence[AdditionalAuthenticationProviderTypeDef]
        ],
        "xrayEnabled": NotRequired[bool],
        "lambdaAuthorizerConfig": NotRequired[LambdaAuthorizerConfigTypeDef],
        "apiType": NotRequired[GraphQLApiTypeType],
        "mergedApiExecutionRoleArn": NotRequired[str],
        "visibility": NotRequired[GraphQLApiVisibilityType],
        "ownerContact": NotRequired[str],
        "introspectionConfig": NotRequired[GraphQLApiIntrospectionConfigType],
        "queryDepthLimit": NotRequired[int],
        "resolverCountLimit": NotRequired[int],
        "enhancedMetricsConfig": NotRequired[EnhancedMetricsConfigTypeDef],
    },
)
GraphqlApiTypeDef = TypedDict(
    "GraphqlApiTypeDef",
    {
        "name": NotRequired[str],
        "apiId": NotRequired[str],
        "authenticationType": NotRequired[AuthenticationTypeType],
        "logConfig": NotRequired[LogConfigTypeDef],
        "userPoolConfig": NotRequired[UserPoolConfigTypeDef],
        "openIDConnectConfig": NotRequired[OpenIDConnectConfigTypeDef],
        "arn": NotRequired[str],
        "uris": NotRequired[Dict[str, str]],
        "tags": NotRequired[Dict[str, str]],
        "additionalAuthenticationProviders": NotRequired[
            List[AdditionalAuthenticationProviderTypeDef]
        ],
        "xrayEnabled": NotRequired[bool],
        "wafWebAclArn": NotRequired[str],
        "lambdaAuthorizerConfig": NotRequired[LambdaAuthorizerConfigTypeDef],
        "dns": NotRequired[Dict[str, str]],
        "visibility": NotRequired[GraphQLApiVisibilityType],
        "apiType": NotRequired[GraphQLApiTypeType],
        "mergedApiExecutionRoleArn": NotRequired[str],
        "owner": NotRequired[str],
        "ownerContact": NotRequired[str],
        "introspectionConfig": NotRequired[GraphQLApiIntrospectionConfigType],
        "queryDepthLimit": NotRequired[int],
        "resolverCountLimit": NotRequired[int],
        "enhancedMetricsConfig": NotRequired[EnhancedMetricsConfigTypeDef],
    },
)
UpdateGraphqlApiRequestRequestTypeDef = TypedDict(
    "UpdateGraphqlApiRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "logConfig": NotRequired[LogConfigTypeDef],
        "authenticationType": NotRequired[AuthenticationTypeType],
        "userPoolConfig": NotRequired[UserPoolConfigTypeDef],
        "openIDConnectConfig": NotRequired[OpenIDConnectConfigTypeDef],
        "additionalAuthenticationProviders": NotRequired[
            Sequence[AdditionalAuthenticationProviderTypeDef]
        ],
        "xrayEnabled": NotRequired[bool],
        "lambdaAuthorizerConfig": NotRequired[LambdaAuthorizerConfigTypeDef],
        "mergedApiExecutionRoleArn": NotRequired[str],
        "ownerContact": NotRequired[str],
        "introspectionConfig": NotRequired[GraphQLApiIntrospectionConfigType],
        "queryDepthLimit": NotRequired[int],
        "resolverCountLimit": NotRequired[int],
        "enhancedMetricsConfig": NotRequired[EnhancedMetricsConfigTypeDef],
    },
)
AssociateMergedGraphqlApiResponseTypeDef = TypedDict(
    "AssociateMergedGraphqlApiResponseTypeDef",
    {
        "sourceApiAssociation": SourceApiAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AssociateSourceGraphqlApiResponseTypeDef = TypedDict(
    "AssociateSourceGraphqlApiResponseTypeDef",
    {
        "sourceApiAssociation": SourceApiAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSourceApiAssociationResponseTypeDef = TypedDict(
    "GetSourceApiAssociationResponseTypeDef",
    {
        "sourceApiAssociation": SourceApiAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateSourceApiAssociationResponseTypeDef = TypedDict(
    "UpdateSourceApiAssociationResponseTypeDef",
    {
        "sourceApiAssociation": SourceApiAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateChannelNamespaceResponseTypeDef = TypedDict(
    "CreateChannelNamespaceResponseTypeDef",
    {
        "channelNamespace": ChannelNamespaceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetChannelNamespaceResponseTypeDef = TypedDict(
    "GetChannelNamespaceResponseTypeDef",
    {
        "channelNamespace": ChannelNamespaceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListChannelNamespacesResponseTypeDef = TypedDict(
    "ListChannelNamespacesResponseTypeDef",
    {
        "channelNamespaces": List[ChannelNamespaceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
UpdateChannelNamespaceResponseTypeDef = TypedDict(
    "UpdateChannelNamespaceResponseTypeDef",
    {
        "channelNamespace": ChannelNamespaceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EventConfigOutputTypeDef = TypedDict(
    "EventConfigOutputTypeDef",
    {
        "authProviders": List[AuthProviderTypeDef],
        "connectionAuthModes": List[AuthModeTypeDef],
        "defaultPublishAuthModes": List[AuthModeTypeDef],
        "defaultSubscribeAuthModes": List[AuthModeTypeDef],
        "logConfig": NotRequired[EventLogConfigTypeDef],
    },
)
EventConfigTypeDef = TypedDict(
    "EventConfigTypeDef",
    {
        "authProviders": Sequence[AuthProviderTypeDef],
        "connectionAuthModes": Sequence[AuthModeTypeDef],
        "defaultPublishAuthModes": Sequence[AuthModeTypeDef],
        "defaultSubscribeAuthModes": Sequence[AuthModeTypeDef],
        "logConfig": NotRequired[EventLogConfigTypeDef],
    },
)
HttpDataSourceConfigTypeDef = TypedDict(
    "HttpDataSourceConfigTypeDef",
    {
        "endpoint": NotRequired[str],
        "authorizationConfig": NotRequired[AuthorizationConfigTypeDef],
    },
)
EvaluateCodeErrorDetailTypeDef = TypedDict(
    "EvaluateCodeErrorDetailTypeDef",
    {
        "message": NotRequired[str],
        "codeErrors": NotRequired[List[CodeErrorTypeDef]],
    },
)
DataSourceIntrospectionModelTypeDef = TypedDict(
    "DataSourceIntrospectionModelTypeDef",
    {
        "name": NotRequired[str],
        "fields": NotRequired[List[DataSourceIntrospectionModelFieldTypeDef]],
        "primaryKey": NotRequired[DataSourceIntrospectionModelIndexTypeDef],
        "indexes": NotRequired[List[DataSourceIntrospectionModelIndexTypeDef]],
        "sdl": NotRequired[str],
    },
)
CreateFunctionRequestRequestTypeDef = TypedDict(
    "CreateFunctionRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "dataSourceName": str,
        "description": NotRequired[str],
        "requestMappingTemplate": NotRequired[str],
        "responseMappingTemplate": NotRequired[str],
        "functionVersion": NotRequired[str],
        "syncConfig": NotRequired[SyncConfigTypeDef],
        "maxBatchSize": NotRequired[int],
        "runtime": NotRequired[AppSyncRuntimeTypeDef],
        "code": NotRequired[str],
    },
)
CreateResolverRequestRequestTypeDef = TypedDict(
    "CreateResolverRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "fieldName": str,
        "dataSourceName": NotRequired[str],
        "requestMappingTemplate": NotRequired[str],
        "responseMappingTemplate": NotRequired[str],
        "kind": NotRequired[ResolverKindType],
        "pipelineConfig": NotRequired[PipelineConfigTypeDef],
        "syncConfig": NotRequired[SyncConfigTypeDef],
        "cachingConfig": NotRequired[CachingConfigTypeDef],
        "maxBatchSize": NotRequired[int],
        "runtime": NotRequired[AppSyncRuntimeTypeDef],
        "code": NotRequired[str],
        "metricsConfig": NotRequired[ResolverLevelMetricsConfigType],
    },
)
FunctionConfigurationTypeDef = TypedDict(
    "FunctionConfigurationTypeDef",
    {
        "functionId": NotRequired[str],
        "functionArn": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "dataSourceName": NotRequired[str],
        "requestMappingTemplate": NotRequired[str],
        "responseMappingTemplate": NotRequired[str],
        "functionVersion": NotRequired[str],
        "syncConfig": NotRequired[SyncConfigTypeDef],
        "maxBatchSize": NotRequired[int],
        "runtime": NotRequired[AppSyncRuntimeTypeDef],
        "code": NotRequired[str],
    },
)
ResolverTypeDef = TypedDict(
    "ResolverTypeDef",
    {
        "typeName": NotRequired[str],
        "fieldName": NotRequired[str],
        "dataSourceName": NotRequired[str],
        "resolverArn": NotRequired[str],
        "requestMappingTemplate": NotRequired[str],
        "responseMappingTemplate": NotRequired[str],
        "kind": NotRequired[ResolverKindType],
        "pipelineConfig": NotRequired[PipelineConfigOutputTypeDef],
        "syncConfig": NotRequired[SyncConfigTypeDef],
        "cachingConfig": NotRequired[CachingConfigOutputTypeDef],
        "maxBatchSize": NotRequired[int],
        "runtime": NotRequired[AppSyncRuntimeTypeDef],
        "code": NotRequired[str],
        "metricsConfig": NotRequired[ResolverLevelMetricsConfigType],
    },
)
UpdateFunctionRequestRequestTypeDef = TypedDict(
    "UpdateFunctionRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "functionId": str,
        "dataSourceName": str,
        "description": NotRequired[str],
        "requestMappingTemplate": NotRequired[str],
        "responseMappingTemplate": NotRequired[str],
        "functionVersion": NotRequired[str],
        "syncConfig": NotRequired[SyncConfigTypeDef],
        "maxBatchSize": NotRequired[int],
        "runtime": NotRequired[AppSyncRuntimeTypeDef],
        "code": NotRequired[str],
    },
)
UpdateResolverRequestRequestTypeDef = TypedDict(
    "UpdateResolverRequestRequestTypeDef",
    {
        "apiId": str,
        "typeName": str,
        "fieldName": str,
        "dataSourceName": NotRequired[str],
        "requestMappingTemplate": NotRequired[str],
        "responseMappingTemplate": NotRequired[str],
        "kind": NotRequired[ResolverKindType],
        "pipelineConfig": NotRequired[PipelineConfigTypeDef],
        "syncConfig": NotRequired[SyncConfigTypeDef],
        "cachingConfig": NotRequired[CachingConfigTypeDef],
        "maxBatchSize": NotRequired[int],
        "runtime": NotRequired[AppSyncRuntimeTypeDef],
        "code": NotRequired[str],
        "metricsConfig": NotRequired[ResolverLevelMetricsConfigType],
    },
)
CreateGraphqlApiResponseTypeDef = TypedDict(
    "CreateGraphqlApiResponseTypeDef",
    {
        "graphqlApi": GraphqlApiTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGraphqlApiResponseTypeDef = TypedDict(
    "GetGraphqlApiResponseTypeDef",
    {
        "graphqlApi": GraphqlApiTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListGraphqlApisResponseTypeDef = TypedDict(
    "ListGraphqlApisResponseTypeDef",
    {
        "graphqlApis": List[GraphqlApiTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
UpdateGraphqlApiResponseTypeDef = TypedDict(
    "UpdateGraphqlApiResponseTypeDef",
    {
        "graphqlApi": GraphqlApiTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ApiTypeDef = TypedDict(
    "ApiTypeDef",
    {
        "apiId": NotRequired[str],
        "name": NotRequired[str],
        "ownerContact": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "dns": NotRequired[Dict[str, str]],
        "apiArn": NotRequired[str],
        "created": NotRequired[datetime],
        "xrayEnabled": NotRequired[bool],
        "wafWebAclArn": NotRequired[str],
        "eventConfig": NotRequired[EventConfigOutputTypeDef],
    },
)
CreateApiRequestRequestTypeDef = TypedDict(
    "CreateApiRequestRequestTypeDef",
    {
        "name": str,
        "ownerContact": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "eventConfig": NotRequired[EventConfigTypeDef],
    },
)
UpdateApiRequestRequestTypeDef = TypedDict(
    "UpdateApiRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "ownerContact": NotRequired[str],
        "eventConfig": NotRequired[EventConfigTypeDef],
    },
)
CreateDataSourceRequestRequestTypeDef = TypedDict(
    "CreateDataSourceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "type": DataSourceTypeType,
        "description": NotRequired[str],
        "serviceRoleArn": NotRequired[str],
        "dynamodbConfig": NotRequired[DynamodbDataSourceConfigTypeDef],
        "lambdaConfig": NotRequired[LambdaDataSourceConfigTypeDef],
        "elasticsearchConfig": NotRequired[ElasticsearchDataSourceConfigTypeDef],
        "openSearchServiceConfig": NotRequired[OpenSearchServiceDataSourceConfigTypeDef],
        "httpConfig": NotRequired[HttpDataSourceConfigTypeDef],
        "relationalDatabaseConfig": NotRequired[RelationalDatabaseDataSourceConfigTypeDef],
        "eventBridgeConfig": NotRequired[EventBridgeDataSourceConfigTypeDef],
        "metricsConfig": NotRequired[DataSourceLevelMetricsConfigType],
    },
)
DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "dataSourceArn": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "type": NotRequired[DataSourceTypeType],
        "serviceRoleArn": NotRequired[str],
        "dynamodbConfig": NotRequired[DynamodbDataSourceConfigTypeDef],
        "lambdaConfig": NotRequired[LambdaDataSourceConfigTypeDef],
        "elasticsearchConfig": NotRequired[ElasticsearchDataSourceConfigTypeDef],
        "openSearchServiceConfig": NotRequired[OpenSearchServiceDataSourceConfigTypeDef],
        "httpConfig": NotRequired[HttpDataSourceConfigTypeDef],
        "relationalDatabaseConfig": NotRequired[RelationalDatabaseDataSourceConfigTypeDef],
        "eventBridgeConfig": NotRequired[EventBridgeDataSourceConfigTypeDef],
        "metricsConfig": NotRequired[DataSourceLevelMetricsConfigType],
    },
)
UpdateDataSourceRequestRequestTypeDef = TypedDict(
    "UpdateDataSourceRequestRequestTypeDef",
    {
        "apiId": str,
        "name": str,
        "type": DataSourceTypeType,
        "description": NotRequired[str],
        "serviceRoleArn": NotRequired[str],
        "dynamodbConfig": NotRequired[DynamodbDataSourceConfigTypeDef],
        "lambdaConfig": NotRequired[LambdaDataSourceConfigTypeDef],
        "elasticsearchConfig": NotRequired[ElasticsearchDataSourceConfigTypeDef],
        "openSearchServiceConfig": NotRequired[OpenSearchServiceDataSourceConfigTypeDef],
        "httpConfig": NotRequired[HttpDataSourceConfigTypeDef],
        "relationalDatabaseConfig": NotRequired[RelationalDatabaseDataSourceConfigTypeDef],
        "eventBridgeConfig": NotRequired[EventBridgeDataSourceConfigTypeDef],
        "metricsConfig": NotRequired[DataSourceLevelMetricsConfigType],
    },
)
EvaluateCodeResponseTypeDef = TypedDict(
    "EvaluateCodeResponseTypeDef",
    {
        "evaluationResult": str,
        "error": EvaluateCodeErrorDetailTypeDef,
        "logs": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataSourceIntrospectionResultTypeDef = TypedDict(
    "DataSourceIntrospectionResultTypeDef",
    {
        "models": NotRequired[List[DataSourceIntrospectionModelTypeDef]],
        "nextToken": NotRequired[str],
    },
)
CreateFunctionResponseTypeDef = TypedDict(
    "CreateFunctionResponseTypeDef",
    {
        "functionConfiguration": FunctionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFunctionResponseTypeDef = TypedDict(
    "GetFunctionResponseTypeDef",
    {
        "functionConfiguration": FunctionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFunctionsResponseTypeDef = TypedDict(
    "ListFunctionsResponseTypeDef",
    {
        "functions": List[FunctionConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
UpdateFunctionResponseTypeDef = TypedDict(
    "UpdateFunctionResponseTypeDef",
    {
        "functionConfiguration": FunctionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateResolverResponseTypeDef = TypedDict(
    "CreateResolverResponseTypeDef",
    {
        "resolver": ResolverTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetResolverResponseTypeDef = TypedDict(
    "GetResolverResponseTypeDef",
    {
        "resolver": ResolverTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListResolversByFunctionResponseTypeDef = TypedDict(
    "ListResolversByFunctionResponseTypeDef",
    {
        "resolvers": List[ResolverTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
ListResolversResponseTypeDef = TypedDict(
    "ListResolversResponseTypeDef",
    {
        "resolvers": List[ResolverTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
UpdateResolverResponseTypeDef = TypedDict(
    "UpdateResolverResponseTypeDef",
    {
        "resolver": ResolverTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateApiResponseTypeDef = TypedDict(
    "CreateApiResponseTypeDef",
    {
        "api": ApiTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetApiResponseTypeDef = TypedDict(
    "GetApiResponseTypeDef",
    {
        "api": ApiTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListApisResponseTypeDef = TypedDict(
    "ListApisResponseTypeDef",
    {
        "apis": List[ApiTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
UpdateApiResponseTypeDef = TypedDict(
    "UpdateApiResponseTypeDef",
    {
        "api": ApiTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDataSourceResponseTypeDef = TypedDict(
    "CreateDataSourceResponseTypeDef",
    {
        "dataSource": DataSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataSourceResponseTypeDef = TypedDict(
    "GetDataSourceResponseTypeDef",
    {
        "dataSource": DataSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {
        "dataSources": List[DataSourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
UpdateDataSourceResponseTypeDef = TypedDict(
    "UpdateDataSourceResponseTypeDef",
    {
        "dataSource": DataSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataSourceIntrospectionResponseTypeDef = TypedDict(
    "GetDataSourceIntrospectionResponseTypeDef",
    {
        "introspectionId": str,
        "introspectionStatus": DataSourceIntrospectionStatusType,
        "introspectionStatusDetail": str,
        "introspectionResult": DataSourceIntrospectionResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
