"""Prompt registry — versioned, loadable by name.

Index: prompts/registry.yaml at the repo root. Each entry is:
    name: research/synthesis
    path: python/agents/prompts/research/synthesis.yaml
    version: 1.0.0
    status: active
    description: one-line purpose

Loading a yaml prompt returns its `prompt:` body (format placeholders are
filled by the caller). Loading a markdown prompt returns the file body with
frontmatter stripped. Version pins are honored when requested.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from config.registry.base import load_yaml, split_frontmatter
from config.schema.errors import ConfigError, ConfigIssue
from config.schema.refs import PromptRef

_PROMPTS_REGISTRY = "prompts/registry.yaml"


@dataclass(frozen=True)
class PromptEntry:
    """One registry row: name -> file path + version metadata."""

    name: str
    path: Path
    version: str
    status: str
    description: str

    def content(self) -> str:
        """Return the prompt body for this entry."""
        text = self.path.read_text(encoding="utf-8")
        if self.path.suffix.lower() in (".yaml", ".yml"):
            data = yaml.safe_load(text)
            if not isinstance(data, dict) or "prompt" not in data:
                raise ConfigError(f"Prompt file {self.path} has no 'prompt' key.")
            return data["prompt"]
        meta, body = split_frontmatter(text)
        file_version = meta.get("version")
        if file_version and str(file_version) != self.version:
            raise ConfigError(
                f"Prompt '{self.name}' version drift.",
                [
                    ConfigIssue(
                        "prompts.version",
                        f"file frontmatter says {file_version}, registry says {self.version}",
                    )
                ],
            )
        return body.strip()


class PromptRegistry:
    """Loads and resolves prompt entries by name from the registry index."""

    def __init__(self, repo_root: Path | None = None):
        self.repo_root = (repo_root or Path(__file__).resolve().parents[3]).resolve()
        self._entries: dict[str, PromptEntry] | None = None

    def _load(self) -> dict[str, PromptEntry]:
        if self._entries is None:
            raw = load_yaml(self.repo_root / _PROMPTS_REGISTRY)
            prompts = raw.get("prompts")
            if not isinstance(prompts, list):
                raise ConfigError(f"{_PROMPTS_REGISTRY} must contain a 'prompts' list.")
            self._entries = {}
            for row in prompts:
                entry = self._row_to_entry(row, self.repo_root)
                if entry.name in self._entries:
                    raise ConfigError(f"Duplicate prompt name in registry: {entry.name}")
                self._entries[entry.name] = entry
        return self._entries

    @staticmethod
    def _row_to_entry(row: object, repo_root: Path) -> PromptEntry:
        if not isinstance(row, dict):
            raise ConfigError("Each registry row must be a mapping with name/path/version.")
        name = row.get("name")
        path = row.get("path")
        version = row.get("version")
        if not isinstance(name, str) or not name:
            raise ConfigError(f"Registry row needs a string name: {row}")
        if not isinstance(path, str) or not path:
            raise ConfigError(f"Registry row for '{name}' needs a string path: {row}")
        if not isinstance(version, str) or not version:
            raise ConfigError(f"Registry row for '{name}' needs a string version: {row}")
        entry_path = repo_root / path
        if not entry_path.is_file():
            raise ConfigError(
                f"Prompt '{name}' path missing.",
                [ConfigIssue("prompts.path", f"not found: {entry_path}")],
            )
        return PromptEntry(
            name=name,
            path=entry_path,
            version=version,
            status=str(row.get("status", "active")),
            description=str(row.get("description", "")),
        )

    def list_names(self) -> list[str]:
        """Return all registered prompt names, sorted."""
        return sorted(self._load())

    def resolve(self, ref: PromptRef) -> PromptEntry:
        """Resolve a PromptRef, honoring an optional version pin."""
        return self.get(ref.name, ref.version)

    def get(self, name: str, version: str | None = None) -> PromptEntry:
        """Return the entry for name; raise actionable ConfigError when missing."""
        entries = self._load()
        entry = entries.get(name)
        if entry is None:
            known = ", ".join(list(entries)[:8])
            raise ConfigError(
                f"Prompt '{name}' is not registered.",
                [
                    ConfigIssue(
                        "prompts", f"Add an entry to prompts/registry.yaml. Known: {known}..."
                    )
                ],
            )
        if version and entry.version != version:
            raise ConfigError(
                f"Prompt '{name}' version mismatch.",
                [
                    ConfigIssue(
                        "prompts.version",
                        f"requested {version}, registry has {entry.version}",
                    )
                ],
            )
        return entry

    def load(self, name: str, version: str | None = None) -> str:
        """Return prompt body text for name (no formatting)."""
        return self.get(name, version).content()

    def load_ref(self, ref: PromptRef) -> str:
        """Resolve and load a PromptRef to prompt body text."""
        return self.resolve(ref).content()
