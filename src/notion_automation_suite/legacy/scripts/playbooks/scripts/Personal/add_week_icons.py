#!/usr/bin/env python3
"""
Script para adicionar ícones aos cards da semana
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
        print(f"✅ Ícone {emoji} adicionado à página")
        return True
    else:
        print(f"❌ Erro ao adicionar ícone: {response.status_code}")
        return False

def get_recent_cards():
    """Busca os cards mais recentes"""
    
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
        print(f"❌ Erro ao buscar cards: {response.status_code}")
        return []
    
    return response.json().get("results", [])

def main():
    """Função principal"""
    
    print("🔍 Buscando cards recentes...")
    cards = get_recent_cards()
    
    if not cards:
        print("❌ Nenhum card encontrado")
        return
    
    # Mapa de títulos para emojis
    title_emoji_map = {
        "Planejamento Semanal": "📝",
        "Pagamento Hamilton (Médico)": "💰",
        "Tratamento": "🏥",
        "Revisão Contábil": "📊",
        "Gestão de Pagamento": "💰",
        "Pagamento de Impostos": "💸"
    }
    
    print(f"📋 Encontrados {len(cards)} cards")
    print("🎨 Adicionando ícones...")
    
    for card in cards[:6]:  # Apenas os 6 mais recentes
        # Buscar o título
        title_property = card.get("properties", {}).get("Nome da tarefa", {})
        title = title_property.get("title", [{}])[0].get("text", {}).get("content", "")
        
        page_id = card["id"]
        
        if title in title_emoji_map:
            emoji = title_emoji_map[title]
            print(f"  {emoji} {title}")
            add_page_icon(page_id, emoji)
    
    print("✅ Ícones adicionados!")

if __name__ == "__main__":
    main()













