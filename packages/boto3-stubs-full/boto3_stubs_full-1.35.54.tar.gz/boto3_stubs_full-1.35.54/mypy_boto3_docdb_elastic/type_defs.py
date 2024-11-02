"""
Type annotations for docdb-elastic service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_docdb_elastic/type_defs/)

Usage::

    ```python
    from mypy_boto3_docdb_elastic.type_defs import ApplyPendingMaintenanceActionInputRequestTypeDef

    data: ApplyPendingMaintenanceActionInputRequestTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Mapping, Sequence

from .literals import AuthType, OptInTypeType, SnapshotTypeType, StatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ApplyPendingMaintenanceActionInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ClusterInListTypeDef",
    "ClusterSnapshotInListTypeDef",
    "ClusterSnapshotTypeDef",
    "ShardTypeDef",
    "CopyClusterSnapshotInputRequestTypeDef",
    "CreateClusterInputRequestTypeDef",
    "CreateClusterSnapshotInputRequestTypeDef",
    "DeleteClusterInputRequestTypeDef",
    "DeleteClusterSnapshotInputRequestTypeDef",
    "GetClusterInputRequestTypeDef",
    "GetClusterSnapshotInputRequestTypeDef",
    "GetPendingMaintenanceActionInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListClusterSnapshotsInputRequestTypeDef",
    "ListClustersInputRequestTypeDef",
    "ListPendingMaintenanceActionsInputRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PendingMaintenanceActionDetailsTypeDef",
    "RestoreClusterFromSnapshotInputRequestTypeDef",
    "StartClusterInputRequestTypeDef",
    "StopClusterInputRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateClusterInputRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListClustersOutputTypeDef",
    "ListClusterSnapshotsOutputTypeDef",
    "CopyClusterSnapshotOutputTypeDef",
    "CreateClusterSnapshotOutputTypeDef",
    "DeleteClusterSnapshotOutputTypeDef",
    "GetClusterSnapshotOutputTypeDef",
    "ClusterTypeDef",
    "ListClusterSnapshotsInputListClusterSnapshotsPaginateTypeDef",
    "ListClustersInputListClustersPaginateTypeDef",
    "ListPendingMaintenanceActionsInputListPendingMaintenanceActionsPaginateTypeDef",
    "ResourcePendingMaintenanceActionTypeDef",
    "CreateClusterOutputTypeDef",
    "DeleteClusterOutputTypeDef",
    "GetClusterOutputTypeDef",
    "RestoreClusterFromSnapshotOutputTypeDef",
    "StartClusterOutputTypeDef",
    "StopClusterOutputTypeDef",
    "UpdateClusterOutputTypeDef",
    "ApplyPendingMaintenanceActionOutputTypeDef",
    "GetPendingMaintenanceActionOutputTypeDef",
    "ListPendingMaintenanceActionsOutputTypeDef",
)

ApplyPendingMaintenanceActionInputRequestTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionInputRequestTypeDef",
    {
        "applyAction": str,
        "optInType": OptInTypeType,
        "resourceArn": str,
        "applyOn": NotRequired[str],
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
ClusterInListTypeDef = TypedDict(
    "ClusterInListTypeDef",
    {
        "clusterArn": str,
        "clusterName": str,
        "status": StatusType,
    },
)
ClusterSnapshotInListTypeDef = TypedDict(
    "ClusterSnapshotInListTypeDef",
    {
        "clusterArn": str,
        "snapshotArn": str,
        "snapshotCreationTime": str,
        "snapshotName": str,
        "status": StatusType,
    },
)
ClusterSnapshotTypeDef = TypedDict(
    "ClusterSnapshotTypeDef",
    {
        "adminUserName": str,
        "clusterArn": str,
        "clusterCreationTime": str,
        "kmsKeyId": str,
        "snapshotArn": str,
        "snapshotCreationTime": str,
        "snapshotName": str,
        "status": StatusType,
        "subnetIds": List[str],
        "vpcSecurityGroupIds": List[str],
        "snapshotType": NotRequired[SnapshotTypeType],
    },
)
ShardTypeDef = TypedDict(
    "ShardTypeDef",
    {
        "createTime": str,
        "shardId": str,
        "status": StatusType,
    },
)
CopyClusterSnapshotInputRequestTypeDef = TypedDict(
    "CopyClusterSnapshotInputRequestTypeDef",
    {
        "snapshotArn": str,
        "targetSnapshotName": str,
        "copyTags": NotRequired[bool],
        "kmsKeyId": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateClusterInputRequestTypeDef = TypedDict(
    "CreateClusterInputRequestTypeDef",
    {
        "adminUserName": str,
        "adminUserPassword": str,
        "authType": AuthType,
        "clusterName": str,
        "shardCapacity": int,
        "shardCount": int,
        "backupRetentionPeriod": NotRequired[int],
        "clientToken": NotRequired[str],
        "kmsKeyId": NotRequired[str],
        "preferredBackupWindow": NotRequired[str],
        "preferredMaintenanceWindow": NotRequired[str],
        "shardInstanceCount": NotRequired[int],
        "subnetIds": NotRequired[Sequence[str]],
        "tags": NotRequired[Mapping[str, str]],
        "vpcSecurityGroupIds": NotRequired[Sequence[str]],
    },
)
CreateClusterSnapshotInputRequestTypeDef = TypedDict(
    "CreateClusterSnapshotInputRequestTypeDef",
    {
        "clusterArn": str,
        "snapshotName": str,
        "tags": NotRequired[Mapping[str, str]],
    },
)
DeleteClusterInputRequestTypeDef = TypedDict(
    "DeleteClusterInputRequestTypeDef",
    {
        "clusterArn": str,
    },
)
DeleteClusterSnapshotInputRequestTypeDef = TypedDict(
    "DeleteClusterSnapshotInputRequestTypeDef",
    {
        "snapshotArn": str,
    },
)
GetClusterInputRequestTypeDef = TypedDict(
    "GetClusterInputRequestTypeDef",
    {
        "clusterArn": str,
    },
)
GetClusterSnapshotInputRequestTypeDef = TypedDict(
    "GetClusterSnapshotInputRequestTypeDef",
    {
        "snapshotArn": str,
    },
)
GetPendingMaintenanceActionInputRequestTypeDef = TypedDict(
    "GetPendingMaintenanceActionInputRequestTypeDef",
    {
        "resourceArn": str,
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
ListClusterSnapshotsInputRequestTypeDef = TypedDict(
    "ListClusterSnapshotsInputRequestTypeDef",
    {
        "clusterArn": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "snapshotType": NotRequired[str],
    },
)
ListClustersInputRequestTypeDef = TypedDict(
    "ListClustersInputRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListPendingMaintenanceActionsInputRequestTypeDef = TypedDict(
    "ListPendingMaintenanceActionsInputRequestTypeDef",
    {
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
PendingMaintenanceActionDetailsTypeDef = TypedDict(
    "PendingMaintenanceActionDetailsTypeDef",
    {
        "action": str,
        "autoAppliedAfterDate": NotRequired[str],
        "currentApplyDate": NotRequired[str],
        "description": NotRequired[str],
        "forcedApplyDate": NotRequired[str],
        "optInStatus": NotRequired[str],
    },
)
RestoreClusterFromSnapshotInputRequestTypeDef = TypedDict(
    "RestoreClusterFromSnapshotInputRequestTypeDef",
    {
        "clusterName": str,
        "snapshotArn": str,
        "kmsKeyId": NotRequired[str],
        "shardCapacity": NotRequired[int],
        "shardInstanceCount": NotRequired[int],
        "subnetIds": NotRequired[Sequence[str]],
        "tags": NotRequired[Mapping[str, str]],
        "vpcSecurityGroupIds": NotRequired[Sequence[str]],
    },
)
StartClusterInputRequestTypeDef = TypedDict(
    "StartClusterInputRequestTypeDef",
    {
        "clusterArn": str,
    },
)
StopClusterInputRequestTypeDef = TypedDict(
    "StopClusterInputRequestTypeDef",
    {
        "clusterArn": str,
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
UpdateClusterInputRequestTypeDef = TypedDict(
    "UpdateClusterInputRequestTypeDef",
    {
        "clusterArn": str,
        "adminUserPassword": NotRequired[str],
        "authType": NotRequired[AuthType],
        "backupRetentionPeriod": NotRequired[int],
        "clientToken": NotRequired[str],
        "preferredBackupWindow": NotRequired[str],
        "preferredMaintenanceWindow": NotRequired[str],
        "shardCapacity": NotRequired[int],
        "shardCount": NotRequired[int],
        "shardInstanceCount": NotRequired[int],
        "subnetIds": NotRequired[Sequence[str]],
        "vpcSecurityGroupIds": NotRequired[Sequence[str]],
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListClustersOutputTypeDef = TypedDict(
    "ListClustersOutputTypeDef",
    {
        "clusters": List[ClusterInListTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
ListClusterSnapshotsOutputTypeDef = TypedDict(
    "ListClusterSnapshotsOutputTypeDef",
    {
        "snapshots": List[ClusterSnapshotInListTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
CopyClusterSnapshotOutputTypeDef = TypedDict(
    "CopyClusterSnapshotOutputTypeDef",
    {
        "snapshot": ClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateClusterSnapshotOutputTypeDef = TypedDict(
    "CreateClusterSnapshotOutputTypeDef",
    {
        "snapshot": ClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteClusterSnapshotOutputTypeDef = TypedDict(
    "DeleteClusterSnapshotOutputTypeDef",
    {
        "snapshot": ClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetClusterSnapshotOutputTypeDef = TypedDict(
    "GetClusterSnapshotOutputTypeDef",
    {
        "snapshot": ClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "adminUserName": str,
        "authType": AuthType,
        "clusterArn": str,
        "clusterEndpoint": str,
        "clusterName": str,
        "createTime": str,
        "kmsKeyId": str,
        "preferredMaintenanceWindow": str,
        "shardCapacity": int,
        "shardCount": int,
        "status": StatusType,
        "subnetIds": List[str],
        "vpcSecurityGroupIds": List[str],
        "backupRetentionPeriod": NotRequired[int],
        "preferredBackupWindow": NotRequired[str],
        "shardInstanceCount": NotRequired[int],
        "shards": NotRequired[List[ShardTypeDef]],
    },
)
ListClusterSnapshotsInputListClusterSnapshotsPaginateTypeDef = TypedDict(
    "ListClusterSnapshotsInputListClusterSnapshotsPaginateTypeDef",
    {
        "clusterArn": NotRequired[str],
        "snapshotType": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListClustersInputListClustersPaginateTypeDef = TypedDict(
    "ListClustersInputListClustersPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListPendingMaintenanceActionsInputListPendingMaintenanceActionsPaginateTypeDef = TypedDict(
    "ListPendingMaintenanceActionsInputListPendingMaintenanceActionsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ResourcePendingMaintenanceActionTypeDef = TypedDict(
    "ResourcePendingMaintenanceActionTypeDef",
    {
        "pendingMaintenanceActionDetails": NotRequired[
            List[PendingMaintenanceActionDetailsTypeDef]
        ],
        "resourceArn": NotRequired[str],
    },
)
CreateClusterOutputTypeDef = TypedDict(
    "CreateClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteClusterOutputTypeDef = TypedDict(
    "DeleteClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetClusterOutputTypeDef = TypedDict(
    "GetClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RestoreClusterFromSnapshotOutputTypeDef = TypedDict(
    "RestoreClusterFromSnapshotOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartClusterOutputTypeDef = TypedDict(
    "StartClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StopClusterOutputTypeDef = TypedDict(
    "StopClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateClusterOutputTypeDef = TypedDict(
    "UpdateClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ApplyPendingMaintenanceActionOutputTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionOutputTypeDef",
    {
        "resourcePendingMaintenanceAction": ResourcePendingMaintenanceActionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPendingMaintenanceActionOutputTypeDef = TypedDict(
    "GetPendingMaintenanceActionOutputTypeDef",
    {
        "resourcePendingMaintenanceAction": ResourcePendingMaintenanceActionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListPendingMaintenanceActionsOutputTypeDef = TypedDict(
    "ListPendingMaintenanceActionsOutputTypeDef",
    {
        "resourcePendingMaintenanceActions": List[ResourcePendingMaintenanceActionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "nextToken": NotRequired[str],
    },
)
