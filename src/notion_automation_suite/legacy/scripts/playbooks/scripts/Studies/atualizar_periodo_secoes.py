#!/usr/bin/env python3
"""
Atualizar período das seções da Formação Completa
Período da seção = data inicial da primeira aula até data final da última aula
"""

import requests
from datetime import datetime
import pytz

# Configuração
NOTION_TOKEN = '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'
NOTION_VERSION = '2022-06-28'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

tz = pytz.timezone('America/Sao_Paulo')

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

def update_page(page_id, properties):
    """Atualiza uma página no Notion."""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    payload = {'properties': properties}
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    return response.status_code == 200

print("\n" + "="*70)
print("📅 ATUALIZANDO PERÍODO DAS SEÇÕES - FORMAÇÃO COMPLETA")
print("="*70 + "\n")

# Buscar curso "Formação Completa"
filter_curso = {
    "property": "Project name",
    "title": {"contains": "Formação Completa"}
}

resultado_curso = query_database(ESTUDOS_DB, filter_curso)

if not resultado_curso or len(resultado_curso['results']) == 0:
    print("❌ Curso não encontrado!\n")
    exit(1)

curso_id = resultado_curso['results'][0]['id']
curso_titulo = resultado_curso['results'][0]['properties']['Project name']['title'][0]['text']['content']

print(f"✅ Curso encontrado: {curso_titulo}\n")

# Buscar todas as seções
filter_secoes = {
    "property": "Parent item",
    "relation": {"contains": curso_id}
}

secoes = query_database(ESTUDOS_DB, filter_secoes)

if not secoes or len(secoes['results']) == 0:
    print("❌ Nenhuma seção encontrada!\n")
    exit(1)

print(f"📁 {len(secoes['results'])} seções encontradas\n")

secoes_atualizadas = 0

for secao_page in secoes['results']:
    secao_id = secao_page['id']
    secao_titulo = secao_page['properties']['Project name']['title'][0]['text']['content']
    
    print(f"📂 {secao_titulo}")
    
    # Buscar todas as aulas desta seção
    filter_aulas = {
        "property": "Parent item",
        "relation": {"contains": secao_id}
    }
    
    aulas = query_database(ESTUDOS_DB, filter_aulas)
    
    if not aulas or len(aulas['results']) == 0:
        print(f"   ⚠️  Nenhuma aula encontrada\n")
        continue
    
    # Coletar todas as datas de início e fim das aulas
    datas_inicio = []
    datas_fim = []
    
    for aula in aulas['results']:
        periodo_prop = aula['properties'].get('Período', {})
        periodo_date = periodo_prop.get('date')
        
        if periodo_date:
            start = periodo_date.get('start')
            end = periodo_date.get('end')
            
            if start:
                try:
                    dt_start = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    datas_inicio.append(dt_start)
                except:
                    pass
            
            if end:
                try:
                    dt_end = datetime.fromisoformat(end.replace('Z', '+00:00'))
                    datas_fim.append(dt_end)
                except:
                    pass
    
    if not datas_inicio or not datas_fim:
        print(f"   ⚠️  Sem datas nas aulas\n")
        continue
    
    # Período da seção = primeira data início até última data fim
    periodo_inicio = min(datas_inicio)
    periodo_fim = max(datas_fim)
    
    # Atualizar seção
    props = {
        "Período": {
            "date": {
                "start": periodo_inicio.isoformat(),
                "end": periodo_fim.isoformat()
            }
        }
    }
    
    if update_page(secao_id, props):
        print(f"   ✅ Período atualizado:")
        print(f"      📅 {periodo_inicio.strftime('%d/%m/%Y %H:%M')} → {periodo_fim.strftime('%d/%m/%Y %H:%M')}")
        secoes_atualizadas += 1
    else:
        print(f"   ❌ Erro ao atualizar")
    
    print()

print("="*70)
print(f"✅ {secoes_atualizadas} seções atualizadas com período!")
print("="*70 + "\n")










