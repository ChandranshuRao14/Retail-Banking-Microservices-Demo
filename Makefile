SHELL := /usr/bin/env bash
.PHONY: lint_test_python
lint_test_python:
	docker run --rm -v "$(CURDIR)":/apps alpine/flake8:3.5.0 --config=./utils/lint/flake8 transferservice
.PHONY: lint_test_go
lint_test_go:
	docker run --rm -v "$(CURDIR)":/data cytopia/golint profileservice
.PHONY: lint_test
lint_test:
	make lint_test_python ; \
	make lint_test_go