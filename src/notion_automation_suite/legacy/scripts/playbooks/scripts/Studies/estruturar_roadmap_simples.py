#!/usr/bin/env python3
"""
Script para estruturar o Roadmap Completo no Notion
Cria card principal + subitens com estrutura correta (Parent/Sub-item)
"""

import os
import requests
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
TOKEN = os.getenv('NOTION_API_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Database ID (Base de Cursos)
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

# Timezone GMT-3
gmt3 = pytz.timezone('America/Sao_Paulo')

def format_date_gmt3(date_obj, hour=19, minute=0):
    """Formata data para GMT-3."""
    return gmt3.localize(date_obj).isoformat()

def create_page(database_id, properties, parent_id=None):
    """Cria uma nova página no Notion."""
    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    
    if parent_id:
        data["properties"]["Parent item"] = {"relation": [{"id": parent_id}]}
    
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao criar página: {response.status_code} - {response.text}")
        return None

def add_content_to_page(page_id, blocks):
    """Adiciona conteúdo (blocos) a uma página."""
    response = requests.patch(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers=HEADERS,
        json={"children": blocks}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao adicionar conteúdo: {response.status_code} - {response.text}")
        return None

def get_roadmap_main_content():
    """Conteúdo detalhado para o card principal do Roadmap."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Visão Geral do Roadmap"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Este roadmap foi criado para transformar Lucas em um Engenheiro de Software Sênior especializado em IA, com foco em:"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Desenvolvimento de habilidades técnicas avançadas"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Construção de portfolio robusto com projetos reais"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Especialização em IA e Machine Learning"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Preparação para mercado de trabalho competitivo"}}]
            }
        }
    ]

def main():
    """Função principal - Estrutura o Roadmap Completo."""
    
    print("🚀 ESTRUTURANDO ROADMAP COMPLETO NO NOTION")
    print("="*60)
    
    if not TOKEN:
        print("❌ NOTION_API_TOKEN não encontrado!")
        print("💡 Crie um arquivo .env com: NOTION_API_TOKEN=seu_token_aqui")
        return
    
    # 1. CRIAR CARD PRINCIPAL
    print("\n📋 1. Criando card principal...")
    
    main_card_properties = {
        "Project name": {"title": [{"text": {"content": "📊 Roadmap Engenheiro de Software IA 2025-26"}}]},
        "Status": {"status": {"name": "Em andamento"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Roadmap"}, {"name": "Desenvolvimento"}]},
        "Período": {
            "date": {
                "start": "2025-10-23T00:00:00.000-03:00",
                "end": "2026-12-31T23:59:59.000-03:00"
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "1000+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Roadmap completo para se tornar Engenheiro de Software com especialização em IA. Inclui formações, projetos de portfolio e desenvolvimento de habilidades técnicas."}}]}
    }
    
    main_card = create_page(ESTUDOS_DB, main_card_properties)
    
    if not main_card:
        print("❌ Falha ao criar card principal!")
        return
    
    main_card_id = main_card['id']
    print(f"✅ Card principal criado: {main_card_id}")
    
    # Adicionar conteúdo detalhado ao card principal
    print("📝 Adicionando conteúdo detalhado ao card principal...")
    add_content_to_page(main_card_id, get_roadmap_main_content())
    
    # 2. CRIAR SUBITENS PRINCIPAIS
    print("\n📋 2. Criando subitens principais...")
    
    # Subitem: Formações e Cursos
    formacoes_properties = {
        "Project name": {"title": [{"text": {"content": "📚 Formações e Cursos"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Estudos"}, {"name": "Formação"}]},
        "Período": {
            "date": {
                "start": "2025-10-23T00:00:00.000-03:00",
                "end": "2026-06-30T23:59:59.000-03:00"
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "400+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Todas as formações e cursos relacionados a IA, desenvolvimento e tecnologias modernas."}}]}
    }
    
    formacoes_card = create_page(ESTUDOS_DB, formacoes_properties, main_card_id)
    if formacoes_card:
        formacoes_id = formacoes_card['id']
        print(f"✅ Formações e Cursos: {formacoes_id}")
    
    # Subitem: Projetos de Portfolio
    portfolio_properties = {
        "Project name": {"title": [{"text": {"content": "💼 Projetos de Portfolio"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Portfolio"}, {"name": "Desenvolvimento"}]},
        "Período": {
            "date": {
                "start": "2025-10-23T00:00:00.000-03:00",
                "end": "2026-12-31T23:59:59.000-03:00"
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "600+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Projetos práticos para demonstrar habilidades e construir portfolio profissional."}}]}
    }
    
    portfolio_card = create_page(ESTUDOS_DB, portfolio_properties, main_card_id)
    if portfolio_card:
        portfolio_id = portfolio_card['id']
        print(f"✅ Projetos de Portfolio: {portfolio_id}")
    
    print("\n" + "="*60)
    print("🎉 ESTRUTURA BÁSICA CRIADA NO NOTION!")
    print("="*60)
    print(f"📋 Card principal: {main_card_id}")
    print(f"📚 Formações: {formacoes_id if 'formacoes_id' in locals() else 'N/A'}")
    print(f"💼 Portfolio: {portfolio_id if 'portfolio_id' in locals() else 'N/A'}")

if __name__ == "__main__":
    main()
