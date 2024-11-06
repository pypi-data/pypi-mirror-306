import hashlib
import hmac
import secrets


class SecurityService:
    """Security service handling core security functionalities."""

    def __init__(self, encryption_key: str) -> None:
        """
        Initialize the SecurityService.

        Args:
            encryption_key (str): Key used for encryption.
        """
        self.encryption_key = encryption_key

    def hash_secret(self, secret: str) -> str:
        """Hash a secret value.

        Args:
            secret (str): The raw secret to hash.

        Returns:
            str: The hashed secret in the format `$salt$key`.
        """
        if secret.startswith("$"):
            return secret  # Already hashed

        salt = secrets.token_hex(16)
        key = hashlib.pbkdf2_hmac("sha256", secret.encode(), salt.encode(), 100000).hex()
        return f"${salt}${key}"

    def verify_secret(self, stored_secret: str, provided_secret: str) -> bool:
        """Verify a provided secret against the stored hashed secret.

        Args:
            stored_secret (str): The stored hashed secret.
            provided_secret (str): The raw secret to verify.

        Returns:
            bool: True if verification succeeds, False otherwise.
        """
        if not stored_secret.startswith("$"):
            return False

        try:
            salt, key = stored_secret[1:].split("$")
        except ValueError:
            return False

        test_key = hashlib.pbkdf2_hmac(
            "sha256", provided_secret.encode(), salt.encode(), 100000
        ).hex()
        return hmac.compare_digest(key, test_key)
