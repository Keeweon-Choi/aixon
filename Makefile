SHELL := /bin/bash
PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
RUFF := $(if $(wildcard .venv/bin/ruff),.venv/bin/ruff,$(PYTHON) -m ruff)
ASTRO_ENV := XDG_CONFIG_HOME=/tmp/aixon-astro-config ASTRO_TELEMETRY_DISABLED=1

comma := ,
empty :=
space := $(empty) $(empty)

# Real data (seedtool takes the files separated by spaces, AIXON_GRAPH by commas).
GRAPH_FILES ?= data/seed/seed_graph.yaml data/graph/atlas.yaml
GRAPH_LIST := $(subst $(space),$(comma),$(strip $(GRAPH_FILES)))

# Test fixtures (never used by the real build).
FIXTURE_GRAPH := tests/fixtures/graph/site_graph.yaml
FIXTURE_WIKI := tests/fixtures/wiki

# The E2E builds are served below /aixon/ to behave like GitHub Pages.
E2E_BASE := /aixon/
E2E_SITE := http://127.0.0.1:4329
E2E_ENV := AIXON_BASE=$(E2E_BASE) AIXON_SITE=$(E2E_SITE)

# `make build-public` output; the Pages workflow overrides both.
PUBLIC_BASE ?= /aixon/
PUBLIC_SITE ?= http://localhost:4321

.PHONY: install format lint typecheck test validate validate-fixtures gate gate-e2e dev \
	build build-public build-e2e build-public-e2e build-seed \
	check-dist check-dist-public check-dist-seed e2e e2e-seed secrets verify verify-online clean

# Public builds read the allow-list computed by tools/public_gate.py (ADR-021).
GATE := .aixon/public-gate.json
GATE_E2E := .aixon/public-gate-e2e.json

install:
	npm ci
	$(PYTHON) -c "import yaml, pytest, numpy, pypdf"

format:
	npx prettier --write .

lint:
	npx prettier --check .
	npx eslint src tests playwright.config.ts
	$(ASTRO_ENV) npx astro check
	$(RUFF) check tools tests

typecheck:
	$(ASTRO_ENV) npx astro check
	npx tsc --noEmit -p .

test:
	npx vitest run
	$(PYTHON) -m pytest tools tests/python -q

validate: gate
	$(PYTHON) tools/seedtool.py validate $(GRAPH_FILES)
	$(PYTHON) tools/validate_content.py --graph "$${AIXON_GRAPH:-$(GRAPH_LIST)}"

gate:
	$(PYTHON) tools/public_gate.py --graph $(GRAPH_LIST) --wiki-dir src/content/wiki --out $(GATE)

gate-e2e:
	$(PYTHON) tools/public_gate.py --graph $(FIXTURE_GRAPH) --wiki-dir $(FIXTURE_WIKI) --out $(GATE_E2E)

dev:
	$(ASTRO_ENV) AIXON_BUILD=preview npx astro dev

validate-fixtures:
	$(PYTHON) tools/seedtool.py validate $(FIXTURE_GRAPH)
	$(PYTHON) tools/validate_content.py --graph $(FIXTURE_GRAPH) --wiki-dir $(FIXTURE_WIKI)

build:
	$(ASTRO_ENV) AIXON_BUILD=preview npx astro build
	npx pagefind --site dist

build-public: gate
	$(ASTRO_ENV) AIXON_BUILD=public AIXON_PUBLIC_GATE=$(GATE) AIXON_BASE=$(PUBLIC_BASE) AIXON_SITE=$(PUBLIC_SITE) npx astro build --outDir dist-public
	npx pagefind --site dist-public

build-e2e:
	$(ASTRO_ENV) $(E2E_ENV) AIXON_BUILD=preview AIXON_GRAPH=$(FIXTURE_GRAPH) AIXON_WIKI_DIR=$(FIXTURE_WIKI) npx astro build --outDir dist-e2e
	npx pagefind --site dist-e2e

build-public-e2e: gate-e2e
	$(ASTRO_ENV) $(E2E_ENV) AIXON_BUILD=public AIXON_PUBLIC_GATE=$(GATE_E2E) AIXON_GRAPH=$(FIXTURE_GRAPH) AIXON_WIKI_DIR=$(FIXTURE_WIKI) npx astro build --outDir dist-public-e2e
	npx pagefind --site dist-public-e2e

build-seed:
	env -u AIXON_GRAPH -u AIXON_WIKI_DIR $(ASTRO_ENV) $(E2E_ENV) AIXON_BUILD=preview npx astro build --outDir dist-seed
	npx pagefind --site dist-seed

check-dist:
	$(PYTHON) tools/check_dist.py dist --base "$${AIXON_BASE:-/}" --mode preview

check-dist-public:
	$(PYTHON) tools/check_dist.py dist-public --base $(PUBLIC_BASE) --site $(PUBLIC_SITE) --mode public --graph "$${AIXON_GRAPH:-$(GRAPH_LIST)}" --gate $(GATE)

check-dist-seed:
	$(PYTHON) tools/check_dist.py dist-seed --base $(E2E_BASE) --mode preview

e2e: build-e2e build-public-e2e
	AIXON_E2E_TARGET=fixture npx playwright test

e2e-seed: build-seed
	AIXON_E2E_TARGET=seed npx playwright test

secrets:
	$(PYTHON) tools/scan_secrets.py

verify:
	$(PYTHON) tools/verify.py

# Network checks (not part of verify: results depend on arXiv availability). Weekly in CI.
verify-online:
	mkdir -p artifacts/verification/online
	$(PYTHON) tools/seedtool.py quotes data/seed/seed_graph.yaml > artifacts/verification/online/quotes.json
	$(PYTHON) tools/verify_identifiers.py $(GRAPH_FILES) --json > artifacts/verification/online/identifiers.json

clean:
	rm -rf dist dist-public dist-e2e dist-seed dist-public-e2e .astro .aixon test-results playwright-report
