"""
Core provider system implementation.
"""

from pathlib import Path
from typing import Any

import yaml
from injector import Injector
from pydantic import BaseModel, Field, HttpUrl

from ..types import (
    CapabilityContext,
    CapabilityType,
    SlugStr,
    VersionStr,
)
from .capabilities import (
    AuthCapability,
    BaseCapability,
    CapabilityConfig,
    SecretsCapability,
    VCSCapability,
)


class ProviderBase(BaseModel):
    """Base provider definition"""

    name: str = Field(..., description="Provider display name")
    slug: SlugStr = Field(..., description="Provider identifier")
    version: VersionStr = Field(..., description="Provider version")
    description: str = Field(..., description="Provider description")
    website: HttpUrl | None = Field(None, description="Provider website URL")
    documentation: HttpUrl | None = Field(None, description="Provider documentation URL")

    # Core capabilities
    auth: AuthCapability | None = Field(None, description="Authentication capability")
    vcs: VCSCapability | None = Field(None, description="Version control capability")
    secrets: SecretsCapability | None = Field(None, description="Secrets management capability")

    # Custom capabilities
    capabilities: dict[str, BaseCapability] = Field(
        default_factory=dict, description="Custom capabilities"
    )
    _injector: Injector = Injector()

    @classmethod
    def load_capabilities(cls, path: str | Path) -> "ProviderBase":
        """Load provider configuration from file"""
        path = Path(path)
        if not path.exists():
            raise ValueError(f"Config file not found: {path}")

        with path.open() as f:
            config = yaml.safe_load(f)

        # Load built-in capabilities
        provider = cls(**config.get("provider", {}))
        if "capabilities" in config:
            cap_config = CapabilityConfig(**config["capabilities"])

            # Dynamically load capabilities
            for cap_type, cap_data in cap_config.capabilities.items():
                if cap_data:
                    capability_class = globals().get(f"{cap_type.capitalize()}Capability")
                    if capability_class:
                        provider.capabilities[cap_type] = capability_class(**cap_data)
                    else:
                        provider.capabilities[cap_type] = BaseCapability(**cap_data)

        return provider

    def register_capability(
        self, *, capability: BaseCapability, implementation: type[Any] | None = None
    ) -> None:
        """Register a capability with optional implementation"""
        key = f"{capability.type.value}.{capability.name}"
        self.capabilities[key] = capability

        if implementation:
            capability.register_implementation(implementation, self._injector)

    def filter_capabilities(self, context: CapabilityContext) -> dict[str, BaseCapability]:
        """Filter capabilities based on context"""
        filtered = {}

        for key, capability in self.capabilities.items():
            filtered_cap = capability.filter_context(context)
            if filtered_cap:
                filtered[key] = filtered_cap

        return filtered

    def get_implementation(self, capability_type: CapabilityType, name: str) -> type[Any] | None:
        """Get implementation for capability"""
        key = f"{capability_type.value}.{name}"
        capability = self.capabilities.get(key)
        return capability.implementation if capability else None


class ProviderRegistry:
    """Provider registration and discovery."""

    def __init__(self, capability_config: CapabilityConfig):
        self.capabilities = capability_config.capabilities
        self.providers: dict[str, ProviderBase] = {}

    def register(self, definition: ProviderBase, module: Any | None) -> None:
        if definition.slug in self.providers:
            raise ValueError("Provider already registered")
        self.providers[definition.slug] = definition
        if module:
            module.register_provider(definition, definition.__class__)
            module.get_provider(definition.slug)  # Invoke get_provider after registration

    def supports_capability(self, capability_type: str) -> bool:
        return capability_type in self.capabilities

    def get_provider(self, slug: str) -> ProviderBase | None:
        return self.providers.get(slug)

    def get_providers_with_capability(self, capability_type: str) -> list[str]:
        """Retrieve providers that support the specified capability type."""
        return [
            slug
            for slug, provider in self.providers.items()
            if isinstance(getattr(provider, capability_type, None), BaseCapability)
        ]

    def get_providers_for_system(self, system: str) -> list[str]:
        """Retrieve providers that support the specified system."""
        return [
            slug
            for slug, provider in self.providers.items()
            if any(
                cap.system == system
                for cap in provider.capabilities.values()
                if isinstance(cap, VCSCapability)
            )
        ]
