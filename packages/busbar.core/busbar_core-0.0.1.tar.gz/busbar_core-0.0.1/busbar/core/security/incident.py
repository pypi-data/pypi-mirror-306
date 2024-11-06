from typing import TYPE_CHECKING, Any  # Add TYPE_CHECKING import
from uuid import UUID

from ..types import RiskLevel
from .events import SecurityEventType

if TYPE_CHECKING:
    from ..audit.base import AuditService  # Import the type alias


class SecurityIncidentCoordinator:
    """Coordinates security incident response across systems"""

    def __init__(self, audit_service: "AuditService"):
        self.audit = audit_service
        self.handlers: dict[SecurityEventType, list[str]] = {}

    def register_handler(self, event_type: SecurityEventType, handler_id: str) -> None:
        """Register incident handler for event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler_id)

    async def handle_security_event(
        self,
        event_type: SecurityEventType,
        source_system: str,
        context: dict[str, Any],
        severity: RiskLevel,
        related_principals: list[UUID],
    ) -> None:
        """Handle security event across systems"""
        # Log incident
        await self.audit.log_event(
            event_type=event_type.value,
            message=f"Security event from {source_system}",
            level=severity.to_log_level(),
            risk_level=severity,
            metadata={
                "source_system": source_system,
                "context": context,
                "related_principals": [str(p) for p in related_principals],
            },
        )

        # Notify registered handlers
        for handler_id in self.handlers.get(event_type, []):
            # Implementation would dispatch to registered incident handlers
            pass
