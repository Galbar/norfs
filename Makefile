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
	PYTHONPATH=. python -m pytest tests/ --cov=norfs --cov-report=term-missing

docs:
	rm -rf docs/_build
	@$(MAKE) -C docs html;

publish:
	python setup.py bdist_wheel
	twine upload dist/*

py3.4: py3.4-clean
	PYTHONPATH=. python backport-py3.4.py

py3.4-publish:
	cp README.rst py3.4/README.rst
	cp LICENSE.txt py3.4/LICENSE.txt
	cd py3.4 && \
		python setup.py bdist_wheel
	cd py3.4 && \
		twine upload dist/*

py3.4-clean:
	rm -rf py3.4/norfs py3.4/tests py3.4/norfs_py3.4.egg-info py3.4/dist py3.4/build py3.4/README.rst py3.4/LICENSE.txt

.PHONY: clean flake mypy tests docs publish py3.4 py3.4-tests py3.4-publish
