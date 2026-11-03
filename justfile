openspec := "npx -y @fission-ai/openspec@1.15.0"

set dotenv-load := true

# list available recipes
default:
    @just --list

# install everything
setup:
    uv sync --all-packages

# run the dev server
dev:
    uv run --package api fastapi dev apps/api/src/api/main.py

# format
fmt:
    uv run ruff format .
    uv run ruff check --fix .

# format check and lint
lint:
    uv run ruff format --check .
    uv run ruff check .

# type check
types:
    uv run pyright

# architecture boundary check (import-linter)
arch:
    uv run lint-imports

# run tests (pass args through: just test -k auth)
test *args:
    uv run pytest {{args}}

# run tests with coverage
cov:
    uv run pytest --cov=core --cov=api --cov-report=term-missing

# validate all OpenSpec specs and changes
spec:
    OPENSPEC_TELEMETRY=0 {{openspec}} validate --all --strict --no-interactive

# run docs/checks (banned patterns, secrets)
harness:
    uv run python docs/checks/run_all.py

# install pre-commit hooks
hooks:
    uvx pre-commit install

# the one command that means "done"
check: lint types arch test spec harness
