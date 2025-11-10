#!/usr/bin/env python3
"""
Script para criar eventos mensais (dias 15, 25, 30) se necessário
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

def create_monthly_events():
    """Cria eventos mensais se necessário"""
    
    if not TOKEN:
        print("❌ Token do Notion não encontrado. Configure a variável NOTION_API_TOKEN.")
        return
    
    # Data atual em GMT-3
    now = datetime.now(timezone(timedelta(hours=-3)))
    
    print(f"📅 Verificando eventos mensais para: {now.strftime('%d/%m/%Y')}")
    
    # Inicializar o engine
    engine = NotionEngine(TOKEN)
    
    # Verificar se precisamos criar eventos para o dia 15
    if now.day >= 15:
        fifteenth = now.replace(day=15)
        
        print(f"📝 Criando eventos do dia 15...")
        
        # Gestão de Pagamento
        result1 = engine.create_card(
            base="PERSONAL",
            data={
                "title": "💰 Gestão de Pagamento",
                "status": "Não iniciado",
                "data": {
                    "start": fifteenth.strftime('%Y-%m-%d'),
                    "end": None
                },
                "categoria": ["Financeiro"],
                "descricao": "Gestão mensal de pagamentos"
            }
        )
        
        if result1:
            print("✅ 💰 Gestão de Pagamento criado")
        
        # Pagamento de Impostos
        result2 = engine.create_card(
            base="PERSONAL",
            data={
                "title": "💸 Pagamento de Impostos",
                "status": "Não iniciado",
                "data": {
                    "start": fifteenth.strftime('%Y-%m-%d'),
                    "end": None
                },
                "categoria": ["Financeiro"],
                "descricao": "Pagamento mensal de impostos"
            }
        )
        
        if result2:
            print("✅ 💸 Pagamento de Impostos criado")
        
        # Revisão Contábil - Dia 15
        result3 = engine.create_card(
            base="PERSONAL",
            data={
                "title": "📊 Revisão Contábil",
                "status": "Não iniciado",
                "data": {
                    "start": fifteenth.strftime('%Y-%m-%d'),
                    "end": None
                },
                "categoria": ["Financeiro"],
                "descricao": "Revisão contábil mensal - dia 15"
            }
        )
        
        if result3:
            print("✅ 📊 Revisão Contábil (dia 15) criado")
    
    # Verificar se precisamos criar evento para o dia 25
    if now.day >= 25:
        twenty_fifth = now.replace(day=25)
        
        print(f"📝 Criando evento do dia 25...")
        
        # Geração de Nota Fiscal
        result4 = engine.create_card(
            base="PERSONAL",
            data={
                "title": "📄 Geração de Nota Fiscal - Astracode",
                "status": "Não iniciado",
                "data": {
                    "start": twenty_fifth.strftime('%Y-%m-%d'),
                    "end": None
                },
                "categoria": ["Trabalho"],
                "descricao": "Geração mensal de nota fiscal da Astracode"
            }
        )
        
        if result4:
            print("✅ 📄 Geração de Nota Fiscal criado")
    
    # Verificar se precisamos criar evento para o dia 30
    if now.day >= 30:
        thirtieth = now.replace(day=30)
        
        print(f"📝 Criando evento do dia 30...")
        
        # Revisão Contábil - Dia 30
        result5 = engine.create_card(
            base="PERSONAL",
            data={
                "title": "📊 Revisão Contábil",
                "status": "Não iniciado",
                "data": {
                    "start": thirtieth.strftime('%Y-%m-%d'),
                    "end": None
                },
                "categoria": ["Financeiro"],
                "descricao": "Revisão contábil mensal - dia 30"
            }
        )
        
        if result5:
            print("✅ 📊 Revisão Contábil (dia 30) criado")
    
    print("✅ Verificação de eventos mensais concluída!")

if __name__ == "__main__":
    create_monthly_events()













