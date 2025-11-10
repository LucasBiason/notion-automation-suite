#!/usr/bin/env python3
"""
Teste da função de consulta médica
"""

import sys
import os
from dotenv import load_dotenv

# Adicionar o diretório models ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from personal_templates import PersonalTemplates

def test_consulta_medica():
    """Testa a criação de consulta médica com os dados fornecidos"""
    
    # Carregar token
    load_dotenv()
    TOKEN = os.getenv('NOTION_API_TOKEN')
    
    if not TOKEN:
        print("❌ Token do Notion não configurado")
        return
    
    # Inicializar classe
    templates = PersonalTemplates(TOKEN)
    
    print("🏥 Teste: Criando consulta médica...")
    print("📅 Data: 14/10/2025")
    print("👩‍⚕️ Médico: Doutora Andrea")
    print("🏥 Especialidade: Endocrino")
    print("⏰ Horário: 8:00 às 10:20")
    
    # Criar consulta médica
    card_id = templates.create_consulta_medica(
        medico="Doutora Andrea",
        especialidade="Endocrino",
        date="2025-10-14",
        hora_inicio="8:00",
        hora_fim="10:20",
        status="Concluído"
    )
    
    if card_id:
        print(f"✅ Consulta médica criada com sucesso!")
        print(f"📋 ID do card: {card_id}")
        print(f"🔗 Link: https://www.notion.so/{card_id}")
        
        # Mostrar como ficou o card
        print(f"\n📝 Detalhes do card criado:")
        print(f"   Título: Consulta Médica: Doutora Andrea Endocrino")
        print(f"   Data: 14/10/2025")
        print(f"   Status: Concluído")
        print(f"   Atividade: Saúde")
        print(f"   Descrição: Consulta médica com Doutora Andrea - Endocrino")
        print(f"            Horário: 8:00 às 10:20")
    else:
        print("❌ Falha ao criar consulta médica")

if __name__ == "__main__":
    test_consulta_medica()













