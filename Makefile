BLACK_ARGS = -l 120 -t py310 bdop_cli tests setup.py

init:
	pip3 install --editable .
	pip3 install -r requirements-test.txt

format:
	python3 -m black $(BLACK_ARGS)

format-check:
	python3 -m black $(BLACK_ARGS) --check

lint:
	python3 -m pylint bdop_cli

mypy:
	python3 -m mypy --install-types --non-interactive .

test:
	python3 -m pytest -vv -s --typeguard-packages=bdop_cli

coverage:
	coverage run -m pytest
	coverage html
	coverage report

checks: format-check lint mypy test

image:
	DOCKER_BUILDKIT=1 docker build --progress=plain -t registry.baloise.dev/bdop-cli:latest .

.PHONY: init format format-check lint mypy test coverage checks image
