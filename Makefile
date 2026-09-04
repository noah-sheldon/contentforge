# contentforge quality gates.
#
# Python: ruff (lint + format) and pyrefly (types) run from the uv workspace.
# JS/TS:  biome (lint + format) and tsc (types) run from the root npm package.
# `make verify` is the single green check: lint + format-check + typecheck + test.

.PHONY: help install sync lint format format-check typecheck pyrefly tsc test smoke verify clean

VENV      = .venv
PY        = $(VENV)/bin/python
RUFF      = $(VENV)/bin/ruff
PYREFLY   = $(VENV)/bin/pyrefly
BIOME     = node_modules/.bin/biome
TSC       = node_modules/.bin/tsc

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: sync ## Alias for sync

sync: ## Install python + JS/TS toolchains
	uv sync --all-packages --dev
	npm install

lint: ## Lint python (ruff) and js/ts (biome)
	$(RUFF) check python/
	$(BIOME) check .

format: ## Auto-fix lint issues and format python + js/ts
	$(RUFF) check --fix python/
	$(RUFF) format python/
	$(BIOME) check --write .

format-check: ## Verify everything is formatted (CI gate)
	$(RUFF) format --check python/
	$(BIOME) check .

typecheck: pyrefly tsc ## Type-check python (pyrefly) and ts (tsc)

pyrefly: ## Pyrefly type-check the python workspace
	cd python && ../$(VENV)/bin/pyrefly check

tsc: ## tsc --noEmit over TypeScript packages (armed; no TS sources yet)
	@if find . -type f \( -name '*.ts' -o -name '*.tsx' \) -not -path './_sources/*' -not -path './node_modules/*' -not -path './.venv/*' | grep -q .; then \
		echo 'Running tsc --noEmit over TypeScript packages...'; \
		find . -type f -name 'tsconfig.json' -not -path './_sources/*' -not -path './node_modules/*' -not -path './.venv/*' -print0 | xargs -0 -r -n1 $(TSC) --noEmit -p; \
	else \
		echo 'No TypeScript sources yet - tsc gate armed for when TS lands (P2/P4).'; \
	fi

test: ## Run the python test suite
	cd python && PYTHONPATH=. ../$(PY) -m pytest -q || [ $$? -eq 5 ]  # pytest 5 = no tests collected yet

smoke: ## P0 smoke test: capture + tighten + transcribe dry run
	./scripts/smoke_test.sh

verify: ## Full local gate: lint + format-check + typecheck + test
	$(MAKE) lint
	$(MAKE) format-check
	$(MAKE) typecheck
	$(MAKE) test

clean: ## Remove toolchains and caches
	rm -rf $(VENV) node_modules
	find . -path './_sources' -prune -o -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null
