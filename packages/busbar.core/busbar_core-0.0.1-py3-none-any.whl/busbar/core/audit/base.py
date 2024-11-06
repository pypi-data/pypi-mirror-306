from __future__ import annotations  # Add this line at the top

import json
import traceback
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Protocol, runtime_checkable
from uuid import UUID, uuid4

from injector import Module, provider, singleton
from pydantic import Field, ValidationInfo, model_validator

from ..config import AuditConfig, CoreConfig
from ..models import CoreModel
from ..types import LogLevel, RiskLevel, SecurityLevel


class ChangeType(str, Enum):
    """Types of changes to track"""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    ACCESS = "access"


class Impact(str, Enum):
    """Change impact levels"""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Change(CoreModel):
    """Tracked change"""

    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime
    type: ChangeType
    impact: Impact
    security_level: SecurityLevel = Field(default=SecurityLevel.PUBLIC)
    risk_level: RiskLevel = Field(default=RiskLevel.LOW)

    # What changed
    resource_type: str
    resource_id: UUID | None
    field: str | None
    old_value: Any | None
    new_value: Any | None

    # Who changed it
    principal_id: UUID
    session_id: UUID | None

    # Context
    source: str | None
    correlation_id: UUID | None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    def validate_metadata_values(cls, info: ValidationInfo | dict[str, Any]) -> dict[str, Any]:
        """Ensure metadata values are JSON serializable"""
        values = info if isinstance(info, dict) else (info.data or {})
        metadata = values.get("metadata", {})
        if metadata:
            try:
                json.dumps(metadata)
            except TypeError:
                values["metadata"] = str(metadata)
        return values


class AuditEvent(CoreModel):
    """Audit log event"""

    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime
    level: LogLevel
    event_type: str
    message: str

    # Security context
    principal_id: UUID | None
    session_id: UUID | None
    security_level: SecurityLevel = Field(default=SecurityLevel.PUBLIC)
    risk_level: RiskLevel = Field(default=RiskLevel.LOW)

    # Source context
    module_id: UUID | None
    signal_id: UUID | None
    correlation_id: UUID | None

    # Details
    changes: list[Change] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: str | None
    stack_trace: str | None

    @model_validator(mode="before")
    def validate_metadata_values(cls, info: ValidationInfo | dict[str, Any]) -> dict[str, Any]:
        """Ensure metadata values are JSON serializable"""
        values = info if isinstance(info, dict) else (info.data or {})
        metadata = values.get("metadata", {})
        if metadata:
            try:
                json.dumps(metadata)
            except TypeError:
                values["metadata"] = str(metadata)
        return values


class AuditBatch:
    """Batched audit events"""

    def __init__(self, *, max_size: int = 1000) -> None:
        self.events: list[AuditEvent] = []
        self.created_at = datetime.now(timezone.utc)
        self.max_size = max_size

    def add_event(self, event: AuditEvent) -> None:
        """Add event to batch."""
        self.events.append(event)

    def is_full(self) -> bool:
        """Check if batch is full"""
        return len(self.events) >= self.max_size


@runtime_checkable
class AuditStore(Protocol):
    """Audit storage interface"""

    async def store_event(self, *, event: AuditEvent) -> None:
        """Store single event"""
        ...

    async def store_batch(self, *, batch: AuditBatch) -> None:
        """Store event batch"""
        ...

    async def get_events(
        self,
        *,
        start: datetime | None = None,
        end: datetime | None = None,
        filters: dict[str, Any] | None = None,
        limit: int | None = None,
    ) -> list[AuditEvent]:
        """Query audit events"""
        ...


class ConcreteAuditStore(AuditStore):
    """Concrete implementation of AuditStore"""

    url: str
    encryption_key: str

    def __init__(self, *, url: str, encryption_key: str) -> None:
        self.url = url
        self.encryption_key = encryption_key
        # Initialize connection to the audit storage using url and encryption_key

    async def store_event(self, *, event: AuditEvent) -> None:
        # Implementation to store a single event
        pass

    async def store_batch(self, *, batch: AuditBatch) -> None:
        # Implementation to store a batch of events
        pass

    async def get_events(
        self,
        *,
        start: datetime | None = None,
        end: datetime | None = None,
        filters: dict[str, Any] | None = None,
        limit: int | None = None,
    ) -> list[AuditEvent]:
        # Implementation to retrieve events based on criteria
        return []  # Replace with actual retrieval logic


class AuditService:
    """Audit service implementation."""

    def __init__(
        self,
        *,  # Enforce keyword-only arguments
        store: AuditStore,
        config: CoreConfig | AuditConfig,
    ) -> None:
        """Initialize audit service.

        Args:
            store: Audit event storage
            config: Core configuration or Audit configuration
        """
        self.store = store
        # Handle both CoreConfig and AuditConfig
        self.config = config.audit if isinstance(config, CoreConfig) else config
        self.batch_size = self.config.batch_size
        self._current_batch = AuditBatch(max_size=self.batch_size)

    @property
    def current_batch(self) -> AuditBatch:
        return self._current_batch

    async def log_event(
        self,
        *,  # Force keyword arguments
        event_type: str,
        message: str,
        level: LogLevel = LogLevel.INFO,
        security_level: SecurityLevel | None = None,
        risk_level: RiskLevel | None = None,
        changes: list[Change] | None = None,
        metadata: dict[str, Any] | None = None,
        error: Exception | None = None,
    ) -> None:
        # ...existing implementation...
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc),
            level=level,
            event_type=event_type,
            message=message,
            principal_id=None,
            session_id=None,
            module_id=None,
            signal_id=None,
            correlation_id=None,
            security_level=security_level or SecurityLevel.PUBLIC,
            risk_level=risk_level or RiskLevel.LOW,
            changes=changes or [],
            metadata=metadata or {},
            error=str(error) if error else None,
            stack_trace=traceback.format_exc() if error else None,
        )

        self.current_batch.add_event(event)
        if self.current_batch.is_full():
            await self.flush()

    async def flush(self) -> None:
        """Flush current batch."""
        if self.current_batch.events:
            await self.store.store_batch(batch=self.current_batch)
            self._current_batch = AuditBatch(max_size=self.batch_size)


class AuditModule(Module):
    """Audit service module"""

    @singleton
    @provider
    def provide_audit_store(self, config: CoreConfig) -> AuditStore:
        """Provide audit store"""
        return ConcreteAuditStore(
            url=config.audit.store_url,
            encryption_key=config.audit.encryption_key.get_secret_value(),
        )

    @singleton
    @provider
    def provide_audit_service(self, store: AuditStore, config: CoreConfig) -> AuditService:
        """Provide audit service"""
        return AuditService(store=store, config=config.audit)  # Pass audit config directly
