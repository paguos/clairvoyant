install:
	pipenv install --dev

tests:
	pipenv run flake8
	pipenv run pytest
	