#!/usr/bin/env python3
"""
Script para recriar cards de teste WORK e PERSONAL com sub-itens linkados
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

def create_work_test():
    """Cria teste na base WORK com sub-itens linkados"""
    
    engine = NotionEngine(TOKEN)
    
    print("🏢 Criando teste WORK...")
    
    # 1. Criar item principal
    main_card_data = {
        'title': 'Meu teste de Automação',
        'status': 'Não iniciado',
        'categoria': 'Desenvolvimento',
        'prioridade': 'Média',
        'descrição': 'Card principal para teste de automação na base WORK',
        'periodo': {
            'start': '2025-10-10T09:00:00-03:00',
            'end': '2025-10-10T17:00:00-03:00'
        },
        'tempo_total': 8
    }
    
    main_card_id = engine.create_card('WORK', main_card_data)
    
    if not main_card_id:
        print("❌ Falha ao criar card principal WORK")
        return None
    
    print(f"✅ Card principal WORK criado: {main_card_id}")
    print(f"🔗 Link: https://notion.so/{main_card_id}")
    
    # 2. Criar sub-itens linkados
    sub_items = [
        {
            'title': 'Meu Item de testes de automação 1',
            'status': 'Não iniciado',
            'categoria': 'Teste',
            'prioridade': 'Alta',
            'descrição': 'Primeiro sub-item de teste',
            'periodo': {
                'start': '2025-10-10T09:00:00-03:00',
                'end': '2025-10-10T12:00:00-03:00'
            },
            'tempo_total': 3,
            'sprint': main_card_id  # Link para o item principal
        },
        {
            'title': 'Meu Item de testes de automação 2',
            'status': 'Não iniciado',
            'categoria': 'Teste',
            'prioridade': 'Média',
            'descrição': 'Segundo sub-item de teste',
            'periodo': {
                'start': '2025-10-10T13:00:00-03:00',
                'end': '2025-10-10T17:00:00-03:00'
            },
            'tempo_total': 4,
            'sprint': main_card_id  # Link para o item principal
        }
    ]
    
    sub_item_ids = []
    for i, sub_data in enumerate(sub_items, 1):
        sub_id = engine.create_card('WORK', sub_data)
        if sub_id:
            sub_item_ids.append(sub_id)
            print(f"✅ Sub-item {i} WORK criado: {sub_id}")
            print(f"🔗 Link: https://notion.so/{sub_id}")
        else:
            print(f"❌ Falha ao criar sub-item {i} WORK")
    
    return {
        'main_card': main_card_id,
        'sub_items': sub_item_ids,
        'main_link': f"https://notion.so/{main_card_id}",
        'sub_links': [f"https://notion.so/{sid}" for sid in sub_item_ids]
    }

def create_personal_test():
    """Cria teste na base PERSONAL com subtarefas linkadas"""
    
    engine = NotionEngine(TOKEN)
    
    print("\n👤 Criando teste PERSONAL...")
    
    # 1. Criar tarefa principal
    main_card_data = {
        'title': 'Meu teste de Automação',
        'status': 'Não iniciado',
        'categoria': 'Teste',
        'prioridade': 'Média',
        'descrição': 'Tarefa principal para teste de automação na base PERSONAL',
        'periodo': {
            'start': '2025-10-10T09:00:00-03:00',
            'end': '2025-10-10T17:00:00-03:00'
        },
        'tempo_total': 8
    }
    
    main_card_id = engine.create_card('PERSONAL', main_card_data)
    
    if not main_card_id:
        print("❌ Falha ao criar tarefa principal PERSONAL")
        return None
    
    print(f"✅ Tarefa principal PERSONAL criada: {main_card_id}")
    print(f"🔗 Link: https://notion.so/{main_card_id}")
    
    # 2. Criar subtarefas linkadas
    sub_items = [
        {
            'title': 'Meu Item de testes de automação 1',
            'status': 'Não iniciado',
            'categoria': 'Teste',
            'prioridade': 'Alta',
            'descrição': 'Primeira subtarefa de teste',
            'periodo': {
                'start': '2025-10-10T09:00:00-03:00',
                'end': '2025-10-10T12:00:00-03:00'
            },
            'tempo_total': 3,
            'subtarefa': main_card_id  # Link para a tarefa principal
        },
        {
            'title': 'Meu Item de testes de automação 2',
            'status': 'Não iniciado',
            'categoria': 'Teste',
            'prioridade': 'Média',
            'descrição': 'Segunda subtarefa de teste',
            'periodo': {
                'start': '2025-10-10T13:00:00-03:00',
                'end': '2025-10-10T17:00:00-03:00'
            },
            'tempo_total': 4,
            'subtarefa': main_card_id  # Link para a tarefa principal
        }
    ]
    
    sub_item_ids = []
    for i, sub_data in enumerate(sub_items, 1):
        sub_id = engine.create_card('PERSONAL', sub_data)
        if sub_id:
            sub_item_ids.append(sub_id)
            print(f"✅ Subtarefa {i} PERSONAL criada: {sub_id}")
            print(f"🔗 Link: https://notion.so/{sub_id}")
        else:
            print(f"❌ Falha ao criar subtarefa {i} PERSONAL")
    
    return {
        'main_card': main_card_id,
        'sub_items': sub_item_ids,
        'main_link': f"https://notion.so/{main_card_id}",
        'sub_links': [f"https://notion.so/{sid}" for sid in sub_item_ids]
    }

def main():
    """Executa os testes de criação"""
    
    print("🚀 Iniciando recriação dos testes WORK e PERSONAL...")
    
    # Criar testes
    work_result = create_work_test()
    personal_result = create_personal_test()
    
    # Resumo dos resultados
    print("\n" + "="*60)
    print("📋 RESUMO DOS TESTES RECRIADOS")
    print("="*60)
    
    if work_result:
        print(f"\n🏢 WORK:")
        print(f"   Principal: {work_result['main_link']}")
        for i, link in enumerate(work_result['sub_links'], 1):
            print(f"   Sub-item {i}: {link}")
    else:
        print("\n❌ WORK: Falha na criação")
    
    if personal_result:
        print(f"\n👤 PERSONAL:")
        print(f"   Principal: {personal_result['main_link']}")
        for i, link in enumerate(personal_result['sub_links'], 1):
            print(f"   Subtarefa {i}: {link}")
    else:
        print("\n❌ PERSONAL: Falha na criação")
    
    print("\n✅ Testes WORK e PERSONAL recriados!")
    print("🎯 Agora você pode validar os links no Notion")

if __name__ == "__main__":
    main()
