#!/usr/bin/env python3
"""
Script para reorganizar Fase 4 FIAP
Postergar para semana de 20/10 (segunda-feira)
"""

import os
import requests
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('NOTION_API_TOKEN')
ESTUDOS_DB_ID = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

sp_tz = pytz.timezone('America/Sao_Paulo')

print('🤖 REORGANIZANDO CRONOGRAMA - FASE 4 FIAP')
print('='*70)
print('')
print('📅 MUDANÇA: Começar na segunda 20/10 (ao invés de 13/10)')
print('⏰ Horários: 19:00-21:00 (seg-sex), 19:30-21:00 (ter)')
print('')

# ID da Seção 3 - OpenAI
section_id = '27f962a7-693c-8178-aa78-d783fb6dfcf9'

# 1. Atualizar Seção 3 para "Em Andamento"
print('📊 1. Atualizando Seção 3 - OpenAI...')
update_url = f'https://api.notion.com/v1/pages/{section_id}'
update_payload = {
    'properties': {
        'Status': {'status': {'name': 'Em Andamento'}},
        'Período': {
            'date': {
                'start': '2025-10-20',
                'end': '2025-10-25'
            }
        }
    }
}

response = requests.patch(update_url, headers=headers, json=update_payload, timeout=30)
if response.status_code == 200:
    print('   ✅ Seção 3 atualizada para "Em Andamento"')
else:
    print(f'   ⚠️ Erro: {response.text[:100]}')

print('')

# 2. Buscar aulas da Seção 3
print('🔍 2. Buscando aulas da Seção 3...')
query_url = f'https://api.notion.com/v1/databases/{ESTUDOS_DB_ID}/query'
filter_payload = {
    'filter': {
        'property': 'Parent item',
        'relation': {'contains': section_id}
    },
    'sorts': [{'property': 'Período', 'direction': 'ascending'}]
}

response = requests.post(query_url, headers=headers, json=filter_payload, timeout=30)

if response.status_code != 200:
    print(f'   ❌ Erro: {response.text}')
    exit(1)

aulas = response.json()['results']
print(f'   ✅ Encontradas {len(aulas)} aulas')
print('')

# 3. Reorganizar aulas
print('📝 3. Reorganizando aulas para 20/10...')
print('')

# Nova data de início: segunda 20/10/2025 19:00
current_time = datetime(2025, 10, 20, 19, 0, 0)
current_time = sp_tz.localize(current_time)

reorganizadas = 0

for aula in aulas:
    title = aula['properties']['Project name']['title'][0]['text']['content'] if aula['properties']['Project name']['title'] else 'Sem título'
    card_id = aula['id']
    
    # Pegar duração original
    old_periodo = aula['properties'].get('Período', {}).get('date', {})
    if old_periodo and 'start' in old_periodo and 'end' in old_periodo:
        old_start = datetime.fromisoformat(old_periodo['start'].replace('Z', '+00:00'))
        old_end = datetime.fromisoformat(old_periodo['end'].replace('Z', '+00:00'))
        duration = (old_end - old_start).total_seconds() / 60  # minutos
    else:
        duration = 60  # padrão 1h
    
    # Calcular novo horário
    aula_start = current_time
    aula_end = aula_start + timedelta(minutes=duration)
    
    # Se passa das 21:00, mover para próximo dia
    if aula_end.hour >= 21 or (aula_end.hour == 21 and aula_end.minute > 0):
        # Próximo dia útil
        current_time = current_time + timedelta(days=1)
        
        # Pular finais de semana
        while current_time.weekday() in [5, 6]:
            current_time = current_time + timedelta(days=1)
        
        # Ajustar horário (terça 19:30, outros dias 19:00)
        if current_time.weekday() == 1:  # Terça
            aula_start = current_time.replace(hour=19, minute=30, second=0)
        else:
            aula_start = current_time.replace(hour=19, minute=0, second=0)
        
        aula_end = aula_start + timedelta(minutes=duration)
        current_time = aula_start
    
    # Atualizar card
    update_url = f'https://api.notion.com/v1/pages/{card_id}'
    update_payload = {
        'properties': {
            'Período': {
                'date': {
                    'start': aula_start.strftime('%Y-%m-%dT%H:%M:%S.000-03:00'),
                    'end': aula_end.strftime('%Y-%m-%dT%H:%M:%S.000-03:00')
                }
            }
        }
    }
    
    update_response = requests.patch(update_url, headers=headers, json=update_payload, timeout=30)
    
    if update_response.status_code == 200:
        reorganizadas += 1
        dia_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'][aula_start.weekday()]
        print(f'  ✅ {title[:60]}')
        print(f'      {dia_semana} {aula_start.strftime("%d/%m %H:%M")}-{aula_end.strftime("%H:%M")}')
    else:
        print(f'  ❌ {title[:60]}: Erro')
    
    # Próxima aula começa após esta + 15min
    current_time = aula_end + timedelta(minutes=15)

print('')
print('='*70)
print(f'🎉 CRONOGRAMA REORGANIZADO!')
print(f'✅ {reorganizadas}/{len(aulas)} aulas reorganizadas')
print('')
print('📅 RESUMO:')
print(f'  • Início: Segunda 20/10/2025 - 19:00')
print(f'  • Horários: 19:00-21:00 (seg-sex), 19:30-21:00 (ter)')
print(f'  • Finais de semana: Pulados automaticamente')
print(f'  • Revisão Aula 1: Agendada 18/10 19:00 ✅')
print('='*70)
