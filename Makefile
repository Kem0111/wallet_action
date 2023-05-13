install:
	poetry install

test:
	poetry run pytest

start:
	poetry run python3 wallet_action/main.py

lint:
	poetry run flake8 wallet_action