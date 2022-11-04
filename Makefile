.PHONY: fmt
fmt:
	isort .
	black .

.PHONY: lint
lint:
	mypy . --ignore-missing-imports
