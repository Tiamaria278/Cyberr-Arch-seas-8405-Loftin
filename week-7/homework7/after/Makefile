# Pre-build security checks
# I was not able to run the make check on either the before or after folder.  I received the following error:
# PS C:\Users\jewel\Documents\Cyberr-Arch-seas-8405-Loftin\week-7\homework7\after> make check
# "Running code analysis with Bandit..."
# docker run --rm -v :/app python:3.9-alpine sh -c "pip install bandit && bandit -r /app"
# docker: invalid spec: :/app: empty section between colons

Run 'docker run --help' for more information
make: *** [Makefile:4: check] Error 125
check:
	@echo "Running code analysis with Bandit..."
	docker run --rm -v $(PWD):/app python:3.9-alpine sh -c "pip install bandit && bandit -r /app"
	@echo "Running dependency check with pip-audit..."
	docker run --rm -v $(PWD):/app python:3.9-alpine sh -c "pip install pip-audit && pip-audit -r /app/requirements.txt"

# Host security check
host-security:
	@echo "Running Docker Bench for Security..."
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker/docker-bench-security

# Build Docker image after security checks
dbuild: check
	docker build -t mywebapp .

# Run the container
run:
	docker run -p 6000:5000 mywebapp

# Scan the built image for vulnerabilities
scan:
	docker scout recommendations mywebapp:latest

build:
	docker compose build

start:
	docker compose up -d

stop:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker system prune -f

restart: stop start
