#!/usr/bin/env python3
"""
Cronograma Completo V2 - busca via Parent Item
"""

import requests
from datetime import datetime, timedelta
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

def format_date_gmt3(dt):
    """Formata data para GMT-3."""
    if dt.tzinfo is None:
        dt = tz.localize(dt)
    return dt.isoformat()

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

def buscar_sub_itens(parent_id, status_filter=None):
    """Busca todos os sub-itens de um card."""
    filter_params = {
        "property": "Parent item",
        "relation": {"contains": parent_id}
    }
    
    if status_filter:
        filter_params = {
            "and": [
                filter_params,
                {"property": "Status", "status": {"equals": status_filter}}
            ]
        }
    
    resultado = query_database(ESTUDOS_DB, filter_params)
    
    if not resultado:
        return []
    
    itens = []
    for page in resultado['results']:
        titulo = page['properties']['Project name']['title'][0]['text']['content']
        page_id = page['id']
        
        # Extrair duração
        tempo_prop = page['properties'].get('Tempo Total', {})
        tempo_text = tempo_prop.get('rich_text', [])
        duracao_str = tempo_text[0]['text']['content'] if tempo_text else "15m"
        
        # Converter duração
        duracao_min = 15
        if 'h' in duracao_str:
            try:
                horas = int(duracao_str.split('h')[0].strip())
                duracao_min = horas * 60
            except:
                duracao_min = 60
        elif 'min' in duracao_str or 'm' in duracao_str:
            try:
                duracao_min = int(duracao_str.replace('min', '').replace('m', '').strip())
            except:
                duracao_min = 15
        
        itens.append({
            'id': page_id,
            'titulo': titulo,
            'duracao_min': duracao_min
        })
    
    return itens

def buscar_todas_aulas_curso(curso_id, status_filter=None):
    """Busca todas as aulas de um curso (via seções)."""
    # Buscar seções do curso
    secoes = buscar_sub_itens(curso_id)
    
    print(f"   📁 {len(secoes)} seções encontradas")
    
    todas_aulas = []
    
    # Para cada seção, buscar as aulas
    for secao in secoes:
        aulas = buscar_sub_itens(secao['id'], status_filter)
        todas_aulas.extend(aulas)
    
    return todas_aulas

def planejar_curso(curso_nome, curso_id, data_inicio, status_filter=None):
    """Planeja cronograma de um curso."""
    print(f"\n{'='*70}")
    print(f"📚 {curso_nome}")
    print(f"{'='*70}\n")
    
    aulas = buscar_todas_aulas_curso(curso_id, status_filter)
    
    if not aulas:
        print(f"   ⚠️  Nenhuma aula encontrada\n")
        return data_inicio
    
    print(f"   ✅ {len(aulas)} aulas para planejar\n")
    
    data_atual = data_inicio
    contador = 0
    
    for aula in aulas:
        # Pular fins de semana
        while data_atual.weekday() >= 5:
            data_atual = data_atual + timedelta(days=1)
            data_atual = data_atual.replace(hour=8, minute=0)
        
        # Calcular fim
        data_fim = data_atual + timedelta(minutes=aula['duracao_min'])
        
        # Se passar de 20:00, próximo dia
        if data_fim.hour >= 20:
            data_atual = data_atual + timedelta(days=1)
            data_atual = data_atual.replace(hour=8, minute=0)
            data_fim = data_atual + timedelta(minutes=aula['duracao_min'])
        
        # Atualizar
        props = {
            "Período": {
                "date": {
                    "start": format_date_gmt3(data_atual),
                    "end": format_date_gmt3(data_fim)
                }
            }
        }
        
        if update_page(aula['id'], props):
            contador += 1
            if contador <= 5 or contador % 20 == 0:  # Mostrar primeiras 5 e depois a cada 20
                print(f"   ✅ {aula['titulo'][:55]}... ({data_atual.strftime('%d/%m %H:%M')})")
        
        # Próxima aula (+ 10 min intervalo)
        data_atual = data_fim + timedelta(minutes=10)
    
    print(f"\n   📊 {contador} aulas planejadas!")
    return data_atual

# IDs dos cursos
CURSOS = [
    ("IA Master", "20a962a7-693c-8084-aff0-dbdd46e06b53", None),
    ("Formação Completa IA/ML", "1ea962a7-693c-8099-8ad2-c577ffb8ab20", "Para Fazer"),
    ("Rocketseat: IA na Prática", "280962a7-693c-8126-813d-ec89120b0943", None),
    ("Rocketseat: IA para Devs", "256962a7-693c-81a6-8ef2-ffac5d783b30", None),
    ("Integration Master", "296962a7-693c-814f-a1b6-d9934f58f092", None),
]

print("\n" + "="*70)
print("🚀 CRONOGRAMA COMPLETO - ROADMAP 2025")
print("="*70)

data_atual = datetime(2025, 11, 10, 8, 0)
print(f"\n📅 Início: {data_atual.strftime('%d/%m/%Y às %H:%M')}")

for curso_nome, curso_id, status_filter in CURSOS:
    data_atual = planejar_curso(curso_nome, curso_id, data_atual, status_filter)

print("\n" + "="*70)
print("✅ CRONOGRAMA FINALIZADO!")
print("="*70)
print(f"\n📅 Conclusão estimada: {data_atual.strftime('%d/%m/%Y')}\n")










