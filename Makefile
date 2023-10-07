SHELL = /usr/bin/env bash -xeuo pipefail

test-unit:
	python3 -m pytest -vv tests/unit
	
localstack-up:
	docker-compose up -d

localstack-down:
	docker-compose down