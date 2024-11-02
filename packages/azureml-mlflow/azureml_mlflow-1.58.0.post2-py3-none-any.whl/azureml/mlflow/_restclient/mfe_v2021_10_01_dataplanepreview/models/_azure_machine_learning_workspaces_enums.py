# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from six import with_metaclass
from azure.core import CaseInsensitiveEnumMeta


class BaseEnvironmentSourceType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Base environment type."""

    ENVIRONMENT_ASSET = "EnvironmentAsset"


class BindingType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Different Binding types"""

    BASIC = "Basic"


class CreatedByType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """The type of identity that created the resource."""

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"


class CredentialsType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine the datastore credentials type."""

    ACCOUNT_KEY = "AccountKey"
    CERTIFICATE = "Certificate"
    NONE = "None"
    SAS = "Sas"
    SERVICE_PRINCIPAL = "ServicePrincipal"


class DataReferenceCredentialType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):

    SAS = "SAS"
    DOCKER_CREDENTIALS = "DockerCredentials"
    MANAGED_IDENTITY = "ManagedIdentity"
    NO_CREDENTIALS = "NoCredentials"


class DatastoreType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine the datastore contents type."""

    AZURE_BLOB = "AzureBlob"
    AZURE_DATA_LAKE_GEN1 = "AzureDataLakeGen1"
    AZURE_DATA_LAKE_GEN2 = "AzureDataLakeGen2"
    AZURE_FILE = "AzureFile"


class DataType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine the type of data."""

    URI_FILE = "uri_file"
    URI_FOLDER = "uri_folder"
    MLTABLE = "mltable"


class DistributionType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine the job distribution type."""

    PY_TORCH = "PyTorch"
    TENSOR_FLOW = "TensorFlow"
    MPI = "Mpi"


class EarlyTerminationPolicyType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):

    BANDIT = "Bandit"
    MEDIAN_STOPPING = "MedianStopping"
    TRUNCATION_SELECTION = "TruncationSelection"


class EnvironmentType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Environment type is either user created or curated by Azure ML service"""

    CURATED = "Curated"
    USER_CREATED = "UserCreated"


class Goal(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Defines supported metric goals for hyperparameter tuning"""

    MINIMIZE = "Minimize"
    MAXIMIZE = "Maximize"


class IdentityConfigurationType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine identity framework."""

    MANAGED = "Managed"
    AML_TOKEN = "AMLToken"


class InferencingServerType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Inferencing server type for various targets."""

    AZURE_ML_ONLINE = "AzureMLOnline"
    AZURE_ML_BATCH = "AzureMLBatch"
    TRITON = "Triton"
    CUSTOM = "Custom"


class InputDataDeliveryMode(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine the input data delivery mode."""

    READ_ONLY_MOUNT = "ReadOnlyMount"
    READ_WRITE_MOUNT = "ReadWriteMount"
    DOWNLOAD = "Download"


class InputPathType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Input path type for package inputs."""

    URL = "Url"
    PATH_ID = "PathId"
    PATH_VERSION = "PathVersion"


class JobInputType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine the Job Input Type."""

    DATASET = "Dataset"
    URI = "Uri"
    LITERAL = "Literal"


class JobLimitsType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):

    COMMAND = "Command"
    SWEEP = "Sweep"


class JobOutputType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine the Job Output Type."""

    URI = "Uri"
    DATASET = "Dataset"


class JobStatus(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """The status of a job."""

    NOT_STARTED = "NotStarted"
    STARTING = "Starting"
    PROVISIONING = "Provisioning"
    PREPARING = "Preparing"
    QUEUED = "Queued"
    RUNNING = "Running"
    FINALIZING = "Finalizing"
    CANCEL_REQUESTED = "CancelRequested"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELED = "Canceled"
    NOT_RESPONDING = "NotResponding"
    PAUSED = "Paused"
    UNKNOWN = "Unknown"


class JobType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine the type of job."""

    COMMAND = "Command"
    SWEEP = "Sweep"
    PIPELINE = "Pipeline"
    BASE = "Base"


class ListViewType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):

    ACTIVE_ONLY = "ActiveOnly"
    ARCHIVED_ONLY = "ArchivedOnly"
    ALL = "All"


class OperatingSystemType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """The type of operating system."""

    LINUX = "Linux"
    WINDOWS = "Windows"


class OutputDataDeliveryMode(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Output data delivery mode enums."""

    READ_WRITE_MOUNT = "ReadWriteMount"
    UPLOAD = "Upload"


class PackageBuildState(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Package build state returned in package response."""

    NOT_STARTED = "NotStarted"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"


class PackageInputDeliveryMode(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Mounting type of the model or the inputs"""

    COPY = "Copy"
    DOWNLOAD = "Download"


class PackageInputType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Type of the inputs."""

    URI_FILE = "UriFile"
    URI_FOLDER = "UriFolder"


class ProtectionLevel(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Protection level associated with the Intellectual Property."""

    ALL = "All"
    NONE = "None"


class ReferenceType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine which reference method to use for an asset."""

    ID = "Id"
    DATA_PATH = "DataPath"
    OUTPUT_PATH = "OutputPath"


class SamplingAlgorithm(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):

    GRID = "Grid"
    RANDOM = "Random"
    BAYESIAN = "Bayesian"


class SecretsType(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):
    """Enum to determine the datastore secrets type."""

    ACCOUNT_KEY = "AccountKey"
    CERTIFICATE = "Certificate"
    SAS = "Sas"
    SERVICE_PRINCIPAL = "ServicePrincipal"


class ServiceDataAccessAuthIdentity(with_metaclass(CaseInsensitiveEnumMeta, str, Enum)):

    NONE = "None"
    WORKSPACE_SYSTEM_ASSIGNED_IDENTITY = "WorkspaceSystemAssignedIdentity"
    WORKSPACE_USER_ASSIGNED_IDENTITY = "WorkspaceUserAssignedIdentity"
