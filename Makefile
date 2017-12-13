all: clean flake mypy tests

clean:
	find . -regex ".*\.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .coverage .cache .mypy_cache

flake:
	python -m flake8 .

mypy:
	mypy --strict --ignore-missing-imports norfs tests

tests:
	PYTHONPATH=. pytest tests/ --cov=norfs --cov-report=term-missing

.PHONY: clean flake mypy tests
