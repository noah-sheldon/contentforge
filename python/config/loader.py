"""Tenant config loading: YAML -> TenantConfig with overrides + ref checks.

Load a tenant blob from config/tenants/<slug>.yaml (or an arbitrary path),
optionally deep-merge an overrides mapping, validate against the Pydantic
schema, then fail fast on registry refs that do not resolve.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from config.registry.prompts import PromptRegistry
from config.registry.recipes import RecipeLibrary
from config.registry.templates import TemplateRegistry
from config.schema.errors import ConfigError, ConfigIssue, config_error_from_pydantic
from config.schema.run import RunConfig
from config.schema.tenant import TenantConfig

_TENANTS_DIR = "config/tenants"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge override into a copy of base; lists replace wholesale."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def normalize_tenant_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return the tenant mapping, accepting a bare blob or a 'tenant:' wrapper."""
    return payload.get("tenant", payload) if isinstance(payload, dict) else payload


def load_tenant_payload(
    path: Path,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Read a tenant YAML file and apply optional deep overrides."""
    if not path.is_file():
        raise ConfigError(f"Tenant config file not found: {path}")
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    payload = normalize_tenant_payload(raw)
    if not isinstance(payload, dict):
        raise ConfigError(f"Tenant config {path} must be a YAML mapping.")
    if overrides:
        payload = _deep_merge(payload, overrides)
    return payload


def validate_tenant_config(
    tenant: TenantConfig,
    repo_root: Path,
) -> TenantConfig:
    """Cross-validate registry refs and file refs; raise ConfigError on failures."""
    issues: list[ConfigIssue] = []

    persona_path = tenant.persona.resolve(repo_root)
    if not persona_path.is_file():
        issues.append(ConfigIssue("persona", f"persona file not found: {persona_path}"))

    if tenant.voice.file:
        voice_path = Path(tenant.voice.file)
        resolved_voice = voice_path if voice_path.is_absolute() else repo_root / voice_path
        if not resolved_voice.is_file():
            issues.append(ConfigIssue("voice.file", f"voice file not found: {resolved_voice}"))

    prompts = PromptRegistry(repo_root)
    for ref in tenant.prompts:
        try:
            prompts.resolve(ref)
        except ConfigError as exc:
            issues.append(ConfigIssue("prompts", str(exc)))

    templates = TemplateRegistry(repo_root)
    for ref in tenant.templates:
        try:
            templates.resolve(ref)
        except ConfigError as exc:
            issues.append(ConfigIssue("templates", str(exc)))

    recipes = RecipeLibrary(repo_root)
    for ref in tenant.recipes:
        try:
            recipes.resolve(ref)
        except ConfigError as exc:
            issues.append(ConfigIssue("recipes", str(exc)))

    if issues:
        raise ConfigError(f"Tenant '{tenant.slug}' config references do not resolve.", issues)
    return tenant


def load_tenant_config(
    path: str | Path,
    overrides: dict[str, Any] | None = None,
    repo_root: Path | None = None,
) -> TenantConfig:
    """Load, validate, and cross-check a tenant config blob.

    Raises ConfigError with per-field issues on invalid data or refs.
    """
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    config_path = Path(path)
    if not config_path.is_absolute():
        config_path = root / config_path
    payload = load_tenant_payload(config_path, overrides)
    try:
        tenant = TenantConfig.model_validate(payload)
    except ValidationError as exc:
        raise config_error_from_pydantic(exc, f"Tenant config {config_path}") from exc
    return validate_tenant_config(tenant, root)


def tenant_config_path(slug: str, repo_root: Path | None = None) -> Path:
    """Return the canonical path for a tenant slug blob."""
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    return root / _TENANTS_DIR / f"{slug}.yaml"


def load_tenant_by_slug(
    slug: str,
    overrides: dict[str, Any] | None = None,
    repo_root: Path | None = None,
) -> TenantConfig:
    """Load a tenant blob from config/tenants/<slug>.yaml."""
    return load_tenant_config(tenant_config_path(slug, repo_root), overrides, repo_root)


# ─── Run config ───────────────────────────────────────────────────────


def normalize_run_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return the run mapping, accepting a bare blob or a 'run:' wrapper."""
    return payload.get("run", payload) if isinstance(payload, dict) else payload


def load_run_config(
    path: str | Path,
    repo_root: Path | None = None,
) -> RunConfig:
    """Load and validate a run config blob (config/runs/*.yaml)."""
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    run_path = Path(path)
    if not run_path.is_absolute():
        run_path = root / run_path
    if not run_path.is_file():
        raise ConfigError(f"Run config file not found: {run_path}")
    with open(run_path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    payload = normalize_run_payload(raw)
    if not isinstance(payload, dict):
        raise ConfigError(f"Run config {run_path} must be a YAML mapping.")
    try:
        return RunConfig.model_validate(payload)
    except ValidationError as exc:
        raise config_error_from_pydantic(exc, f"Run config {run_path}") from exc
