"""Security event and orchestration context handling."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..types import RiskLevel, SecurityLevel


class SecurityEventType(str, Enum):
    """Types of security events."""

    AUTH_DELEGATION = "auth_delegation"
    TOKEN_EXCHANGE = "token_exchange"
    PERMISSION_CHECK = "permission_check"
    SESSION_CREATE = "session_create"
    SESSION_TERMINATE = "session_terminate"
    ACCESS_DENIED = "access_denied"
    CONFIG_CHANGE = "config_change"
    SYSTEM_ACCESS = "system_access"


class SystemDelegation(BaseModel):
    """Record of system-to-system security delegation."""

    model_config = ConfigDict(frozen=True)

    source_system: str = Field(..., min_length=1)
    target_system: str = Field(..., min_length=1)
    delegation_type: SecurityEventType
    timestamp: datetime
    context: dict[str, Any] = Field(default_factory=dict)
    principal_id: UUID
    original_principal_id: UUID
    session_id: UUID
    security_level: SecurityLevel = SecurityLevel.INTERNAL
    risk_level: RiskLevel = RiskLevel.LOW


class ValidationResult(BaseModel):
    """Result of a security validation operation."""

    model_config = ConfigDict(frozen=True)

    valid: bool
    errors: list[str] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)


class OrchestrationContext(BaseModel):
    """Security context for orchestration operations."""

    model_config = ConfigDict(validate_assignment=True)

    principal_id: UUID | None = None
    session_id: UUID | None = None
    security_level: SecurityLevel = Field(default=SecurityLevel.INTERNAL)
    risk_level: RiskLevel = Field(default=RiskLevel.LOW)
    delegation_chain: list[SystemDelegation] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def add_delegation(self, delegation: SystemDelegation) -> None:
        """Add delegation to the chain."""
        self.delegation_chain.append(delegation)

    async def validate_operation(
        self, operation_type: str, required_level: SecurityLevel, **context: Any
    ) -> ValidationResult:
        """Validate security context for an operation."""

        # Higher enum index means higher security
        security_levels = list(SecurityLevel)
        current_level_idx = security_levels.index(self.security_level)
        required_level_idx = security_levels.index(required_level)

        valid = current_level_idx >= required_level_idx

        result = ValidationResult(
            valid=valid,
            context={
                "operation_type": operation_type,
                "required_level": required_level,
                "actual_level": self.security_level,
                **context,
            },
        )

        if not valid:
            result.errors.append("insufficient_security_level")

        return result
