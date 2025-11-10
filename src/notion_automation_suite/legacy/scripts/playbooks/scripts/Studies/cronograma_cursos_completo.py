#!/usr/bin/env python3
"""
Cronograma Completo de Todos os Cursos
Ordem de prioridade após Tech Challenge:
1. IA Master
2. Formação Completa IA/ML (só "Para Fazer")
3. Rocketseat: IA na Prática
4. Rocketseat IA para Devs
5. Integration Master
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
        print(f"❌ Erro: {response.status_code} - {response.text}")
        return None

def update_page(page_id, properties):
    """Atualiza uma página no Notion."""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    payload = {'properties': properties}
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro: {response.status_code} - {response.text}")
        return None

def buscar_aulas_curso(curso_nome, status_filter=None):
    """Busca aulas de um curso específico."""
    # Buscar card do curso
    filter_curso = {
        "property": "Project name",
        "title": {"contains": curso_nome}
    }
    
    resultado_curso = query_database(ESTUDOS_DB, filter_curso)
    
    if not resultado_curso or len(resultado_curso['results']) == 0:
        print(f"   ❌ Curso '{curso_nome}' não encontrado!")
        return None, []
    
    # Pegar o card principal (primeiro resultado)
    curso_id = resultado_curso['results'][0]['id']
    curso_titulo = resultado_curso['results'][0]['properties']['Project name']['title'][0]['text']['content']
    
    # Buscar todas as aulas (diretas e indiretas - via seções)
    filter_aulas = {
        "and": [
            {
                "property": "Categorias",
                "multi_select": {"contains": "Aula"}
            }
        ]
    }
    
    if status_filter:
        filter_aulas["and"].append({
            "property": "Status",
            "status": {"equals": status_filter}
        })
    
    todas_aulas = query_database(ESTUDOS_DB, filter_aulas)
    
    if not todas_aulas:
        return curso_id, []
    
    # Filtrar aulas que pertencem a este curso (via parent ou via seção)
    aulas_curso = []
    
    for page in todas_aulas['results']:
        titulo = page['properties']['Project name']['title'][0]['text']['content']
        
        # Verificar se pertence ao curso verificando nome
        if curso_nome.lower() in titulo.lower() or \
           any(curso_nome.lower() in tag['name'].lower() 
               for tag in page['properties'].get('Categorias', {}).get('multi_select', [])):
            
            page_id = page['id']
            
            # Extrair duração
            tempo_prop = page['properties'].get('Tempo Total', {})
            tempo_text = tempo_prop.get('rich_text', [])
            duracao_str = tempo_text[0]['text']['content'] if tempo_text else "15m"
            
            # Converter duração para minutos
            duracao_min = 15  # padrão
            if 'h' in duracao_str:
                horas = int(duracao_str.split('h')[0].strip())
                duracao_min = horas * 60
            elif 'min' in duracao_str or 'm' in duracao_str:
                duracao_min = int(duracao_str.replace('min', '').replace('m', '').strip())
            
            aulas_curso.append({
                'id': page_id,
                'titulo': titulo,
                'duracao_min': duracao_min
            })
    
    return curso_id, aulas_curso

def planejar_curso(curso_nome, data_inicio, status_filter=None):
    """Planeja cronograma de um curso."""
    print(f"\n{'='*70}")
    print(f"📚 Planejando: {curso_nome}")
    print(f"{'='*70}\n")
    
    curso_id, aulas = buscar_aulas_curso(curso_nome, status_filter)
    
    if not aulas:
        print(f"   ⚠️  Nenhuma aula encontrada para '{curso_nome}'\n")
        return data_inicio
    
    print(f"✅ {len(aulas)} aulas encontradas\n")
    
    data_atual = data_inicio
    aulas_atualizadas = 0
    
    for aula in aulas:
        # Pular fins de semana
        if data_atual.weekday() >= 5:
            dias_ate_segunda = 7 - data_atual.weekday()
            data_atual = data_atual + timedelta(days=dias_ate_segunda)
            data_atual = data_atual.replace(hour=8, minute=0)
        
        # Calcular fim da aula
        data_fim = data_atual + timedelta(minutes=aula['duracao_min'])
        
        # Se ultrapassar 20:00, mover para o próximo dia
        if data_fim.hour >= 20 or (data_fim.hour == 20 and data_fim.minute > 0):
            data_atual = data_atual + timedelta(days=1)
            data_atual = data_atual.replace(hour=8, minute=0)
            data_fim = data_atual + timedelta(minutes=aula['duracao_min'])
        
        # Atualizar aula
        props = {
            "Período": {
                "date": {
                    "start": format_date_gmt3(data_atual),
                    "end": format_date_gmt3(data_fim)
                }
            }
        }
        
        resultado = update_page(aula['id'], props)
        if resultado:
            print(f"   ✅ {aula['titulo'][:60]}...")
            print(f"      📅 {data_atual.strftime('%d/%m %H:%M')} - {data_fim.strftime('%H:%M')}")
            aulas_atualizadas += 1
        
        # Avançar (aula + 10 min de intervalo)
        data_atual = data_fim + timedelta(minutes=10)
    
    print(f"\n✅ {aulas_atualizadas} aulas de '{curso_nome}' planejadas!")
    
    return data_atual

# ============================================================
# CRONOGRAMA COMPLETO
# ============================================================
print("\n" + "="*70)
print("🚀 CRONOGRAMA COMPLETO DE CURSOS - ROADMAP 2025")
print("="*70)

# Data inicial: 10/11 (segunda após Tech Challenge)
data_inicio = datetime(2025, 11, 10, 8, 0)

print(f"\n📅 Início dos cursos: {data_inicio.strftime('%d/%m/%Y às %H:%M')}\n")

# 1. IA Master
data_inicio = planejar_curso("IA Master", data_inicio)

# 2. Formação Completa IA/ML (só "Para Fazer")
data_inicio = planejar_curso("Formação Completa", data_inicio, status_filter="Para Fazer")

# 3. Rocketseat: IA na Prática
data_inicio = planejar_curso("IA na Prática", data_inicio)

# 4. Rocketseat IA para Devs
data_inicio = planejar_curso("IA para Devs", data_inicio)

# 5. Integration Master
data_inicio = planejar_curso("Integration Master", data_inicio)

print("\n" + "="*70)
print("✅ CRONOGRAMA COMPLETO FINALIZADO!")
print("="*70)
print(f"\n📅 Data estimada de conclusão: {data_inicio.strftime('%d/%m/%Y')}")
print("\n📊 Resumo do Cronograma:")
print("   • FIAP Fase 4: 27/10-31/10")
print("   • Tech Challenge: 03/11-07/11")
print("   • IA Master: 10/11 em diante")
print("   • Formação IA/ML (Para Fazer): após IA Master")
print("   • Rocketseat: IA na Prática: após Formação")
print("   • Rocketseat: IA para Devs: após IA na Prática")
print("   • Integration Master: após IA para Devs")
print("\n")










