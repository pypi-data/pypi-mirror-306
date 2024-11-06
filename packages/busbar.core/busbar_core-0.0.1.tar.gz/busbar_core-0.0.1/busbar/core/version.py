import subprocess
from pathlib import Path


def get_version() -> str:
    """Get the current version from git tags."""
    try:
        # Get the latest tag
        tag = (
            subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                cwd=Path(__file__).parent,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )

        return tag.lstrip("v")
    except subprocess.CalledProcessError:
        return "0.0.0"


__version__: str = get_version()
