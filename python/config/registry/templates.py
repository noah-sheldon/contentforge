"""Template registry — HyperFrames templates as data.

A template is a directory under templates/ that contains hyperframes.json,
meta.json, and an index.html composition. Its registry name is the directory
relative to templates/, e.g. short-form/day-in-my-life. Discovery walks the
tree so a new template is a new folder with zero code changes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from config.schema.errors import ConfigError, ConfigIssue
from config.schema.refs import TemplateRef

_TEMPLATES_DIR = "templates"
_REQUIRED_FILES = ("hyperframes.json", "meta.json", "index.html")


@dataclass(frozen=True)
class Template:
    """A discovered HyperFrames template folder."""

    name: str
    root: Path
    meta: dict
    hyperframes: dict
    spec: str

    @property
    def index_html(self) -> Path:
        return self.root / "index.html"

    @property
    def description(self) -> str:
        return str(self.meta.get("name", self.name))


class TemplateRegistry:
    """Discovers templates under templates/ and resolves refs."""

    def __init__(self, repo_root: Path | None = None):
        self.repo_root = (repo_root or Path(__file__).resolve().parents[3]).resolve()
        self._templates_root = self.repo_root / _TEMPLATES_DIR

    def list_names(self) -> list[str]:
        """Return registry names of every discovered template, sorted."""
        return sorted(self._discover())

    def get(self, name: str) -> Template:
        """Return a template by registry name; actionable error when missing."""
        root = self._templates_root / name
        missing = [req for req in _REQUIRED_FILES if not (root / req).is_file()]
        if missing:
            raise ConfigError(
                f"Template '{name}' is incomplete or not a template directory.",
                [
                    ConfigIssue(
                        name,
                        f"missing required files: {', '.join(missing)}",
                    )
                ],
            )
        meta_path = root / "meta.json"
        hyper_path = root / "hyperframes.json"
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            hyper = json.loads(hyper_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise ConfigError(f"Template '{name}' has unreadable metadata: {exc}") from exc
        spec_path = root / "spec.md"
        spec = spec_path.read_text(encoding="utf-8") if spec_path.is_file() else ""
        return Template(name=name, root=root, meta=meta, hyperframes=hyper, spec=spec)

    def resolve(self, ref: TemplateRef) -> Template:
        """Resolve a TemplateRef, honoring an optional version pin when set."""
        if ref.version:
            # Templates are discovered from the tree; index versions land with the
            # golden-render fixture (P1.5). Pins must match the meta id today.
            template = self.get(ref.name)
            if str(template.meta.get("id", "")) != ref.version:
                raise ConfigError(
                    f"Template '{ref.name}' version mismatch.",
                    [
                        ConfigIssue(
                            "templates.version",
                            f"requested {ref.version}, template meta has {template.meta.get('id')}",
                        )
                    ],
                )
            return template
        return self.get(ref.name)

    def _discover(self) -> list[str]:
        if not self._templates_root.is_dir():
            return []
        names: list[str] = []
        for root in _walk_dirs(self._templates_root):
            if all((root / req).is_file() for req in _REQUIRED_FILES):
                names.append(str(root.relative_to(self._templates_root)))
        return names


def _walk_dirs(base: Path):
    """Yield every directory under base (including base itself)."""
    yield base
    for child in base.iterdir():
        if child.is_dir():
            yield from _walk_dirs(child)
