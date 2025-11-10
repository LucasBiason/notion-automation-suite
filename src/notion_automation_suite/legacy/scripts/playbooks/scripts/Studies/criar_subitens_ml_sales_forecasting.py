#!/usr/bin/env python3
"""
Script para criar subitens do projeto ML Sales Forecasting no Notion.
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from core.notion_client import NotionClient

# IDs do Notion
DATABASE_ID = "1fa962a7693c80deb90beaa513dcf9d1"  # Base de Cursos
PARENT_CARD_ID = "296962a7693c81bdba7fda10d3b0ff06"  # ML Sales Forecasting

# Definição dos subitens
SUBITENS = [
    {
        "title": "Fase 1: Notebooks ML - Analise e Modelagem",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-27",
        "end_date": "2025-10-28",
        "categorias": ["ML", "Notebooks", "Portfolio"]
    },
    {
        "title": "Fase 2: API Backend FastAPI",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-28",
        "end_date": "2025-10-29",
        "categorias": ["Backend", "FastAPI", "Portfolio"]
    },
    {
        "title": "Fase 3: Docker & Infraestrutura",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-29",
        "end_date": "2025-10-29",
        "categorias": ["Docker", "DevOps", "Portfolio"]
    },
    {
        "title": "Fase 4: Testes Automatizados",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-29",
        "end_date": "2025-10-29",
        "categorias": ["Testes", "Pytest", "Portfolio"]
    },
    {
        "title": "Fase 5: Frontend React",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-29",
        "end_date": "2025-10-29",
        "categorias": ["Frontend", "React", "Portfolio"]
    },
    {
        "title": "Fase 6: Documentacao Final",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-29",
        "end_date": "2025-10-29",
        "categorias": ["Documentacao", "Portfolio"]
    },
]


def criar_subitem(client: NotionClient, subitem_data: dict) -> str:
    """Cria um subitem no Notion."""
    
    properties = {
        "Project name": {
            "title": [
                {
                    "text": {
                        "content": subitem_data["title"]
                    }
                }
            ]
        },
        "Status": {
            "select": {
                "name": subitem_data["status"]
            }
        },
        "Prioridade": {
            "select": {
                "name": subitem_data["priority"]
            }
        },
        "Parent item": {
            "relation": [
                {"id": PARENT_CARD_ID}
            ]
        },
        "Categorias": {
            "multi_select": [
                {"name": cat} for cat in subitem_data["categorias"]
            ]
        }
    }
    
    # Adicionar período se fornecido
    if "start_date" in subitem_data:
        properties["Período"] = {
            "date": {
                "start": subitem_data["start_date"],
                "end": subitem_data.get("end_date")
            }
        }
    
    try:
        response = client.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=properties
        )
        
        page_id = response["id"]
        print(f"✓ Criado: {subitem_data['title']}")
        print(f"  ID: {page_id}")
        print(f"  Período: {subitem_data.get('start_date')} -> {subitem_data.get('end_date')}")
        
        return page_id
        
    except Exception as e:
        print(f"✗ Erro ao criar '{subitem_data['title']}': {e}")
        return None


def main():
    """Função principal."""
    print("=" * 60)
    print("Criando Subitens: ML Sales Forecasting")
    print("=" * 60)
    print()
    
    # Inicializar cliente
    client = NotionClient()
    
    print(f"Database ID: {DATABASE_ID}")
    print(f"Parent Card ID: {PARENT_CARD_ID}")
    print(f"Total de subitens: {len(SUBITENS)}")
    print()
    
    # Criar cada subitem
    created = 0
    for i, subitem in enumerate(SUBITENS, 1):
        print(f"[{i}/{len(SUBITENS)}] Criando: {subitem['title']}")
        
        page_id = criar_subitem(client, subitem)
        
        if page_id:
            created += 1
        
        print()
    
    # Resumo
    print("=" * 60)
    print("Resumo:")
    print(f"  Total: {len(SUBITENS)} subitens")
    print(f"  Criados: {created}")
    print(f"  Falhas: {len(SUBITENS) - created}")
    print("=" * 60)


if __name__ == "__main__":
    main()

