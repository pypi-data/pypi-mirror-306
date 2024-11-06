from collections.abc import Awaitable, Callable
from typing import TypeVar

from injector import inject

from ..audit import AuditService, AuditStore
from ..config import AuditConfig
from ..security.security_service import SecurityService
from ..types import RiskLevel, SecurityLevel
from .client import APIEndpoint, APIRequest

T = TypeVar("T")
Response = TypeVar("Response")


@inject
def endpoint(
    *,  # Force all args to be keyword-only
    request_model: type[T],
    response_model: type[Response],
    security_service: SecurityService,  # Injected SecurityService
    audit_service: AuditService,  # Injected AuditService
    audit_store: AuditStore,  # Inject AuditStore
    config: AuditConfig,  # Inject AuditConfig
    security_level: SecurityLevel = SecurityLevel.INTERNAL,
    risk_level: RiskLevel = RiskLevel.LOW,
) -> Callable:
    """Decorator to create secure API endpoints"""

    def decorator(
        handler: Callable[[APIRequest[T]], Awaitable[Response]],
    ) -> APIEndpoint[T, Response]:
        class DecoratedEndpoint(APIEndpoint[T, Response]):
            async def handle(self, request: APIRequest[T]) -> Response:
                return await handler(request)

        return DecoratedEndpoint(
            request_model=request_model,
            response_model=response_model,
            security_service=security_service,  # Use injected SecurityService
            audit_service=audit_service,  # Use injected AuditService
            security_level=security_level,
            risk_level=risk_level,
        )

    return decorator
