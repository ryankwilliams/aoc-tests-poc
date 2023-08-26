.DEFAULT_GOAL := pre-commit

clean-ansible:
	rm -rf .cache/

clean: clean-ansible
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

python-venv-setup:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

podman-start-service:
	podman system service -t 0 &

collection-install:
	ansible-galaxy collection install -r requirements.yml --force

setup: python-venv-setup collection-install podman-start-service

pre-commit:
	pre-commit run --all-files --verbose --show-diff-on-failure
