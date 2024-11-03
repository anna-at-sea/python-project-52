install:
	poetry install

dev:
	poetry run python3 manage.py runserver

lint:
	poetry run flake8 hexlet_django_blog

makemigrations:
	poetry run python3 manage.py makemigrations

migrate:
	poetry run python3 manage.py migrate

repl:
	poetry run python3 manage.py shell

PORT ?= 8000
start:
	poetry run gunicorn task_manager.wsgi:application --bind 0.0.0.0:$(PORT)