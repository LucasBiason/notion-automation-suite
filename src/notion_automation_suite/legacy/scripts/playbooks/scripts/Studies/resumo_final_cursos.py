#!/usr/bin/env python3
"""Resumo final de todos os cursos"""

import requests

NOTION_TOKEN = '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'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'
FORMACOES_CURSOS_ID = '294962a7-693c-814c-867d-c81836cece10'

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
print("📊 RESUMO FINAL DE TODOS OS CURSOS")
print("="*70 + "\n")

# Buscar todos os cursos
filter_cursos = {
    "property": "Parent item",
    "relation": {"contains": FORMACOES_CURSOS_ID}
}

cursos = query_database(ESTUDOS_DB, filter_cursos)

if not cursos:
    print("❌ Erro ao buscar cursos!\n")
    exit(1)

print(f"📚 Total de cursos: {len(cursos['results'])}\n")

total_secoes = 0
total_aulas = 0
cursos_planejados = 0

for curso in cursos['results']:
    titulo = curso['properties']['Project name']['title'][0]['text']['content']
    curso_id = curso['id']
    
    icon_info = curso.get('icon', {})
    icon_emoji = icon_info.get('emoji', '❓') if icon_info else '❓'
    
    # Buscar seções
    filter_secoes = {
        "property": "Parent item",
        "relation": {"contains": curso_id}
    }
    
    secoes = query_database(ESTUDOS_DB, filter_secoes)
    num_secoes = len(secoes['results']) if secoes else 0
    total_secoes += num_secoes
    
    # Contar aulas
    num_aulas = 0
    aulas_com_cronograma = 0
    
    if secoes and num_secoes > 0:
        for secao in secoes['results']:
            secao_id = secao['id']
            
            filter_aulas = {
                "property": "Parent item",
                "relation": {"contains": secao_id}
            }
            
            aulas = query_database(ESTUDOS_DB, filter_aulas)
            if aulas:
                num_aulas += len(aulas['results'])
                
                # Verificar quantas têm período definido
                for aula in aulas['results']:
                    periodo = aula['properties'].get('Período', {}).get('date')
                    if periodo:
                        aulas_com_cronograma += 1
    
    total_aulas += num_aulas
    
    # Status do cronograma
    status_cronograma = "❌ Não planejado"
    if aulas_com_cronograma > 0:
        percentual = (aulas_com_cronograma / num_aulas * 100) if num_aulas > 0 else 0
        if percentual >= 90:
            status_cronograma = f"✅ Planejado ({aulas_com_cronograma}/{num_aulas})"
            cursos_planejados += 1
        else:
            status_cronograma = f"⚠️  Parcial ({aulas_com_cronograma}/{num_aulas})"
    
    print(f"{icon_emoji} {titulo}")
    print(f"   📁 Seções: {num_secoes}")
    print(f"   📝 Aulas: {num_aulas}")
    print(f"   📅 Cronograma: {status_cronograma}")
    print()

print("="*70)
print(f"📊 TOTAIS:")
print(f"   📚 Cursos: {len(cursos['results'])}")
print(f"   📁 Seções: {total_secoes}")
print(f"   📝 Aulas: {total_aulas}")
print(f"   ✅ Cursos planejados: {cursos_planejados}/{len(cursos['results'])}")
print("="*70 + "\n")

print("🎯 CURSOS QUE FALTAM PLANEJAR:\n")

# Cursos esperados
CURSOS_ESPERADOS = [
    "Rocketseat - IA para Devs",
    "Formação Rocketseat - IA para Devs",
]

for curso_esperado in CURSOS_ESPERADOS:
    encontrado = False
    for curso in cursos['results']:
        titulo = curso['properties']['Project name']['title'][0]['text']['content']
        if curso_esperado.lower() in titulo.lower():
            encontrado = True
            break
    
    if encontrado:
        print(f"   ✅ {curso_esperado} - ENCONTRADO")
    else:
        print(f"   ❌ {curso_esperado} - FALTANDO")

print("\n")










