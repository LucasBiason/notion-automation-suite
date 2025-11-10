#!/usr/bin/env python3
"""
Script para verificar os cards existentes na base personal
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

def get_personal_cards():
    """Busca todos os cards da base personal"""
    
    url = f"https://api.notion.com/v1/databases/1fa962a7-693c-8032-8996-dd9cd2607dbf/query"
    
    data = {
        "page_size": 100,
        "sorts": [
            {
                "property": "Data",
                "direction": "descending"
            }
        ]
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar cards: {response.status_code} - {response.text}")
        return []
    
    return response.json().get("results", [])

def main():
    """Função principal"""
    
    print("🔍 Verificando cards da base personal...")
    cards = get_personal_cards()
    
    if not cards:
        print("❌ Nenhum card encontrado")
        return
    
    print(f"📋 Total de cards encontrados: {len(cards)}")
    print("\n📝 Cards existentes:")
    
    for i, card in enumerate(cards[:20]):  # Mostrar apenas os 20 mais recentes
        # Buscar o título do card
        title_property = card.get("properties", {}).get("Tarefa", {})
        title = title_property.get("title", [{}])[0].get("text", {}).get("content", "")
        
        # Buscar o status
        status_property = card.get("properties", {}).get("Status", {})
        status = status_property.get("select", {}).get("name", "Sem status")
        
        # Buscar a data
        data_property = card.get("properties", {}).get("Data", {})
        data = data_property.get("date", {}).get("start", "Sem data")
        
        page_id = card["id"]
        
        print(f"{i+1:2d}. {title} | {status} | {data} | {page_id}")

if __name__ == "__main__":
    main()













