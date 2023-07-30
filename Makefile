-include .env
export

db.run:
	@docker-compose up -d db

db.migrate:
	@poetry run python api/manage.py migrate

rabbit.run:
	@docker-compose up -d rabbitmq

api.run:
	@poetry run python api/manage.py runserver

parser.run:
	@poetry run python -m parser
