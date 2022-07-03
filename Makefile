install:
	poetry install

lint: install
	poetry run black .
	poetry run isort .
	poetry run flake8 .
	poetry run pre-commit run --all-files
