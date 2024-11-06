from __future__ import annotations  # Add this line at the top

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from busbar.core.providers.capabilities import (
    AuthCapability,
    SecretsCapability,
    VCSCapability,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    field_validator,
    model_validator,
)

if TYPE_CHECKING:
    from ..audit.base import AuditService  # Import the type alias
    from ..security.security_service import SecurityService

from ..types import (
    ConnectionType,
    InterfaceType,
    RiskLevel,
    SecurityLevel,
    SlugStr,
)


class ProviderCapability(BaseModel):
    """Provider capability definition"""

    interface_types: list[InterfaceType]
    connection_types: list[ConnectionType]
    required_secrets: list[str] = Field(default_factory=list)
    optional_features: list[str] = Field(default_factory=list)


class Provider(BaseModel):
    """System provider definition"""

    id: UUID = Field(default_factory=uuid4)
    name: str
    slug: SlugStr
    capabilities: list[ProviderCapability]

    # Example instances would be:
    # - GitHub: VCS+CI+PLATFORM provider
    # - GitLab: VCS+CI provider
    # - Bitbucket: VCS provider
    # - Auth0: AUTHENTICATION provider
    # - Salesforce: PLATFORM provider
    # - AWS Secrets Manager: SECRETS provider
    # etc.


class Connection(BaseModel):
    """System connection configuration"""

    id: UUID = Field(default_factory=uuid4)
    provider: Provider
    interface_type: InterfaceType
    connection_type: ConnectionType
    config: dict[str, Any] = Field(default_factory=dict)
    secrets: dict[str, SecretStr] = Field(default_factory=dict)


class Rack(BaseModel):
    """Collection of configured providers"""

    id: UUID = Field(default_factory=uuid4)
    name: str
    providers: dict[str, Provider]
    connections: dict[str, Connection]


class CoreModel(BaseModel):
    """Base model for all busbar models with metadata and validation"""

    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True,
    )

    id: UUID = Field(
        default_factory=uuid4,
        title="Identifier",
        description="Unique identifier for this resource",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Created At",
        description="Timestamp when this resource was created",
        examples=["2024-01-01T00:00:00Z"],
        json_schema_extra={
            "format": "date-time",
            "readOnly": True,
        },
    )

    updated_at: datetime | None = Field(
        default=None,
        title="Updated At",
        description="Timestamp when this resource was last updated",
        examples=["2024-01-01T00:00:00Z"],
        json_schema_extra={
            "format": "date-time",
            "readOnly": True,
        },
    )

    created_by: UUID | None = Field(
        default=None,
        title="Created By",
        description="ID of the user who created this resource",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
        json_schema_extra={
            "readOnly": True,
        },
    )

    updated_by: UUID | None = Field(
        default=None,
        title="Updated By",
        description="ID of the user who last updated this resource",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
        json_schema_extra={
            "readOnly": True,
        },
    )

    security_level: SecurityLevel = Field(
        default=SecurityLevel.PUBLIC,
        title="Security Level",
        description=(
            "Security classification level for this resource. Determines access "
            "controls and audit logging requirements."
        ),
        examples=["public", "internal", "sensitive", "secret"],
        json_schema_extra={
            "deprecated": False,
            "writeOnly": False,
        },
    )

    risk_level: RiskLevel = Field(
        default=RiskLevel.LOW,
        title="Risk Level",
        description=(
            "Risk assessment level for operations on this resource. Affects "
            "approval requirements and audit detail level."
        ),
        examples=["low", "medium", "high", "critical"],
    )

    tags: dict[str, str] = Field(
        default_factory=dict,
        title="Tags",
        description=(
            "Key-value pairs for resource organization and filtering. Keys and values "
            "must be strings and keys must be valid identifiers."
        ),
        examples=[{"environment": "production", "team": "platform"}],
        json_schema_extra={
            "additionalProperties": {"type": "string", "maxLength": 64},
            "maxProperties": 50,
            "propertyNames": {"pattern": "^[a-zA-Z][a-zA-Z0-9_]*$", "maxLength": 64},
        },
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        title="Metadata",
        description=(
            "Additional metadata about this resource. Unlike tags, values can be of "
            "any JSON-serializable type."
        ),
        examples=[{"version_history": ["1.0.0", "1.1.0"], "custom_data": {"key": "value"}}],
        json_schema_extra={
            "additionalProperties": True,
            "maxProperties": 100,
            "propertyNames": {"pattern": "^[a-zA-Z][a-zA-Z0-9_]*$", "maxLength": 64},
        },
    )

    _security_service: SecurityService | None = None
    _audit_service: AuditService | None = None

    @property
    def security_service(self) -> SecurityService:
        if self._security_service is None:
            from busbar.core.containers import CoreModule
            from injector import Injector

            injector = Injector([CoreModule()])
            self._security_service = injector.get(SecurityService)
        return self._security_service

    @property
    def audit_service(self) -> AuditService:
        if self._audit_service is None:
            from busbar.core.containers import CoreModule
            from injector import Injector

            injector = Injector([CoreModule()])
            self._audit_service = injector.get(AuditService)
        return self._audit_service

    @model_validator(mode="before")
    @classmethod
    def set_timestamps(cls, data: dict[str, Any] | Any) -> dict[str, Any]:
        """Set creation/update timestamps"""
        if not isinstance(data, dict):
            return data

        now = datetime.now(timezone.utc)
        if not data.get("created_at"):
            data["created_at"] = now
        if not data.get("updated_at"):
            data["updated_at"] = now
        return data

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata(cls, value: dict[str, Any] | None) -> dict[str, Any]:
        """Validate metadata is JSON serializable"""
        if not value:
            return {}

        try:
            import json
            json.dumps(value)
            return value
        except TypeError as e:
            raise ValueError(f"Metadata must be JSON serializable: {e}")


class ProviderDefinition(BaseModel):
    """Definition of a provider with its capabilities."""

    model_config = ConfigDict(
        type_selection="type",  # Discriminator field for capabilities
        smart_union=True,
    )

    name: str = Field(..., description="Provider display name")
    slug: str = Field(..., description="Provider identifier")
    version: str = Field(..., description="Provider version")
    description: str = Field(..., description="Provider description")
    capabilities: dict[str, AuthCapability | VCSCapability | SecretsCapability] = Field(
        default_factory=dict, description="Provider capabilities"
    )


class Credential(CoreModel):
    """Security credential associated with a principal."""

    id: UUID = Field(default_factory=uuid4)
    principal_id: UUID = Field(title="Principal ID", description="Owner of this credential")
    type: str = Field(title="Credential Type", description="Type of credential")
    secret: SecretStr = Field(title="Secret Value", description="Credential secret value")
    issued_at: datetime = Field(
        title="Issued At", description="Timestamp when credential was issued"
    )
    expires_at: datetime | None = Field(
        title="Expires At", description="Timestamp when credential expires"
    )
    metadata: dict[str, str] = Field(
        default_factory=dict,
        title="Metadata",
        description="Additional credential metadata",
    )

    @classmethod
    async def create_credential(cls, security_service: SecurityService, **kwargs) -> Credential:
        """
        Create a new credential with hashed secret.

        Args:
            security_service (SecurityService): Instance of SecurityService.
            **kwargs: Other fields for Credential.

        Returns:
            Credential: The created credential.
        """
        raw_secret = kwargs.get("secret")
        if raw_secret is None:
            raise ValueError("Secret is required to create a credential")
        hashed_secret = security_service.hash_secret(raw_secret)
        kwargs["secret"] = SecretStr(hashed_secret)
        return cls(**kwargs)
