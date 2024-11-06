"""
This module defines core types and enumerations used throughout the busbar system.
"""

from enum import Enum
from typing import TYPE_CHECKING, Annotated, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, confloat, conint, constr

if TYPE_CHECKING:
    pass

# Core type variables
SignalValue = TypeVar("SignalValue")
ConfigValue = TypeVar("ConfigValue")

# Validated string types
# Remove duplicate definitions of VersionStr
SlugStr = Annotated[str, Field(description="Provider identifier")]
VersionStr = Annotated[str, Field(description="Provider version")]
NameStr = constr(min_length=1, max_length=255)
ShortCodeStr = constr(pattern=r"^[A-Z]{2}-[A-Z0-9]{6}$")
SemVerStr = constr(
    pattern=(
        r"^(?P<major>0|[1-9]\d*)\."
        r"(?P<minor>0|[1-9]\d*)\."
        r"(?P<patch>0|[1-9]\d*)"
        r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?"
        r":\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )
)
PathStr = constr(pattern=r"^[a-zA-Z0-9\-_\/\.]+$")
KeyStr = constr(pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$", min_length=1, max_length=64)

# Validated numeric types
NormalizedFloat = confloat(ge=0.0, le=1.0)
PositiveInt = conint(gt=0)
NonNegativeInt = conint(ge=0)

# Resource identifiers
ResourceId = Union[UUID, Annotated[str, SlugStr]]


# Core enumerations
class SecurityLevel(str, Enum):
    """Security classification levels."""

    PUBLIC = "public"  # No security implications
    INTERNAL = "internal"  # Internal system data
    SENSITIVE = "sensitive"  # Business sensitive
    SECRET = "secret"  # Security critical


class RiskLevel(str, Enum):
    """Risk assessment levels."""

    NONE = "none"  # No risk
    LOW = "low"  # Minor impact
    MEDIUM = "medium"  # Significant impact
    HIGH = "high"  # Major impact
    CRITICAL = "critical"  # Catastrophic impact

    def to_log_level(self) -> str:
        """Convert risk level to log level"""
        return {
            self.NONE: "DEBUG",
            self.LOW: "INFO",
            self.MEDIUM: "WARNING",
            self.HIGH: "ERROR",
            self.CRITICAL: "CRITICAL",
        }[self]


class CapabilityType(str, Enum):
    """Core capability types."""

    AUTH = "auth"
    SECRETS = "secrets"
    VCS = "vcs"
    CUSTOM = "custom"


class CapabilityContext(BaseModel):
    """Context for capability filtering."""

    model_config = ConfigDict(frozen=True)

    required_features: set[str] = Field(
        default_factory=set, description="Features that must be present"
    )
    allowed_features: set[str] = Field(
        default_factory=set, description="Features that may be used if available"
    )
    security_level: SecurityLevel = Field(
        default=SecurityLevel.PUBLIC, description="Minimum security level required"
    )
    risk_level: RiskLevel = Field(
        default=RiskLevel.LOW, description="Maximum acceptable risk level"
    )


class ConnectionType(str, Enum):
    """Types of connections for providers."""

    WEB = "web"
    API = "api"
    CLI = "cli"


class InterfaceType(str, Enum):
    """Types of interfaces for providers."""

    API = "api"
    CLI = "cli"
    WEB = "web"


class SignalTypeModel(BaseModel):
    """Base model for signal types."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    type: str = Field(..., description="The type of signal")


class SignalType:
    """Signal type constants."""

    CV = "cv"  # Control voltage (analog)
    GATE = "gate"  # Gate (digital)

    @classmethod
    def to_model(cls, type_str: str) -> SignalTypeModel:
        """Convert string type to model"""
        return SignalTypeModel(type=type_str)


class ModuleType(str, Enum):
    """Types of processing modules."""

    SOURCE = "source"  # Generates signals
    MODIFY = "modify"  # Modifies signals
    COMPARE = "compare"  # Logic/threshold
    ENVELOPE = "envelope"  # Shape over time
    TAP = "tap"  # Monitor/capture
    TRIGGER = "trigger"  # Generate events


class ErrorSeverity(str, Enum):
    """Error severity levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogLevel(str, Enum):
    """Logging levels."""

    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AccessLevel(str, Enum):
    """Access control levels."""

    NONE = "none"  # No access
    READ = "read"  # Read only
    WRITE = "write"  # Read and write
    ADMIN = "admin"  # Full control


class ExclusionType(str, Enum):
    """Types of configuration exclusions."""

    KEY = "key"  # Exclude specific config keys
    FILE = "file"  # Exclude entire files/paths
    CAPABILITY = "capability"  # Exclude specific capabilities
    FEATURE = "feature"  # Exclude specific capability features


class ExclusionReason(str, Enum):
    """Reasons for configuration exclusions."""

    SECURITY = "security"  # Security requirement
    COMPLIANCE = "compliance"  # Compliance requirement
    UNSUPPORTED = "unsupported"  # Feature not supported
    CUSTOM = "custom"  # Custom reason
