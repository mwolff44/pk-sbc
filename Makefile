# Makefile — P-KISS-SBC documentation
#
# Workflow:
#   make install   → create venv + install deps
#   make build     → mkdocs build + jampack optimization
#   make serve     → live-reload dev server
#   make test      → build + check for unexpected warnings
#
# Copyright: (c) 2007-2026 Mathias WOLFF (mathias@celea.org)
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)
# SPDX-License-Identifier: AGPL-3.0-or-later

VENV        := .venv
PYTHON      := python3
PIP         := $(VENV)/bin/pip
MKDOCS      := $(VENV)/bin/mkdocs
NPM         := npm
REQUIREMENTS := requirements.txt

# ==================================================================================== #
# HELPERS
# ==================================================================================== #

## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' | sed -e 's/^/ /'

.PHONY: confirm
confirm:
	@echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y ]

# ==================================================================================== #
# VENV
# ==================================================================================== #

## venv: create the virtual environment
.PHONY: venv
venv:
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@echo "  [✓] venv ready at $(VENV)/"

## install: install/update dependencies in the venv
.PHONY: install
install: venv
	$(PIP) install --upgrade pip --quiet
	$(PIP) install -r $(REQUIREMENTS) --quiet
	@echo "  [✓] dependencies installed"

## update: upgrade all deps to latest and freeze
.PHONY: update
update: venv
	$(PIP) install --upgrade pip --quiet
	$(PIP) install --upgrade -r $(REQUIREMENTS) --quiet
	@echo "  [✓] dependencies upgraded"

# ==================================================================================== #
# DOCS
# ==================================================================================== #

## serve: start the live-reload dev server
.PHONY: serve
serve: install
	$(MKDOCS) serve

## build: build the static site into site/ and optimize with jampack
.PHONY: build
build: install
	$(MKDOCS) build
	$(NPM) run optimize
	@echo "  [✓] site built and optimized"

## optimize: run jampack post-processing on an existing site/
.PHONY: optimize
optimize:
	$(NPM) run optimize
	@echo "  [✓] site optimized"

## test: build with --strict (warnings treated as errors)
# NOTE: mkdocs-rss-plugin has a known bug where `date_from_meta.default_time`
# is parsed twice when mkdocs-static-i18n runs two build passes (en + fr).
# On the second pass the value is already a datetime object, causing a TypeError
# that triggers a WARNING regardless of config. This is an upstream bug:
# https://github.com/Guts/mkdocs-rss-plugin/issues
# We run a normal build, capture stderr, strip the known spurious warning,
# then fail if any other WARNING or ERROR remains.
.PHONY: test
test: install
	@$(MKDOCS) build 2>/tmp/mkdocs-build.log; \
	grep -v "date_from_meta.default_time" /tmp/mkdocs-build.log > /tmp/mkdocs-filtered.log; \
	cat /tmp/mkdocs-build.log; \
	if grep -qE "^WARNING|^ERROR" /tmp/mkdocs-filtered.log; then \
		echo "  [✗] build failed — unexpected warnings or errors found:"; \
		grep -E "^WARNING|^ERROR" /tmp/mkdocs-filtered.log; \
		exit 1; \
	else \
		echo "  [✓] build passed (no unexpected warnings or errors)"; \
	fi

# ==================================================================================== #
# CLEAN
# ==================================================================================== #

## clean: remove the generated site/ and jampack cache
.PHONY: clean
clean:
	rm -rf site/ .jampack/
	@echo "  [✓] site/ and .jampack/ removed"

## clean/venv: remove the virtual environment
.PHONY: clean/venv
clean/venv: confirm
	rm -rf $(VENV)
	@echo "  [✓] venv removed"

## clean/all: remove site/ and venv
.PHONY: clean/all
clean/all: clean clean/venv
