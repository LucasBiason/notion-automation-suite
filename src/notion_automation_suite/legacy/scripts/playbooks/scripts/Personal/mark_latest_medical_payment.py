#!/usr/bin/env python3
"""
Script para marcar o pagamento médico mais recente como concluído
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
                "status": {
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

def find_latest_medical_payment():
    """Busca o card de pagamento médico mais recente"""
    
    url = f"https://api.notion.com/v1/databases/1fa962a7-693c-8032-8996-dd9cd2607dbf/query"
    
    # Buscar o card mais recente de pagamento médico
    data = {
        "filter": {
            "property": "Nome da tarefa",
            "title": {
                "contains": "Hamilton"
            }
        },
        "sorts": [
            {
                "property": "Data",
                "direction": "descending"
            }
        ],
        "page_size": 1
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar cards: {response.status_code} - {response.text}")
        return None
    
    results = response.json().get("results", [])
    return results[0] if results else None

def main():
    """Função principal"""
    
    print("🔍 Buscando o pagamento médico mais recente...")
    card = find_latest_medical_payment()
    
    if not card:
        print("❌ Nenhum card de pagamento médico encontrado")
        return
    
    # Buscar informações do card
    title_property = card.get("properties", {}).get("Nome da tarefa", {})
    title = title_property.get("title", [{}])[0].get("text", {}).get("content", "")
    
    status_property = card.get("properties", {}).get("Status", {})
    current_status = status_property.get("select", {}).get("name", "Sem status")
    
    page_id = card["id"]
    
    print(f"📝 Card encontrado: {title}")
    print(f"📊 Status atual: {current_status}")
    
    # Marcar como concluído
    if current_status != "Concluído":
        print(f"✅ Marcando como concluído...")
        if update_card_status(page_id, "Concluído"):
            print("🎉 Pagamento médico marcado como concluído!")
    else:
        print("ℹ️ O pagamento médico já está marcado como concluído")

if __name__ == "__main__":
    main()
