BLACK_CHECK = black -l 90 --check --diff .
BLACK_FIX = black -l 90 .
FOXPUPPET_TESTS = pytest --driver Firefox --cov --html results/report.html

code_format: install_dependencies
	poetry run $(BLACK_CHECK)

install_dependencies:
	poetry install

test: install_dependencies
	poetry run $(FOXPUPPET_TESTS)

lint: install_dependencies
	poetry run $(BLACK_CHECK)
