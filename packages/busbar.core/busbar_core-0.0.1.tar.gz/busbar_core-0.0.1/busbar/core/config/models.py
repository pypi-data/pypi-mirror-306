"""Configuration schema definitions."""

from pydantic import BaseModel, Field

from ..types import (
    ErrorSeverity,
    ExclusionReason,
    ExclusionType,
    RiskLevel,
    SecurityLevel,
)


class ExceptionConfig(BaseModel):
    """Exception configuration."""

    severity: ErrorSeverity = Field(
        ...,
        description="Severity level for this exception",
    )
    risk_level: RiskLevel = Field(
        ...,
        description="Risk level associated with this exception",
    )


class FeatureConfig(BaseModel):
    """Feature configuration."""

    description: str = Field(
        ...,
        description="Feature description",
    )
    input: str = Field(
        ...,
        description="Fully qualified input model path",
    )
    output: str = Field(
        ...,
        description="Fully qualified output model path",
    )
    exceptions: dict[str, ExceptionConfig] = Field(
        default_factory=dict,
        description="Exception configurations keyed by exception name",
    )


class CapabilityConfig(BaseModel):
    """Capability configuration."""

    title: str = Field(
        ...,
        description="Display title for the capability",
    )
    description: str = Field(
        ...,
        description="Detailed capability description",
    )
    security_level: SecurityLevel = Field(
        ...,
        description="Required security level",
    )
    risk_level: RiskLevel = Field(
        ...,
        description="Associated risk level",
    )
    features: dict[str, FeatureConfig] = Field(
        ...,
        description="Feature configurations keyed by feature name",
    )


class SecurityContextConfig(BaseModel):
    """Security context configuration."""

    description: str = Field(
        ...,
        description="Context description",
    )
    security_level: SecurityLevel = Field(
        ...,
        description="Required security level",
    )
    risk_level: RiskLevel = Field(
        ...,
        description="Associated risk level",
    )
    requires: list[str] = Field(
        default_factory=list,
        description="Required capabilities",
    )


class ExclusionConfig(BaseModel):
    """Configuration exclusion definition."""

    type: ExclusionType = Field(
        ...,
        description="Type of exclusion",
    )
    pattern: str = Field(
        ...,
        description="Pattern to match for exclusion",
    )
    reason: ExclusionReason = Field(
        ...,
        description="Reason for exclusion",
    )
    details: str = Field(
        ...,
        description="Detailed explanation",
    )
    allowed_override: bool = Field(
        default=False,
        description="Whether this exclusion can be overridden",
    )


class ExclusionList(BaseModel):
    """List of configuration exclusions."""

    version: str = Field(..., description="Exclusion list version")
    exclusions: list[ExclusionConfig] = Field(
        default_factory=list,
        description="List of exclusions",
    )


class BusbarConfig(BaseModel):
    """Root configuration model."""

    version: str = Field(
        ...,
        description="Configuration schema version",
    )
    capabilities: dict[str, CapabilityConfig] = Field(
        ...,
        description="Capability configurations keyed by capability name",
    )
    security_contexts: dict[str, SecurityContextConfig] = Field(
        ...,
        description="Security context configurations keyed by context name",
    )
