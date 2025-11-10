#!/usr/bin/env python3
"""Verificar propriedades do database de Estudos"""

import requests
import json

NOTION_TOKEN = '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'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

url = f'https://api.notion.com/v1/databases/{ESTUDOS_DB}'
response = requests.get(url, headers=headers, timeout=60)

if response.status_code == 200:
    db_info = response.json()
    print("📊 PROPRIEDADES DO DATABASE:\n")
    for prop_name, prop_info in db_info['properties'].items():
        print(f"   - {prop_name}: {prop_info['type']}")
else:
    print(f"❌ Erro: {response.status_code} - {response.text}")










