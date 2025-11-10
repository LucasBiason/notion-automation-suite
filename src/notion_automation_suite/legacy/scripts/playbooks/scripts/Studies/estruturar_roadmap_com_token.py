#!/usr/bin/env python3
"""
Script para estruturar o Roadmap Completo no Notion
Solicita token do usuário para execução
"""

import requests
import os
from datetime import datetime
import pytz

# Configurações
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

def format_date_gmt3(date_obj):
    """Formata data para GMT-3 (São Paulo)."""
    tz = pytz.timezone('America/Sao_Paulo')
    return date_obj.astimezone(tz).strftime('%Y-%m-%dT%H:%M:%S.000-03:00')

def create_page(database_id, properties, parent_id=None, icon=None, headers=None):
    """Cria uma página no Notion."""
    url = 'https://api.notion.com/v1/pages'
    
    payload = {
        'parent': {'database_id': database_id},
        'properties': properties
    }
    if parent_id:
        payload['properties']['Item Principal'] = {"relation": [{"id": parent_id}]}
    if icon:
        payload['icon'] = icon
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao criar página: {response.status_code} - {response.text}")
        return None

def add_content_to_page(page_id, blocks, headers=None):
    """Adiciona conteúdo (blocos) a uma página."""
    response = requests.patch(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers=headers,
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
                "rich_text": [{"type": "text", "text": {"content": "Roadmap completo para se tornar Engenheiro de Software com especialização em IA. Inclui formações, projetos de portfolio e desenvolvimento de habilidades técnicas."}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📊 Estatísticas"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Duração: 15 meses (Out 2025 - Dez 2026)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Horas totais: 1000+ horas"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Formações: 4 cursos"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Projetos: 4 projetos principais"}}]
            }
        }
    ]

def get_formacoes_content():
    """Conteúdo detalhado para Formações e Cursos."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "📚 Formações e Cursos"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Todas as formações e cursos relacionados a IA, desenvolvimento e tecnologias modernas."}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎓 Cursos Incluídos"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Pós Tech FIAP - IA para Devs (Em andamento)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Udemy - Formação Completa IA e ML"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Rocketseat - IA na Prática do Zero"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Rocketseat - IA para Devs"}}]
            }
        }
    ]

def get_portfolio_content():
    """Conteúdo detalhado para Projetos de Portfolio."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "💼 Projetos de Portfolio"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Projetos práticos para demonstrar habilidades e construir portfolio profissional."}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🚀 Projetos Incluídos"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "MyLocalPlace v2.0 - Modernização completa"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "FastAPI Microservice Framework - Biblioteca reutilizável"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "IntelliCart - E-commerce com CQRS e Event Sourcing"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "IA Knowledge Base - Base de conhecimento em IA"}}]
            }
        }
    ]

def main():
    """Função principal - Estrutura o Roadmap Completo."""
    print("🚀 ESTRUTURANDO ROADMAP COMPLETO NO NOTION")
    print("="*60)
    
    # Solicitar token do Notion
    notion_token = input("🔑 Digite seu token do Notion: ").strip()
    
    if not notion_token:
        print("❌ Token é obrigatório!")
        return
    
    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    
    # 1. CRIAR CARD PRINCIPAL
    print("\n📋 1. Criando card principal...")
    
    main_card_properties = {
        "Project name": {"title": [{"text": {"content": "Roadmap Engenheiro de Software IA 2025-26"}}]},
        "Status": {"status": {"name": "Em andamento"}},
        "Prioridade": {"select": {"name": "Crítica"}},
        "Categorias": {"multi_select": [{"name": "Roadmap"}, {"name": "Desenvolvimento"}, {"name": "IA"}]},
        "Período": {
            "date": {
                "start": format_date_gmt3(datetime(2025, 10, 22)),
                "end": format_date_gmt3(datetime(2026, 12, 31))
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "1000+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Roadmap completo para se tornar Engenheiro de Software com especialização em IA. Inclui formações, projetos de portfolio e desenvolvimento de habilidades técnicas."}}]}
    }
    
    main_card = create_page(ESTUDOS_DB, main_card_properties, icon={"type": "emoji", "emoji": "📊"}, headers=headers)
    
    if not main_card:
        print("❌ Falha ao criar card principal!")
        return
    
    main_card_id = main_card['id']
    print(f"✅ Card principal criado: {main_card_id}")
    
    # Adicionar conteúdo detalhado ao card principal
    print("📝 Adicionando conteúdo detalhado ao card principal...")
    add_content_to_page(main_card_id, get_roadmap_main_content(), headers)
    
    # 2. CRIAR SUBITENS PRINCIPAIS
    print("\n📋 2. Criando subitens principais...")
    
    # Subitem: Formações e Cursos
    formacoes_properties = {
        "Project name": {"title": [{"text": {"content": "Formações e Cursos"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Estudos"}, {"name": "Formação"}]},
        "Período": {
            "date": {
                "start": format_date_gmt3(datetime(2025, 10, 23)),
                "end": format_date_gmt3(datetime(2026, 6, 30))
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "400+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Todas as formações e cursos relacionados a IA, desenvolvimento e tecnologias modernas."}}]}
    }
    
    formacoes_card = create_page(ESTUDOS_DB, formacoes_properties, main_card_id, icon={"type": "emoji", "emoji": "📚"}, headers=headers)
    if formacoes_card:
        formacoes_id = formacoes_card['id']
        print(f"✅ Formações e Cursos: {formacoes_id}")
        
        # Adicionar conteúdo detalhado
        print("📝 Adicionando conteúdo detalhado às Formações...")
        add_content_to_page(formacoes_id, get_formacoes_content(), headers)
    
    # Subitem: Projetos de Portfolio
    portfolio_properties = {
        "Project name": {"title": [{"text": {"content": "Projetos de Portfolio"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Portfolio"}, {"name": "Desenvolvimento"}]},
        "Período": {
            "date": {
                "start": format_date_gmt3(datetime(2025, 10, 23)),
                "end": format_date_gmt3(datetime(2026, 12, 31))
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "600+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Projetos práticos para demonstrar habilidades e construir portfolio profissional."}}]}
    }
    
    portfolio_card = create_page(ESTUDOS_DB, portfolio_properties, main_card_id, icon={"type": "emoji", "emoji": "💼"}, headers=headers)
    if portfolio_card:
        portfolio_id = portfolio_card['id']
        print(f"✅ Projetos de Portfolio: {portfolio_id}")
        
        # Adicionar conteúdo detalhado
        print("📝 Adicionando conteúdo detalhado ao Portfolio...")
        add_content_to_page(portfolio_id, get_portfolio_content(), headers)
    
    # 3. CRIAR CARDS DE FORMAÇÕES
    print("\n📚 3. Criando cards de formações...")
    
    formacoes_list = [
        {
            "name": "Pós Tech FIAP - IA para Devs",
            "status": "Em andamento",
            "periodo": ("2025-03-27T00:00:00.000-03:00", "2026-02-28T23:59:59.000-03:00"),
            "tempo": "200+ horas",
            "desc": "Formação principal em IA para desenvolvedores - Fase 4 em andamento",
            "icon": "🎓"
        },
        {
            "name": "Udemy - Formação Completa IA e ML",
            "status": "Para Fazer",
            "periodo": ("2025-11-01T00:00:00.000-03:00", "2026-03-31T23:59:59.000-03:00"),
            "tempo": "100+ horas",
            "desc": "Formação complementar em IA e Machine Learning",
            "icon": "📚"
        },
        {
            "name": "Rocketseat - IA na Prática do Zero",
            "status": "Para Fazer",
            "periodo": ("2025-12-01T00:00:00.000-03:00", "2026-02-28T23:59:59.000-03:00"),
            "tempo": "80+ horas",
            "desc": "Formação prática em IA com projetos reais",
            "icon": "🚀"
        },
        {
            "name": "Rocketseat - IA para Devs",
            "status": "Para Fazer",
            "periodo": ("2026-03-01T00:00:00.000-03:00", "2026-05-31T23:59:59.000-03:00"),
            "tempo": "60+ horas",
            "desc": "Aprofundamento em IA para desenvolvedores",
            "icon": "🚀"
        }
    ]
    
    for formacao in formacoes_list:
        formacao_properties = {
            "Project name": {"title": [{"text": {"content": formacao["name"]}}]},
            "Status": {"status": {"name": formacao["status"]}},
            "Prioridade": {"select": {"name": "Alta"}},
            "Categorias": {"multi_select": [{"name": "Formação"}, {"name": "IA"}]},
            "Período": {
                "date": {
                    "start": formacao["periodo"][0],
                    "end": formacao["periodo"][1]
                }
            },
            "Tempo Total": {"rich_text": [{"text": {"content": formacao["tempo"]}}]},
            "Descrição": {"rich_text": [{"text": {"content": formacao["desc"]}}]},
            "Item Principal": {"relation": [{"id": formacoes_id}]}
        }
        formacao_card = create_page(ESTUDOS_DB, formacao_properties, icon={"type": "emoji", "emoji": formacao["icon"]}, headers=headers)
        if formacao_card:
            print(f"✅ {formacao['name']}: {formacao_card['id']}")
    
    # 4. CRIAR CARDS DE PROJETOS
    print("\n💼 4. Criando cards de projetos...")
    
    projetos_list = [
        {
            "name": "MyLocalPlace v2.0",
            "status": "Para Fazer",
            "periodo": ("2025-10-23T00:00:00.000-03:00", "2025-12-31T23:59:59.000-03:00"),
            "tempo": "120+ horas",
            "desc": "Modernização do ambiente local de desenvolvimento com dashboard Streamlit",
            "icon": "🚀"
        },
        {
            "name": "FastAPI Microservice Framework",
            "status": "Para Fazer",
            "periodo": ("2025-11-01T00:00:00.000-03:00", "2026-02-28T23:59:59.000-03:00"),
            "tempo": "200+ horas",
            "desc": "Biblioteca reutilizável para criação de microserviços FastAPI",
            "icon": "🔧"
        },
        {
            "name": "IntelliCart - E-commerce com CQRS",
            "status": "Para Fazer",
            "periodo": ("2026-01-01T00:00:00.000-03:00", "2026-08-31T23:59:59.000-03:00"),
            "tempo": "300+ horas",
            "desc": "E-commerce completo com CQRS, Event Sourcing e IA",
            "icon": "🛒"
        },
        {
            "name": "IA Knowledge Base",
            "status": "Em andamento",
            "periodo": ("2025-09-01T00:00:00.000-03:00", "2026-12-31T23:59:59.000-03:00"),
            "tempo": "100+ horas",
            "desc": "Base de conhecimento em IA com resumos e exercícios",
            "icon": "🧠"
        }
    ]
    
    for projeto in projetos_list:
        projeto_properties = {
            "Project name": {"title": [{"text": {"content": projeto["name"]}}]},
            "Status": {"status": {"name": projeto["status"]}},
            "Prioridade": {"select": {"name": "Alta"}},
            "Categorias": {"multi_select": [{"name": "Portfolio"}, {"name": "Desenvolvimento"}]},
            "Período": {
                "date": {
                    "start": projeto["periodo"][0],
                    "end": projeto["periodo"][1]
                }
            },
            "Tempo Total": {"rich_text": [{"text": {"content": projeto["tempo"]}}]},
            "Descrição": {"rich_text": [{"text": {"content": projeto["desc"]}}]},
            "Item Principal": {"relation": [{"id": portfolio_id}]}
        }
        
        projeto_card = create_page(ESTUDOS_DB, projeto_properties, icon={"type": "emoji", "emoji": projeto["icon"]}, headers=headers)
        if projeto_card:
            print(f"✅ {projeto['name']}: {projeto_card['id']}")
    
    print("\n" + "="*60)
    print("🎉 ESTRUTURA COMPLETA CRIADA NO NOTION!")
    print("="*60)
    print(f"📋 Card principal: {main_card_id}")
    print(f"📚 Formações: {formacoes_id}")
    print(f"💼 Portfolio: {portfolio_id}")

if __name__ == "__main__":
    main()
