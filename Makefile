BLACK_CHECK = black -l 90 --check --diff .
BLACK_FIX = black -l 90 .
MINIMUM_COVERAGE = 95.41
FOXPUPPET_TESTS = pytest -vvv --driver Firefox --cov --cov-fail-under=$(MINIMUM_COVERAGE) --html results/report.html

check: install_poetry lint test

code_format: install_dependencies
	poetry run $(BLACK_FIX)

install_dependencies:
	poetry install

install_poetry:
	curl -sSL https://install.python-poetry.org | python3 -

test: install_dependencies
	poetry run $(FOXPUPPET_TESTS)

lint: install_dependencies
	poetry run $(BLACK_CHECK)

typecheck: install_dependencies
	poetry run mypy .
