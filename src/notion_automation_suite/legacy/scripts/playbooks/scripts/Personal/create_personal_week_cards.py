#!/usr/bin/env python3
"""
Script para criar cards pessoais da semana atual
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
PERSONAL_DB_ID = "288962a7693c8171982ff9b13993df67"

def create_week_personal_cards():
    """Cria os cards pessoais para a semana atual"""
    
    if not TOKEN:
        print("❌ Token do Notion não encontrado. Configure a variável NOTION_TOKEN.")
        return
    
    # Data atual em GMT-3
    now = datetime.now(timezone(timedelta(hours=-3)))
    
    # Calcular início e fim da semana (segunda a domingo)
    start_of_week = now - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    print(f"📅 Criando cards para a semana: {start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m')}")
    
    # Inicializar o engine
    engine = NotionEngine(TOKEN)
    
    # Cards da semana
    week_cards = [
        {
            "title": "💰 Pagamento Médico",
            "status": "Concluído",
            "data": {
                "start": start_of_week.strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Financeiro"],
            "descricao": "Pagamento mensal do plano médico"
        },
        {
            "title": "🏠 Limpeza da Casa",
            "status": "Não iniciado",
            "data": {
                "start": (start_of_week + timedelta(days=1)).strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Casa"],
            "descricao": "Limpeza geral da casa - quartos, banheiros e cozinha"
        },
        {
            "title": "🛒 Compras Supermercado",
            "status": "Não iniciado", 
            "data": {
                "start": (start_of_week + timedelta(days=2)).strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Compras"],
            "descricao": "Lista de compras da semana - frutas, verduras e itens essenciais"
        },
        {
            "title": "💻 Backup dos Projetos",
            "status": "Não iniciado",
            "data": {
                "start": (start_of_week + timedelta(days=3)).strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Tecnologia"],
            "descricao": "Backup semanal dos projetos no GitHub e drive"
        },
        {
            "title": "📚 Revisão de Estudos",
            "status": "Não iniciado",
            "data": {
                "start": (start_of_week + timedelta(days=4)).strftime('%Y-%m-%d'),
                "end": None
            },
            "categoria": ["Estudos"],
            "descricao": "Revisão do conteúdo estudado durante a semana"
        }
    ]
    
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
    print(f"\n📊 RESUMO DA SEMANA:")
    print(f"📅 Período: {start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m')}")
    print(f"✅ Cards criados: {len(created_cards)}")
    
    for card in created_cards:
        status_emoji = "✅" if card["status"] == "Concluído" else "⏳"
        print(f"  {status_emoji} {card['title']} - {card['status']}")
    
    return created_cards

if __name__ == "__main__":
    create_week_personal_cards()
