#!/usr/bin/env python3
"""
Atualizar ícones das seções do IA Master com base nos nomes reais
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

def update_page_icon(page_id, emoji):
    """Atualiza apenas o ícone de uma página."""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    payload = {
        'icon': {'type': 'emoji', 'emoji': emoji}
    }
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    return response.status_code == 200

print("\n" + "="*70)
print("🎨 ATUALIZANDO ÍCONES - IA MASTER")
print("="*70 + "\n")

# Mapeamento de palavras-chave para ícones
ICONES_MAPPING = {
    "Introdução": "👋",
    "OpenAI": "🤖",
    "GPT": "🤖",
    "LangChain": "⛓️",
    "Agentes": "🔧",
    "Ferramentas": "🔨",
    "RAG": "📚",
    "Retrieval": "📚",
    "WhatsApp": "📱",
    "ChatBot": "💬",
    "Streamlit": "📊",
    "Dicas": "💡",
    "Truques": "✨",
}

# Buscar IA Master
filter_ia_master = {
    "property": "Project name",
    "title": {"contains": "IA Master"}
}

resultado = query_database(ESTUDOS_DB, filter_ia_master)

if not resultado or len(resultado['results']) == 0:
    print("❌ IA Master não encontrado!\n")
    exit(1)

ia_master_id = resultado['results'][0]['id']
print(f"✅ IA Master encontrado!\n")

# Buscar seções
filter_secoes = {
    "property": "Parent item",
    "relation": {"contains": ia_master_id}
}

secoes = query_database(ESTUDOS_DB, filter_secoes)

if not secoes or len(secoes['results']) == 0:
    print("❌ Nenhuma seção encontrada!\n")
    exit(1)

print(f"📁 {len(secoes['results'])} seções encontradas\n")

secoes_atualizadas = 0

for secao in secoes['results']:
    secao_titulo = secao['properties']['Project name']['title'][0]['text']['content']
    secao_id = secao['id']
    
    # Determinar ícone baseado em palavras-chave
    icone = "📁"  # padrão
    
    for palavra_chave, emoji in ICONES_MAPPING.items():
        if palavra_chave.lower() in secao_titulo.lower():
            icone = emoji
            break
    
    if update_page_icon(secao_id, icone):
        print(f"✅ {icone} {secao_titulo}")
        secoes_atualizadas += 1
    else:
        print(f"❌ Erro: {secao_titulo}")

print(f"\n{'='*70}")
print(f"✅ {secoes_atualizadas} seções do IA Master atualizadas!")
print(f"{'='*70}\n")










