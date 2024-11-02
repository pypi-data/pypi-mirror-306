# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
from typing import Any

from azureml.mlflow._restclient.registry_discovery import (
    AzureMachineLearningWorkspaces as ServiceClientRegistryDiscovery,
)
from azureml.mlflow._restclient.mfe_v2021_10_01_dataplanepreview import (
    AzureMachineLearningWorkspaces,
)
from azureml.mlflow._restclient.mfe_v2021_10_01_dataplanepreview.models import (
    BlobReferenceSASRequestDto,
    TemporaryDataReferenceRequestDto,
)
from azure.core.exceptions import HttpResponseError

module_logger = logging.getLogger(__name__)

MFE_PATH_PREFIX = "mferp/managementfrontend"

REGISTRY_ASSET_ID = "azureml://registries/{}/{}/{}/versions/{}"


class RegistryDiscovery:
    def __init__(
        self,
        credential: str,
        registry_name: str,
        service_client_registry_discovery_client: ServiceClientRegistryDiscovery,
        **kwargs,
    ):
        self.credential = credential
        self.registry_name = registry_name
        self.service_client_registry_discovery_client = (
            service_client_registry_discovery_client
        )
        self.kwargs = kwargs
        self._resource_group = None
        self._subscription_id = None
        self._base_url = None

    def _get_registry_details(self) -> str:
        response = self.service_client_registry_discovery_client.registry_management_non_workspace.registry_management_non_workspace(  # noqa: E501
            self.registry_name
        )
        self._base_url = (
            f"{response.primary_region_resource_provider_uri}{MFE_PATH_PREFIX}"
        )
        self._subscription_id = response.subscription_id
        self._resource_group = response.resource_group

    def get_registry_service_client(self) -> AzureMachineLearningWorkspaces:
        self._get_registry_details()
        self.kwargs.pop("subscription_id", None)
        self.kwargs.pop("resource_group", None)
        service_client_10_2021_dataplanepreview = (
            AzureMachineLearningWorkspaces(
                subscription_id=self._subscription_id,
                resource_group=self._resource_group,
                credential=self.credential,
                base_url=self._base_url,
                **self.kwargs,
            )
        )
        return service_client_10_2021_dataplanepreview

    @property
    def subscription_id(self) -> str:
        """The subscription id of the registry.

        :return: Subscription Id
        :rtype: str
        """
        return self._subscription_id

    @property
    def resource_group(self) -> str:
        """The resource group of the registry.

        :return: Resource Group
        :rtype: str
        """
        return self._resource_group


def get_sas_uri_for_registry_asset(
    service_client, name, version, resource_group, registry, body
) -> str:
    """Get sas_uri for registry asset.

    :param service_client: Service client
    :type service_client: AzureMachineLearningWorkspaces
    :param name: Asset name
    :type name: str
    :param version: Asset version
    :type version: str
    :param resource_group: Resource group
    :type resource_group: str
    :param registry: Registry name
    :type registry: str
    :param body: Request body
    :type body: TemporaryDataReferenceRequestDto
    :rtype: str
    """
    sas_uri = None
    try:
        res = service_client.temporary_data_references.create_or_get_temporary_data_reference(
            name=name,
            version=version,
            resource_group_name=resource_group,
            registry_name=registry,
            body=body,
        )
        sas_uri = res.blob_reference_for_consumption.credential.additional_properties[
            "sasUri"
        ]
        blob_uri = res.blob_reference_for_consumption.blob_uri
    except HttpResponseError as e:
        # "Asset already exists" exception is thrown from service with error code 409, that we need to ignore
        if e.status_code == 409:
            module_logger.debug(
                "Skipping file upload, reason:  %s", str(e.reason)
            )
        else:
            raise e
    return sas_uri, blob_uri


def get_asset_body_for_registry_storage(
    registry_name: str, asset_type: str, asset_name: str, asset_version: str
) -> TemporaryDataReferenceRequestDto:
    """Get Asset body for registry.

    :param registry_name: Registry name.
    :type registry_name: str
    :param asset_type: Asset type.
    :type asset_type: str
    :param asset_name: Asset name.
    :type asset_name: str
    :param asset_version: Asset version.
    :type asset_version: str
    :rtype: TemporaryDataReferenceRequestDto
    """
    body = TemporaryDataReferenceRequestDto(
        asset_id=REGISTRY_ASSET_ID.format(
            registry_name, asset_type, asset_name, asset_version
        ),
        temporary_data_reference_type="TemporaryBlobReference",
    )
    return body


def get_storage_details_for_registry_assets(
    service_client: AzureMachineLearningWorkspaces,
    asset_type: str,
    asset_name: str,
    asset_version: str,
    rg_name: str,
    reg_name: str,
    uri: str,
) -> str:
    """Get storage details for registry assets.

    :param service_client: AzureMachineLearningWorkspaces service client.
    :type service_client: AzureMachineLearningWorkspaces
    :param asset_type: Asset type.
    :type asset_type: str
    :param asset_name: Asset name.
    :type asset_name: str
    :param asset_version: Asset version.
    :type asset_version: str
    :param rg_name: Resource group name.
    :type rg_name: str
    :param reg_name: Registry name
    :type reg_name: str
    :param uri: asset uri
    :type uri: str
    :rtype: str
    """
    body = BlobReferenceSASRequestDto(
        asset_id=REGISTRY_ASSET_ID.format(
            reg_name, asset_type, asset_name, asset_version
        ),
        blob_uri=uri,
    )
    sas_uri = service_client.data_references.get_blob_reference_sas(
        name=asset_name,
        version=asset_version,
        resource_group_name=rg_name,
        registry_name=reg_name,
        body=body,
    )
    if (
        sas_uri.blob_reference_for_consumption.credential.credential_type
        == "NoCredentials"
    ):
        return sas_uri.blob_reference_for_consumption.blob_uri, "NoCredentials"

    return (
        sas_uri.blob_reference_for_consumption.credential.additional_properties[
            "sasUri"
        ],
        "SAS",
    )


def get_registry_client(registry_name, auth, **kwargs):
    base_url = "https://eastus.api.azureml.ms/"
    service_client_registry_discovery_client = ServiceClientRegistryDiscovery(
        credential=auth, base_url=base_url, **kwargs
    )
    registry_discovery = RegistryDiscovery(
        auth, registry_name, service_client_registry_discovery_client, **kwargs
    )
    service_client_10_2021_dataplanepreview = (
        registry_discovery.get_registry_service_client()
    )
    subscription_id = registry_discovery.subscription_id
    resource_group_name = registry_discovery.resource_group

    return (
        service_client_10_2021_dataplanepreview,
        resource_group_name,
        subscription_id,
    )


def _get_next_version_from_container(
    name: str,
    container_operation: Any,
    resource_group_name: str,
    workspace_name: str,
    registry_name: str = None,
    **kwargs,
) -> str:
    try:
        container = container_operation.get(
            name=name,
            resource_group_name=resource_group_name,
            registry_name=registry_name,
            **kwargs,
        )
        version = container.properties.next_version

    except Exception:
        version = "1"
    return version
