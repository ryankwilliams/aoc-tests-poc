.DEFAULT_GOAL := lint

.PHONY: clean
clean:
	find ./ \
		\( \
		-iname '*.pyc' \
		-o -iname '*.pyo' \
		-o -iname __pycache__ \
		-o -iname .pytest_cache \
		-o -iname coverage \
		-o -iname .coverage \
		\) \
		-exec rm -rfv {} +


lint:
	pre-commit run --all-files --verbose --show-diff-on-failure
