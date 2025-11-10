#!/usr/bin/env python3
"""
Script para criar teste fictício YOUTUBER - Série Pokemon Legends Z-A
Teste com série principal + 20 episódios com datas específicas
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

def create_youtuber_fictitious_series():
    """Cria série fictícia Pokemon Legends Z-A com 20 episódios"""
    
    engine = NotionEngine(TOKEN)
    
    print("🎬 Criando série fictícia YOUTUBER...")
    
    # Sinopse fictícia para o primeiro episódio
    synopsis = """
    Bem-vindos à nossa jornada épica através da região de Kalos em Pokemon Legends Z-A! 
    
    Nesta série fictícia, embarcaremos em uma aventura única onde exploraremos as profundezas 
    da história de Kalos, descobrindo segredos antigos e enfrentando desafios nunca antes vistos. 
    
    Cada episódio nos levará mais fundo na mitologia Pokemon, com batalhas épicas, 
    descobertas arqueológicas e momentos emocionantes que farão você se apaixonar 
    novamente pelo mundo dos Pokemon.
    
    Prepare-se para uma experiência imersiva como nunca antes!
    """
    
    # 1. Criar série principal (Item Principal)
    series_data = {
        'title': 'Pokemon Legends Z-A',
        'status': 'Não iniciado',
        'categoria': 'Gaming',
        'prioridade': 'Alta',
        'descrição': 'Série fictícia de gameplay de Pokemon Legends Z-A - 20 episódios',
        'periodo': {
            'start': '2025-10-16T12:00:00-03:00',  # Data de lançamento da série
            'end': '2025-11-04T12:00:00-03:00'     # Data final (20 dias depois)
        },
        'tempo_total': 400  # 20 episódios x 20 horas estimadas
    }
    
    series_id = engine.create_card('YOUTUBER', series_data)
    
    if not series_id:
        print("❌ Falha ao criar série principal YOUTUBER")
        return None
    
    print(f"✅ Série principal criada: {series_id}")
    print(f"🔗 Link: https://notion.so/{series_id}")
    
    # 2. Criar 20 episódios
    episodes = []
    base_date = datetime(2025, 10, 16, tzinfo=SAO_PAULO_TZ)  # 16/10/2025
    
    for i in range(1, 21):  # Episódios 1 a 20
        episode_date = base_date + timedelta(days=i-1)
        
        # Horário de lançamento: 12:00
        launch_time = episode_date.replace(hour=12, minute=0, second=0)
        
        # Horário de período (criação):
        # Episódio 1: 7:00-9:00 no mesmo dia
        # Episódios 2+: dois por dia das 21:00-11:50 (próximo dia)
        if i == 1:
            period_start = episode_date.replace(hour=7, minute=0, second=0)
            period_end = episode_date.replace(hour=9, minute=0, second=0)
        else:
            # Para episódios pares (2, 4, 6...): 21:00-23:50
            # Para episódios ímpares (3, 5, 7...): 21:00-11:50 (próximo dia)
            if i % 2 == 0:  # Par
                period_start = episode_date.replace(hour=21, minute=0, second=0)
                period_end = episode_date.replace(hour=23, minute=50, second=0)
            else:  # Ímpar
                period_start = episode_date.replace(hour=21, minute=0, second=0)
                period_end = (episode_date + timedelta(days=1)).replace(hour=11, minute=50, second=0)
        
        episode_data = {
            'title': f'Episódio {i:02d}',
            'status': 'Não iniciado',
            'categoria': 'Gaming',
            'prioridade': 'Alta',
            'descrição': f'Episódio {i} da série Pokemon Legends Z-A - Exploração da região de Kalos',
            'periodo': {
                'start': period_start.isoformat(),
                'end': period_end.isoformat()
            },
            'tempo_total': 20,  # 20 minutos por episódio
            'data_lancamento': launch_time.isoformat(),
            'item_principal': series_id,  # Link para a série
            'resumo_episodio': synopsis if i == 1 else f'Episódio {i} da nossa jornada épica através de Kalos. Descubra novos segredos e enfrente desafios únicos neste episódio emocionante!'
        }
        
        episode_id = engine.create_card('YOUTUBER', episode_data)
        
        if episode_id:
            episodes.append({
                'number': i,
                'id': episode_id,
                'link': f"https://notion.so/{episode_id}",
                'launch_date': launch_time.strftime('%d/%m/%Y %H:%M'),
                'period': f"{period_start.strftime('%d/%m/%Y %H:%M')} - {period_end.strftime('%d/%m/%Y %H:%M')}"
            })
            print(f"✅ Episódio {i:02d} criado: {episode_id}")
        else:
            print(f"❌ Falha ao criar episódio {i}")
    
    return {
        'series': {
            'id': series_id,
            'link': f"https://notion.so/{series_id}",
            'title': 'Pokemon Legends Z-A'
        },
        'episodes': episodes,
        'total_episodes': len(episodes)
    }

def main():
    """Executa o teste fictício YOUTUBER"""
    
    print("🎮 Iniciando teste fictício YOUTUBER...")
    print("📅 Série: Pokemon Legends Z-A")
    print("📺 Episódios: 20 (lançamento diário às 12:00)")
    print("⏰ Período: Ep.1 (7:00-9:00), Demais (21:00-11:50)")
    print()
    
    result = create_youtuber_fictitious_series()
    
    if result:
        print("\n" + "="*80)
        print("📋 RESUMO DO TESTE FICTÍCIO YOUTUBER")
        print("="*80)
        
        print(f"\n🎬 SÉRIE PRINCIPAL:")
        print(f"   Título: {result['series']['title']}")
        print(f"   Link: {result['series']['link']}")
        
        print(f"\n📺 EPISÓDIOS CRIADOS ({result['total_episodes']}):")
        for ep in result['episodes']:
            print(f"   Ep. {ep['number']:02d}: {ep['link']}")
            print(f"           Lançamento: {ep['launch_date']}")
            print(f"           Período: {ep['period']}")
            print()
        
        print("✅ Teste fictício YOUTUBER concluído!")
        print("🎯 Série criada com sinopse no primeiro episódio")
        print("📅 Datas de lançamento: diário às 12:00 a partir de 16/10/2025")
        print("⏰ Períodos de criação respeitados conforme especificado")
        
    else:
        print("❌ Falha na criação do teste fictício YOUTUBER")

if __name__ == "__main__":
    main()


