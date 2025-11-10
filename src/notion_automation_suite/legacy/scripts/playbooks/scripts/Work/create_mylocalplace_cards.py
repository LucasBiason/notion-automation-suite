#!/usr/bin/env python3
"""
Cria cards do projeto MyLocalPlace no Notion
"""

import requests
import os

NOTION_TOKEN = os.getenv('NOTION_TOKEN', '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')
NOTION_VERSION = '2022-06-28'
BASE_URL = 'https://api.notion.com/v1'
HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

WORK_DB_ID = '1f9962a7-693c-80a3-b947-c471a975acb0'

def create_main_card():
    """Cria card principal MyLocalPlace"""
    
    payload = {
        "parent": {"database_id": WORK_DB_ID},
        "icon": {"emoji": "🏠"},
        "properties": {
            "Nome do projeto": {
                "title": [{"text": {"content": "Refatoração My Local Place"}}]
            },
            "Status": {
                "status": {"name": "Em Andamento"}
            },
            "Cliente": {
                "select": {"name": "Pessoal"}
            },
            "Projeto": {
                "select": {"name": "MyLocalPlace"}
            },
            "Prioridade": {
                "select": {"name": "Média"}
            }
        }
    }
    
    response = requests.post(f'{BASE_URL}/pages', headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        page_id = response.json()['id']
        print(f"✅ Card principal criado: {page_id}")
        return page_id
    else:
        print(f"❌ Erro: {response.text}")
        return None

def create_phase_card(parent_id, phase_data):
    """Cria card de fase"""
    
    payload = {
        "parent": {"database_id": WORK_DB_ID},
        "icon": {"emoji": phase_data['emoji']},
        "properties": {
            "Nome do projeto": {
                "title": [{"text": {"content": phase_data['title']}}]
            },
            "Status": {
                "status": {"name": "Não iniciado"}
            },
            "Cliente": {
                "select": {"name": "Pessoal"}
            },
            "Projeto": {
                "select": {"name": "MyLocalPlace"}
            },
            "Prioridade": {
                "select": {"name": phase_data['priority']}
            },
            "Sprint": {
                "relation": [{"id": parent_id}]
            }
        }
    }
    
    response = requests.post(f'{BASE_URL}/pages', headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        print(f"   ✅ {phase_data['title']}")
        return response.json()['id']
    else:
        print(f"   ❌ {phase_data['title']}: {response.text}")
        return None

def main():
    print("🏠 Criando cards do MyLocalPlace...\n")
    
    # Criar card principal
    parent_id = create_main_card()
    
    if not parent_id:
        return
    
    print("\n📋 Criando fases...\n")
    
    # Definir fases do MyLocalPlace
    phases = [
        {
            'emoji': '🔐',
            'title': 'FASE 1: Implementar Segurança',
            'priority': 'Alta'
        },
        {
            'emoji': '📦',
            'title': 'FASE 2: Atualizar Stack Docker',
            'priority': 'Alta'
        },
        {
            'emoji': '📱',
            'title': 'FASE 3: Implementar Novas Features',
            'priority': 'Média'
        },
        {
            'emoji': '⚡',
            'title': 'FASE 4: Otimização e Performance',
            'priority': 'Média'
        },
        {
            'emoji': '🧪',
            'title': 'FASE 5: Testes e Qualidade',
            'priority': 'Média'
        },
        {
            'emoji': '🚀',
            'title': 'FASE 6: Deploy e Produção',
            'priority': 'Alta'
        },
        {
            'emoji': '📊',
            'title': 'FASE 7: Monitoramento',
            'priority': 'Baixa'
        },
        {
            'emoji': '📚',
            'title': 'FASE 8: Documentação',
            'priority': 'Média'
        },
        {
            'emoji': '🎨',
            'title': 'FASE 9: Melhorias UX/UI',
            'priority': 'Baixa'
        }
    ]
    
    # Criar cada fase
    for phase in phases:
        create_phase_card(parent_id, phase)
    
    print(f"\n🎉 MyLocalPlace criado!")
    print(f"   URL: https://notion.so/{parent_id.replace('-', '')}")

if __name__ == '__main__':
    main()

