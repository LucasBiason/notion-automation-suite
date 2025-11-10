#!/usr/bin/env python3
"""
Script simples para adicionar ícones aos cards pessoais
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

def add_page_icon(page_id: str, emoji: str):
    """Adiciona um ícone a uma página do Notion"""
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    data = {
        "icon": {
            "type": "emoji",
            "emoji": emoji
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        print(f"✅ Ícone {emoji} adicionado à página {page_id}")
        return True
    else:
        print(f"❌ Erro ao adicionar ícone: {response.status_code} - {response.text}")
        return False

def get_recent_personal_cards():
    """Busca os cards mais recentes da base personal"""
    
    url = f"https://api.notion.com/v1/databases/1fa962a7-693c-8032-8996-dd9cd2607dbf/query"
    
    data = {
        "page_size": 10,
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
    
    print("🔍 Buscando cards recentes da base personal...")
    cards = get_recent_personal_cards()
    
    if not cards:
        print("❌ Nenhum card encontrado")
        return
    
    print(f"📋 Encontrados {len(cards)} cards")
    
    # Lista de emojis para os cards da semana
    emojis = ["💰", "🏠", "🛒", "💻", "📚"]
    
    # Adicionar ícones aos 5 cards mais recentes
    for i, card in enumerate(cards[:5]):
        page_id = card["id"]
        emoji = emojis[i] if i < len(emojis) else "📝"
        
        print(f"🎨 Adicionando ícone {emoji} ao card {i+1}...")
        add_page_icon(page_id, emoji)
    
    print("✅ Concluído!")

if __name__ == "__main__":
    main()













