#!/usr/bin/env python3
"""
Script para marcar o pagamento médico como concluído
"""

import sys
import os
import requests
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

def update_card_status(page_id: str, status: str):
    """Atualiza o status de um card"""
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    data = {
        "properties": {
            "Status": {
                "select": {
                    "name": status
                }
            }
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        print(f"✅ Status atualizado para '{status}' na página {page_id}")
        return True
    else:
        print(f"❌ Erro ao atualizar status: {response.status_code} - {response.text}")
        return False

def find_medical_payment_card():
    """Busca o card de pagamento médico"""
    
    url = f"https://api.notion.com/v1/databases/1fa962a7-693c-8032-8996-dd9cd2607dbf/query"
    
    # Buscar cards com "Pagamento" no título
    data = {
        "filter": {
            "property": "Tarefa",
            "title": {
                "contains": "Pagamento"
            }
        },
        "page_size": 10
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar cards: {response.status_code} - {response.text}")
        return []
    
    return response.json().get("results", [])

def main():
    """Função principal"""
    
    print("🔍 Buscando cards de pagamento médico...")
    cards = find_medical_payment_card()
    
    if not cards:
        print("❌ Nenhum card de pagamento encontrado")
        return
    
    print(f"📋 Encontrados {len(cards)} cards de pagamento")
    
    for card in cards:
        # Buscar o título do card
        title_property = card.get("properties", {}).get("Tarefa", {})
        title = title_property.get("title", [{}])[0].get("text", {}).get("content", "")
        
        # Buscar o status atual
        status_property = card.get("properties", {}).get("Status", {})
        current_status = status_property.get("select", {}).get("name", "Sem status")
        
        page_id = card["id"]
        
        print(f"📝 Card: {title} | Status atual: {current_status}")
        
        # Se for o pagamento de tratamento e não estiver concluído, marcar como concluído
        if "Tratamento" in title and current_status != "Concluído":
            print(f"✅ Marcando como concluído: {title}")
            update_card_status(page_id, "Concluído")
        elif "Pagamento Médico" in title and current_status != "Concluído":
            print(f"✅ Marcando como concluído: {title}")
            update_card_status(page_id, "Concluído")

if __name__ == "__main__":
    main()

