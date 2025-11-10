#!/usr/bin/env python3
"""Buscar ID correto da Fase 4"""

import requests

NOTION_TOKEN = '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'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def query_database(database_id, filter_params=None):
    """Consulta database do Notion."""
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    payload = {}
    if filter_params:
        payload['filter'] = filter_params
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro: {response.status_code} - {response.text}")
        return None

# Buscar Fase 4
filter_fase4 = {
    "property": "Project name",
    "title": {
        "contains": "Fase 4"
    }
}

print("🔍 Buscando Fase 4...\n")
resultado = query_database(ESTUDOS_DB, filter_fase4)

if resultado and len(resultado['results']) > 0:
    for page in resultado['results']:
        titulo = page['properties']['Project name']['title'][0]['text']['content']
        page_id = page['id']
        print(f"📚 {titulo}")
        print(f"   ID: {page_id}\n")
else:
    print("❌ Fase 4 não encontrada!")










