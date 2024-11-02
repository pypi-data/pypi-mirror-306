# Title: Makefile for uv-demo project

SHELL=/bin/bash

.PHONY: all install gact test test-verbose test-all tox serve-coverage clean update publish docs docs-serve

all: install test

# SETUP
install:
	uv run pre-commit install --install-hooks
	uv sync --dev --frozen

# GITHUB ACTIONS
gact:
	# install gh-act with:
	# gh extension install nektos/gh-act
	gh act --workflows .github/workflows --secret-file config/secrets.env

# TESTS
test:
	uv run pytest -vvv --cov=src
test-verbose:
	uv run pytest -vvv --cov=src --capture=no
test-all:
	# pyv=("3.11" "3.12" "3.13"); for py in "${pyv[@]}"; do echo "${py}"; uv run -p "${py}" tox run -vvv -e "python${py}"; done
	uv run -p "3.11" tox run -e "python3.11"
	uv run -p "3.12" tox run -e "python3.12"
	uv run -p "3.13" tox run -e "python3.13"

serve-coverage:
	python -m http.server 8000 -d tests/htmlcov

# CLEANUP
clean:
	rm -rf \
		.tox .coverage \
		.pytest_cache .python-version .cache dist \
		.venv .eggs .eggs/ \
		*.egg-info *.egg-info/

# UPDATE
update:
	uv sync --upgrade
	uv run pre-commit autoupdate

# PUBLISH
publish:
	@if [ ! -f config/secrets.env ]; then \
		echo "Error: config/secrets.env does not exist."; \
		exit 1; \
	fi
	export UV_PUBLISH_TOKEN=$$(grep PYPI_API_TOKEN config/secrets.env | cut -d '=' -f2)
	uv build
	uv publish

# GITHUB ACTIONS
gact:
	# install gh-act with:
	# gh extension install nektos/gh-act
	gh act \
		--workflows "$$(git rev-parse --show-toplevel)/.github/workflows"
gact-release:
	gh act \
		--workflows "$$(git rev-parse --show-toplevel)/.github/workflows" \
		--secret-file config/secrets.env \
		release
gact-pr:
	$(MAKE) gact-pull-request
gact-pull-request:
	# this will test the build and publish jobs, but the publish job will only
	# run successfully on the GitHub repo, as the configured trusted publisher.
	gh act \
		--workflows "$$(git rev-parse --show-toplevel)/.github/workflows" \
		--secret-file config/secrets.env \
		pull-request

# DOCUMENTATION
docs:
	uv run pdoc src/uv_demo/ -o docs/
docs-serve:
	$(MAKE) docs
	uv run -m http.server 12001 -d docs/ &> /dev/null & disown
	sleep 1
	xdg-open http://localhost:12001/
