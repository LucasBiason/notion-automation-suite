#!/usr/bin/env python3
"""
Script para deletar os cards incorretos criados
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

def archive_page(page_id: str):
    """Arquiva uma página do Notion"""
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    data = {
        "archived": True
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        print(f"✅ Página {page_id} arquivada com sucesso")
        return True
    else:
        print(f"❌ Erro ao arquivar página: {response.status_code} - {response.text}")
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
    
    # Cards incorretos para deletar (exceto o pagamento médico que está correto)
    wrong_titles = [
        "Limpeza da Casa",
        "Compras Supermercado", 
        "Backup dos Projetos",
        "Revisão de Estudos"
    ]
    
    deleted_count = 0
    
    for card in cards:
        # Buscar o título do card
        title_property = card.get("properties", {}).get("Tarefa", {})
        title = title_property.get("title", [{}])[0].get("text", {}).get("content", "")
        
        # Verificar se é um card incorreto
        if any(wrong_title in title for wrong_title in wrong_titles):
            page_id = card["id"]
            print(f"🗑️ Deletando card incorreto: {title}")
            if archive_page(page_id):
                deleted_count += 1
    
    print(f"✅ {deleted_count} cards incorretos deletados!")

if __name__ == "__main__":
    main()













