#!/usr/bin/env python3
"""
Script para criar testes CORRIGIDOS em todas as bases Notion
Com todas as correções solicitadas pelo usuário
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

# Credenciais
TOKEN = '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'

# Timezone GMT-3 (São Paulo)
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

def create_work_test_corrected():
    """Cria teste WORK corrigido com vínculos e ícone"""
    
    engine = NotionEngine(TOKEN)
    
    print("🏢 Criando teste WORK corrigido...")
    
    # 1. Criar item principal com ícone
    main_card_data = {
        'title': 'Meu teste de Automação',
        'status': 'Não iniciado',
        'cliente': 'Astracode',  # Sempre Astracode
        'projeto': 'ExpenseIQ',  # Sempre ExpenseIQ para agentes
        'prioridade': 'Média',
        'periodo': {
            'start': '2025-10-10T09:00:00-03:00',
            'end': '2025-10-10T17:00:00-03:00'
        }
    }
    
    main_card_id = engine.create_card('WORK', main_card_data)
    
    if not main_card_id:
        print("❌ Falha ao criar card principal WORK")
        return None
    
    print(f"✅ Card principal WORK criado: {main_card_id}")
    
    # 2. Criar sub-itens com vínculo correto
    sub_items = [
        {
            'title': 'Meu Item de testes de automação 1',
            'status': 'Não iniciado',
            'cliente': 'Astracode',
            'projeto': 'ExpenseIQ',
            'prioridade': 'Alta',
            'periodo': {
                'start': '2025-10-10T09:00:00-03:00',
                'end': '2025-10-10T12:00:00-03:00'
            },
            'item_principal': main_card_id  # Vínculo correto
        },
        {
            'title': 'Meu Item de testes de automação 2',
            'status': 'Não iniciado',
            'cliente': 'Astracode',
            'projeto': 'ExpenseIQ',
            'prioridade': 'Média',
            'periodo': {
                'start': '2025-10-10T13:00:00-03:00',
                'end': '2025-10-10T17:00:00-03:00'
            },
            'item_principal': main_card_id  # Vínculo correto
        }
    ]
    
    sub_item_ids = []
    for i, sub_data in enumerate(sub_items, 1):
        sub_id = engine.create_card('WORK', sub_data)
        if sub_id:
            sub_item_ids.append(sub_id)
            print(f"✅ Sub-item {i} WORK criado: {sub_id}")
        else:
            print(f"❌ Falha ao criar sub-item {i} WORK")
    
    return {
        'main_card': main_card_id,
        'sub_items': sub_item_ids
    }

def create_personal_test_corrected():
    """Cria teste PERSONAL corrigido com subtarefas linkadas"""
    
    engine = NotionEngine(TOKEN)
    
    print("\n👤 Criando teste PERSONAL corrigido...")
    
    # 1. Criar tarefa principal
    main_card_data = {
        'title': 'Meu teste de Automação',
        'status': 'Não iniciado',
        'atividade': 'Teste',
        'periodo': {
            'start': '2025-10-10T09:00:00-03:00',
            'end': '2025-10-10T17:00:00-03:00'
        }
    }
    
    main_card_id = engine.create_card('PERSONAL', main_card_data)
    
    if not main_card_id:
        print("❌ Falha ao criar tarefa principal PERSONAL")
        return None
    
    print(f"✅ Tarefa principal PERSONAL criada: {main_card_id}")
    
    # 2. Criar subtarefas com vínculo correto
    sub_items = [
        {
            'title': 'Meu Item de testes de automação 1',
            'status': 'Não iniciado',
            'atividade': 'Teste',
            'periodo': {
                'start': '2025-10-10T09:00:00-03:00',
                'end': '2025-10-10T12:00:00-03:00'
            },
            'tarefa_principal': main_card_id  # Vínculo correto
        },
        {
            'title': 'Meu Item de testes de automação 2',
            'status': 'Não iniciado',
            'atividade': 'Teste',
            'periodo': {
                'start': '2025-10-10T13:00:00-03:00',
                'end': '2025-10-10T17:00:00-03:00'
            },
            'tarefa_principal': main_card_id  # Vínculo correto
        }
    ]
    
    sub_item_ids = []
    for i, sub_data in enumerate(sub_items, 1):
        sub_id = engine.create_card('PERSONAL', sub_data)
        if sub_id:
            sub_item_ids.append(sub_id)
            print(f"✅ Subtarefa {i} PERSONAL criada: {sub_id}")
        else:
            print(f"❌ Falha ao criar subtarefa {i} PERSONAL")
    
    return {
        'main_card': main_card_id,
        'sub_items': sub_item_ids
    }

def create_youtuber_test_corrected():
    """Cria teste YOUTUBER corrigido com todos os ajustes"""
    
    engine = NotionEngine(TOKEN)
    
    print("\n🎬 Criando teste YOUTUBER corrigido...")
    
    # Sinopse para o primeiro episódio
    synopsis = """
    Bem-vindos à nossa jornada épica através da região de Kalos em Pokemon Legends Z-A! 
    
    Nesta série fictícia, embarcaremos em uma aventura única onde exploraremos as profundezas 
    da história de Kalos, descobrindo segredos antigos e enfrentando desafios nunca antes vistos. 
    
    Cada episódio nos levará mais fundo na mitologia Pokemon, com batalhas épicas, 
    descobertas arqueológicas e momentos emocionantes que farão você se apaixonar 
    novamente pelo mundo dos Pokemon.
    
    Prepare-se para uma experiência imersiva como nunca antes!
    """
    
    # Datas de gravação dos episódios
    base_date = datetime(2025, 10, 16, tzinfo=SAO_PAULO_TZ)
    
    # Primeiro episódio: 7:00-9:00 no dia 16/10
    first_ep_period_start = base_date.replace(hour=7, minute=0, second=0)
    first_ep_period_end = base_date.replace(hour=9, minute=0, second=0)
    
    # Último episódio: 21:00-11:50 (próximo dia) no dia 03/11
    last_date = base_date + timedelta(days=18)  # 20 episódios = dia 03/11
    last_ep_period_start = last_date.replace(hour=21, minute=0, second=0)
    last_ep_period_end = (last_date + timedelta(days=1)).replace(hour=11, minute=50, second=0)
    
    # 1. Criar série principal (sem data de lançamento, período correto)
    series_data = {
        'title': 'Pokemon Legends Z-A',
        'status': 'Não iniciado',
        'periodo': {
            'start': first_ep_period_start.isoformat(),  # Inicia na gravação do primeiro
            'end': last_ep_period_end.isoformat()        # Termina na gravação do último
        }
        # SEM data de lançamento (correto)
    }
    
    series_id = engine.create_card('YOUTUBER', series_data)
    
    if not series_id:
        print("❌ Falha ao criar série principal YOUTUBER")
        return None
    
    print(f"✅ Série principal criada: {series_id}")
    
    # 2. Criar apenas 2 episódios como teste (com todos os campos corretos)
    episodes = []
    
    for i in range(1, 3):  # Apenas 2 episódios para teste
        episode_date = base_date + timedelta(days=i-1)
        
        # Lançamento: 12:00
        launch_time = episode_date.replace(hour=12, minute=0, second=0)
        
        # Período (gravação):
        if i == 1:
            period_start = episode_date.replace(hour=7, minute=0, second=0)
            period_end = episode_date.replace(hour=9, minute=0, second=0)
        else:
            # Segundo episódio: 21:00-11:50 (próximo dia)
            period_start = episode_date.replace(hour=21, minute=0, second=0)
            period_end = (episode_date + timedelta(days=1)).replace(hour=11, minute=50, second=0)
        
        episode_data = {
            'title': f'Episódio {i:02d}',
            'status': 'Não iniciado',
            'periodo': {
                'start': period_start.isoformat(),
                'end': period_end.isoformat()
            },
            'data_lancamento': launch_time.isoformat(),  # Data de lançamento
            'item_principal': series_id,  # Vínculo para a série
            'resumo_episodio': synopsis if i == 1 else f'Episódio {i} da nossa jornada épica através de Kalos. Descubra novos segredos e enfrente desafios únicos neste episódio emocionante!'
        }
        
        episode_id = engine.create_card('YOUTUBER', episode_data)
        
        if episode_id:
            episodes.append({
                'number': i,
                'id': episode_id
            })
            print(f"✅ Episódio {i:02d} criado: {episode_id}")
        else:
            print(f"❌ Falha ao criar episódio {i}")
    
    return {
        'series': series_id,
        'episodes': episodes
    }

def main():
    """Executa todos os testes corrigidos"""
    
    print("🚀 Iniciando testes CORRIGIDOS...")
    print("=" * 60)
    
    # Criar testes corrigidos
    work_result = create_work_test_corrected()
    personal_result = create_personal_test_corrected()
    youtuber_result = create_youtuber_test_corrected()
    
    # Buscar links corretos
    print("\n🔗 Buscando links corretos...")
    
    def get_notion_url(card_id):
        try:
            import requests
            url = f'https://api.notion.com/v1/pages/{card_id}'
            headers = {
                'Authorization': f'Bearer {TOKEN}',
                'Notion-Version': '2022-06-28'
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('url', f'https://www.notion.so/{card_id}')
            return f'https://www.notion.so/{card_id}'
        except:
            return f'https://www.notion.so/{card_id}'
    
    # Resumo final
    print("\n" + "="*80)
    print("📋 RESUMO DOS TESTES CORRIGIDOS")
    print("="*80)
    
    if work_result:
        print(f"\n🏢 WORK:")
        main_url = get_notion_url(work_result['main_card'])
        print(f"   Principal: {main_url}")
        for i, sub_id in enumerate(work_result['sub_items'], 1):
            sub_url = get_notion_url(sub_id)
            print(f"   Sub-item {i}: {sub_url}")
    
    if personal_result:
        print(f"\n👤 PERSONAL:")
        main_url = get_notion_url(personal_result['main_card'])
        print(f"   Principal: {main_url}")
        for i, sub_id in enumerate(personal_result['sub_items'], 1):
            sub_url = get_notion_url(sub_id)
            print(f"   Subtarefa {i}: {sub_url}")
    
    if youtuber_result:
        print(f"\n🎬 YOUTUBER:")
        series_url = get_notion_url(youtuber_result['series'])
        print(f"   Série: {series_url}")
        for ep in youtuber_result['episodes']:
            ep_url = get_notion_url(ep['id'])
            print(f"   Ep. {ep['number']:02d}: {ep_url}")
    
    print("\n✅ TODOS OS TESTES CORRIGIDOS!")
    print("🎯 Agora você pode validar os cards no Notion")

if __name__ == "__main__":
    main()


