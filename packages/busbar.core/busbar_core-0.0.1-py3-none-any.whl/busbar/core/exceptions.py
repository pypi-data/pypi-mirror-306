from typing import Any
from uuid import UUID

from .types import ErrorSeverity


class busbarError(Exception):
    """Base exception for all busbar errors."""

    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        code: str | None = None,
        details: dict[str, Any] | None = None,
        source_id: UUID | None = None,
        suggestion: str | None = None,
    ) -> None:
        """
        Initialize a busbarError.

        Args:
            message (str): Description of the error.
            severity (ErrorSeverity, optional): Severity level of the error. Defaults to ErrorSeverity.ERROR.
            code (Optional[str], optional): Error code. Defaults to None.
            details (Optional[Dict[str, Any]], optional): Additional details about the error. Defaults to None.
            source_id (Optional[UUID], optional): UUID of the source where the error originated. Defaults to None.
            suggestion (Optional[str], optional): Suggested action to resolve the error. Defaults to None.
        """
        self.message = message
        self.severity = severity
        self.code = code
        self.details = details or {}
        self.source_id = source_id
        self.suggestion = suggestion
        super().__init__(message)


class ConfigurationError(busbarError):
    """Exception raised for configuration-related errors."""

    pass


class ValidationError(busbarError):
    """Exception raised for data validation errors."""

    pass


class SecurityError(busbarError):
    """Exception raised for security-related errors."""

    def __init__(self, message: str, security_level: str | None = None, **kwargs: Any) -> None:
        """
        Initialize a SecurityError.

        Args:
            message (str): Description of the security error.
            security_level (Optional[str], optional): Level of security concern. Defaults to None.
            **kwargs (Any): Additional keyword arguments for the base class.
        """
        self.security_level = security_level
        super().__init__(message, severity=ErrorSeverity.ERROR, **kwargs)


class SignalError(busbarError):
    """Exception raised for signal processing errors."""

    def __init__(
        self,
        message: str,
        signal_id: UUID | None = None,
        channel: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize a SignalError.

        Args:
            message (str): Description of the signal error.
            signal_id (Optional[UUID], optional): UUID of the related signal. Defaults to None.
            channel (Optional[str], optional): Channel where the error occurred. Defaults to None.
            **kwargs (Any): Additional keyword arguments for the base class.
        """
        self.signal_id = signal_id
        self.channel = channel
        super().__init__(message, **kwargs)


class ModuleError(busbarError):
    """Exception raised for module execution errors."""

    def __init__(
        self,
        message: str,
        module_id: UUID | None = None,
        step: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize a ModuleError.

        Args:
            message (str): Description of the module error.
            module_id (Optional[UUID], optional): UUID of the related module. Defaults to None.
            step (Optional[str], optional): Step during which the error occurred. Defaults to None.
            **kwargs (Any): Additional keyword arguments for the base class.
        """
        self.module_id = module_id
        self.step = step
        super().__init__(message, **kwargs)


class ConfigError(busbarError):
    """Error raised for invalid configuration parameters."""
    pass
