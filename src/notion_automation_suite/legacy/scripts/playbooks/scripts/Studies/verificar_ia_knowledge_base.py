#!/usr/bin/env python3
"""Verificar se ia-ml-knowledge-base está no cronograma"""

import requests

NOTION_TOKEN = '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'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'
PORTFOLIO_CARD_ID = '294962a7-693c-81be-afc2-e098c9ac8b92'  # Projetos de Portfolio

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
        return None

print("\n" + "="*70)
print("🔍 VERIFICANDO IA-ML-KNOWLEDGE-BASE NO CRONOGRAMA")
print("="*70 + "\n")

# Buscar por ia-ml-knowledge-base
filter_ia_kb = {
    "property": "Project name",
    "title": {"contains": "ia-ml-knowledge-base"}
}

resultado = query_database(ESTUDOS_DB, filter_ia_kb)

if not resultado or len(resultado['results']) == 0:
    print("❌ ia-ml-knowledge-base NÃO encontrado no cronograma!")
    print("\n🔍 Buscando variações...")
    
    # Buscar variações
    variacoes = ["knowledge", "IA Knowledge", "ML Knowledge", "snippets", "receitas"]
    
    for variacao in variacoes:
        filter_var = {
            "property": "Project name",
            "title": {"contains": variacao}
        }
        resultado_var = query_database(ESTUDOS_DB, filter_var)
        
        if resultado_var and len(resultado_var['results']) > 0:
            print(f"✅ Encontrado com '{variacao}':")
            for item in resultado_var['results']:
                titulo = item['properties']['Project name']['title'][0]['text']['content']
                print(f"   📚 {titulo}")
        else:
            print(f"   ❌ Nada com '{variacao}'")
    
    print("\n📋 Projetos de Portfolio encontrados:")
    
    # Buscar todos os projetos de portfolio
    filter_portfolio = {
        "property": "Parent item",
        "relation": {"contains": PORTFOLIO_CARD_ID}
    }
    
    portfolio = query_database(ESTUDOS_DB, filter_portfolio)
    
    if portfolio and len(portfolio['results']) > 0:
        for projeto in portfolio['results']:
            titulo = projeto['properties']['Project name']['title'][0]['text']['content']
            print(f"   📁 {titulo}")
    else:
        print("   ❌ Nenhum projeto de portfolio encontrado")
    
    print(f"\n{'='*70}")
    print("💡 AÇÃO NECESSÁRIA:")
    print("   Criar card para ia-ml-knowledge-base no cronograma!")
    print(f"{'='*70}\n")
    
else:
    print("✅ ia-ml-knowledge-base ENCONTRADO no cronograma!")
    
    for item in resultado['results']:
        titulo = item['properties']['Project name']['title'][0]['text']['content']
        item_id = item['id']
        status = item['properties'].get('Status', {}).get('status', {}).get('name', 'N/A')
        periodo = item['properties'].get('Período', {}).get('date', {})
        
        print(f"   📚 {titulo}")
        print(f"   🆔 ID: {item_id}")
        print(f"   📊 Status: {status}")
        
        if periodo:
            start = periodo.get('start', 'N/A')
            end = periodo.get('end', 'N/A')
            print(f"   📅 Período: {start} → {end}")
        else:
            print(f"   📅 Período: Não definido")
        
        print()









