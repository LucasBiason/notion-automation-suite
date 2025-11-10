#!/usr/bin/env python3
"""
Script para adicionar ícones aos cards pessoais da semana
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

def add_icons_to_personal_cards():
    """Adiciona ícones aos cards pessoais da semana"""
    
    # IDs dos cards criados (você pode obter estes IDs do output do script anterior)
    # Vou buscar os cards mais recentes da base personal
    
    url = f"https://api.notion.com/v1/databases/1fa962a7-693c-8032-8996-dd9cd2607dbf/query"
    
    # Buscar os 5 cards mais recentes
    data = {
        "page_size": 5,
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
        return
    
    results = response.json().get("results", [])
    
    # Mapear títulos para emojis
    title_emoji_map = {
        "💰 Pagamento Médico": "💰",
        "🏠 Limpeza da Casa": "🏠", 
        "🛒 Compras Supermercado": "🛒",
        "💻 Backup dos Projetos": "💻",
        "📚 Revisão de Estudos": "📚"
    }
    
    print(f"🎨 Adicionando ícones a {len(results)} cards...")
    
    for card in results:
        title_property = card.get("properties", {}).get("Tarefa", {})
        title = title_property.get("title", [{}])[0].get("text", {}).get("content", "")
        
        if title in title_emoji_map:
            page_id = card["id"]
            emoji = title_emoji_map[title]
            
            # Remover emoji do título se já existir
            clean_title = title.replace(emoji + " ", "")
            
            # Atualizar título sem emoji
            update_title(page_id, clean_title)
            
            # Adicionar ícone
            add_page_icon(page_id, emoji)
        else:
            print(f"⚠️ Título não mapeado: {title}")

def update_title(page_id: str, new_title: str):
    """Atualiza o título de uma página"""
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    data = {
        "properties": {
            "Tarefa": {
                "title": [
                    {
                        "text": {
                            "content": new_title
                        }
                    }
                ]
            }
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        print(f"✅ Título atualizado: {new_title}")
        return True
    else:
        print(f"❌ Erro ao atualizar título: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    add_icons_to_personal_cards()
