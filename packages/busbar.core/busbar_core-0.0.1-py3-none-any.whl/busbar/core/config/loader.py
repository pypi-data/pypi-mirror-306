"""Configuration loader supporting both file and directory-based configurations."""

import fnmatch
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from ..types import PathStr
from .models import ExclusionConfig, ExclusionList, ExclusionType


class ConfigOrder(BaseModel):
    """Configuration loading order definition."""

    files: list[PathStr] = Field(
        default_factory=list,
        description="List of configuration files to load in order",
    )
    exclude: list[PathStr] = Field(
        default_factory=list,
        description="List of files or patterns to exclude",
    )


class ConfigExclusionError(Exception):
    """Raised when an excluded configuration is accessed."""

    pass


class ConfigLoader:
    """Load and merge configuration from files and directories."""

    def __init__(
        self,
        *,  # Enforce keyword args
        base_path: str | Path,
        default_pattern: str = "*.yml",
    ) -> None:
        """Initialize config loader."""
        self.base_path = Path(base_path)
        self.default_pattern = default_pattern
        self._loaded_configs: dict[str, Any] = {}
        self._exclusions: list[ExclusionConfig] = []
        self._applied_exclusions: set[str] = set()

    def _merge_dicts(self, base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
        """Deep merge two dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_dicts(base[key], value)
            else:
                base[key] = value
        return base

    def _load_yaml(self, path: Path) -> dict[str, Any]:
        """Load and parse YAML file."""
        with path.open("r") as f:
            return yaml.safe_load(f) or {}

    def _load_order(self, directory: Path) -> ConfigOrder | None:
        """Load .order.yml from directory if it exists."""
        order_file = directory / ".order.yml"
        if order_file.exists():
            data = self._load_yaml(order_file)
            return ConfigOrder(**data)
        return None

    def _load_exclusions(self, path: Path) -> None:
        """Load exclusion configuration if it exists."""
        exclude_file = path / ".exclude.yml"
        if exclude_file.exists():
            data = self._load_yaml(exclude_file)
            exclusion_list = ExclusionList(**data)
            self._exclusions.extend(exclusion_list.exclusions)

    def _check_exclusions(self, path: str | Path, config: dict[str, Any]) -> dict[str, Any]:
        """Check and apply exclusions to configuration."""
        path_str = str(path)

        for exclusion in self._exclusions:
            if exclusion.type == ExclusionType.FILE:
                if fnmatch.fnmatch(path_str, exclusion.pattern):
                    if not exclusion.allowed_override:
                        raise ConfigExclusionError(
                            f"Configuration file {path_str} is excluded: {exclusion.details}"
                        )
                    self._applied_exclusions.add(f"file:{path_str}")
                    return {}

        return config  # Return the unmodified config if not excluded

    def _get_key_paths(self, d: dict[str, Any], prefix: str = "") -> list[str]:
        """Get all possible key paths in a nested dictionary."""
        paths = []
        for k, v in d.items():
            key_path = f"{prefix}.{k}" if prefix else k
            paths.append(key_path)
            if isinstance(v, dict):
                paths.extend(self._get_key_paths(v, key_path))
        return paths

    def _remove_key_path(self, d: dict[str, Any], path: str) -> None:
        """Remove a key path from a nested dictionary."""
        parts = path.split(".")
        current = d
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                return
            current = current[part]
        if parts[-1] in current:
            del current[parts[-1]]

    def _load_directory(self, directory: Path, order: ConfigOrder | None = None) -> dict[str, Any]:
        """Load all configs from directory respecting order if specified."""
        config: dict[str, Any] = {}

        # Load ordered files first if order specified
        if order:
            for file_path in order.files:
                full_path = directory / file_path
                if full_path.is_file():
                    data = self._load_yaml(full_path)
                    config = self._merge_dicts(config, self._check_exclusions(full_path, data))
                elif full_path.is_dir():
                    subdir_config = self.load_config(full_path)
                    config = self._merge_dicts(
                        config, self._check_exclusions(full_path, subdir_config)
                    )

        # Load remaining files if no order specified
        if not order:
            for file_path in sorted(directory.glob(self.default_pattern)):
                if file_path.name != ".order.yml":  # Updated check
                    data = self._load_yaml(file_path)
                    config = self._merge_dicts(config, self._check_exclusions(file_path, data))

        return config

    def load_config(self, path: str | Path | None = None) -> dict[str, Any]:
        """
        Load configuration from file or directory.

        Args:
            path: Optional override path, defaults to base_path

        Returns:
            Dict containing merged configuration
        """
        load_path = Path(path) if path else self.base_path
        config: dict[str, Any] = {}

        # Load exclusions first
        self._load_exclusions(load_path)

        # Load and filter base config
        yml_path = load_path / "busbar.yml"
        yaml_path = load_path / "busbar.yaml"
        if yml_path.is_file():
            base_config = self._load_yaml(yml_path)
            config = self._merge_dicts(config, self._check_exclusions(yml_path, base_config))
        elif yaml_path.is_file():
            base_config = self._load_yaml(yaml_path)
            config = self._merge_dicts(config, self._check_exclusions(yaml_path, base_config))

        # Load and filter directory config
        busbar_d = load_path / "busbar.d"
        if busbar_d.is_dir():
            self._load_exclusions(busbar_d)  # Check for directory-level exclusions
            order = self._load_order(busbar_d)
            dir_config = self._load_directory(busbar_d, order)
            config = self._merge_dicts(config, self._check_exclusions(busbar_d, dir_config))

        if not config:
            raise FileNotFoundError(
                f"No configuration found at {load_path}. Expected busbar.yml, "
                "busbar.yaml, or busbar.d/ directory."
            )

        return config

    @property
    def applied_exclusions(self) -> set[str]:
        """Get set of applied exclusions."""
        return self._applied_exclusions
