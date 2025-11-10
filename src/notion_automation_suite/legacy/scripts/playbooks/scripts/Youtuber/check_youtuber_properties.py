#!/usr/bin/env python3
"""
Script para verificar propriedades da base YOUTUBER
"""

import requests

TOKEN = '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'
YOUTUBER_DB_ID = '1fa962a7-693c-80ce-9f1d-ff86223d6bda'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

url = f'https://api.notion.com/v1/databases/{YOUTUBER_DB_ID}'
response = requests.get(url, headers=headers, timeout=30)

if response.status_code == 200:
    data = response.json()
    properties = data.get('properties', {})
    
    print("📊 PROPRIEDADES DA BASE YOUTUBER:")
    print("="*60)
    for prop_name, prop_data in properties.items():
        prop_type = prop_data.get('type', 'unknown')
        print(f"  {prop_name}: {prop_type}")
        
        # Se for select ou status, mostrar opções
        if prop_type == 'select' and 'select' in prop_data:
            options = prop_data['select'].get('options', [])
            print(f"    Opções: {[opt['name'] for opt in options]}")
        elif prop_type == 'status' and 'status' in prop_data:
            options = prop_data['status'].get('options', [])
            print(f"    Opções: {[opt['name'] for opt in options]}")
else:
    print(f"❌ Erro: {response.status_code}")
    print(response.text)



