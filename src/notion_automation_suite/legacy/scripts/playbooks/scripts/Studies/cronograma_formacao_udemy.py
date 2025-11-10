#!/usr/bin/env python3
"""
Cronograma específico para Formação Udemy (aulas Para Fazer)
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

print("\n" + "="*70)
print("📚 CRONOGRAMA - Formação Completa IA/ML (Para Fazer)")
print("="*70)

# Buscar curso
filter_curso = {
    "property": "Project name",
    "title": {"contains": "Formação Completa"}
}

resultado_curso = query_database(ESTUDOS_DB, filter_curso)

if not resultado_curso or len(resultado_curso['results']) == 0:
    print("\n❌ Curso não encontrado!\n")
    exit(1)

curso_id = resultado_curso['results'][0]['id']
print(f"\n✅ Curso encontrado! ID: {curso_id}\n")

# Buscar TODAS as seções do curso
filter_secoes = {
    "property": "Parent item",
    "relation": {"contains": curso_id}
}

secoes = query_database(ESTUDOS_DB, filter_secoes)

if not secoes or len(secoes['results']) == 0:
    print("❌ Nenhuma seção encontrada!\n")
    exit(1)

print(f"📁 {len(secoes['results'])} seções encontradas\n")

# Para cada seção, buscar aulas "Para Fazer"
todas_aulas = []

for secao_page in secoes['results']:
    secao_id = secao_page['id']
    secao_titulo = secao_page['properties']['Project name']['title'][0]['text']['content']
    
    # Buscar aulas desta seção com status "Para Fazer"
    filter_aulas = {
        "and": [
            {
                "property": "Parent item",
                "relation": {"contains": secao_id}
            },
            {
                "property": "Status",
                "status": {"equals": "Para Fazer"}
            }
        ]
    }
    
    aulas_secao = query_database(ESTUDOS_DB, filter_aulas)
    
    if aulas_secao and len(aulas_secao['results']) > 0:
        print(f"   📚 {secao_titulo}: {len(aulas_secao['results'])} aulas Para Fazer")
        
        for aula_page in aulas_secao['results']:
            aula_id = aula_page['id']
            aula_titulo = aula_page['properties']['Project name']['title'][0]['text']['content']
            
            # Extrair duração
            tempo_prop = aula_page['properties'].get('Tempo Total', {})
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
            
            todas_aulas.append({
                'id': aula_id,
                'titulo': aula_titulo,
                'duracao_min': duracao_min,
                'secao': secao_titulo
            })

print(f"\n✅ Total de aulas Para Fazer: {len(todas_aulas)}\n")

if len(todas_aulas) == 0:
    print("⚠️  Nenhuma aula Para Fazer encontrada!\n")
    exit(0)

# Planejar a partir de 12/11/2025 (após IA Master)
data_atual = datetime(2025, 11, 12, 13, 20)  # Continua de onde parou
contador = 0

print("📅 Iniciando planejamento...\n")

for aula in todas_aulas:
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
        if contador <= 5 or contador % 15 == 0:
            print(f"   ✅ {aula['titulo'][:50]}... ({data_atual.strftime('%d/%m %H:%M')})")
    
    # Próxima aula (+ 10 min intervalo)
    data_atual = data_fim + timedelta(minutes=10)

print(f"\n{'='*70}")
print(f"✅ {contador} aulas da Formação Udemy planejadas!")
print(f"📅 Conclusão estimada: {data_atual.strftime('%d/%m/%Y')}")
print(f"{'='*70}\n")










