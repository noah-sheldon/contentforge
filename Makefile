.PHONY: install clean

install:
	cd python && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

clean:
	cd python && find . -path './.venv' -prune -o -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null
