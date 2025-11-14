PYTHON ?= python3

.PHONY: help deps compile test run version bump-major bump-minor bump-patch build package clean

help:
	@echo "Common build automation commands:"
	@echo "  make deps        Install runtime and build dependencies"
	@echo "  make compile     Byte-compile the Django apps"
	@echo "  make test        Execute the Django test suite"
	@echo "  make run         Start the local development server"
	@echo "  make build       Produce distributable artifacts (sdist/wheel)"
	@echo "  make version     Show the current semantic version"
	@echo "  make bump-patch  Increment the patch version"

deps: ## Dependency management
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install build

compile: ## Compilation
	$(PYTHON) -m compileall config trips ml_models

test: ## Run Django tests
	$(PYTHON) manage.py test

run: ## Run the development server
	$(PYTHON) manage.py runserver 0.0.0.0:8000

version: ## Version management
	$(PYTHON) scripts/bump_version.py show

bump-major:
	$(PYTHON) scripts/bump_version.py bump major

bump-minor:
	$(PYTHON) scripts/bump_version.py bump minor

bump-patch:
	$(PYTHON) scripts/bump_version.py bump patch

build: package

package: clean ## Packaging
	$(PYTHON) -m build

clean:
	rm -rf build dist *.egg-info
