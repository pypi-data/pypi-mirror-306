from datetime import datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator

from ..exceptions import SecurityError
from ..types import AccessLevel, RiskLevel, SecurityLevel


class Permission(BaseModel):
    """Granular permission definition."""

    resource_type: str = Field(
        title="Resource Type", description="Type of resource this permission applies to"
    )
    action: str = Field(title="Action", description="Allowed action on the resource")
    scope: str | None = Field(
        default="*", title="Scope", description="Permission scope specification"
    )
    conditions: dict[str, str] = Field(
        default_factory=dict,
        title="Conditions",
        description="Additional conditions for permission",
    )


class Scope(BaseModel):
    """OAuth/JWT scope definition."""

    name: str = Field(title="Scope Name", description="Unique identifier for this scope")
    description: str = Field(title="Description", description="Human-readable description")
    permissions: list[Permission] = Field(
        title="Permissions", description="Permissions granted by this scope"
    )
    risk_level: RiskLevel = Field(
        title="Risk Level", description="Risk level of granting this scope"
    )


class Principal(BaseModel):
    """Security principal representing a user or service."""

    id: UUID = Field(default_factory=uuid4)
    type: str = Field(title="Principal Type", description="Type of security principal")
    identifiers: dict[str, str] = Field(
        title="Identifiers", description="External system identifiers"
    )
    permissions: list[Permission] = Field(default_factory=list, title="Direct Permissions")
    roles: list[str] = Field(default_factory=list, title="Assigned Roles")
    groups: list[str] = Field(default_factory=list, title="Group Memberships")
    access_level: AccessLevel = Field(default=AccessLevel.NONE, title="Base Access Level")
    disabled: bool = Field(default=False, title="Disabled Status")


class Credential(BaseModel):
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


class Session(BaseModel):
    """Active security session for a principal."""

    id: UUID = Field(default_factory=uuid4)
    principal_id: UUID = Field(title="Principal ID", description="Session owner")
    credential_id: UUID = Field(title="Credential ID", description="Credential used for session")
    scopes: list[str] = Field(title="Granted Scopes", description="Scopes granted to this session")
    created_at: datetime = Field(
        title="Created At", description="Timestamp when session was created"
    )
    expires_at: datetime = Field(title="Expires At", description="Timestamp when session expires")
    metadata: dict[str, str] = Field(
        default_factory=dict, title="Metadata", description="Session metadata"
    )

    @model_validator(mode="after")
    def validate_session(self):
        created = self.created_at
        expires = self.expires_at

        if created and expires:
            max_duration = timedelta(days=7)
            if expires - created > max_duration:
                raise ValueError(f"Session cannot exceed {max_duration}")
        return self


class SecurityContext(BaseModel):
    """Security context for API operations"""

    model_config = ConfigDict(
        frozen=False,  # Allow mutation for stack operations
        arbitrary_types_allowed=True,  # Allow Principal and Session objects
    )

    principal_id: UUID = Field(..., description="Unique identifier of the authenticated principal")
    security_level: SecurityLevel = Field(..., description="Required security level for operation")
    risk_level: RiskLevel = Field(default=RiskLevel.LOW, description="Risk level of the operation")
    delegation_chain: list[UUID] = Field(
        default_factory=list, description="Chain of delegation for the operation"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional security metadata"
    )

    # Stack management
    principal: Principal | None = Field(default=None, description="Active security principal")
    session: Session | None = Field(default=None, description="Active security session")
    stack: list[dict[str, Any]] = Field(
        default_factory=list, description="Context stack for delegation"
    )

    def push(
        self,
        *,  # Enforce keyword args
        principal: Principal | None = None,
        session: Session | None = None,
    ) -> None:
        """Push a new security context onto the stack."""
        self.stack.append({"principal": self.principal, "session": self.session})
        self.principal = principal
        self.session = session

    def pop(self) -> None:
        """Pop the last security context from the stack."""
        if not self.stack:
            raise SecurityError("No context to pop")

        context = self.stack.pop()
        self.principal = context["principal"]
        self.session = context["session"]
