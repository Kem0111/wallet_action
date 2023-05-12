install:
	poetry install

test:
	poetry run pytest

make start:
	poetry run python3 wallet_action/main.py
