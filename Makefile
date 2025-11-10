.PHONY: help install install-dev test lint format type-check run docker-build docker-run clean

help:
	@echo "Notion Automation Suite - Comandos Disponíveis"
	@echo ""
	@echo "  make install        - Instalar dependências de produção"
	@echo "  make install-dev    - Instalar dependências de desenvolvimento"
	@echo "  make test           - Executar testes"
	@echo "  make lint           - Executar linter (ruff)"
	@echo "  make format         - Formatar código (black)"
	@echo "  make type-check     - Verificar tipos (mypy)"
	@echo "  make run            - Executar servidor localmente"
	@echo "  make docker-build   - Build imagem Docker"
	@echo "  make docker-run     - Executar via Docker"
	@echo "  make clean          - Limpar arquivos temporários"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=notion_mcp --cov-report=html --cov-report=term

lint:
	ruff check src tests

format:
	black src tests
	ruff check --fix src tests

type-check:
	mypy src

run:
	notion-mcp-server

docker-build:
	docker build -t notion-automation-suite:latest .

docker-run:
	docker compose up

docker-stop:
	docker compose down

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

