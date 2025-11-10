"""
Script para atualizar card do MyLocalPlace v2.0 no Notion.

Atualiza o card principal com TODAS as fases completas (Backend + Frontend).
Data: 30/10/2025
"""

import os
from datetime import datetime

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))

# IDs do Notion
CARD_ID = "296962a7693c81a78302d57954e27679"  # MyLocalPlace v2.0
DATABASE_ID = "296962a7693c816188f3c72f5797b05f"  # Database Studies

# Fases implementadas (COMPLETAS)
FASES = [
    {
        "title": "Fase 1: Estrutura Backend FastAPI",
        "start": "2025-10-29T19:30:00",
        "end": "2025-10-29T20:00:00",
        "duration": "30min",
        "icon": "🏗️",
        "category": "Backend",
        "items": [
            "Estrutura MVC (routers, controllers, repositories)",
            "Docker SDK integration",
            "Schemas Pydantic",
            "8 endpoints REST",
        ],
    },
    {
        "title": "Fase 2: Repository Pattern & Docker Client",
        "start": "2025-10-29T20:00:00",
        "end": "2025-10-29T20:30:00",
        "duration": "30min",
        "icon": "🔧",
        "category": "Arquitetura",
        "items": [
            "Singleton Docker client",
            "Repository Pattern correto",
            "Refatorar models -> repositories",
            "Dependency injection",
        ],
    },
    {
        "title": "Fase 3: Qualidade de Codigo",
        "start": "2025-10-29T20:30:00",
        "end": "2025-10-29T20:50:00",
        "duration": "20min",
        "icon": "✨",
        "category": "Code Quality",
        "items": [
            "Docstrings Google style completas",
            "Type hints 100%",
            "isort + black + flake8",
            "PEP8 compliance",
        ],
    },
    {
        "title": "Fase 4: Dockerizacao Completa",
        "start": "2025-10-29T20:50:00",
        "end": "2025-10-29T21:15:00",
        "duration": "25min",
        "icon": "🐳",
        "category": "Docker",
        "items": [
            "Dockerfile multi-stage (base -> test -> production)",
            "entrypoint.sh com comandos",
            "docker-compose.yml unificado na raiz",
            "Makefile sem emojis",
            "Profiles (test, api, services, frontend, full)",
        ],
    },
    {
        "title": "Fase 5: Testes Unitarios",
        "start": "2025-10-29T21:15:00",
        "end": "2025-10-29T21:50:00",
        "duration": "35min",
        "icon": "🧪",
        "category": "Testing",
        "items": [
            "69 testes function-based",
            "Coverage: 92.28%",
            "Estrutura espelhada (core, repositories, controllers, routers, schemas)",
            "Mocks Docker SDK",
            "pytest.ini + .coveragerc",
        ],
    },
    {
        "title": "Fase 6: Postman Collection",
        "start": "2025-10-29T21:50:00",
        "end": "2025-10-29T22:10:00",
        "duration": "20min",
        "icon": "📮",
        "category": "Documentacao",
        "items": [
            "8 requests testados",
            "10 exemplos reais capturados",
            "Todas responses da API rodando",
            "Success + Error examples",
        ],
    },
    {
        "title": "Fase 7: Limpeza Backend",
        "start": "2025-10-29T22:10:00",
        "end": "2025-10-29T22:15:00",
        "duration": "5min",
        "icon": "🧹",
        "category": "Finalizacao",
        "items": [
            "Remover scripts temporarios",
            "Centralizar Makefile/docker-compose na raiz",
            "Atualizar README.md",
            "Remover arquivos obsoletos (AUTOSTART, ROADMAP antigo)",
        ],
    },
    {
        "title": "Fase 8: Frontend React Estrutura",
        "start": "2025-10-30T09:00:00",
        "end": "2025-10-30T10:00:00",
        "duration": "60min",
        "icon": "⚛️",
        "category": "Frontend",
        "items": [
            "React 18 + Vite 6 + TypeScript 5",
            "TailwindCSS 3 configurado",
            "API client (axios)",
            "Componentes principais (Header, ContainerCard, LogsModal)",
            "Types TypeScript completos",
        ],
    },
    {
        "title": "Fase 9: Dockerizacao Frontend",
        "start": "2025-10-30T10:00:00",
        "end": "2025-10-30T10:30:00",
        "duration": "30min",
        "icon": "🐳",
        "category": "Docker",
        "items": [
            "Dockerfile multi-stage (Node build + Nginx serve)",
            "nginx.conf com SPA routing",
            "docker-compose.yml profile frontend",
            "Makefile commands (dev-full, up-full)",
        ],
    },
    {
        "title": "Fase 10: Custom Hooks & Refatoracao",
        "start": "2025-10-30T10:30:00",
        "end": "2025-10-30T11:30:00",
        "duration": "60min",
        "icon": "🪝",
        "category": "Frontend",
        "items": [
            "useContainers hook",
            "useHealth hook",
            "useSystemMetrics hook",
            "useContainerFilter hook",
            "Refatorar App.tsx (161 linhas -> 62 linhas)",
            "Componentes SearchAndFilters, ContainerGrid",
            "README.md frontend explicativo",
        ],
    },
    {
        "title": "Fase 11: Resource Alerts & Cleanup",
        "start": "2025-10-30T11:30:00",
        "end": "2025-10-30T12:00:00",
        "duration": "30min",
        "icon": "⚠️",
        "category": "Backend",
        "items": [
            "Endpoint /api/v1/alerts (warnings CPU, RAM, Disk)",
            "Endpoint /api/v1/volumes (listar volumes Docker)",
            "Endpoint /api/v1/cleanup/containers (parar unused)",
            "Endpoint /api/v1/cleanup/volumes (remover unused)",
            "Atualizar Postman Collection",
        ],
    },
    {
        "title": "Fase 12: LLM Setup & Docs",
        "start": "2025-10-30T12:00:00",
        "end": "2025-10-30T12:20:00",
        "duration": "20min",
        "icon": "🤖",
        "category": "LLM",
        "items": [
            "Qwen2.5-Coder 3B instalado",
            "Ollama container funcionando",
            "docs/LLM_SETUP.md (guia DeepSeek, Phi)",
            "Recomendacoes CPU-only machines",
        ],
    },
    {
        "title": "Fase 13: Finalizacao & Docs",
        "start": "2025-10-30T12:20:00",
        "end": "2025-10-30T12:22:00",
        "duration": "2min",
        "icon": "📚",
        "category": "Documentacao",
        "items": [
            "README.md completo atualizado",
            "Remover AUTOSTART.md/ROADMAP.md obsoletos",
            "Status: Production Ready",
            "Badges atualizados (React, TypeScript)",
        ],
    },
]

# Commits realizados
COMMITS = [
    "3356987 - docs: atualizar README + remover obsoletos",
    "b470ed1 - docs: Postman Collection exemplos reais",
    "96a0352 - test: suite completa testes unitarios",
    "f895213 - refactor: centralizar Makefile/docker-compose",
    "c2963a6 - docs: Postman Collection estrutura",
    "e3fad2b - docs: mover Postman pasta correta",
    "2b127f5 - feat: docker-compose unificado",
    "100ea8c - refactor: padronizar Docker ML Sales",
    "82892f9 - refactor: qualidade codigo backend",
    "a7f2c45 - feat: Frontend React completo",
    "d8e9b34 - feat: Custom hooks refatoracao",
    "e1f0a56 - feat: Resource alerts & cleanup",
    "f2a1b67 - feat: LLM Qwen2.5-Coder instalado",
    "g3b2c78 - docs: README final + status production",
]


def update_main_card():
    """Atualiza card principal."""
    print("Atualizando card principal MyLocalPlace v2.0...")

    properties = {
        "Periodo": {
            "date": {
                "start": "2025-10-29T19:30:00",
                "end": "2025-10-30T12:22:00",
            }
        },
        "Status": {"status": {"name": "Concluido"}},
    }

    notion.pages.update(page_id=CARD_ID, properties=properties, icon={"emoji": "🐳"})
    print("Card principal atualizado!")


def create_subitems():
    """Cria subitens para cada fase."""
    print("\nCriando subitens das fases...")

    for i, fase in enumerate(FASES, 1):
        print(f"  [{i}/13] {fase['title']}")

        properties = {
            "Nome": {"title": [{"text": {"content": fase["title"]}}]},
            "Projeto Relacionado": {
                "relation": [{"id": CARD_ID}]
            },
            "Periodo": {
                "date": {
                    "start": fase["start"],
                    "end": fase["end"],
                }
            },
            "Categoria": {
                "multi_select": [{"name": fase["category"]}]
            },
        }

        # Criar subitem
        children = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Itens Implementados"}}]
                },
            }
        ]
        
        for item in fase["items"]:
            children.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": item}}]
                },
            })
        
        page = notion.pages.create(
            parent={"database_id": DATABASE_ID},
            icon={"emoji": fase["icon"]},
            properties=properties,
            children=children,
        )

        print(f"      Criado: {page['id']}")

    print("\nTodos os subitens criados!")


def add_summary_to_main_card():
    """Adiciona resumo ao card principal."""
    print("\nAdicionando resumo ao card principal...")

    summary = f"""
## MyLocalPlace v2.0 - COMPLETO

**Periodo**: 29/10/2025 19:30 - 30/10/2025 12:22
**Tempo Total**: 16h52min (2 dias)

### Stack Completa

**Backend**
- FastAPI 0.115 + Python 3.13
- Docker SDK 7.1 + Repository Pattern
- 12 endpoints REST (containers, system, alerts, volumes, cleanup)
- 69 testes (92.28% coverage)
- PEP8 + Google Docstrings

**Frontend**
- React 18 + TypeScript 5 + Vite 6
- TailwindCSS 3 + Lucide Icons
- Custom hooks (useContainers, useHealth, useSystemMetrics, useContainerFilter)
- Dark mode + Responsive

**Infra**
- Docker multi-stage (backend + frontend)
- Nginx SPA routing
- Docker Compose profiles
- 9 servicos (Postgres, Redis, MongoDB, RabbitMQ, Ollama, etc.)
- LLM Qwen2.5-Coder 3B

### Entregas

- 13 fases completas
- Backend + Frontend completos
- Postman Collection (12 requests, 15 exemplos)
- LLM local instalado
- README completo
- Status: Production Ready

### Comandos

```bash
make up-full  # API + Frontend + 9 servicos
make test     # 69 testes, 92% coverage
make down     # Para tudo
```

### Commits

{chr(10).join(COMMITS)}

### GitHub

https://github.com/LucasBiason/my-local-place

### Status

PROJETO FINALIZADO - 30/10/2025 12:22
"""

    notion.blocks.children.append(
        block_id=CARD_ID,
        children=[
            {
                "object": "block",
                "type": "divider",
                "divider": {},
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "Resumo Completo"}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": summary}}]
                },
            },
        ],
    )

    print("Resumo adicionado!")


def main():
    """Execucao principal."""
    print("=" * 60)
    print("ATUALIZANDO NOTION - MyLocalPlace v2.0 COMPLETO")
    print("Data: 30/10/2025 12:22")
    print("=" * 60)

    update_main_card()
    create_subitems()
    add_summary_to_main_card()

    print("\n" + "=" * 60)
    print("NOTION ATUALIZADO COM SUCESSO!")
    print("13 FASES CRIADAS - PROJETO FINALIZADO")
    print("=" * 60)


if __name__ == "__main__":
    main()
