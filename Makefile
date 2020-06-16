all: clean flake mypy tests

clean:
	find . -regex ".*\.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .coverage .cache .mypy_cache build dist norfs.egg-info

flake:
	python -m flake8 .

mypy:
	mypy --strict --ignore-missing-imports norfs tests

tests:
	PYTHONPATH=. python -m pytest tests/ --cov=norfs --cov-report=term-missing

docs:
	rm -rf docs/_build
	@$(MAKE) -C docs html;

publish:
	python setup.py bdist_wheel
	twine upload dist/*

.PHONY: clean flake mypy tests docs publish
