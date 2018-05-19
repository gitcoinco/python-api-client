# Help
.DEFAULT_GOAL := help

.PHONY: help

build: ## Build the pypi package and wheels.
	@python setup.py sdist bdist_wheel

deploy: install ## Deploy package and wheel to PyPi.
	@twine upload dist/*

deploy-test: install ## Deploy package and wheel to PyPi test environment.
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*

install: ## Install local, editable version of the gitcoin client.
	@pip install -e .

test: ## Run pytest.
	@python setup.py test

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
