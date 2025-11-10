#!/usr/bin/env python3
"""
Atualizar card do ExpenseIQ Deploy no Notion
Marca todos os subitens como concluído e atualiza status do card principal
"""

import sys
import os
from dotenv import load_dotenv
import requests

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.notion_manager import NotionAPIManager, NotionConfig

# Configuração
TOKEN = os.getenv('NOTION_API_TOKEN', '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')
CARD_ID = '285962a7693c81c1a58dc80c08c42885'  # ID do card principal

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

def get_page_url(page_id):
    """Busca URL oficial do Notion"""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('url', f'https://www.notion.so/{page_id}')
    return f'https://www.notion.so/{page_id}'

def get_subitems(parent_id):
    """Busca todos os subitens de um card"""
    # Buscar na database de trabalho
    db_id = '1f9962a7693c80a3b947c471a975acb0'
    url = f'https://api.notion.com/v1/databases/{db_id}/query'
    
    query = {
        "filter": {
            "property": "item principal",
            "relation": {"contains": parent_id}
        }
    }
    
    response = requests.post(url, headers=headers, json=query)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        return results
    else:
        print(f"❌ Erro ao buscar subitens: {response.status_code}")
        return []

def update_page_status(page_id, status, add_notes=None):
    """Atualiza status de uma página"""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    
    update_data = {
        "properties": {
            "Status": {
                "status": {"name": status}
            }
        }
    }
    
    response = requests.patch(url, headers=headers, json=update_data)
    
    if response.status_code == 200:
        return True
    else:
        print(f"❌ Erro ao atualizar {page_id}: {response.status_code}")
        return False

def main():
    print("=" * 80)
    print("🔄 ATUALIZANDO CARD DO NOTION - EXPENSEIQ DEPLOY")
    print("=" * 80)
    
    # Normalizar ID (remover hífens)
    card_id_normalized = CARD_ID.replace('-', '')
    
    # 1. Buscar subitens
    print(f"\n📋 1. Buscando subitens do card principal...")
    subitems = get_subitems(card_id_normalized)
    
    print(f"✅ Encontrados {len(subitems)} subitens")
    
    # 2. Marcar todos como concluído
    print(f"\n✅ 2. Marcando todos os subitens como 'Concluído'...")
    
    for i, item in enumerate(subitems, 1):
        item_id = item['id']
        
        # Extrair título
        title_prop = item['properties'].get('Nome do projeto', {})
        title = 'Sem título'
        if title_prop.get('title'):
            title = title_prop['title'][0]['text']['content']
        
        # Extrair status atual
        status_prop = item['properties'].get('Status', {})
        status_atual = status_prop.get('status', {}).get('name', 'Desconhecido')
        
        # Atualizar para Concluído
        success = update_page_status(item_id, 'Concluído')
        
        if success:
            print(f"   ✅ [{i}/{len(subitems)}] {title}")
            print(f"      Status: {status_atual} → Concluído")
        else:
            print(f"   ❌ [{i}/{len(subitems)}] {title} - FALHOU")
    
    # 3. Atualizar card principal para "Revisando"
    print(f"\n🔄 3. Atualizando card principal para 'Revisando'...")
    
    success = update_page_status(card_id_normalized, 'Em Revisão')
    
    if success:
        print(f"✅ Card principal atualizado para 'Em Revisão'")
    else:
        print(f"❌ Erro ao atualizar card principal")
    
    # 4. Mostrar URL
    print(f"\n🔗 Card principal:")
    card_url = get_page_url(card_id_normalized)
    print(f"   {card_url}")
    
    print("\n" + "=" * 80)
    print("✅ ATUALIZAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print(f"\n📊 Resumo:")
    print(f"   - {len(subitems)} subitens marcados como 'Concluído'")
    print(f"   - Card principal marcado como 'Em Revisão'")
    print(f"\n🔗 Verifique: {card_url}")

if __name__ == "__main__":
    main()













