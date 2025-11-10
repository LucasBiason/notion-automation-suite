#!/usr/bin/env python3
"""Verificar cursos que faltaram no cronograma"""

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
print("🔍 VERIFICANDO CURSOS CRIADOS")
print("="*70 + "\n")

# Buscar todos os cursos (sub-itens de "Formações e Cursos")
filter_cursos = {
    "property": "Parent item",
    "relation": {"contains": FORMACOES_CURSOS_ID}
}

cursos = query_database(ESTUDOS_DB, filter_cursos)

if not cursos or len(cursos['results']) == 0:
    print("❌ Nenhum curso encontrado!\n")
else:
    print(f"📚 {len(cursos['results'])} cursos encontrados:\n")
    
    for curso in cursos['results']:
        titulo = curso['properties']['Project name']['title'][0]['text']['content']
        curso_id = curso['id']
        
        # Ver se tem ícone
        icon_info = curso.get('icon', {})
        icon_emoji = icon_info.get('emoji', '❓') if icon_info else '❓'
        
        # Buscar seções
        filter_secoes = {
            "property": "Parent item",
            "relation": {"contains": curso_id}
        }
        
        secoes = query_database(ESTUDOS_DB, filter_secoes)
        num_secoes = len(secoes['results']) if secoes else 0
        
        # Para cada seção, contar aulas
        total_aulas = 0
        if secoes and num_secoes > 0:
            for secao in secoes['results']:
                secao_id = secao['id']
                
                filter_aulas = {
                    "property": "Parent item",
                    "relation": {"contains": secao_id}
                }
                
                aulas = query_database(ESTUDOS_DB, filter_aulas)
                if aulas:
                    total_aulas += len(aulas['results'])
        
        print(f"   {icon_emoji} {titulo}")
        print(f"      📁 Seções: {num_secoes}")
        print(f"      📝 Aulas: {total_aulas}")
        print()

print("="*70)
print("\n📊 Cursos que DEVEM estar no cronograma:")
print("   1. ✅ FIAP Fase 4")
print("   2. ✅ IA Master")
print("   3. ✅ Formação Completa IA/ML")
print("   4. ❓ Rocketseat: IA na Prática")
print("   5. ❓ Rocketseat: IA para Devs")
print("   6. ❓ Formação Rocketseat IA para Devs (outro?)")
print("   7. ✅ Integration Master")
print("\n")










