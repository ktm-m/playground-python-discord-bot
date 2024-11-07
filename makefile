run-local:
	python3 main.py

run-build:
	docker compose up -d

stop:
	docker compose down