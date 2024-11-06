import logging
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from busbar.core.types import SecurityLevel  # Added import

from ..exceptions import SecurityError
from .models import Credential, Permission, Session
from .security_service import SecurityService  # Corrected import

logger = logging.getLogger(__name__)


class CredentialStore:
    """Secure credential storage service."""

    def __init__(self, encryption_key: str) -> None:
        """
        Initialize the CredentialStore.

        Args:
            encryption_key (str): Key used for encrypting credentials.
        """
        self.encryption_key = encryption_key

    async def create(
        self,
        principal_id: UUID,
        credential_type: str,
        secret: str,
        metadata: dict[str, str] | None = None,
        expires_in: timedelta | None = None,
    ) -> Credential:
        """
        Create a new credential.

        Args:
            principal_id (UUID): UUID of the principal owning the credential.
            credential_type (str): Type of the credential.
            secret (str): Secret value for the credential.
            metadata (Optional[Dict[str, str]], optional): Additional metadata. Defaults to None.
            expires_in (Optional[timedelta], optional): Expiration duration. Defaults to None.

        Returns:
            Credential: The created credential.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError()

    async def get(self, credential_id: UUID) -> Credential | None:
        """
        Retrieve a credential by its UUID.

        Args:
            credential_id (UUID): UUID of the credential to retrieve.

        Returns:
            Optional[Credential]: The retrieved credential, or None if not found.
        """
        raise NotImplementedError()

    async def delete(self, credential_id: UUID) -> None:
        """
        Delete a credential by its UUID.

        Args:
            credential_id (UUID): UUID of the credential to delete.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError()


class SessionStore:
    """Session management service."""

    def __init__(self, encryption_key: str) -> None:
        """
        Initialize the SessionStore.

        Args:
            encryption_key (str): Key used for encrypting session data.
        """
        self.encryption_key = encryption_key

    async def create(
        self,
        principal_id: UUID,
        credential_id: UUID,
        scopes: list[str],
        metadata: dict[str, str] | None = None,
        expires_in: timedelta | None = None,
    ) -> Session:
        """
        Create a new session.

        Args:
            principal_id (UUID): UUID of the principal owning the session.
            credential_id (UUID): UUID of the credential used.
            scopes (List[str]): Scopes granted to the session.
            metadata (Optional[Dict[str, str]], optional): Additional metadata. Defaults to None.
            expires_in (Optional[timedelta], optional): Session expiration duration. Defaults to None.

        Returns:
            Session: The created session.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError()

    async def get(self, session_id: UUID) -> Session | None:
        """
        Retrieve a session by its UUID.

        Args:
            session_id (UUID): UUID of the session to retrieve.

        Returns:
            Optional[Session]: The retrieved session, or None if not found.
        """
        raise NotImplementedError()

    async def delete(self, session_id: UUID) -> None:
        """
        Delete a session by its UUID.

        Args:
            session_id (UUID): UUID of the session to delete.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError()


class Authenticator:
    """Authentication service for handling credential-based authentication."""

    def __init__(
        self,
        credential_store: CredentialStore,
        session_store: SessionStore,
        security_service: SecurityService,
    ) -> None:
        """
        Initialize the Authenticator.

        Args:
            credential_store (CredentialStore): Instance of CredentialStore.
            session_store (SessionStore): Instance of SessionStore.
            security_service (SecurityService): Instance of SecurityService.
        """
        self.credential_store = credential_store
        self.session_store = session_store
        self.security_service = security_service

    async def authenticate(self, credential_id: UUID, secret: str) -> Session:
        """
        Authenticate a credential and create a session.

        Args:
            credential_id (UUID): UUID of the credential to authenticate.
            secret (str): Secret value to verify.

        Returns:
            Session: The created session upon successful authentication.

        Raises:
            SecurityError: If the credential is invalid, secret verification fails, or credential is expired.
        """
        credential = await self.credential_store.get(credential_id)
        if not credential:
            raise SecurityError("Invalid credential")

        if not self.security_service.verify_secret(credential.secret.get_secret_value(), secret):
            raise SecurityError("Invalid secret")

        if credential.expires_at and credential.expires_at < datetime.now(timezone.utc):
            raise SecurityError("Expired credential")

        # Create session
        session = await self.session_store.create(
            principal_id=credential.principal_id,
            credential_id=credential.id,
            scopes=["*"],  # TODO: Proper scope handling
            expires_in=timedelta(hours=1),
        )

        return session

    async def verify_session(self, session_id: UUID) -> Session:
        """
        Verify the validity of a session.

        Args:
            session_id (UUID): UUID of the session to verify.

        Returns:
            Session: The verified session.

        Raises:
            SecurityError: If the session is invalid or expired.
        """
        session = await self.session_store.get(session_id)
        if not session:
            raise SecurityError("Invalid session")

        if session.expires_at < datetime.now(timezone.utc):
            raise SecurityError("Expired session")

        return session


class Authorizer:
    """Authorization service for managing access control."""

    def __init__(self, session_store: SessionStore) -> None:
        """
        Initialize the Authorizer.

        Args:
            session_store (SessionStore): Instance of SessionStore.
        """
        self.session_store = session_store

    async def authorize(
        self,
        session_id: UUID,
        required_permission: Permission,
        resource_id: UUID | None = None,
    ) -> bool:
        """
        Check if a session has the required permission for a resource.

        Args:
            session_id (UUID): UUID of the session to check.
            required_permission (Permission): The permission required.
            resource_id (Optional[UUID], optional): UUID of the resource. Defaults to None.

        Returns:
            bool: True if authorized, False otherwise.
        """
        session = await self.session_store.get(session_id)
        if not session:
            return False

        # TODO: Implement proper permission checking
        return "*" in session.scopes


class SecurityAudit:
    """Security audit logging service."""

    def __init__(self, level: SecurityLevel = SecurityLevel.INTERNAL) -> None:
        """
        Initialize the SecurityAudit logger.

        Args:
            level (SecurityLevel, optional): The security level for auditing. Defaults to SecurityLevel.INTERNAL.
        """
        self.level = level

    async def log_auth(
        self,
        principal_id: UUID,
        action: str,
        status: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Log an authentication event.

        Args:
            principal_id (UUID): UUID of the principal involved.
            action (str): Description of the authentication action.
            status (str): Outcome of the authentication attempt.
            details (Optional[Dict[str, Any]], optional): Additional details. Defaults to None.
        """
        logger.info(
            f"Auth: {action} for {principal_id} - {status}",
            extra={
                "principal_id": str(principal_id),
                "action": action,
                "status": status,
                "details": details or {},
            },
        )

    async def log_authz(
        self,
        principal_id: UUID,
        permission: Permission,
        granted: bool,
        resource_id: UUID | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Log an authorization check event.

        Args:
            principal_id (UUID): UUID of the principal involved.
            permission (Permission): The permission being checked.
            granted (bool): Outcome of the authorization check.
            resource_id (Optional[UUID], optional): UUID of the resource, if applicable. Defaults to None.
            details (Optional[Dict[str, Any]], optional): Additional details. Defaults to None.
        """
        logger.info(
            f"Authz: {permission.action} on {permission.resource_type} - {'granted' if granted else 'denied'}",
            extra={
                "principal_id": str(principal_id),
                "permission": permission.dict(),
                "granted": granted,
                "resource_id": str(resource_id) if resource_id else None,
                "details": details or {},
            },
        )
