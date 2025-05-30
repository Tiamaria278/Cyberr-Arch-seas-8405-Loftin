
all: build up

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down -v --remove-orphans

stop:
	docker-compose stop


logs:
	docker-compose logs -f


logs-service:
	docker-compose logs -f $(service)


reset: down build up
	@echo "Environment reset and started."
	@echo "Keycloak should be available at http://localhost:8080"
	@echo "Flask app should be available at http://localhost:5001"


test-public-flask:
	@echo "Testing public Flask endpoint..."
	@curl http://localhost:5001/api/public || echo "Flask app not responding or public endpoint error."