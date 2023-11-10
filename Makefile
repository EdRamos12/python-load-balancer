test:
	docker-compose up -d
	pytest --disable-warnings || cls
	docker-compose down