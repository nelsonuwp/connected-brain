# projects/

Code projects. Each project is a fully self-contained, standalone unit.

## Design principle

Projects are bubbles. They own their own credentials, config, schemas, and
dependencies. Nothing imports from a shared library. This means any project
can be handed off or containerized without untangling dependencies.

## _reference/

Pattern library — not a dependency. You READ from _reference/ and COPY
into your project. Your project then owns that copy and can modify freely.

## Starting a new project

1. mkdir projects/new-project-name/
2. Copy relevant files from _reference/ into it
3. Create .env.example listing only the credentials this project needs
4. Copy those values from the root .env into a local .env (not committed)
5. Build in isolation

## Credential flow

Root .env (master store, never committed)
  → you manually copy relevant values
  → projects/new-project/.env (project copy, never committed)
  → projects/new-project/.env.example (committed, shows what keys are needed)
