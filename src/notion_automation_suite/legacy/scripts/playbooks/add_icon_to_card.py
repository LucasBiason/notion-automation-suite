#!/usr/bin/env python3
"""
Script para adicionar ícone a um card específico
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

def add_icon_to_card(page_id: str, emoji: str):
    """Adiciona um ícone a um card específico"""
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    data = {
        "icon": {
            "type": "emoji",
            "emoji": emoji
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        print(f"✅ Ícone {emoji} adicionado ao card {page_id}")
        return True
    else:
        print(f"❌ Erro ao adicionar ícone: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    # ID do card de consulta médica criado
    card_id = "28d962a7-693c-816a-b1af-df512c4df0d0"
    
    print(f"🎨 Adicionando ícone 🏥 ao card de consulta médica...")
    add_icon_to_card(card_id, "🏥")













