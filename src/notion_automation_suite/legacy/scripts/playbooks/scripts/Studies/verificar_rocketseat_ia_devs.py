#!/usr/bin/env python3
"""Verificar curso Formação Rocketseat IA para Devs"""

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
        return None

print("\n" + "="*70)
print("🔍 VERIFICANDO FORMAÇÃO ROCKETSEAT IA PARA DEVS")
print("="*70 + "\n")

# Buscar pelo ID direto
curso_id = "256962a7-693c-81a6-8ef2-ffac5d783b30"

# Buscar info do curso
url = f'https://api.notion.com/v1/pages/{curso_id}'
response = requests.get(url, headers=headers, timeout=60)

if response.status_code == 200:
    curso = response.json()
    titulo = curso['properties']['Project name']['title'][0]['text']['content']
    icon_info = curso.get('icon', {})
    icon_emoji = icon_info.get('emoji', '❓') if icon_info else '❓'
    
    print(f"✅ Curso encontrado!")
    print(f"   {icon_emoji} {titulo}")
    print(f"   ID: {curso_id}\n")
    
    # Buscar seções
    filter_secoes = {
        "property": "Parent item",
        "relation": {"contains": curso_id}
    }
    
    secoes = query_database(ESTUDOS_DB, filter_secoes)
    
    if not secoes or len(secoes['results']) == 0:
        print("❌ Nenhuma seção encontrada!\n")
    else:
        print(f"📁 {len(secoes['results'])} seções encontradas:\n")
        
        total_aulas = 0
        total_com_cronograma = 0
        
        for secao in secoes['results']:
            secao_titulo = secao['properties']['Project name']['title'][0]['text']['content']
            secao_id = secao['id']
            
            # Buscar aulas
            filter_aulas = {
                "property": "Parent item",
                "relation": {"contains": secao_id}
            }
            
            aulas = query_database(ESTUDOS_DB, filter_aulas)
            num_aulas = len(aulas['results']) if aulas else 0
            total_aulas += num_aulas
            
            # Verificar cronograma
            aulas_com_periodo = 0
            if aulas:
                for aula in aulas['results']:
                    periodo = aula['properties'].get('Período', {}).get('date')
                    if periodo:
                        aulas_com_periodo += 1
            
            total_com_cronograma += aulas_com_periodo
            
            status_cronograma = "❌" if aulas_com_periodo == 0 else "✅" if aulas_com_periodo == num_aulas else "⚠️"
            
            print(f"   {status_cronograma} {secao_titulo}")
            print(f"      📝 Aulas: {num_aulas}")
            print(f"      📅 Com cronograma: {aulas_com_periodo}/{num_aulas}")
        
        print(f"\n{'='*70}")
        print(f"📊 RESUMO:")
        print(f"   📁 Total de seções: {len(secoes['results'])}")
        print(f"   📝 Total de aulas: {total_aulas}")
        print(f"   📅 Aulas com cronograma: {total_com_cronograma}/{total_aulas}")
        
        percentual = (total_com_cronograma / total_aulas * 100) if total_aulas > 0 else 0
        
        if percentual == 100:
            print(f"   ✅ Status: COMPLETAMENTE PLANEJADO")
        elif percentual > 0:
            print(f"   ⚠️  Status: PARCIALMENTE PLANEJADO ({percentual:.0f}%)")
        else:
            print(f"   ❌ Status: NÃO PLANEJADO")
        
        print(f"{'='*70}\n")
else:
    print(f"❌ Erro ao buscar curso: {response.status_code}\n")










