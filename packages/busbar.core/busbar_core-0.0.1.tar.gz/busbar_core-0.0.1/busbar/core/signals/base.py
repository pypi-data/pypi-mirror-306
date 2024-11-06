from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from typing import (
    Annotated,
    Any,
    Literal,
    TypeVar,
)
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator  # Added import

from ..types import SignalType

T = TypeVar("T")


class Signal(BaseModel):  # Changed inheritance from CoreModel to BaseModel
    """Base class for all signals"""

    signal_type: SignalType = Field(
        title="Signal Type",
        description=(
            "Type of signal being transmitted. Determines how the signal "
            "value should be interpreted and processed."
        ),
    )

    value: Any = Field(
        title="Signal Value",
        description="The actual value being transmitted through the signal",
    )

    source_id: UUID | None = Field(
        default=None,
        title="Source ID",
        description="ID of the module that generated this signal",
    )

    target_id: UUID | None = Field(
        default=None,
        title="Target ID",
        description="ID of the module this signal is intended for",
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Timestamp",
        description="When this signal was generated",
        json_schema_extra={"format": "date-time"},
    )

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=True,  # Allow SignalType enum
        use_enum_values=True,  # Added for proper enum handling
    )


NumericValue = Annotated[
    float,
    Field(
        ...,
        description="Numeric value for the CV signal",
        json_schema_extra={"type": "number"},
    ),
]


class CVSignal(Signal):
    """Control voltage signal with numeric values"""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    signal_type: Literal[SignalType.CV] = Field(
        default=SignalType.CV,
        frozen=True,
    )
    value: NumericValue

    @field_validator("value", mode="before")
    @classmethod
    def validate_numeric(cls, v: Any) -> float:
        """Validate that the value is numeric."""
        if isinstance(v, bool):
            raise ValueError("CV signal value cannot be boolean")
        if not isinstance(v, int | float):
            raise ValueError("CV signal value must be numeric (int or float)")
        return float(v)


class GateSignal(Signal):
    """Gate signal with boolean values"""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        arbitrary_types_allowed=True,
        strict=True,  # Add strict validation
    )

    signal_type: Literal[SignalType.GATE] = Field(
        default=SignalType.GATE,
        frozen=True,
    )
    value: bool = Field(
        ...,
        description="Boolean value for the gate signal",
        strict=True,  # Add strict validation
    )

    @field_validator("value", mode="before")
    @classmethod
    def validate_bool(cls, v: Any) -> bool:
        """Validate that the value is boolean."""
        if not isinstance(v, bool):
            raise ValueError("Gate signal value must be boolean")
        return v


class SignalBus:
    """Core signal routing system"""

    def __init__(self) -> None:
        self._subscribers: dict[str, set[Callable[[Signal], Awaitable[None]]]] = {}

    async def publish(self, signal: Signal, channel: str) -> None:
        """
        Publish signal to channel.

        Args:
            signal: The signal to publish.
            channel: The channel to publish the signal to.
        """
        if channel not in self._subscribers:
            return

        for callback in self._subscribers[channel]:
            await callback(signal)

    def subscribe(self, channel: str, callback: Callable[[Signal], Awaitable[None]]) -> None:
        """
        Subscribe to channel.

        Args:
            channel: The channel to subscribe to.
            callback: The callback to invoke when a signal is published to the channel.
        """
        if channel not in self._subscribers:
            self._subscribers[channel] = set()
        self._subscribers[channel].add(callback)

    def unsubscribe(self, channel: str, callback: Callable[[Signal], Awaitable[None]]) -> None:
        """
        Unsubscribe from channel.

        Args:
            channel: The channel to unsubscribe from.
            callback: The callback to remove from the channel's subscribers.
        """
        if channel in self._subscribers:
            self._subscribers[channel].discard(callback)
            if not self._subscribers[channel]:
                del self._subscribers[channel]
