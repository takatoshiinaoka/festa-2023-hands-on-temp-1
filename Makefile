SHELL = /usr/bin/env bash -xeuo pipefail

test-unit:
	python3 -m pytest -vv tests/unit