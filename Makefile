cat > Makefile <<'MAKE'
.PHONY: build test report up down clean

build:
	docker compose build tests

test:
	docker compose run --rm tests

report:
	docker compose up -d allure allure-ui
	curl "http://localhost:5050/generate-report?project_id=default" || true
	@echo "Open Allure UI: http://localhost:5252/allure-docker-service-ui/projects/default"

up:
	docker compose up -d

down:
	docker compose down

clean:
	rm -rf allure-results allure-report
	docker compose down -v --remove-orphans
MAKE
