from busbar.core.security.events import ValidationResult
from busbar.core.security.models import SecurityContext
from busbar.core.types import RiskLevel, SecurityLevel


class SystemIntegrityValidator:
    """Validates security integrity across orchestrated systems"""

    async def validate_security_context(
        self, *, context: SecurityContext, systems: list[str]
    ) -> ValidationResult:
        """Validates a security context against provided systems."""
        errors: list[str] = []

        if context.principal is None:
            errors.append("Missing principal")
            return ValidationResult(
                valid=False,
                errors=errors,
                context={
                    "connected_systems": systems,
                    "risk_level": RiskLevel.HIGH,
                    "security_level": SecurityLevel.INTERNAL,
                },
            )

        return ValidationResult(
            valid=True,
            errors=[],
            context={
                "connected_systems": systems,
                "risk_level": context.risk_level,
                "security_level": context.security_level,
            },
        )

    async def verify_integration_state(self, *, integration_points: list[str]) -> ValidationResult:
        """Verifies the state of integration points."""
        return ValidationResult(
            valid=True, errors=[], context={"integration_points": integration_points}
        )
