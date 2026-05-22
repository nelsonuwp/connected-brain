.PHONY: all build run run-prod run-headless shell clean

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

# Prod: gunicorn, no debug, no source mount. cost_drivers.json still mounted so
# /settings POSTs persist on the host.
run-prod:
	docker run --rm -it \
		--env-file .env \
		-p $(PORT):$(PORT) \
		-v $(PWD)/cost_drivers.json:/app/cost_drivers.json \
		$(IMAGE)

# Headless: stop any existing container, start detached, tail the log.
# Safe to re-run on redeploy — old container is stopped first.
run-headless:
	-docker stop $$(docker ps -q --filter ancestor=$(IMAGE)) 2>/dev/null || true
	nohup docker run --rm \
		--env-file .env \
		-p $(PORT):$(PORT) \
		-v $(PWD)/cost_drivers.json:/app/cost_drivers.json \
		$(IMAGE) \
		> /tmp/cpq.log 2>&1 &
	@echo "Container started. Tailing /tmp/cpq.log (Ctrl+C to stop watching — container keeps running)..."
	@sleep 1 && tail -f /tmp/cpq.log

shell:
	docker run --rm -it --env-file .env --entrypoint bash $(IMAGE)

clean:
	-docker rmi $(IMAGE)
