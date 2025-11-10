#!/usr/bin/env python3
"""
Script para verificar as propriedades da base personal
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

def get_database_properties():
    """Busca as propriedades da base personal"""
    
    url = f"https://api.notion.com/v1/databases/1fa962a7-693c-8032-8996-dd9cd2607dbf"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar base: {response.status_code} - {response.text}")
        return None
    
    database_info = response.json()
    properties = database_info.get("properties", {})
    
    print("📋 Propriedades da base PERSONAL:")
    for prop_name, prop_info in properties.items():
        prop_type = prop_info.get("type", "unknown")
        print(f"  - {prop_name}: {prop_type}")
    
    return properties

def main():
    """Função principal"""
    
    print("🔍 Verificando propriedades da base personal...")
    properties = get_database_properties()
    
    if properties:
        print(f"✅ Encontradas {len(properties)} propriedades")

if __name__ == "__main__":
    main()













