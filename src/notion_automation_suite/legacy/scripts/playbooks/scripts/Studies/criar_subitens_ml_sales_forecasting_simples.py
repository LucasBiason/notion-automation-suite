#!/usr/bin/env python3
"""
Script simples para criar subitens do projeto ML Sales Forecasting no Notion.
"""

import os
from notion_client import Client

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
    },
    {
        "title": "Fase 2: API Backend FastAPI",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-28",
        "end_date": "2025-10-29",
    },
    {
        "title": "Fase 3: Docker & Infraestrutura",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-29",
        "end_date": "2025-10-29",
    },
    {
        "title": "Fase 4: Testes Automatizados",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-29",
        "end_date": "2025-10-29",
    },
    {
        "title": "Fase 5: Frontend React",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-29",
        "end_date": "2025-10-29",
    },
    {
        "title": "Fase 6: Documentacao Final",
        "status": "Concluido",
        "priority": "Alta",
        "start_date": "2025-10-29",
        "end_date": "2025-10-29",
    },
]


def main():
    """Função principal."""
    print("=" * 70)
    print("Criando Subitens: ML Sales Forecasting")
    print("=" * 70)
    print()
    
    # Pegar token do ambiente
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("ERRO: NOTION_TOKEN não encontrado no ambiente")
        return
    
    # Inicializar cliente
    notion = Client(auth=token)
    
    print(f"Database ID: {DATABASE_ID}")
    print(f"Parent Card ID: {PARENT_CARD_ID}")
    print(f"Total de subitens: {len(SUBITENS)}")
    print()
    
    # Criar cada subitem
    created = 0
    for i, subitem in enumerate(SUBITENS, 1):
        print(f"[{i}/{len(SUBITENS)}] Criando: {subitem['title']}")
        
        try:
            properties = {
                "Project name": {
                    "title": [
                        {
                            "text": {
                                "content": subitem["title"]
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": subitem["status"]
                    }
                },
                "Prioridade": {
                    "select": {
                        "name": subitem["priority"]
                    }
                },
                "Parent item": {
                    "relation": [
                        {"id": PARENT_CARD_ID}
                    ]
                },
                "Período": {
                    "date": {
                        "start": subitem["start_date"],
                        "end": subitem.get("end_date")
                    }
                }
            }
            
            response = notion.pages.create(
                parent={"database_id": DATABASE_ID},
                properties=properties
            )
            
            page_id = response["id"]
            print(f"  ✓ ID: {page_id}")
            print(f"  ✓ Período: {subitem['start_date']} -> {subitem.get('end_date')}")
            created += 1
            
        except Exception as e:
            print(f"  ✗ Erro: {e}")
        
        print()
    
    # Resumo
    print("=" * 70)
    print("Resumo:")
    print(f"  Total: {len(SUBITENS)} subitens")
    print(f"  Criados: {created}")
    print(f"  Falhas: {len(SUBITENS) - created}")
    print("=" * 70)


if __name__ == "__main__":
    main()

