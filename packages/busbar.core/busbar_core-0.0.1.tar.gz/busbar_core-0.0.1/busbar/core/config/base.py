from pathlib import Path
from typing import Any

import yaml
from pydantic import ConfigDict, Field, SecretStr

from ..models import CoreModel
from ..types import LogLevel, SecurityLevel


class AuditConfig(CoreModel):
    """Audit configuration settings"""

    security_level: SecurityLevel = Field(
        default=SecurityLevel.PUBLIC,
        title="Audit Security Level",
        description="Default security level for audit events",
    )
    batch_size: int = Field(
        default=1000,
        title="Batch Size",
        description="Maximum number of events per batch",
    )
    store_url: str = Field(
        default="memory://",
        title="Store URL",
        description="URL for the audit store",
    )
    encryption_key: SecretStr = Field(
        default=SecretStr(""),
        title="Encryption Key",
        description="Key for encrypting audit data",
    )


class SecurityConfig(CoreModel):
    """Security configuration settings"""

    level: SecurityLevel = Field(
        default=SecurityLevel.INTERNAL,
        description="Default security level for the system",
    )
    key: SecretStr = Field(
        ...,  # Required field
        description="Encryption key for security operations",
    )


class CoreConfig(CoreModel):
    """Base configuration for busbar core"""

    model_config = ConfigDict(extra="allow")  # Allow extra fields for backwards compatibility

    audit: AuditConfig = Field(
        default_factory=AuditConfig,
        description="Configuration for audit logging",
    )
    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        description="Default logging level",
    )
    secrets_file: Path | None = Field(
        default=None,
        description="Path to secrets file",
    )
    security: SecurityConfig = Field(
        ...,  # Required field
        description="Security configuration",
    )
    providers: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Configuration for enabled providers",
    )

    @classmethod
    def load(cls, path: Path) -> "CoreConfig":
        """Load configuration from file"""
        if not path.exists():
            return cls()

        with path.open() as f:
            data = yaml.safe_load(f)
            return cls.parse_obj(data)

    def merge(self, other: "CoreConfig") -> "CoreConfig":
        """Merge another config into this one"""
        data = self.dict()
        other_data = other.dict()

        # Deep merge dictionaries
        for key, value in other_data.items():
            if key in data and isinstance(data[key], dict):
                data[key].update(value)
            else:
                data[key] = value

        return CoreConfig.parse_obj(data)
