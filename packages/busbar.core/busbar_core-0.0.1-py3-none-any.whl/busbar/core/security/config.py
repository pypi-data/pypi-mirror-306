from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from ..types import RiskLevel, SecurityLevel


class ConfigurationChangeTracker:
    """Tracks configuration changes without storing sensitive data"""

    def __init__(self, *, audit_service) -> None:
        self.audit = audit_service
        self.sensitive_keys: set[str] = {"password", "secret", "key", "token"}

    def _redact_sensitive(self, data: dict[str, Any]) -> dict[str, Any]:
        """Redact sensitive values from configuration"""
        redacted = copy.deepcopy(data)
        for key, value in redacted.items():
            if any(s in key.lower() for s in self.sensitive_keys):
                redacted[key] = "**REDACTED**"
            elif isinstance(value, dict):
                redacted[key] = self._redact_sensitive(value) if isinstance(value, dict) else value

        return redacted

    async def track_change(
        self,
        *,  # Force keyword arguments
        path: str,
        change_type: str,
        principal_id: UUID,
        old_config: dict[str, Any],
        new_config: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        from ..audit import (  # Moved import inside the function
            Change,
            ChangeType,
            Impact,
        )

        # Redact sensitive values
        old_safe = self._redact_sensitive(old_config) if old_config else None
        new_safe = self._redact_sensitive(new_config) if new_config else None

        # Create change record
        change = Change(
            timestamp=datetime.now(timezone.utc),
            type=ChangeType.UPDATE,
            impact=Impact.MEDIUM,
            security_level=SecurityLevel.INTERNAL,
            risk_level=RiskLevel.MEDIUM,
            resource_type="configuration",
            resource_id=None,
            field=path,
            old_value=old_safe,
            new_value=new_safe,
            principal_id=principal_id,
            metadata=metadata or {},
            # Add required fields
            session_id=None,  # No active session for config changes
            source="config_tracker",
            correlation_id=str(uuid4()),  # Generate a unique correlation ID
        )

        # Log through audit service
        await self.audit.log_event(
            event_type="config_change",
            message=f"Configuration change at {path}",
            changes=[change],
            metadata=metadata,
            security_level=SecurityLevel.INTERNAL,
            risk_level=RiskLevel.MEDIUM,
        )
