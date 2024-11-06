import asyncio
import json
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from typing import (
    Any,
    Generic,
    TypeVar,
)
from uuid import UUID, uuid4

import httpx
from cachetools import TTLCache
from injector import inject
from pydantic import BaseModel, ConfigDict, Field

from ..audit import AuditService
from ..models import CoreModel
from ..security.events import OrchestrationContext, SecurityEventType
from ..security.security_service import SecurityService
from ..types import LogLevel, RiskLevel, SecurityLevel

T = TypeVar("T", bound=BaseModel)
ResponseType: TypeVar = TypeVar("ResponseType", bound=BaseModel)
ResponseModelType = TypeVar("ResponseModelType", bound=BaseModel)


class APIError(Exception):
    """Base API error."""

    def __init__(
        self,
        message: str,
        *,  # Enforce keyword-only arguments
        code: str,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class APIRequest(CoreModel, Generic[T]):
    """Base API request wrapper."""

    id: UUID = Field(
        default_factory=uuid4,
        description="Unique request identifier.",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Request timestamp.",
    )
    security_context: OrchestrationContext = Field(
        ...,
        description="Security context of the request.",
    )
    data: T = Field(
        ...,
        description="Request data payload.",
    )

    model_config = ConfigDict(title="APIRequest", frozen=True)


class APIResponse(CoreModel, Generic[ResponseType]):
    """Base API response wrapper"""

    request_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status_code: int = Field(
        ..., description="HTTP status code of the response."
    )  # Added status_code
    data: ResponseType = Field(..., description="Response data payload.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class APICache:
    """API response caching"""

    def __init__(self, ttl: int = 300):
        self.etag_cache = TTLCache(maxsize=1000, ttl=ttl)
        self.response_cache = TTLCache(maxsize=1000, ttl=ttl)

    async def get_etag(self, key: str) -> str | None:
        return self.etag_cache.get(key)

    async def set_etag(self, key: str, etag: str) -> None:
        self.etag_cache[key] = etag

    async def get_response(self, key: str) -> httpx.Response | None:
        cached = self.response_cache.get(key)
        if cached and isinstance(cached, dict):
            # Create a mock response with cached data
            response = httpx.Response(200, json=cached)
            return response
        return cached

    async def set_response(self, key: str, response: httpx.Response) -> None:
        try:
            # Cache the JSON content
            self.response_cache[key] = response.json()
        except Exception:
            # Fall back to raw content if not JSON
            self.response_cache[key] = response.text


class RateLimiter:
    """Rate limit tracking and management"""

    def __init__(self, *, testing: bool = False):
        self.reset_time: datetime | None = None
        self.remaining: int | None = None
        self.max_retries: int = 3
        self.base_delay: float = 1.0
        self.testing = testing

    async def check_limit(self, response: httpx.Response) -> None:
        """Update rate limit info from response"""
        if "X-RateLimit-Remaining" in response.headers:
            self.remaining = int(response.headers["X-RateLimit-Remaining"])

        if "X-RateLimit-Reset" in response.headers:
            reset_timestamp = int(response.headers["X-RateLimit-Reset"])
            self.reset_time = datetime.fromtimestamp(reset_timestamp)

    async def handle_limit(self, retry_count: int = 0) -> None:
        """Handle rate limiting with exponential backoff"""
        if retry_count >= self.max_retries:
            raise APIError("Rate limit exceeded", "rate_limit_exceeded", 429)

        if self.reset_time and not self.testing:
            wait_time = (self.reset_time - datetime.now()).total_seconds()
            wait_time = max(wait_time, 0)
            wait_time += self.base_delay * (2**retry_count)  # Exponential backoff
            await asyncio.sleep(wait_time)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


@inject
class SecureAPIClient(Generic[ResponseModelType]):
    """Base secure API client."""

    def __init__(
        self,  # Remove * to allow self as positional
        *,  # Force remaining args to be keyword-only
        response_model: type[ResponseModelType],
        security_service: SecurityService,
        audit_service: AuditService,
        base_url: str,
        security_level: SecurityLevel = SecurityLevel.INTERNAL,
        risk_level: RiskLevel = RiskLevel.LOW,
        testing: bool = False,
    ) -> None:
        self.response_model = response_model
        self.security_service = security_service
        self.audit_service = audit_service
        self.base_url = base_url.rstrip("/")
        self.security_level = security_level
        self.risk_level = risk_level
        # Add short timeouts for testing
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(1.0) if testing else httpx.Timeout(30.0)
        )
        self.cache = APICache()
        self.rate_limiter = RateLimiter(testing=testing)

    async def close(self) -> None:
        await self.client.aclose()

    async def _check_response(self, response: httpx.Response) -> None:
        """Check response status and raise appropriate errors"""
        if response.status_code == 304:
            return
        if response.is_success:
            return

        error_data = {}
        try:
            error_data = response.json()
        except Exception:
            pass

        # Ensure that log_event is awaited
        await self.audit_service.log_event(
            event_type="api_request_error",
            message="HTTP 500 error",
            level=LogLevel.ERROR,
            security_level=self.security_level,
            risk_level=self.risk_level,
            metadata={
                "method": response.request.method if response.request else "UNKNOWN",
                "url": response.request.url.path if response.request else "UNKNOWN",
                "status_code": response.status_code,
                "error": error_data,
            },
        )

        raise APIError(
            message=str(error_data),
            code="request_failed",
            status_code=response.status_code,
            details=error_data,
        )

    async def _make_request(
        self,
        *,
        method: str,
        url: str,
        security_context: OrchestrationContext,
        **kwargs: Any,
    ) -> APIResponse[ResponseModelType]:
        full_url = f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"
        json_data = kwargs.get("json")
        if json_data:
            if isinstance(json_data, BaseModel):
                kwargs["content"] = json_data.model_dump_json()
                kwargs.pop("json")
            else:
                kwargs["content"] = json.dumps(json_data, default=str)
                kwargs.pop("json")
        # Ensure the content type is set to application/json
        headers = kwargs.get("headers", {})
        headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers
        # Remove 'security_context' from kwargs if present
        kwargs.pop("security_context", None)

        # Check for cached response
        cached_response = await self.cache.get_response(full_url)
        if cached_response:
            headers["If-None-Match"] = await self.cache.get_etag(full_url)

        response = await self.client.request(method=method, url=full_url, **kwargs)

        if response.status_code == 200:
            response_data = response.json()
            data_model = self.response_model(**response_data)
            # Cache the response
            await self.cache.set_response(full_url, response)
            await self.cache.set_etag(full_url, response.headers.get("ETag", ""))
            return APIResponse(
                request_id=uuid4(),
                status_code=response.status_code,
                data=data_model,
            )
        elif response.status_code == 304 and cached_response:
            # Return cached response
            response_data = cached_response.json()
            data_model = self.response_model(**response_data)
            return APIResponse(
                request_id=uuid4(),
                status_code=response.status_code,
                data=data_model,
            )
        elif response.status_code == 429:
            # Handle rate limiting
            await self.rate_limiter.check_limit(response)
            raise APIError(
                code="rate_limit_exceeded",
                message="Rate limit exceeded",
                status_code=response.status_code,
            )
        elif not response.is_success:
            # Ensure the error is raised
            await self._check_response(response)


class APIEndpoint(Generic[T, ResponseType]):
    """Base API endpoint handler with security"""

    def __init__(
        self,
        request_model: type[T],
        response_model: type[ResponseType],
        security_service: SecurityService,
        audit_service: AuditService,
        security_level: SecurityLevel = SecurityLevel.INTERNAL,
        risk_level: RiskLevel = RiskLevel.LOW,
    ):
        self.request_model = request_model
        self.response_model = response_model
        self.security_service = security_service
        self.audit_service = audit_service
        self.security_level = security_level
        self.risk_level = risk_level
        self.pre_request_hooks: list[Callable[[APIRequest[T]], Awaitable[None]]] = []
        self.post_request_hooks: list[
            Callable[[APIRequest[T], APIResponse[ResponseType]], Awaitable[None]]
        ] = []

    async def pre_process(self, request: APIRequest[T]) -> None:
        """Pre-process request with security validation"""
        # Validate security context
        result = await request.security_context.validate_operation(
            "api_request",
            self.security_level,
            endpoint=self.__class__.__name__,
            request_id=request.id,
        )
        if not result.valid:
            raise APIError(
                message="Insufficient security context",
                code="insufficient_security",
                status_code=403,
                details=result.context,
            )

        # Run pre-request hooks
        for hook in self.pre_request_hooks:
            await hook(request)

    async def post_process(
        self, request: APIRequest[T], response: APIResponse[ResponseType]
    ) -> None:
        """Post-process response with audit trail"""
        # Run post-request hooks
        for hook in self.post_request_hooks:
            await hook(request, response)

        # Audit request completion
        await self.audit_service.log_event(
            event_type=SecurityEventType.TOKEN_EXCHANGE,
            message=f"API request completed: {self.__class__.__name__}",
            security_level=self.security_level,
            risk_level=self.risk_level,
            metadata={
                "request_id": str(request.id),
                "endpoint": self.__class__.__name__,
                "principal_id": request.security_context.principal_id,
                "session_id": request.security_context.session_id,
            },
        )

    def pre_request(self, hook: Callable[[APIRequest[T]], Awaitable[None]]) -> None:
        """Add pre-request hook"""
        self.pre_request_hooks.append(hook)

    def post_request(
        self,
        hook: Callable[[APIRequest[T], APIResponse[ResponseType]], Awaitable[None]],
    ) -> None:
        """Add post-request hook"""
        self.post_request_hooks.append(hook)

    async def handle(self, request: APIRequest[T]) -> ResponseType:
        """Handle request (to be implemented by subclasses)"""
        raise NotImplementedError

    async def __call__(self, request: APIRequest[T]) -> APIResponse[ResponseType]:
        """Handle API request with full security lifecycle"""
        try:
            # Pre-process
            await self.pre_process(request)

            # Handle request
            response_data = await self.handle(request=request)

            # Create response
            response = APIResponse(
                request_id=request.id,
                status_code=200,  # Add status_code
                data=response_data,
            )

            # Post-process
            await self.post_process(request, response)

            return response

        except Exception as e:
            # Audit error
            await self.audit_service.log_event(
                event_type="api_request_error",
                message=str(e),
                level="ERROR",
                security_level=self.security_level,
                risk_level=self.risk_level,
                metadata={
                    "request_id": str(request.id),
                    "endpoint": self.__class__.__name__,
                    "error": str(e),
                },
                error=e,
            )
            raise


def endpoint(
    *,  # Force all args to be keyword-only
    request_model: type[T],
    response_model: type[ResponseType],
    security_service: SecurityService,
    audit_service: AuditService,
    security_level: SecurityLevel = SecurityLevel.INTERNAL,
    risk_level: RiskLevel = RiskLevel.LOW,
) -> Callable:
    """Decorator to create secure API endpoints"""

    def decorator(
        handler: Callable[[APIRequest[T]], Awaitable[ResponseType]],
    ) -> APIEndpoint[T, ResponseType]:
        class DecoratedEndpoint(APIEndpoint[T, ResponseType]):
            async def handle(self, request: APIRequest[T]) -> ResponseType:
                return await handler(request)

        return DecoratedEndpoint(
            request_model=request_model,
            response_model=response_model,
            security_service=security_service,
            audit_service=audit_service,
            security_level=security_level,
            risk_level=risk_level,
        )

    return decorator
