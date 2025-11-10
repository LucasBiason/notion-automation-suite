#!/usr/bin/env python3
"""
Script para criar cards usando os templates/modelos do Notion
"""

import sys
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
TOKEN = os.getenv('NOTION_API_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_database_templates():
    """Busca os templates disponíveis na base personal"""
    
    url = f"https://api.notion.com/v1/databases/1fa962a7-693c-8032-8996-dd9cd2607dbf"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar templates: {response.status_code}")
        return None
    
    database_info = response.json()
    
    # Verificar se há templates configurados
    if 'template_pages' in database_info:
        templates = database_info['template_pages']
        print(f"📋 Templates encontrados: {len(templates)}")
        
        for template in templates:
            print(f"  📌 {template.get('title', 'Sem título')}")
        
        return templates
    else:
        print("ℹ️ Nenhum template configurado na base")
        return []

def create_from_template(template_id: str, data: dict):
    """Cria um card a partir de um template"""
    
    url = f"https://api.notion.com/v1/pages"
    
    payload = {
        "parent": {"database_id": "1fa962a7-693c-8032-8996-dd9cd2607dbf"},
        "properties": {}
    }
    
    # Se o template tiver propriedades, usá-las como base
    # Por enquanto, vamos criar cards baseados nos templates conhecidos
    template_names = {
        "📝 Planejamento Semanal": {
            "title": "Planejamento Semanal",
            "atividade": "Gestão",
            "description": "Planejamento semanal e organização de tarefas"
        },
        "💰 Pagamento Hamilton (Médico)": {
            "title": "Pagamento Hamilton (Médico)",
            "atividade": "Finanças",
            "description": "Pagamento mensal do tratamento médico - Dr. Hamilton"
        },
        "🏥 Tratamento Médico": {
            "title": "Tratamento",
            "atividade": "Saúde",
            "description": "Sessão de tratamento médico"
        },
        "📊 Revisão Financeira": {
            "title": "Revisão Contábil",
            "atividade": "Finanças",
            "description": "Revisão contábil mensal"
        },
        "💰 Gestão de Pagamento": {
            "title": "Gestão de Pagamento",
            "atividade": "Finanças",
            "description": "Gestão mensal de pagamentos"
        },
        "💸 Pagamento de Impostos": {
            "title": "Pagamento de Impostos",
            "atividade": "Finanças",
            "description": "Pagamento mensal de impostos"
        }
    }
    
    # Usar os dados fornecidos ou padrões do template
    template_data = template_names.get(data.get('template_name', ''), {})
    
    payload["properties"] = {
        "Nome da tarefa": {"title": [{"text": {"content": data.get('title', template_data.get('title', 'Nova Tarefa'))}}]},
        "Status": {"status": {"name": data.get('status', 'Concluído')}},
        "Atividade": {"select": {"name": data.get('atividade', template_data.get('atividade', 'Desenvolvimento'))}},
        "Data": {"date": {"start": data.get('data', '2025-10-15')}},
        "Descrição": {"rich_text": [{"text": {"content": data.get('description', template_data.get('description', ''))}}]}
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f"❌ Erro ao criar card: {response.status_code} - {response.text}")
        return None

def create_weekly_cards_from_templates():
    """Cria cards da semana usando os templates"""
    
    print("🎯 Criando cards da semana usando templates do Notion...")
    
    # Cards da semana baseados nos templates
    weekly_cards = [
        {
            "template_name": "📝 Planejamento Semanal",
            "title": "Planejamento Semanal",
            "status": "Concluído",
            "data": "2025-10-14",
            "atividade": "Gestão",
            "description": "Planejamento semanal e organização de tarefas"
        },
        {
            "template_name": "💰 Pagamento Hamilton (Médico)",
            "title": "Pagamento Hamilton (Médico)",
            "status": "Concluído",
            "data": "2025-10-14",
            "atividade": "Finanças",
            "description": "Pagamento mensal do tratamento médico - Dr. Hamilton"
        },
        {
            "template_name": "🏥 Tratamento Médico",
            "title": "Tratamento",
            "status": "Concluído",
            "data": "2025-10-15",
            "atividade": "Saúde",
            "description": "Sessão de tratamento médico"
        },
        {
            "template_name": "📊 Revisão Financeira",
            "title": "Revisão Contábil",
            "status": "Concluído",
            "data": "2025-10-15",
            "atividade": "Finanças",
            "description": "Revisão contábil mensal - dia 15"
        },
        {
            "template_name": "💰 Gestão de Pagamento",
            "title": "Gestão de Pagamento",
            "status": "Concluído",
            "data": "2025-10-15",
            "atividade": "Finanças",
            "description": "Gestão mensal de pagamentos"
        },
        {
            "template_name": "💸 Pagamento de Impostos",
            "title": "Pagamento de Impostos",
            "status": "Concluído",
            "data": "2025-10-15",
            "atividade": "Finanças",
            "description": "Pagamento mensal de impostos"
        }
    ]
    
    created_cards = []
    
    for card_data in weekly_cards:
        print(f"📝 Criando: {card_data['title']} (template: {card_data['template_name']})")
        
        card_id = create_from_template(None, card_data)
        
        if card_id:
            created_cards.append({
                "title": card_data["title"],
                "id": card_id,
                "template": card_data["template_name"]
            })
            print(f"✅ {card_data['title']} criado com sucesso")
        else:
            print(f"❌ Falha ao criar: {card_data['title']}")
    
    # Resumo
    print(f"\n📊 RESUMO DOS CARDS CRIADOS:")
    print(f"📅 Semana: 13-19 de outubro")
    print(f"✅ Cards criados: {len(created_cards)}")
    
    for card in created_cards:
        print(f"  ✅ {card['title']} (template: {card['template']})")
    
    return created_cards

def main():
    """Função principal"""
    
    print("🔍 Verificando templates disponíveis...")
    templates = get_database_templates()
    
    print("\n🎯 Criando cards da semana...")
    create_weekly_cards_from_templates()

if __name__ == "__main__":
    main()













