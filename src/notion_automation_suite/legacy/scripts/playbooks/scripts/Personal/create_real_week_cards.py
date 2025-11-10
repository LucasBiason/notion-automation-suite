#!/usr/bin/env python3
"""
Script para criar os cards pessoais reais da semana (13-19 de outubro)
"""

import sys
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

# Importar o NotionEngine
from core.notion_engine import NotionEngine

# Configurações
TOKEN = os.getenv('NOTION_API_TOKEN')

def create_real_week_cards():
    """Cria os cards pessoais reais da semana"""
    
    if not TOKEN:
        print("❌ Token do Notion não encontrado. Configure a variável NOTION_API_TOKEN.")
        return
    
    # Data atual em GMT-3
    now = datetime.now(timezone(timedelta(hours=-3)))
    
    print(f"📅 Criando cards para a semana de 13-19 de outubro")
    
    # Inicializar o engine
    engine = NotionEngine(TOKEN)
    
    # Cards da semana seguindo os eventos recorrentes REAIS
    week_cards = [
        # Segunda-feira 14/10 - Planejamento Semanal (JÁ FEITO)
        {
            "title": "Planejamento Semanal",
            "status": "Concluído",
            "data": {
                "start": "2025-10-14",
                "end": None
            },
            "atividade": "Planejamento",
            "descricao": "Planejamento semanal e organização de tarefas"
        },
        # Segunda-feira 14/10 - Pagamento Tratamento Hamilton (JÁ FEITO)
        {
            "title": "Pagamento Hamilton (Médico)",
            "status": "Concluído",
            "data": {
                "start": "2025-10-14",
                "end": None
            },
            "atividade": "Financeiro",
            "descricao": "Pagamento mensal do tratamento médico - Dr. Hamilton"
        },
        # Terça-feira 15/10 - Tratamento (JÁ FEITO)
        {
            "title": "Tratamento",
            "status": "Concluído",
            "data": {
                "start": "2025-10-15",
                "end": None
            },
            "atividade": "Saúde",
            "descricao": "Sessão de tratamento médico"
        },
        # Terça-feira 15/10 - Revisão Contábil (JÁ FEITO HOJE)
        {
            "title": "Revisão Contábil",
            "status": "Concluído",
            "data": {
                "start": "2025-10-15",
                "end": None
            },
            "atividade": "Financeiro",
            "descricao": "Revisão contábil mensal - dia 15"
        },
        # Terça-feira 15/10 - Gestão de Pagamento
        {
            "title": "Gestão de Pagamento",
            "status": "Concluído",
            "data": {
                "start": "2025-10-15",
                "end": None
            },
            "atividade": "Financeiro",
            "descricao": "Gestão mensal de pagamentos"
        },
        # Terça-feira 15/10 - Pagamento de Impostos (JÁ FEITO HOJE)
        {
            "title": "Pagamento de Impostos",
            "status": "Concluído",
            "data": {
                "start": "2025-10-15",
                "end": None
            },
            "atividade": "Financeiro",
            "descricao": "Pagamento mensal de impostos"
        }
    ]
    
    created_cards = []
    
    for card_data in week_cards:
        try:
            print(f"📝 Criando: {card_data['title']} ({card_data['status']})")
            
            # Criar o card principal
            result = engine.create_card(
                base="PERSONAL",
                data={
                    "title": card_data["title"],
                    "status": card_data["status"],
                    "periodo": card_data["data"],
                    "atividade": card_data["atividade"],
                    "description": card_data["descricao"]
                }
            )
            
            if result:
                created_cards.append({
                    "title": card_data["title"],
                    "id": result,
                    "status": card_data["status"]
                })
                print(f"✅ {card_data['title']} criado com sucesso")
            else:
                print(f"❌ Falha ao criar: {card_data['title']}")
                
        except Exception as e:
            print(f"❌ Erro ao criar {card_data['title']}: {str(e)}")
    
    # Resumo
    print(f"\n📊 RESUMO DOS CARDS CRIADOS:")
    print(f"📅 Semana: 13-19 de outubro")
    print(f"✅ Cards criados: {len(created_cards)}")
    
    concluidos = [c for c in created_cards if c['status'] == 'Concluído']
    pendentes = [c for c in created_cards if c['status'] != 'Concluído']
    
    print(f"\n✅ Concluídos ({len(concluidos)}):")
    for card in concluidos:
        print(f"  ✅ {card['title']}")
    
    if pendentes:
        print(f"\n⏳ Pendentes ({len(pendentes)}):")
        for card in pendentes:
            print(f"  ⏳ {card['title']}")
    
    return created_cards

if __name__ == "__main__":
    create_real_week_cards()
