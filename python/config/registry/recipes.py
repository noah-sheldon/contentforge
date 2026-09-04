"""Capture recipe library — recipes as data files under config/recipes/.

Each YAML file is one Recipe blob (config/schema/recipe.py). New recipe =
new YAML file, zero code changes.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from config.registry.base import load_yaml
from config.schema.errors import ConfigError, ConfigIssue, config_error_from_pydantic
from config.schema.recipe import Recipe
from config.schema.refs import RecipeRef

_RECIPES_DIR = "config/recipes"


class RecipeLibrary:
    """Loads recipe YAML data files and resolves recipe refs."""

    def __init__(self, repo_root: Path | None = None):
        self.repo_root = (repo_root or Path(__file__).resolve().parents[3]).resolve()
        self._recipes: dict[str, Recipe] | None = None

    def _load(self) -> dict[str, Recipe]:
        if self._recipes is None:
            recipes_dir = self.repo_root / _RECIPES_DIR
            if not recipes_dir.is_dir():
                raise ConfigError(f"Recipe library dir not found: {recipes_dir}")
            found: dict[str, Recipe] = {}
            for path in sorted(recipes_dir.glob("*.yaml")):
                recipe = self._parse_file(path)
                if recipe.id in found:
                    raise ConfigError(f"Duplicate recipe id '{recipe.id}' across recipe files.")
                found[recipe.id] = recipe
            self._recipes = found
        return self._recipes

    @staticmethod
    def _parse_file(path: Path) -> Recipe:
        raw = load_yaml(path)
        data = raw.get("recipe") if isinstance(raw, dict) and "recipe" in raw else raw
        try:
            return Recipe.model_validate(data)
        except ValidationError as exc:
            raise config_error_from_pydantic(exc, f"Recipe file {path.name}") from exc

    def list_ids(self) -> list[str]:
        """Return every available recipe id, sorted."""
        return sorted(self._load())

    def resolve(self, ref: RecipeRef) -> Recipe:
        """Resolve a RecipeRef, honoring an optional version pin."""
        return self.get(ref.name, ref.version)

    def get(self, name: str, version: str | None = None) -> Recipe:
        """Return the recipe by id; actionable ConfigError when missing."""
        recipes = self._load()
        recipe = recipes.get(name)
        if recipe is None:
            known = ", ".join(sorted(recipes))
            raise ConfigError(
                f"Recipe '{name}' is not in the library.",
                [ConfigIssue("recipes", f"Known recipes: {known}")],
            )
        if version and recipe.version != version:
            raise ConfigError(
                f"Recipe '{name}' version mismatch.",
                [
                    ConfigIssue(
                        "recipes.version",
                        f"requested {version}, library has {recipe.version}",
                    )
                ],
            )
        return recipe


def yaml_dump(recipe: Recipe) -> str:
    """Render a Recipe as the config/recipes YAML shape (recipe: top key)."""
    return yaml.safe_dump({"recipe": recipe.model_dump(mode="json")}, sort_keys=False)
