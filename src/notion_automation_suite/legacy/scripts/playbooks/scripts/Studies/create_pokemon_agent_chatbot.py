#!/usr/bin/env python3
"""
Create Pokemon Agent Chatbot Cards Script
Versão: 1.0
Data: 28/10/2025
Status: Ativo

Script para criar estrutura completa do projeto Pokemon Agent Chatbot no Notion.
"""

import requests
from datetime import datetime, timedelta
import pytz

# Configurações
NOTION_TOKEN = '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'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'
PROJETOS_PORTFOLIO_2025_ID = "294962a7693c81beafc2e098c9ac8b92"

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

gmt3 = pytz.timezone('America/Sao_Paulo')

def format_date_gmt3(dt):
    """Formata data para GMT-3."""
    if dt.tzinfo is None:
        dt = gmt3.localize(dt)
    return dt.isoformat()

def create_page(database_id, properties, parent_id=None, icon=None):
    """Cria uma página no Notion."""
    url = 'https://api.notion.com/v1/pages'
    
    payload = {
        'parent': {'database_id': database_id},
        'properties': properties
    }
    if parent_id:
        payload['properties']['Parent item'] = {"relation": [{"id": parent_id}]}
    if icon:
        payload['icon'] = icon
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao criar página: {response.status_code} - {response.text}")
        return None

def add_content_to_page(page_id, blocks):
    """Adiciona conteúdo a uma página."""
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    payload = {'children': blocks}
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    return response.status_code == 200

def main():
    """Função principal para criar estrutura completa do projeto."""
    print("=" * 70)
    print("🎮 CRIANDO POKÉMON EXPERT AGENT CHATBOT - NOTION")
    print("=" * 70)
    
    # Datas
    data_inicio_projeto = datetime(2025, 10, 28)
    data_fim_projeto = datetime(2025, 11, 25)
    
    # 1. CRIAR CARD PRINCIPAL
    print("\n📌 1. Criando card principal...")
    
    main_properties = {
        "Project name": {"title": [{"text": {"content": "Pokemon Expert Agent Chatbot"}}]},
        "Status": {"status": {"name": "Em Andamento"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Portfolio"}, {"name": "IA"}, {"name": "Desenvolvimento"}]},
        "Período": {
            "date": {
                "start": format_date_gmt3(data_inicio_projeto),
                "end": format_date_gmt3(data_fim_projeto)
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "100+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Chatbot especializado em Pokemon com arquitetura hibrida (RAG + Rules), interface React minimalista, e sistema de recomendacoes precisas."}}]}
    }
    
    main_card = create_page(
        ESTUDOS_DB,
        main_properties,
        parent_id=PROJETOS_PORTFOLIO_2025_ID,
        icon={"type": "emoji", "emoji": "🎮"}
    )
    
    if not main_card:
        print("Falha ao criar card principal!")
        return False
    
    main_card_id = main_card['id']
    main_url = main_card.get('url', 'N/A')
    print(f"✅ Card principal criado: {main_card_id}")
    print(f"   URL: {main_url}")
    
    # 2. CRIAR CARDS DAS FASES
    print("\n📋 2. Criando cards das fases...")
    
    phases = [
        {
            "name": "Fase 1: Setup e Dados",
            "icon": "📊",
            "duracao": 4,
            "offset": 0
        },
        {
            "name": "Fase 2: Backend Core",
            "icon": "⚙️",
            "duracao": 6,
            "offset": 4
        },
        {
            "name": "Fase 3: Agente LLM",
            "icon": "🤖",
            "duracao": 5,
            "offset": 10
        },
        {
            "name": "Fase 4: Sistema de Recomendacao",
            "icon": "🎯",
            "duracao": 4,
            "offset": 15
        },
        {
            "name": "Fase 5: Frontend React",
            "icon": "🎨",
            "duracao": 6,
            "offset": 19
        },
        {
            "name": "Fase 6: Integracao e Deploy",
            "icon": "🚀",
            "duracao": 4,
            "offset": 25
        }
    ]
    
    phase_results = []
    
    for phase in phases:
        data_inicio = data_inicio_projeto + timedelta(days=phase["offset"])
        data_fim = data_inicio + timedelta(days=phase["duracao"] - 1)
        
        phase_properties = {
            "Project name": {"title": [{"text": {"content": phase["name"]}}]},
            "Status": {"status": {"name": "Para Fazer"}},
            "Categorias": {"multi_select": [{"name": "Fase"}, {"name": "Portfolio"}]},
            "Período": {
                "date": {
                    "start": format_date_gmt3(data_inicio),
                    "end": format_date_gmt3(data_fim)
                }
            }
        }
        
        phase_card = create_page(
            ESTUDOS_DB,
            phase_properties,
            parent_id=main_card_id,
            icon={"type": "emoji", "emoji": phase["icon"]}
        )
        
        if phase_card:
            phase_results.append(phase_card)
            print(f"✅ {phase['name']}: {phase_card['id']}")
        else:
            print(f"❌ Falha ao criar {phase['name']}")
    
    # 3. CRIAR SUB-CARDS DA FASE 1
    if len(phase_results) >= 1:
        print("\n📝 3. Criando sub-cards da Fase 1...")
        
        phase1_id = phase_results[0]['id']
        
        subtasks = [
            {"name": "1.1 - Estrutura do Projeto", "icon": "🏗️"},
            {"name": "1.2 - Analise de Datasets", "icon": "🔍"},
            {"name": "1.3 - Unificacao de Dados", "icon": "🔗"},
            {"name": "1.4 - Integracao PokeAPI", "icon": "🔌"},
            {"name": "1.5 - Type Chart Oficial", "icon": "⚔️"}
        ]
        
        subtask_results = []
        
        for subtask in subtasks:
            subtask_properties = {
                "Project name": {"title": [{"text": {"content": subtask["name"]}}]},
                "Status": {"status": {"name": "Para Fazer"}},
                "Categorias": {"multi_select": [{"name": "Sub-tarefa"}, {"name": "Portfolio"}]}
            }
            
            subtask_card = create_page(
                ESTUDOS_DB,
                subtask_properties,
                parent_id=phase1_id,
                icon={"type": "emoji", "emoji": subtask["icon"]}
            )
            
            if subtask_card:
                subtask_results.append(subtask_card)
                print(f"✅ {subtask['name']}: {subtask_card['id']}")
            else:
                print(f"❌ Falha ao criar {subtask['name']}")
    
    # MOSTRAR RESULTADOS
    print("\n" + "=" * 70)
    print("📊 ESTRUTURA CRIADA COM SUCESSO!")
    print("=" * 70)
    print(f"\n🎮 Card Principal:")
    print(f"   ID: {main_card_id}")
    print(f"   URL: {main_url}")
    print(f"\n📋 Fases Criadas: {len(phase_results)}")
    for i, phase in enumerate(phases, 1):
        print(f"   {i}. {phase['name']}")
    
    if len(phase_results) >= 1:
        print(f"\n📝 Sub-tarefas Fase 1: {len(subtask_results)}")
        for i, subtask in enumerate(subtasks, 1):
            print(f"   {i}. {subtask['name']}")
    
    print("\n" + "=" * 70)
    print("🎉 Processo concluído!")
    print("🔗 Acesse: https://www.notion.so/" + main_card_id.replace("-", ""))
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erro na execução: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
