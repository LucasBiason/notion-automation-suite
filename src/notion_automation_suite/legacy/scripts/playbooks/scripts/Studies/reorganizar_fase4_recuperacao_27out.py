#!/usr/bin/env python3
"""
Script para reorganizar cronograma da Fase 4 FIAP
Início: 27/10/2025 (recuperação após doença)

Reorganiza:
- Aula 01: Já concluída (13/10)
- Revisão Aula 01: Manter (18/10 ou reagendar)
- Aulas 2-6 OpenAI: 27/10 - 31/10
- Aulas 1-3 AWS: 03/11 - 05/11
- Projetos e Tech Challenge: Novembro
"""

import os
import requests
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('NOTION_API_TOKEN')
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# Timezone GMT-3
gmt3 = pytz.timezone('America/Sao_Paulo')

def format_date_gmt3(date_obj, hour=19, minute=0):
    """Formata data para GMT-3"""
    dt = datetime.combine(date_obj, datetime.min.time())
    dt = dt.replace(hour=hour, minute=minute)
    dt_gmt3 = gmt3.localize(dt)
    return dt_gmt3.isoformat()

def get_aulas_fase4():
    """Busca todas as aulas da Fase 4 que NÃO estão concluídas"""
    url = f'https://api.notion.com/v1/databases/{ESTUDOS_DB}/query'
    
    payload = {
        "filter": {
            "and": [
                {
                    "property": "Project name",
                    "title": {
                        "contains": "Aula"
                    }
                },
                {
                    "property": "Project name",
                    "title": {
                        "contains": "OpenAI"
                    }
                },
                {
                    "property": "Status",
                    "status": {
                        "does_not_equal": "Concluido"
                    }
                }
            ]
        },
        "sorts": [{"property": "Project name", "direction": "ascending"}]
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f'Erro ao buscar aulas: {response.text}')
        return []

def reorganizar_aulas_openai():
    """Reorganiza aulas 2-6 do módulo OpenAI para 27/10 - 31/10"""
    print('🔄 Reorganizando aulas do módulo OpenAI...')
    print('')
    
    aulas = get_aulas_fase4()
    
    if not aulas:
        print('❌ Nenhuma aula encontrada para reorganizar')
        return
    
    # Datas de reorganização (27/10 - 31/10)
    inicio = datetime(2025, 10, 27).date()
    
    # Mapeamento de aulas
    cronograma = [
        {'aula': 'Aula 2', 'dia': inicio, 'hora': 19, 'minuto': 0},  # Seg 27/10
        {'aula': 'Aula 3', 'dia': inicio + timedelta(days=1), 'hora': 19, 'minuto': 30},  # Ter 28/10
        {'aula': 'Aula 4', 'dia': inicio + timedelta(days=2), 'hora': 19, 'minuto': 0},  # Qua 29/10
        {'aula': 'Aula 5', 'dia': inicio + timedelta(days=3), 'hora': 19, 'minuto': 0},  # Qui 30/10
        {'aula': 'Aula 6', 'dia': inicio + timedelta(days=4), 'hora': 19, 'minuto': 0},  # Sex 31/10
    ]
    
    reorganizadas = 0
    
    for aula_card in aulas:
        titulo = aula_card['properties']['Project name']['title'][0]['plain_text']
        
        # Identificar qual aula é
        numero_aula = None
        for item in cronograma:
            if item['aula'].lower() in titulo.lower():
                numero_aula = item
                break
        
        if not numero_aula:
            print(f'⏭️  Pulando: {titulo} (não identificada)')
            continue
        
        # Atualizar data
        nova_data = format_date_gmt3(numero_aula['dia'], numero_aula['hora'], numero_aula['minuto'])
        
        url = f'https://api.notion.com/v1/pages/{aula_card["id"]}'
        payload = {
            "properties": {
                "Período": {
                    "date": {
                        "start": nova_data
                    }
                },
                "Status": {
                    "status": {
                        "name": "Para Fazer"
                    }
                }
            }
        }
        
        response = requests.patch(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            data_formatada = numero_aula['dia'].strftime('%d/%m')
            hora_formatada = f"{numero_aula['hora']:02d}:{numero_aula['minuto']:02d}"
            print(f'✅ {titulo}')
            print(f'   Nova data: {data_formatada} às {hora_formatada}')
            print('')
            reorganizadas += 1
        else:
            print(f'❌ Erro ao atualizar {titulo}: {response.text}')
            print('')
    
    return reorganizadas

def reorganizar_aulas_aws():
    """Reorganiza aulas AWS para início em 03/11"""
    print('🔄 Reorganizando aulas do módulo AWS...')
    print('')
    
    url = f'https://api.notion.com/v1/databases/{ESTUDOS_DB}/query'
    
    payload = {
        "filter": {
            "and": [
                {
                    "property": "Project name",
                    "title": {
                        "contains": "AWS"
                    }
                },
                {
                    "property": "Status",
                    "status": {
                        "does_not_equal": "Concluido"
                    }
                }
            ]
        },
        "sorts": [{"property": "Project name", "direction": "ascending"}]
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        print(f'Erro ao buscar aulas AWS: {response.text}')
        return 0
    
    aulas = response.json().get('results', [])
    
    # Datas AWS (03/11 - 05/11)
    inicio_aws = datetime(2025, 11, 3).date()
    
    cronograma_aws = [
        {'dia': inicio_aws, 'hora': 19, 'minuto': 0},  # Seg 03/11
        {'dia': inicio_aws + timedelta(days=1), 'hora': 19, 'minuto': 30},  # Ter 04/11
        {'dia': inicio_aws + timedelta(days=2), 'hora': 19, 'minuto': 0},  # Qua 05/11
    ]
    
    reorganizadas = 0
    
    for idx, aula_card in enumerate(aulas[:3]):
        titulo = aula_card['properties']['Project name']['title'][0]['plain_text']
        
        if idx >= len(cronograma_aws):
            break
        
        nova_data = format_date_gmt3(
            cronograma_aws[idx]['dia'],
            cronograma_aws[idx]['hora'],
            cronograma_aws[idx]['minuto']
        )
        
        url_update = f'https://api.notion.com/v1/pages/{aula_card["id"]}'
        payload_update = {
            "properties": {
                "Período": {
                    "date": {
                        "start": nova_data
                    }
                },
                "Status": {
                    "status": {
                        "name": "Para Fazer"
                    }
                }
            }
        }
        
        response = requests.patch(url_update, headers=headers, json=payload_update, timeout=60)
        
        if response.status_code == 200:
            data_formatada = cronograma_aws[idx]['dia'].strftime('%d/%m')
            hora_formatada = f"{cronograma_aws[idx]['hora']:02d}:{cronograma_aws[idx]['minuto']:02d}"
            print(f'✅ {titulo}')
            print(f'   Nova data: {data_formatada} às {hora_formatada}')
            print('')
            reorganizadas += 1
        else:
            print(f'❌ Erro ao atualizar {titulo}: {response.text}')
    
    return reorganizadas

def main():
    print('=' * 80)
    print('🚨 REORGANIZAÇÃO DE CRONOGRAMA - FASE 4 FIAP')
    print('   Modo Recuperação - Início 27/10/2025')
    print('=' * 80)
    print('')
    
    print('📋 SITUAÇÃO:')
    print('   ✅ Aula 1: Concluída (13/10)')
    print('   🏥 Pausa por doença (14-26/10)')
    print('   🔄 Reinício: 27/10/2025')
    print('')
    print('─' * 80)
    print('')
    
    # Reorganizar OpenAI
    openai_count = reorganizar_aulas_openai()
    
    print('─' * 80)
    print('')
    
    # Reorganizar AWS
    aws_count = reorganizar_aulas_aws()
    
    print('=' * 80)
    print('✅ REORGANIZAÇÃO CONCLUÍDA!')
    print('=' * 80)
    print('')
    print(f'📊 Resumo:')
    print(f'   • Aulas OpenAI reorganizadas: {openai_count if openai_count else 0}')
    print(f'   • Aulas AWS reorganizadas: {aws_count if aws_count else 0}')
    total = (openai_count if openai_count else 0) + (aws_count if aws_count else 0)
    print(f'   • Total reorganizado: {total}')
    print('')
    print('📅 Novo cronograma:')
    print('   • Aulas OpenAI: 27/10 - 31/10 (Semana 1)')
    print('   • Aulas AWS: 03/11 - 05/11 (Semana 2)')
    print('   • Projetos: 01/11 - 10/11')
    print('   • Tech Challenge: 11/11 - 23/11')
    print('')
    print('🎯 Próxima ação: Segunda 27/10 19:00 - Aula 02!')
    print('')
    print('💪 Melhoras, Lucas! Você vai recuperar o tempo perdido!')

if __name__ == '__main__':
    main()

