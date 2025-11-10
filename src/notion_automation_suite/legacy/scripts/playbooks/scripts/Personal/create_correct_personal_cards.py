#!/usr/bin/env python3
"""
Script para criar os cards pessoais corretos seguindo o fluxo de eventos recorrentes
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

def create_correct_personal_cards():
    """Cria os cards pessoais corretos seguindo o fluxo de eventos recorrentes"""
    
    if not TOKEN:
        print("❌ Token do Notion não encontrado. Configure a variável NOTION_API_TOKEN.")
        return
    
    # Data atual em GMT-3
    now = datetime.now(timezone(timedelta(hours=-3)))
    
    print(f"📅 Criando cards para a semana atual: {now.strftime('%d/%m/%Y')}")
    
    # Inicializar o engine
    engine = NotionEngine(TOKEN)
    
    # Calcular datas da semana atual
    start_of_week = now - timedelta(days=now.weekday())  # Segunda-feira
    tuesday = start_of_week + timedelta(days=1)  # Terça-feira
    fifteenth = now.replace(day=15)  # Dia 15 do mês
    twenty_fifth = now.replace(day=25)  # Dia 25 do mês
    thirtieth = now.replace(day=30)  # Dia 30 do mês
    
    # Cards seguindo o fluxo de eventos recorrentes
    week_cards = []
    
    # Segunda-feira: Planejamento Semanal e pagamento Tratamento
    if start_of_week.month == now.month:  # Se ainda estamos na semana que contém a segunda
        week_cards.append({
            "title": "📝 Planejamento Semanal",
            "status": "Não iniciado",
            "data": {
                "start": start_of_week.strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Planejamento"],
            "descricao": "Planejamento semanal e organização de tarefas"
        })
        
        week_cards.append({
            "title": "💰 Pagamento Tratamento",
            "status": "Não iniciado",
            "data": {
                "start": start_of_week.strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Financeiro"],
            "descricao": "Pagamento mensal do tratamento médico"
        })
    
    # Terça-feira: Tratamento
    if tuesday.month == now.month:  # Se ainda estamos na semana que contém a terça
        week_cards.append({
            "title": "🏥 Tratamento",
            "status": "Não iniciado",
            "data": {
                "start": tuesday.strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Saúde"],
            "descricao": "Sessão de tratamento médico"
        })
    
    # Dia 15: Gestão de Pagamento e Pagamento de Impostos
    if now.day >= 15:  # Se já passou do dia 15
        week_cards.append({
            "title": "💰 Gestão de Pagamento",
            "status": "Não iniciado",
            "data": {
                "start": fifteenth.strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Financeiro"],
            "descricao": "Gestão mensal de pagamentos"
        })
        
        week_cards.append({
            "title": "💸 Pagamento de Impostos",
            "status": "Não iniciado",
            "data": {
                "start": fifteenth.strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Financeiro"],
            "descricao": "Pagamento mensal de impostos"
        })
    
    # Dia 15 e 30: Revisão Contábil
    if now.day >= 15 and now.month == fifteenth.month:  # Se já passou do dia 15
        week_cards.append({
            "title": "📊 Revisão Contábil",
            "status": "Não iniciado",
            "data": {
                "start": fifteenth.strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Financeiro"],
            "descricao": "Revisão contábil mensal - dia 15"
        })
    
    if now.day >= 30 and now.month == thirtieth.month:  # Se já passou do dia 30
        week_cards.append({
            "title": "📊 Revisão Contábil",
            "status": "Não iniciado",
            "data": {
                "start": thirtieth.strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Financeiro"],
            "descricao": "Revisão contábil mensal - dia 30"
        })
    
    # Dia 25: Geração de Nota Fiscal - Astracode
    if now.day >= 25 and now.month == twenty_fifth.month:  # Se já passou do dia 25
        week_cards.append({
            "title": "📄 Geração de Nota Fiscal - Astracode",
            "status": "Não iniciado",
            "data": {
                "start": twenty_fifth.strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Trabalho"],
            "descricao": "Geração mensal de nota fiscal da Astracode"
        })
    
    # Se não há cards para criar, informar
    if not week_cards:
        print("ℹ️ Não há eventos recorrentes para criar nesta data.")
        return
    
    created_cards = []
    
    for card_data in week_cards:
        try:
            print(f"📝 Criando: {card_data['title']}")
            
            # Criar o card principal
            result = engine.create_card(
                base="PERSONAL",
                data={
                    "title": card_data["title"],
                    "status": card_data["status"],
                    "data": card_data["data"],
                    "categoria": card_data["categoria"],
                    "descricao": card_data["descricao"]
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
    print(f"📅 Data atual: {now.strftime('%d/%m/%Y')}")
    print(f"✅ Cards criados: {len(created_cards)}")
    
    for card in created_cards:
        print(f"  ✅ {card['title']} - {card['status']}")
    
    return created_cards

if __name__ == "__main__":
    create_correct_personal_cards()













