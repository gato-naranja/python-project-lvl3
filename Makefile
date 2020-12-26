install:
		@poetry install

lint:
		poetry run flake8 page_loader

test:
		poetry run pytest -q --cov=page_loader --cov-report xml tests/

build:
		poetry build

package-install:
		pip install --user dist/*.whl

.PHONY: lint test