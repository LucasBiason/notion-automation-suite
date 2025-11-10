#!/usr/bin/env python3
"""
Script de TESTE - Criação de Cards no Notion
Versão: 1.0
Data: 10/10/2025
Responsável: Guardião do Notion

Testa criação de cards em todas as 4 bases do Notion:
- WORK: Item principal + 2 subitens (via Sprint)
- PERSONAL: Tarefa principal + 2 subtarefas (via Subtarefa)
- STUDIES: Item principal + 2 subitens (via Parent item)
- YOUTUBER: Item principal + 2 episódios (via Série Principal)

Cada base tem padrões diferentes que devem ser respeitados.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.notion_engine import NotionEngine
from datetime import datetime, timezone, timedelta

# Credenciais
TOKEN = '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'

# Timezone GMT-3 (São Paulo)
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

def format_date_gmt3(dt, include_time=True):
    """Formata data para GMT-3"""
    if include_time:
        return dt.strftime('%Y-%m-%dT%H:%M:%S.000-03:00')
    else:
        return dt.strftime('%Y-%m-%d')

def test_work_base(engine):
    """Testa criação na base WORK"""
    print("\n" + "="*80)
    print("1️⃣  TESTANDO BASE: TRABALHO (WORK)")
    print("="*80)
    
    # Card principal
    print("\n📋 Criando card principal...")
    main_card_data = {
        'title': 'Meu teste de Automação',
        'emoji': '🧪',
        'status': 'Não iniciado',
        'cliente': 'Pessoal',
        'projeto': 'Automação',
        'priority': 'Média'
    }
    
    main_card_id = engine.create_card('WORK', main_card_data)
    
    if not main_card_id:
        print("❌ Falha ao criar card principal WORK")
        return None
    
    print(f"✅ Card principal criado: {main_card_id}")
    
    # Subitens
    print("\n📋 Criando 2 subitens...")
    subitems = [
        {
            'title': 'Meu Item de testes de automação 1',
            'emoji': '✅',
            'status': 'Não iniciado',
            'cliente': 'Pessoal',
            'projeto': 'Automação',
            'priority': 'Média'
        },
        {
            'title': 'Meu Item de testes de automação 2',
            'emoji': '✅',
            'status': 'Não iniciado',
            'cliente': 'Pessoal',
            'projeto': 'Automação',
            'priority': 'Média'
        }
    ]
    
    result = engine.create_subitems_only('WORK', main_card_id, subitems)
    
    print(f"\n📊 Resultado WORK:")
    print(f"   ✅ Criados: {result['created']}/2")
    print(f"   ❌ Falhas: {result['failed']}")
    print(f"   🔗 Card principal: https://notion.so/{main_card_id.replace('-', '')}")
    
    return {
        'base': 'WORK',
        'main_id': main_card_id,
        'created': result['created'],
        'failed': result['failed']
    }

def test_personal_base(engine):
    """Testa criação na base PERSONAL"""
    print("\n" + "="*80)
    print("2️⃣  TESTANDO BASE: PESSOAL (PERSONAL)")
    print("="*80)
    
    # Card principal
    print("\n📋 Criando tarefa principal...")
    main_card_data = {
        'title': 'Meu teste de Automação',
        'emoji': '🧪',
        'status': 'Não iniciado',
        'atividade': 'Desenvolvimento'
    }
    
    main_card_id = engine.create_card('PERSONAL', main_card_data)
    
    if not main_card_id:
        print("❌ Falha ao criar tarefa principal PERSONAL")
        return None
    
    print(f"✅ Tarefa principal criada: {main_card_id}")
    
    # Subtarefas
    print("\n📋 Criando 2 subtarefas...")
    subtasks = [
        {
            'title': 'Meu Item de testes de automação 1',
            'emoji': '✅',
            'status': 'Não iniciado',
            'atividade': 'Desenvolvimento'
        },
        {
            'title': 'Meu Item de testes de automação 2',
            'emoji': '✅',
            'status': 'Não iniciado',
            'atividade': 'Desenvolvimento'
        }
    ]
    
    result = engine.create_subitems_only('PERSONAL', main_card_id, subtasks)
    
    print(f"\n📊 Resultado PERSONAL:")
    print(f"   ✅ Criados: {result['created']}/2")
    print(f"   ❌ Falhas: {result['failed']}")
    print(f"   🔗 Tarefa principal: https://notion.so/{main_card_id.replace('-', '')}")
    
    return {
        'base': 'PERSONAL',
        'main_id': main_card_id,
        'created': result['created'],
        'failed': result['failed']
    }

def test_studies_base(engine):
    """Testa criação na base STUDIES"""
    print("\n" + "="*80)
    print("3️⃣  TESTANDO BASE: CURSOS (STUDIES)")
    print("="*80)
    
    # Card principal
    print("\n📋 Criando item principal...")
    
    # Data de início e fim (sem horário)
    start_date = datetime.now(SAO_PAULO_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=7)
    
    main_card_data = {
        'title': 'Meu teste de Automação',
        'emoji': '🧪',
        'status': 'Para Fazer',
        'categorias': ['Testes', 'Automação'],
        'periodo': {
            'start': format_date_gmt3(start_date, include_time=False),
            'end': format_date_gmt3(end_date, include_time=False)
        },
        'tempo_total': '02:00:00'
    }
    
    main_card_id = engine.create_card('STUDIES', main_card_data)
    
    if not main_card_id:
        print("❌ Falha ao criar item principal STUDIES")
        return None
    
    print(f"✅ Item principal criado: {main_card_id}")
    
    # Subitens (com horário)
    print("\n📋 Criando 2 subitens...")
    
    # Calcular períodos com horário
    aula1_start = start_date.replace(hour=19, minute=0)
    aula1_end = aula1_start + timedelta(minutes=60)
    
    aula2_start = aula1_end + timedelta(minutes=15)  # 15 min revisão
    aula2_end = aula2_start + timedelta(minutes=60)
    
    subitems = [
        {
            'title': 'Meu Item de testes de automação 1',
            'emoji': '✅',
            'status': 'Para Fazer',
            'categorias': ['Testes', 'Automação', 'Aula'],
            'periodo': {
                'start': format_date_gmt3(aula1_start, include_time=True),
                'end': format_date_gmt3(aula1_end, include_time=True)
            },
            'tempo_total': '01:00:00'
        },
        {
            'title': 'Meu Item de testes de automação 2',
            'emoji': '✅',
            'status': 'Para Fazer',
            'categorias': ['Testes', 'Automação', 'Aula'],
            'periodo': {
                'start': format_date_gmt3(aula2_start, include_time=True),
                'end': format_date_gmt3(aula2_end, include_time=True)
            },
            'tempo_total': '01:00:00'
        }
    ]
    
    result = engine.create_subitems_only('STUDIES', main_card_id, subitems)
    
    print(f"\n📊 Resultado STUDIES:")
    print(f"   ✅ Criados: {result['created']}/2")
    print(f"   ❌ Falhas: {result['failed']}")
    print(f"   🔗 Item principal: https://notion.so/{main_card_id.replace('-', '')}")
    
    return {
        'base': 'STUDIES',
        'main_id': main_card_id,
        'created': result['created'],
        'failed': result['failed']
    }

def test_youtuber_base(engine):
    """Testa criação na base YOUTUBER"""
    print("\n" + "="*80)
    print("4️⃣  TESTANDO BASE: YOUTUBE (YOUTUBER)")
    print("="*80)
    
    # Card principal
    print("\n📋 Criando série principal...")
    
    # Data de lançamento (sem horário)
    launch_date = datetime.now(SAO_PAULO_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    
    main_card_data = {
        'title': 'Meu teste de Automação',
        'emoji': '🧪',
        'status': 'Não iniciado'
    }
    
    main_card_id = engine.create_card('YOUTUBER', main_card_data)
    
    if not main_card_id:
        print("❌ Falha ao criar série principal YOUTUBER")
        return None
    
    print(f"✅ Série principal criada: {main_card_id}")
    
    # Episódios (com período de gravação)
    print("\n📋 Criando 2 episódios...")
    
    # Calcular períodos de gravação
    ep1_start = launch_date.replace(hour=21, minute=0)
    ep1_end = ep1_start + timedelta(hours=1)
    
    ep2_start = (launch_date + timedelta(days=1)).replace(hour=21, minute=0)
    ep2_end = ep2_start + timedelta(hours=1)
    
    episodes = [
        {
            'title': 'Meu Item de testes de automação 1',
            'emoji': '✅',
            'status': 'Não iniciado',
            'periodo': {
                'start': format_date_gmt3(ep1_start, include_time=True),
                'end': format_date_gmt3(ep1_end, include_time=True)
            }
        },
        {
            'title': 'Meu Item de testes de automação 2',
            'emoji': '✅',
            'status': 'Não iniciado',
            'periodo': {
                'start': format_date_gmt3(ep2_start, include_time=True),
                'end': format_date_gmt3(ep2_end, include_time=True)
            }
        }
    ]
    
    result = engine.create_subitems_only('YOUTUBER', main_card_id, episodes)
    
    print(f"\n📊 Resultado YOUTUBER:")
    print(f"   ✅ Criados: {result['created']}/2")
    print(f"   ❌ Falhas: {result['failed']}")
    print(f"   🔗 Série principal: https://notion.so/{main_card_id.replace('-', '')}")
    
    return {
        'base': 'YOUTUBER',
        'main_id': main_card_id,
        'created': result['created'],
        'failed': result['failed']
    }

def main():
    """Função principal de teste"""
    print("="*80)
    print("🧪 TESTE COMPLETO - CRIAÇÃO DE CARDS NAS 4 BASES DO NOTION")
    print("="*80)
    print("\nGuardião do Notion - Validação de Padrões")
    print(f"Data: {datetime.now(SAO_PAULO_TZ).strftime('%d/%m/%Y %H:%M')} GMT-3")
    print("="*80)
    
    # Inicializar engine
    print("\n🔧 Inicializando Notion Engine...")
    engine = NotionEngine(TOKEN)
    print("✅ Engine inicializado")
    
    # Testar cada base
    results = []
    
    try:
        # 1. WORK
        work_result = test_work_base(engine)
        if work_result:
            results.append(work_result)
        
        # 2. PERSONAL
        personal_result = test_personal_base(engine)
        if personal_result:
            results.append(personal_result)
        
        # 3. STUDIES
        studies_result = test_studies_base(engine)
        if studies_result:
            results.append(studies_result)
        
        # 4. YOUTUBER
        youtuber_result = test_youtuber_base(engine)
        if youtuber_result:
            results.append(youtuber_result)
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Resumo final
    print("\n" + "="*80)
    print("📊 RESUMO FINAL DOS TESTES")
    print("="*80)
    
    total_created = 0
    total_failed = 0
    
    for result in results:
        base = result['base']
        created = result['created']
        failed = result['failed']
        main_id = result['main_id']
        
        status = "✅" if created == 2 and failed == 0 else "⚠️"
        print(f"\n{status} {base}:")
        print(f"   Card principal: {main_id}")
        print(f"   Subitens criados: {created}/2")
        print(f"   Falhas: {failed}")
        print(f"   URL: https://notion.so/{main_id.replace('-', '')}")
        
        total_created += created
        total_failed += failed
    
    print("\n" + "="*80)
    print(f"📊 TOTAL GERAL:")
    print(f"   Bases testadas: {len(results)}/4")
    print(f"   Cards principais: {len(results)}")
    print(f"   Subitens criados: {total_created}/8")
    print(f"   Falhas: {total_failed}")
    print("="*80)
    
    if len(results) == 4 and total_created == 8 and total_failed == 0:
        print("\n🎉 SUCESSO TOTAL! Todos os cards foram criados corretamente!")
        print("\n✅ VALIDAÇÃO NECESSÁRIA:")
        print("   Por favor, verifique no Notion se os cards estão corretos:")
        print("   1. Emojis aparecem como ÍCONES (não no título)")
        print("   2. Subitens estão vinculados ao card principal")
        print("   3. Propriedades estão corretas em cada base")
        print("   4. Timezone GMT-3 está correto nos períodos")
        return True
    else:
        print("\n⚠️ ATENÇÃO! Algumas bases apresentaram problemas.")
        print("   Verifique os detalhes acima.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

