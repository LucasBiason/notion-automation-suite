#!/usr/bin/env python3
"""
Script para atualizar cards do ML Sales Forecasting no Notion.
Adiciona icones, categorias e horarios exatos.

Data: 29/10/2025
Autor: Lucas Biason
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
load_dotenv()

import requests

# Configuração Notion
NOTION_TOKEN = os.getenv("NOTION_TOKEN") or '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'
NOTION_VERSION = "2022-06-28"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

# Cards para atualizar com HORÁRIOS EXATOS
CARDS = [
    {
        "page_id": "29b962a7693c81009894ed89182b4eda",
        "title": "Fase 1: Notebooks ML",
        "icon": "📊",
        "categorias": ["Portfolio", "ML", "Notebooks", "Python"],
        "periodo_start": "2025-10-27T08:00:00",
        "periodo_end": "2025-10-28T21:00:00"
    },
    {
        "page_id": "29b962a7693c811ba96cc2844e69b2e0",
        "title": "Fase 2: API Backend",
        "icon": "⚡",
        "categorias": ["Portfolio", "FastAPI", "API"],
        "periodo_start": "2025-10-28T08:00:00",
        "periodo_end": "2025-10-29T14:00:00"
    },
    {
        "page_id": "29b962a7693c81dfb94fd338cbc30c47",
        "title": "Fase 3: Docker",
        "icon": "🐳",
        "categorias": ["Portfolio", "Docker", "DevOps"],
        "periodo_start": "2025-10-29T10:00:00",
        "periodo_end": "2025-10-29T12:00:00"
    },
    {
        "page_id": "29b962a7693c810b9c85d0c004da56a4",
        "title": "Fase 4: Testes",
        "icon": "🧪",
        "categorias": ["Portfolio", "Testes", "Python"],
        "periodo_start": "2025-10-29T12:00:00",
        "periodo_end": "2025-10-29T14:30:00"
    },
    {
        "page_id": "29b962a7693c81878ad3c0e90dc6cbf7",
        "title": "Fase 5: Frontend",
        "icon": "🎨",
        "categorias": ["Portfolio", "React", "Frontend"],
        "periodo_start": "2025-10-29T14:30:00",
        "periodo_end": "2025-10-29T17:00:00"
    },
    {
        "page_id": "29b962a7693c814982c3e0bd1e101de3",
        "title": "Fase 6: Docs",
        "icon": "📝",
        "categorias": ["Portfolio", "Documentação"],
        "periodo_start": "2025-10-29T17:00:00",
        "periodo_end": "2025-10-29T18:30:00"
    },
    # Sub-cards Notebooks
    {
        "page_id": "29b962a7693c81d8b275d1179dd15569",
        "title": "01 - EDA",
        "icon": "🔍",
        "categorias": ["ML", "Notebooks", "Data Science"],
        "periodo_start": "2025-10-27T19:00:00",
        "periodo_end": "2025-10-27T23:00:00"
    },
    {
        "page_id": "29b962a7693c810dafc3c3d49ab7526c",
        "title": "02 - Model Selection",
        "icon": "🤖",
        "categorias": ["ML", "Regression", "Python"],
        "periodo_start": "2025-10-28T08:00:00",
        "periodo_end": "2025-10-28T13:00:00"
    },
    {
        "page_id": "29b962a7693c81bb8d79ebc52a0d63e8",
        "title": "03 - Tuning",
        "icon": "⚙️",
        "categorias": ["ML", "Python"],
        "periodo_start": "2025-10-28T14:00:00",
        "periodo_end": "2025-10-28T16:00:00"
    },
    {
        "page_id": "29b962a7693c812cb3eef5fce7cc970e",
        "title": "04 - Pipeline",
        "icon": "🔧",
        "categorias": ["ML", "Python"],
        "periodo_start": "2025-10-28T16:00:00",
        "periodo_end": "2025-10-28T18:00:00"
    },
]


def update_page(page_id, icon, categorias, periodo_start, periodo_end):
    """Atualiza uma página com ícone, categorias e período com horários."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    data = {
        "icon": {
            "type": "emoji",
            "emoji": icon
        },
        "properties": {
            "Categorias": {
                "multi_select": [{"name": cat} for cat in categorias]
            },
            "Período": {
                "date": {
                    "start": periodo_start,
                    "end": periodo_end,
                    "time_zone": "America/Sao_Paulo"
                }
            }
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    return response.json()


def main():
    """Função principal."""
    print("=" * 70)
    print("Atualizando Cards ML Sales Forecasting - Notion")
    print("=" * 70)
    print()
    
    if not NOTION_TOKEN:
        print("❌ ERRO: NOTION_TOKEN não encontrado no ambiente")
        return
    
    print(f"Total de cards: {len(CARDS)}")
    print()
    
    success = 0
    errors = 0
    
    for i, card in enumerate(CARDS, 1):
        print(f"[{i}/{len(CARDS)}] {card['title']}")
        
        try:
            result = update_page(
                card["page_id"],
                card["icon"],
                card["categorias"],
                card["periodo_start"],
                card["periodo_end"]
            )
            
            if "object" in result and result["object"] == "error":
                print(f"  ❌ Erro: {result.get('message')}")
                errors += 1
            else:
                print(f"  ✓ Ícone: {card['icon']}")
                print(f"  ✓ Categorias: {', '.join(card['categorias'])}")
                print(f"  ✓ Período: {card['periodo_start']} -> {card['periodo_end']}")
                success += 1
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            errors += 1
        
        print()
    
    # Resumo
    print("=" * 70)
    print("Resumo:")
    print(f"  Total: {len(CARDS)} cards")
    print(f"  Sucesso: {success}")
    print(f"  Erros: {errors}")
    print("=" * 70)


if __name__ == "__main__":
    main()

