"""Module for managing and merging configuration files."""

import copy
import re
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from yaml import FullLoader, Loader, UnsafeLoader

from ..exceptions import ConfigurationError


class MergeOperation(str, Enum):
    """Config merge operations"""

    REPLACE = "="  # Replace value completely
    APPEND = "+"  # Append to lists/sets
    PREPEND = "^"  # Prepend to lists/sets
    DELETE = "-"  # Remove key/value
    MERGE = "&"  # Deep merge (default)
    OVERRIDE = "!"  # Override but don't merge deeper
    DEFAULT = "?"  # Only set if not already set
    EVAL = "|"  # Evaluate expression


class MergeTag:
    """YAML tag for merge operations"""

    def __init__(self, value: Any, operation: MergeOperation):
        self.value = value
        self.operation = operation


def merge_tag_constructor(loader: Loader | FullLoader | UnsafeLoader, node: yaml.Node) -> Any:
    """Construct MergeTag from YAML"""
    if isinstance(node, yaml.ScalarNode):
        value = loader.construct_scalar(node)
    else:
        value = None
    # Extract operation from tag
    tag = node.tag.split("/")[-1]
    return MergeTag(value, MergeOperation(tag))


# Register custom YAML tags
for op in MergeOperation:
    yaml.add_constructor(f"!{op.value}", merge_tag_constructor)


class ConfigMergeError(ConfigurationError):
    """Error merging configurations"""

    def __init__(
        self,
        message: str,
        path: str | None = None,
        source: str | None = None,
    ):
        self.path = path
        self.source = source
        super().__init__(
            f"Error merging config at {path or 'root'} from " f"{source or 'unknown'}: {message}"
        )


class ConfigStack:
    """Manages stack of config files with merging"""

    def __init__(self):
        self._stack: list[dict[str, Any]] = []
        self._sources: list[str] = []

    def push(self, config: dict[str, Any], source: str) -> None:
        """Push config onto stack"""
        self._stack.append(config)
        self._sources.append(source)

    def load_file(self, path: str | Path) -> None:
        """Load and push config file"""
        path = Path(path)
        if not path.exists():
            return

        with path.open(encoding="utf-8") as f:
            try:
                config = yaml.safe_load(f)
                self.push(config, str(path))
            except yaml.YAMLError as e:
                raise ConfigurationError(f"Failed to load config from {path}: {e}") from e

    def merge(self) -> dict[str, Any]:
        """Merge entire config stack"""
        if not self._stack:
            return {}

        result = copy.deepcopy(self._stack[0])
        for i, config in enumerate(self._stack[1:], 1):
            try:
                self._merge_dicts(result, config, path="", source=self._sources[i])
            except ConfigMergeError as e:
                raise ConfigurationError(
                    f"Failed to merge config from {self._sources[i]}: {e}"
                ) from e
        return result

    def _merge_dicts(
        self, base: dict[str, Any], overlay: dict[str, Any], path: str, source: str
    ) -> None:
        """Merge overlay into base dict"""
        for key, value in overlay.items():
            current_path = f"{path}.{key}" if path else key

            # Handle merge tags
            if isinstance(value, MergeTag):
                self._apply_merge_operation(
                    base, key, value.value, value.operation, current_path, source
                )
                continue

            # Regular merge
            if key not in base:
                base[key] = copy.deepcopy(value)
                continue

            try:
                base[key] = self._merge_values(base[key], value, current_path, source)
            except ConfigMergeError as e:
                raise ConfigMergeError(str(e), path=current_path, source=source) from e

    def _merge_values(
        self,
        base: list[Any] | dict[str, Any] | None,
        overlay: list[Any] | dict[str, Any] | Any,
        path: str,
        source: str,
    ) -> Any:
        """Merge two values based on their types"""

        # Handle None
        if overlay is None:
            return base
        if base is None:
            return copy.deepcopy(overlay)

        # Lists
        if isinstance(base, list):
            if not isinstance(overlay, list):
                raise ConfigMergeError(
                    f"Cannot merge {type(overlay)} into list", path=path, source=source
                )
            if all(isinstance(item, type(base[0])) for item in overlay):  # type: ignore
                return base + overlay  # type: ignore
            else:
                raise ConfigMergeError(
                    "Cannot merge lists with different element types",
                    path=path,
                    source=source,
                )

        # Dicts
        if not isinstance(overlay, dict):
            raise ConfigMergeError(
                f"Cannot merge {type(overlay)} into dict", path=path, source=source
            )
        self._merge_dicts(base, overlay, path, source)  # type: ignore
        return base

    def _apply_merge_operation(
        self,
        base: dict[str, Any],
        key: str,
        value: Any,
        operation: MergeOperation,
        path: str,
        source: str,
    ) -> None:
        """Apply merge operation to value"""
        if operation == MergeOperation.REPLACE:
            base[key] = value
        elif operation == MergeOperation.APPEND:
            if key not in base:
                base[key] = []
            if not isinstance(base[key], list):
                raise ConfigMergeError("Can only append to lists", path=path, source=source)
            base[key].extend(value if isinstance(value, list) else [value])
        elif operation == MergeOperation.MERGE:
            if key not in base:
                base[key] = {}
            if not isinstance(base[key], dict) or not isinstance(value, dict):
                raise ConfigMergeError("Cannot merge non-dict types", path=path, source=source)
            base[key].update(value)
        elif operation == MergeOperation.DELETE:
            base.pop(key, None)
        elif operation == MergeOperation.OVERRIDE:
            base[key] = copy.deepcopy(value)
        elif operation == MergeOperation.DEFAULT:
            if key not in base:
                base[key] = copy.deepcopy(value)
        elif operation == MergeOperation.EVAL:
            if not isinstance(value, str):
                raise ConfigMergeError(
                    "Eval operation requires string value", path=path, source=source
                )
            base[key] = self._evaluate_template(value, base, path, source)

    def _evaluate_template(
        self, template: str, context: dict[str, Any], path: str, source: str
    ) -> str:
        """Evaluate template string"""

        def replace(match: re.Match[str]) -> str:
            var: str = match.group(1)
            if var not in context:
                raise ConfigMergeError(f"Undefined variable: {var}", path=path, source=source)
            return str(context[var])

        return re.sub(r"\${(\w+)}", replace, template)
