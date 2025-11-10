#!/usr/bin/env python3
"""
Script para estruturar o Roadmap Engenheiro de Software IA 2025-26 no Notion

Ações:
1. Criar card principal "Roadmap Engenheiro de Software IA 2025-26"
2. Criar 2 subitens principais:
   - Formações e Cursos
   - Projetos de Portfolio
3. Mover formações existentes para "Formações e Cursos"
4. Criar cards de projetos em "Projetos de Portfolio"
"""

import os
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('NOTION_API_TOKEN')

# IDs dos databases e páginas
PROJETOS_DB = '1fa962a7-693c-80ae-a58b-ffb2e1c84aee'  # Database Projetos
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'   # Database Estudos

# IDs das formações existentes (para mover)
FIAP_POS_ID = '1fa962a7-693c-80ce-93ab-fb5ca6861890'  # FIAP - Pós Tech IA para Devs

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

gmt3 = pytz.timezone('America/Sao_Paulo')

def format_date_gmt3(date_obj):
    """Formata data para GMT-3."""
    return gmt3.localize(date_obj).isoformat()

def create_page(database_id, properties, parent_id=None):
    """Cria uma página no Notion."""
    url = 'https://api.notion.com/v1/pages'
    
    payload = {
        'parent': {'database_id': database_id},
        'properties': properties
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Erro ao criar página: {response.status_code} - {response.text}')

def update_page(page_id, properties):
    """Atualiza uma página no Notion."""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    
    payload = {'properties': properties}
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Erro ao atualizar página: {response.status_code} - {response.text}')

def main():
    """Estruturar Roadmap no Notion."""
    print('📊 Estruturando Roadmap Engenheiro de Software IA 2025-26...')
    print('=' * 80)
    
    # Passo 1: Criar card principal
    print('\n1️⃣ Criando card principal...')
    
    try:
        roadmap_card = create_page(
            database_id=PROJETOS_DB,
            properties={
                "Project name": {
                    "title": [{"text": {"content": "📊 Roadmap Engenheiro de Software IA 2025-26"}}]
                },
                "Status": {
                    "status": {"name": "Em Andamento"}
                },
                "Período": {
                    "date": {
                        "start": format_date_gmt3(datetime(2025, 10, 22)),
                        "end": format_date_gmt3(datetime(2026, 12, 31))
                    }
                }
            }
        )
        roadmap_id = roadmap_card['id']
        print(f'   ✅ Card principal criado: {roadmap_id}')
    except Exception as e:
        print(f'   ❌ Erro: {e}')
        return
    
    # Passo 2: Criar subitem "Formações e Cursos"
    print('\n2️⃣ Criando subitem "Formações e Cursos"...')
    
    try:
        formacoes_card = create_page(
            database_id=PROJETOS_DB,
            properties={
                "Project name": {
                    "title": [{"text": {"content": "📚 Formações e Cursos"}}]
                },
                "Status": {
                    "status": {"name": "Em Andamento"}
                },
                "Item Principal": {
                    "relation": [{"id": roadmap_id}]
                }
            }
        )
        formacoes_id = formacoes_card['id']
        print(f'   ✅ Formações e Cursos criado: {formacoes_id}')
    except Exception as e:
        print(f'   ❌ Erro: {e}')
        formacoes_id = None
    
    # Passo 3: Criar subitem "Projetos de Portfolio"
    print('\n3️⃣ Criando subitem "Projetos de Portfolio"...')
    
    try:
        portfolio_card = create_page(
            database_id=PROJETOS_DB,
            properties={
                "Project name": {
                    "title": [{"text": {"content": "💼 Projetos de Portfolio"}}]
                },
                "Status": {
                    "status": {"name": "Em Andamento"}
                },
                "Item Principal": {
                    "relation": [{"id": roadmap_id}]
                }
            }
        )
        portfolio_id = portfolio_card['id']
        print(f'   ✅ Projetos de Portfolio criado: {portfolio_id}')
    except Exception as e:
        print(f'   ❌ Erro: {e}')
        portfolio_id = None
    
    # Passo 4: Mover FIAP para "Formações e Cursos"
    print('\n4️⃣ Movendo FIAP para "Formações e Cursos"...')
    
    if formacoes_id:
        try:
            update_page(
                page_id=FIAP_POS_ID,
                properties={
                    "Item Principal": {
                        "relation": [{"id": formacoes_id}]
                    }
                }
            )
            print('   ✅ FIAP movido com sucesso!')
        except Exception as e:
            print(f'   ❌ Erro ao mover FIAP: {e}')
    
    # Passo 5: Criar cards de projetos em "Projetos de Portfolio"
    print('\n5️⃣ Criando cards de projetos...')
    
    if portfolio_id:
        projetos = [
            {
                "nome": "🚀 MyLocalPlace v2.0 - DevTools Dashboard",
                "periodo_inicio": datetime(2025, 10, 23),
                "periodo_fim": datetime(2025, 10, 27),
                "status": "Para Fazer"
            },
            {
                "nome": "🔧 fastapi-framework - Biblioteca Reutilizável",
                "periodo_inicio": datetime(2025, 11, 10),
                "periodo_fim": datetime(2025, 11, 30),
                "status": "Para Fazer"
            },
            {
                "nome": "🛒 IntelliCart - E-commerce CQRS",
                "periodo_inicio": datetime(2025, 12, 10),
                "periodo_fim": datetime(2025, 12, 31),
                "status": "Para Fazer"
            }
        ]
        
        for projeto in projetos:
            try:
                create_page(
                    database_id=PROJETOS_DB,
                    properties={
                        "Project name": {
                            "title": [{"text": {"content": projeto["nome"]}}]
                        },
                        "Status": {
                            "status": {"name": projeto["status"]}
                        },
                        "Período": {
                            "date": {
                                "start": format_date_gmt3(projeto["periodo_inicio"]),
                                "end": format_date_gmt3(projeto["periodo_fim"])
                            }
                        },
                        "Item Principal": {
                            "relation": [{"id": portfolio_id}]
                        }
                    }
                )
                print(f'   ✅ Criado: {projeto["nome"]}')
            except Exception as e:
                print(f'   ❌ Erro ao criar {projeto["nome"]}: {e}')
    
    print('\n' + '=' * 80)
    print('✅ ESTRUTURAÇÃO COMPLETA!')
    print('=' * 80)
    print('')
    print('📋 Próximos Passos:')
    print('   1. Acessar Notion e verificar estrutura')
    print('   2. Mover manualmente outras formações (Udemy, Rocketseat)')
    print('   3. Criar subitens de fases para cada projeto')
    print('   4. Começar a executar! 🚀')

if __name__ == '__main__':
    if not TOKEN:
        print("Erro: NOTION_API_TOKEN não está configurado no arquivo .env")
    else:
        main()










