.PHONY: all build run run-prod shell clean

.ONESHELL:
.SHELLFLAGS = -ec
SHELL = /bin/bash

.DEFAULT_GOAL := all

IMAGE := cpq-front-end
PORT  := 5050

all: build run

build:
	docker build -t $(IMAGE) .

# Dev: Flask debug + auto-reload. Source bind-mounted so edits are live.
# Single worker because the sshtunnel/psycopg connection is module-level state.
run:
	docker run --rm -it \
		--env-file .env \
		-p $(PORT):$(PORT) \
		-v $(PWD)/app.py:/app/app.py \
		-v $(PWD)/templates:/app/templates \
		-v $(PWD)/routes:/app/routes \
		-v $(PWD)/db:/app/db \
		-v $(PWD)/lib:/app/lib \
		-v $(PWD)/cost_drivers.json:/app/cost_drivers.json \
		$(IMAGE) \
		flask --app app --debug run --host 0.0.0.0 --port $(PORT)

# Prod: gunicorn, detached, always restarts unless manually stopped.
# Safe to re-run on redeploy — old container is stopped and removed first.
# Logs: docker logs cpq-front-end -f
run-prod:
	-docker stop cpq-front-end 2>/dev/null || true
	-docker rm cpq-front-end 2>/dev/null || true
	docker run -d \
		--name cpq-front-end \
		--restart=unless-stopped \
		--env-file .env \
		-p $(PORT):$(PORT) \
		-v $(PWD)/cost_drivers.json:/app/cost_drivers.json \
		$(IMAGE)
	@echo "Container started. Logs: docker logs cpq-front-end -f"

shell:
	docker run --rm -it --env-file .env --entrypoint bash $(IMAGE)

clean:
	-docker rmi $(IMAGE)
