install:
	pipenv install --dev

test:
	pipenv run flake8
	pipenv run pytest
	