# Makefile — P-KISS-SBC documentation
#
# Copyright: (c) 2007-2026 Mathias WOLFF (mathias@celea.org)
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)
# SPDX-License-Identifier: AGPL-3.0-or-later

VENV        := .venv
PYTHON      := python3
PIP         := $(VENV)/bin/pip
MKDOCS      := $(VENV)/bin/mkdocs
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

## build: build the static site into site/
.PHONY: build
build: install
	$(MKDOCS) build

## test: build with --strict (warnings treated as errors)
.PHONY: test
test: install
	$(MKDOCS) build --strict
	@echo "  [✓] build passed (strict mode)"

# ==================================================================================== #
# CLEAN
# ==================================================================================== #

## clean: remove the generated site/
.PHONY: clean
clean:
	rm -rf site/
	@echo "  [✓] site/ removed"

## clean/venv: remove the virtual environment
.PHONY: clean/venv
clean/venv: confirm
	rm -rf $(VENV)
	@echo "  [✓] venv removed"

## clean/all: remove site/ and venv
.PHONY: clean/all
clean/all: clean clean/venv
