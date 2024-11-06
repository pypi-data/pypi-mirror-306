# providers/capabilities.py
"""
Dynamic provider capability definitions with default configurations.
"""

import builtins
from enum import Enum
from typing import Any, Literal, Optional

from injector import Injector
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from ..types import (
    CapabilityContext,
    CapabilityType,
    ConnectionType,
    InterfaceType,
    SecurityLevel,
)


class FlowType(str, Enum):
    """Generic authentication flow types"""

    OAUTH2_AUTHZ_CODE = "oauth2_authorization_code"
    OAUTH2_CLIENT_CREDS = "oauth2_client_credentials"
    OAUTH2_DEVICE = "oauth2_device"
    OIDC_BASIC = "oidc_basic"
    OIDC_HYBRID = "oidc_hybrid"
    API_KEY = "api_key"
    MUTUAL_TLS = "mutual_tls"
    JWT_BEARER = "jwt_bearer"


class BaseCapability(BaseModel):
    """Base class for all capabilities."""

    model_config = ConfigDict(frozen=True)

    type: CapabilityType = Field(..., description="The type of capability")
    name: str = Field(..., description="Name of the capability")
    features: set[str] = Field(default_factory=set, description="Set of supported features")
    settings: dict[str, Any] = Field(default_factory=dict, description="Configuration settings")
    security_level: SecurityLevel = Field(default=SecurityLevel.PUBLIC)
    implementation: builtins.type[Any] | None = None

    def filter_context(self, context: CapabilityContext) -> Optional["BaseCapability"]:
        """Filter capability based on context"""
        if self.security_level < context.security_level:
            return None

        filtered = self.model_copy()
        if context.required_features:
            if not context.required_features <= self.features:
                return None
            filtered.features &= context.required_features

        if context.allowed_features:
            filtered.features &= context.required_features | context.allowed_features

        return filtered if filtered.features else None

    def register_implementation(self, impl: builtins.type[Any], injector: Injector) -> None:
        """Register implementation with dependency injection"""
        self.implementation = impl
        injector.binder.bind(impl)


class AuthCapability(BaseCapability):
    """Authentication capability with flexible features"""

    type: Literal[CapabilityType.AUTH] = Field(
        CapabilityType.AUTH, description="Authentication capability type"
    )
    flows: set[FlowType] = Field(default_factory=set, description="Supported authentication flows")
    endpoints: dict[str, HttpUrl] = Field(
        default_factory=dict, description="Authentication endpoints"
    )
    scopes: list[str] = Field(default_factory=list, description="OAuth scopes")
    token_formats: list[str] = Field(default_factory=list, description="Supported token formats")
    features: set[str] = Field(default_factory=lambda: {"auth"}, description="Capability features")


class VCSCapability(BaseCapability):
    """Version Control System capability."""

    type: Literal[CapabilityType.VCS] = Field(CapabilityType.VCS, description="VCS capability type")
    system: str = Field(..., description="VCS system type")
    interface_types: list[InterfaceType] = Field(..., description="Supported interface types")
    connection_types: list[ConnectionType] = Field(..., description="Supported connection types")
    branch_map: dict[str, str] = Field(default_factory=dict, description="Branch name mappings")
    protected_patterns: list[str] = Field(
        default_factory=list, description="Protected branch patterns"
    )


class SecretsCapability(BaseCapability):
    """Secrets management capability with flexible features"""

    type: Literal[CapabilityType.SECRETS] = Field(
        CapabilityType.SECRETS, description="Secrets capability type"
    )
    supports_scoped_access: bool = Field(default=False)
    supports_rotation: bool = Field(default=False)
    supports_versioning: bool = Field(default=False)


class CapabilityConfig(BaseModel):
    """Dynamic capability configuration that can be loaded from files"""

    capabilities: dict[str, BaseCapability] = Field(
        default_factory=lambda: {
            "auth": AuthCapability(
                type=CapabilityType.AUTH,
                name="auth_cap",
                flows={"oauth2_authorization_code"},
                endpoints={"auth_url": "https://auth.example.com"},
                scopes=["read", "write"],
                token_formats=["jwt"],
            ),
            # Add other capabilities if necessary
            "vcs": VCSCapability(
                type=CapabilityType.VCS,
                name="vcs_cap",
                system="git",
                interface_types=[InterfaceType.API],
                connection_types=[ConnectionType.WEB],
                branch_map={"main": "master"},
                protected_patterns=["release/*"],
            ),
        }
    )
