from pathlib import Path
from typing import Any

import yaml
from injector import Module, provider, singleton

from busbar.core.audit import AuditService
from busbar.core.config import CoreConfig
from busbar.core.models import ProviderDefinition
from busbar.core.security.security_service import SecurityService

from .security.services import (
    Authenticator,
    Authorizer,
    CredentialStore,
    SessionStore,
)


class CoreModule(Module):
    """core_service_module"""

    @singleton
    @provider
    def provide_config(self) -> CoreConfig:
        """provide_core_configuration"""
        config = CoreConfig()

        # Load config files in order
        paths = [
            Path(__file__).parent / "config" / "default.yml",
            Path.home() / ".busbar" / "config.yml",
            Path("busbar.yml"),
        ]

        for path in paths:
            if path.exists():
                with path.open() as f:
                    data = yaml.safe_load(f)
                    config = config.merge(CoreConfig.parse_obj(data))

        return config

    @singleton
    @provider
    def provide_security_service(self, config: CoreConfig) -> SecurityService:
        """provide_security_service"""
        return SecurityService(encryption_key=config.security.key)

    @singleton
    @provider
    def provide_audit_service(
        self, config: CoreConfig, security_service: SecurityService
    ) -> AuditService:
        """provide_audit_service"""
        if not hasattr(config, "audit"):
            raise ValueError("audit_configuration_not_found")
        return AuditService(
            store=config.audit.store_url,
            config=config.audit,
        )

    @singleton
    @provider
    def provide_credential_store(self, config: CoreConfig) -> CredentialStore:
        """provide_credential_store"""
        return CredentialStore(encryption_key=config.security.key)

    @singleton
    @provider
    def provide_session_store(self, config: CoreConfig) -> SessionStore:
        """provide_session_store"""
        return SessionStore(encryption_key=config.security.key)

    @singleton
    @provider
    def provide_authenticator(
        self,
        credential_store: CredentialStore,
        session_store: SessionStore,
        security_service: SecurityService,
    ) -> Authenticator:
        """provide_authenticator"""
        return Authenticator(
            credential_store=credential_store,
            session_store=session_store,
            security_service=security_service,
        )

    @singleton
    @provider
    def provide_authorizer(self, session_store: SessionStore) -> Authorizer:
        """provide_authorizer"""
        return Authorizer(session_store=session_store)


class ProviderModule(Module):
    """provider_registration_module"""

    def __init__(self):
        self._providers: dict[str, type[Any]] = {}

    def register_provider(self, definition: ProviderDefinition, module: Module) -> None:
        """register_provider_module"""
        if definition.slug in self._providers:
            raise ValueError(f"provider_{definition.slug}_already_registered")

        self._providers[definition.slug] = module

    def get_provider(self, slug: str) -> type[Any] | None:
        """get_registered_provider"""
        return self._providers.get(slug)

    def get_providers_for_system(self, system_type: str) -> dict[str, type[Any]]:
        """get_providers_for_system_type"""
        return {
            slug: provider
            for slug, provider in self._providers.items()
            if system_type in provider.get_capabilities()
        }

    def configure(self, binder):
        """configure_bindings"""
        for provider in self._providers.values():
            binder.install(provider)
