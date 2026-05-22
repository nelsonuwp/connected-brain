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

shell:
	docker run --rm -it --env-file .env --entrypoint bash $(IMAGE)

clean:
	-docker rmi $(IMAGE)
