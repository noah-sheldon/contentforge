.PHONY: install sync lint format test smoke clean help

VENV = .venv
PY = $(VENV)/bin/python
RUFF = $(VENV)/bin/ruff

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: sync ## Alias for sync

sync: ## Install all workspace packages (+ dev) into .venv
	uv sync --all-packages --dev

lint: ## Ruff check the python workspace
	$(RUFF) check python/

format: ## Auto-fix safe ruff issues + format
	$(RUFF) check --fix python/
	$(RUFF) format python/

test: ## Run python test suite
	cd python && PYTHONPATH=. ../$(PY) -m pytest -q

smoke: ## P0 smoke test: capture + tighten + transcribe dry run
	./scripts/smoke_test.sh

clean: ## Remove venv and caches
	rm -rf $(VENV)
	find . -path './_sources' -prune -o -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null
