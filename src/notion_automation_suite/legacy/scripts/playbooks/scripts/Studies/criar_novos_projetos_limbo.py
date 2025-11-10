#!/usr/bin/env python3
"""
Criar cards para novos projetos identificados no Limbo
"""

import requests
from datetime import datetime
import pytz

NOTION_TOKEN = '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'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'
PORTFOLIO_CARD_ID = '294962a7-693c-81be-afc2-e098c9ac8b92'  # Projetos de Portfolio

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

gmt3 = pytz.timezone('America/Sao_Paulo')

def format_date_gmt3(dt):
    return gmt3.localize(dt).isoformat()

def create_page(database_id, properties, parent_id=None, icon=None):
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
        print(f"❌ Erro ao criar página: {response.status_code} - {response.text}")
        return None

def add_content_to_page(page_id, blocks):
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    payload = {'children': blocks}
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    return response.status_code == 200

def main():
    print("\n" + "="*70)
    print("📦 CRIANDO NOVOS PROJETOS DO LIMBO")
    print("="*70 + "\n")
    
    projetos_criados = []
    
    # 1. Smart OCR Platform
    print("🔍 Criando Smart OCR Platform...")
    
    ocr_properties = {
        "Project name": {"title": [{"text": {"content": "Smart OCR Platform"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [
            {"name": "Portfolio"}, 
            {"name": "IA/ML"}, 
            {"name": "API"},
            {"name": "Microserviço"}
        ]},
        "Tempo Total": {"rich_text": [{"text": {"content": "120 horas (5 semanas)"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Plataforma multimodal de OCR com cadastro de modelos de extração. Suporta múltiplas LLMs (OpenAI, Claude, Gemini, Ollama, DeepSeek) com seleção manual ou automática. Dashboard Streamlit para gestão de modelos."}}]}
    }
    
    ocr_card = create_page(
        ESTUDOS_DB,
        ocr_properties,
        parent_id=PORTFOLIO_CARD_ID,
        icon={"type": "emoji", "emoji": "🔍"}
    )
    
    if ocr_card:
        ocr_id = ocr_card['id']
        print(f"✅ Smart OCR Platform criado: {ocr_id}")
        projetos_criados.append(("Smart OCR Platform", ocr_id))
        
        # Adicionar conteúdo detalhado
        ocr_content = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "🎯 Objetivo"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Criar uma plataforma genérica de OCR multimodal onde é possível cadastrar modelos de extração personalizados com prompts, validações e escolha de LLM."}}]}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "✨ Features Principais"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Cadastro de modelos de extração com prompts customizados"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Multi-LLM: OpenAI, Claude, Gemini, Ollama, DeepSeek"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Modo AUTO (igual ao Cursor) ou seleção manual de modelo"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Validações: regex, range, enum, Python customizado"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Dashboard Streamlit para gestão de modelos"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "API REST completa para extração"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Fallback automático entre LLMs"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Confidence scoring e A/B testing"}}]}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "🛠️ Stack Técnica"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Backend: FastAPI, LiteLLM, PostgreSQL, Redis, Celery"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Frontend: Streamlit com Plotly"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": "AI: OpenAI, Anthropic, Google, Ollama, DeepSeek SDKs"}}]}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "📋 Diferenciais"}}]}
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Multi-LLM com modo AUTO (único no mercado)"}}]}
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Validações Python executadas no servidor"}}]}
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Dashboard completo de gestão"}}]}
            },
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Histórico e auditoria completa"}}]}
            }
        ]
        
        add_content_to_page(ocr_id, ocr_content)
    
    # 2. Celery Job Manager & Queue Monitor (2 projetos separados)
    print("\n🔄 Criando Celery Job Manager...")
    
    job_manager_properties = {
        "Project name": {"title": [{"text": {"content": "Celery Job Manager"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [
            {"name": "Portfolio"}, 
            {"name": "Microserviço"},
            {"name": "FastAPI"},
            {"name": "Async"}
        ]},
        "Tempo Total": {"rich_text": [{"text": {"content": "80 horas (4 semanas)"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Microserviço de gerenciamento de Jobs assíncronos com Celery/Redis. FastAPI + Streamlit para monitoramento em tempo real com progress bar. Agendamento (único/recorrente), retry, webhooks."}}]}
    }
    
    job_card = create_page(
        ESTUDOS_DB,
        job_manager_properties,
        parent_id=PORTFOLIO_CARD_ID,
        icon={"type": "emoji", "emoji": "⚙️"}
    )
    
    if job_card:
        job_id = job_card['id']
        print(f"✅ Celery Job Manager criado: {job_id}")
        projetos_criados.append(("Celery Job Manager", job_id))
    
    print("\n📬 Criando Queue Monitor...")
    
    queue_monitor_properties = {
        "Project name": {"title": [{"text": {"content": "Queue Monitor - Event Stream Tracker"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Média"}},
        "Categorias": {"multi_select": [
            {"name": "Portfolio"}, 
            {"name": "Microserviço"},
            {"name": "Observabilidade"}
        ]},
        "Tempo Total": {"rich_text": [{"text": {"content": "60 horas (3 semanas)"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Microserviço de monitoramento de filas (RabbitMQ, Redis Streams, Kafka). Dashboard em tempo real para visualizar eventos, dead letters, latência, throughput. Ideal para sistemas event-driven."}}]}
    }
    
    queue_card = create_page(
        ESTUDOS_DB,
        queue_monitor_properties,
        parent_id=PORTFOLIO_CARD_ID,
        icon={"type": "emoji", "emoji": "📬"}
    )
    
    if queue_card:
        queue_id = queue_card['id']
        print(f"✅ Queue Monitor criado: {queue_id}")
        projetos_criados.append(("Queue Monitor", queue_id))
    
    # 3. MoneSync (em holding)
    print("\n💰 Criando MoneSync (Holding)...")
    
    money_properties = {
        "Project name": {"title": [{"text": {"content": "MoneSync - Financial Automation"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Baixa"}},
        "Categorias": {"multi_select": [
            {"name": "Portfolio"}, 
            {"name": "Uso Pessoal"},
            {"name": "ML"},
            {"name": "Automação"}
        ]},
        "Tempo Total": {"rich_text": [{"text": {"content": "80 horas (4 semanas)"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Sistema financeiro pessoal completo. Importação automática (CSV, OCR, Email, APIs bancárias), categorização ML, orçamento, investimentos. Dashboard Streamlit. Projeto para uso pessoal futuro."}}]}
    }
    
    money_card = create_page(
        ESTUDOS_DB,
        money_properties,
        parent_id=PORTFOLIO_CARD_ID,
        icon={"type": "emoji", "emoji": "💰"}
    )
    
    if money_card:
        money_id = money_card['id']
        print(f"✅ MoneSync criado: {money_id}")
        projetos_criados.append(("MoneSync", money_id))
    
    print("\n" + "="*70)
    print("✅ PROJETOS CRIADOS COM SUCESSO!")
    print("="*70)
    print("\nResumo:")
    for nome, card_id in projetos_criados:
        print(f"  ✅ {nome}")
        print(f"     https://www.notion.so/{card_id.replace('-', '')}")
    
    print("\n⚠️  IMPORTANTE: Estes projetos ainda NÃO estão no cronograma")
    print("    Aguardando definição de quando encaixá-los no roadmap")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
