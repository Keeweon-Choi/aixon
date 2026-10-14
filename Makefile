SHELL := /bin/bash
PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
ASTRO_ENV := XDG_CONFIG_HOME=/tmp/aixon-astro-config
GRAPH ?= data/seed/seed_graph.yaml

.PHONY: install lint typecheck test validate build build-public check-dist e2e verify secrets
install:
	npm ci
	$(PYTHON) -c "import yaml, pytest"
lint:
	npx eslint src --ext .ts,.tsx,.astro
	$(ASTRO_ENV) npx astro check
	$(if $(wildcard .venv/bin/ruff),.venv/bin/ruff check tools tests,$(PYTHON) -m ruff check tools tests)
typecheck:
	$(ASTRO_ENV) npx astro check
	npx tsc --noEmit -p .
test:
	npx vitest run
	$(PYTHON) -m pytest tools tests/python
validate:
	$(PYTHON) tools/seedtool.py validate $(GRAPH)
	$(PYTHON) tools/validate_content.py --graph "$${AIXON_GRAPH:-$(GRAPH)}" --wiki-dir "$${AIXON_WIKI_DIR:-src/content/wiki}"
build:
	$(ASTRO_ENV) AIXON_BUILD=preview npx astro build
	npx pagefind --site dist
build-public:
	$(ASTRO_ENV) AIXON_BUILD=public AIXON_BASE=/aixon/ npx astro build --outDir dist-public
	npx pagefind --site dist-public
check-dist:
	$(PYTHON) tools/check_dist.py dist
e2e:
	$(ASTRO_ENV) npx playwright test
verify:
	$(PYTHON) tools/verify.py
secrets:
	$(PYTHON) tools/scan_secrets.py
