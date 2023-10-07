SHELL = /usr/bin/env bash -xeuo pipefail

test-unit:
	AWS_ACCESS_KEY_ID=dummy \
	AWS_SECRET_ACCESS_KEY=dummy \
	AWS_DEFAULT_REGION=ap-northeast-1 \
	python3 -m pytest -vv tests/unit
	
localstack-up:
	docker-compose up -d

localstack-down:
	docker-compose down