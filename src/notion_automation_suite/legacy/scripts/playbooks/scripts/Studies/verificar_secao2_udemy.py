#!/usr/bin/env python3
"""Verificar e corrigir Seção 2 da Formação Udemy"""

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

def create_page(database_id, properties, parent_id=None, icon=None):
    """Cria uma página no Notion."""
    url = 'https://api.notion.com/v1/pages'
    
    payload = {
        'parent': {'database_id': database_id},
        'properties': properties
    }
    
    if parent_id:
        payload['properties']['Parent item'] = {"relation": [{"id": parent_id}]}
    
    if icon:
        payload['icon'] = icon
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao criar página: {response.status_code} - {response.text}")
        return None

# Aulas da Seção 2
SECAO2_AULAS = [
    {"title": "8. Introdução", "duration": "9m", "completed": True},
    {"title": "9. Aplicações", "duration": "7m", "completed": True},
    {"title": "10. Definições Gerais", "duration": "6m", "completed": True},
    {"title": "11. Conceitos Fundamentais", "duration": "10m", "completed": True},
    {"title": "12. Introdução a Classificação", "duration": "21m", "completed": True},
    {"title": "13. Avaliação de Performance e Matriz de Confusão", "duration": "21m", "completed": True},
    {"title": "14. Avaliação de Performance para Regressão", "duration": "12m", "completed": True},
    {"title": "15. Codificação de Categorias", "duration": "7m", "completed": True},
    {"title": "16. Dimensionamento de Características", "duration": "9m", "completed": True},
    {"title": "17. Fundamentos de Agrupamentos", "duration": "8m", "completed": True},
    {"title": "18. Regras de Associação", "duration": "12m", "completed": True},
    {"title": "Teste 1: Fundamentos de Machine Learning", "duration": None, "completed": True},
    {"title": "Role play 1: Fundamentos de Machine Learning", "duration": None, "completed": True},
]

print("🔍 Buscando Seção 2: Fundamentos de Machine Learning...\n")

# Buscar a seção
filter_secao = {
    "property": "Project name",
    "title": {
        "contains": "Seção 2: Fundamentos de Machine Learning"
    }
}

result = query_database(ESTUDOS_DB, filter_secao)

if not result or len(result['results']) == 0:
    print("❌ Seção 2 não encontrada!")
else:
    secao_id = result['results'][0]['id']
    secao_titulo = result['results'][0]['properties']['Project name']['title'][0]['text']['content']
    print(f"✅ Seção encontrada: {secao_titulo}")
    print(f"   ID: {secao_id}\n")
    
    # Buscar aulas existentes
    filter_aulas = {
        "property": "Parent item",
        "relation": {
            "contains": secao_id
        }
    }
    
    aulas_existentes = query_database(ESTUDOS_DB, filter_aulas)
    aulas_existentes_titulos = []
    
    if aulas_existentes and len(aulas_existentes['results']) > 0:
        print(f"📚 Aulas já existentes: {len(aulas_existentes['results'])}")
        for aula in aulas_existentes['results']:
            titulo = aula['properties']['Project name']['title'][0]['text']['content']
            aulas_existentes_titulos.append(titulo)
            print(f"   - {titulo}")
        print()
    else:
        print("📚 Nenhuma aula encontrada. Criando todas...\n")
    
    # Criar aulas faltantes
    criadas = 0
    puladas = 0
    
    for idx, aula_data in enumerate(SECAO2_AULAS, 1):
        aula_titulo = aula_data["title"]
        
        if aula_titulo in aulas_existentes_titulos:
            print(f"   ⏭️  {idx}/13: {aula_titulo} - JÁ EXISTE")
            puladas += 1
            continue
        
        duracao = aula_data.get("duration", "")
        completed = aula_data["completed"]
        status = "Concluido" if completed else "Para Fazer"
        
        aula_props = {
            "Project name": {"title": [{"text": {"content": aula_titulo}}]},
            "Status": {"status": {"name": status}},
            "Prioridade": {"select": {"name": "Média"}},
            "Categorias": {"multi_select": [{"name": "Aula"}, {"name": "IA/ML"}]},
        }
        
        if duracao:
            aula_props["Tempo Total"] = {"rich_text": [{"text": {"content": duracao}}]}
        
        aula_card = create_page(
            ESTUDOS_DB,
            aula_props,
            parent_id=secao_id,
            icon={"type": "emoji", "emoji": "📝"}
        )
        
        if aula_card:
            print(f"   ✅ {idx}/13: {aula_titulo} - CRIADA ({status})")
            criadas += 1
        else:
            print(f"   ❌ {idx}/13: {aula_titulo} - ERRO")
    
    print(f"\n{'='*60}")
    print(f"✅ Aulas criadas: {criadas}")
    print(f"⏭️  Aulas já existentes: {puladas}")
    print(f"{'='*60}\n")










