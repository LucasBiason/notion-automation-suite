#!/usr/bin/env python3
"""
Corrigir curso Algoritmos Genéticos:
1. Remover todas as aulas das seções
2. Marcar seções como Concluido
"""

import requests

# Configuração
NOTION_TOKEN = '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'
NOTION_VERSION = '2022-06-28'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

# IDs das seções
SECOES = [
    "20a962a7-693c-8035-810b-f4881a392072",  # Seção 2
    "20a962a7-693c-80b0-a093-f45c9b71d1b7",  # Seção 1
]

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
        return None

def delete_page(page_id):
    """Arquiva (deleta) uma página."""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    payload = {'archived': True}
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    return response.status_code == 200

def update_page(page_id, properties):
    """Atualiza uma página."""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    payload = {'properties': properties}
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    return response.status_code == 200

print("\n" + "="*70)
print("🔧 CORRIGINDO CURSO ALGORITMOS GENÉTICOS")
print("="*70 + "\n")

total_removidas = 0

for secao_id in SECOES:
    # Buscar aulas desta seção
    filter_aulas = {
        "property": "Parent item",
        "relation": {"contains": secao_id}
    }
    
    aulas = query_database(ESTUDOS_DB, filter_aulas)
    
    if not aulas or len(aulas['results']) == 0:
        print(f"📁 Seção {secao_id[:8]}... : sem aulas")
    else:
        print(f"📁 Seção {secao_id[:8]}... : {len(aulas['results'])} aulas encontradas")
        
        # Remover todas as aulas
        for aula in aulas['results']:
            aula_id = aula['id']
            aula_titulo = aula['properties']['Project name']['title'][0]['text']['content']
            
            if delete_page(aula_id):
                print(f"   🗑️  Removida: {aula_titulo[:50]}...")
                total_removidas += 1
            else:
                print(f"   ❌ Erro ao remover: {aula_titulo[:50]}...")
    
    # Atualizar seção para Concluido
    props = {
        "Status": {"status": {"name": "Concluido"}}
    }
    
    if update_page(secao_id, props):
        print(f"   ✅ Seção marcada como Concluido\n")
    else:
        print(f"   ❌ Erro ao atualizar seção\n")

print("="*70)
print(f"✅ Correção concluída!")
print(f"🗑️  Total de aulas removidas: {total_removidas}")
print(f"✅ 2 seções marcadas como Concluido")
print("="*70 + "\n")










