from __future__ import annotations

from typing import Any

from pydantic import Field, ValidationInfo, model_validator

from ..models import CoreModel
from ..signals import Signal
from ..types import ModuleType


class ModuleDefinition(CoreModel):
    """Base module definition"""

    module_type: ModuleType = Field(
        title="Module Type",
        description=(
            "Type of signal processing this module performs. Determines how "
            "signals flow through the module."
        ),
    )

    input_channels: dict[str, type[Signal]] = Field(
        default_factory=dict,
        title="Input Channels",
        description="Named input channels and their expected signal types",
    )

    output_channels: dict[str, type[Signal]] = Field(
        default_factory=dict,
        title="Output Channels",
        description="Named output channels and their produced signal types",
    )

    required_config: dict[str, type] = Field(
        default_factory=dict,
        title="Required Configuration",
        description="Configuration parameters required by this module",
    )

    optional_config: dict[str, type] = Field(
        default_factory=dict,
        title="Optional Configuration",
        description="Optional configuration parameters",
    )

    @model_validator(mode="after")
    def validate_channels(self) -> ModuleDefinition:
        """Validate channel configurations based on module type"""
        # if self.module_type == ModuleType.SOURCE:
        #     if self.input_channels:
        #         raise ValueError("Source modules cannot have input channels")
        # elif self.module_type == ModuleType.TAP:
        #     if self.output_channels:
        #         raise ValueError("Tap modules cannot have output channels")
        return self

    class Config:
        json_schema_extra = {
            "title": "Module Definition",
            "description": (
                "Defines a signal processing module's interface including "
                "channels and configuration."
            ),
        }


class ModuleInstance(CoreModel):
    """Runtime instance of a module with configuration."""

    definition: ModuleDefinition = Field(
        title="Module Definition",
        description="The module definition this instance implements",
    )

    config: dict[str, Any] = Field(
        default_factory=dict,
        title="Module Configuration",
        description="Configuration values for this module instance",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_config(cls, info: ValidationInfo | dict[str, Any]) -> dict[str, Any]:
        """Validate config matches definition requirements"""
        values = info if isinstance(info, dict) else (info.data or {})

        definition = values.get("definition")
        if not definition:
            return values

        config = values.get("config", {})

        # Validate required config parameters
        for param, param_type in definition.required_config.items():
            if param not in config:
                raise ValueError(f"Missing required config parameter: {param}")
            if not isinstance(config[param], param_type):
                raise ValueError(
                    f"Invalid type for config parameter {param}. "
                    f"Expected {param_type}, got {type(config[param])}"
                )

        # Validate optional config parameters
        for param, param_type in definition.optional_config.items():
            if param in config and not isinstance(config[param], param_type):
                raise ValueError(
                    f"Invalid type for config parameter {param}. "
                    f"Expected {param_type}, got {type(config[param])}"
                )

        # Check for unknown parameters
        valid_params = set(definition.required_config) | set(definition.optional_config)
        unknown = set(config) - valid_params
        if unknown:
            raise ValueError(f"Unknown config parameters: {', '.join(unknown)}")

        return values

    async def process(self, inputs: dict[str, Signal]) -> dict[str, Signal]:
        """Process input signals to outputs"""
        raise NotImplementedError

    async def validate_inputs(self, inputs: dict[str, Signal]) -> None:
        """Validate input signals match definition"""
        for channel, signal in inputs.items():
            if channel not in self.definition.input_channels:
                raise ValueError(f"Unknown input channel: {channel}")
            expected_type = self.definition.input_channels[channel]
            if not isinstance(signal, expected_type):
                raise ValueError(
                    f"Invalid signal type for channel {channel}. "
                    f"Expected {expected_type.__name__}, got {type(signal).__name__}"
                )
