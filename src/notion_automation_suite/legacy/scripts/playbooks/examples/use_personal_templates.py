#!/usr/bin/env python3
"""
Exemplo de uso da classe PersonalTemplates
"""

import sys
import os
from dotenv import load_dotenv

# Adicionar o diretório models ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

from personal_templates import PersonalTemplates

def main():
    """Exemplo de uso dos templates pessoais"""
    
    # Carregar token
    load_dotenv()
    TOKEN = os.getenv('NOTION_API_TOKEN')
    
    if not TOKEN:
        print("❌ Token do Notion não configurado")
        return
    
    # Inicializar classe
    templates = PersonalTemplates(TOKEN)
    
    print("🎯 PersonalTemplates - Exemplos de Uso\n")
    
    # 1. Listar templates disponíveis
    print("1️⃣ Templates disponíveis:")
    for name, data in templates.list_available_templates().items():
        print(f"   • {name}: {data['title']} ({data['emoji']})")
    
    print("\n" + "="*50)
    
    # 2. Criar um card específico
    print("\n2️⃣ Criar um card específico:")
    print("   Exemplo: Planejamento Semanal para 21/10/2025")
    
    # card_id = templates.create_card_from_template(
    #     "planejamento_semanal", 
    #     "2025-10-21", 
    #     "Não iniciado"
    # )
    # if card_id:
    #     print(f"   ✅ Card criado: {card_id}")
    
    print("   (Comentado - descomente para executar)")
    
    # 3. Criar eventos da semana
    print("\n3️⃣ Criar eventos da semana:")
    print("   Exemplo: Semana de 21/10/2025")
    
    # cards = templates.create_weekly_events("2025-10-21", mark_completed=False)
    # print(f"   Cards criados: {len(cards)}")
    # for template, card_id in cards.items():
    #     if card_id:
    #         print(f"   ✅ {template}: {card_id}")
    
    print("   (Comentado - descomente para executar)")
    
    # 4. Criar eventos do mês
    print("\n4️⃣ Criar eventos do mês:")
    print("   Exemplo: Outubro 2025")
    
    # cards = templates.create_monthly_events(2025, 10, mark_completed=False)
    # print(f"   Cards criados: {len(cards)}")
    # for template, card_id in cards.items():
    #     if card_id:
    #         print(f"   ✅ {template}: {card_id}")
    
    print("   (Comentado - descomente para executar)")
    
    # 5. Criar card com dados customizados
    print("\n5️⃣ Criar card com dados customizados:")
    print("   Exemplo: Tratamento com descrição personalizada")
    
    # custom_data = {
    #     "description": "Sessão de tratamento médico - consulta de retorno",
    #     "atividade": "Saúde"
    # }
    # 
    # card_id = templates.create_card_from_template(
    #     "tratamento_medico",
    #     "2025-10-22",
    #     "Não iniciado",
    #     custom_data=custom_data
    # )
    # if card_id:
    #     print(f"   ✅ Card customizado criado: {card_id}")
    
    print("   (Comentado - descomente para executar)")
    
    print("\n" + "="*50)
    print("📝 COMO USAR:")
    print("1. Descomente as linhas que você quer executar")
    print("2. Ajuste as datas conforme necessário")
    print("3. Execute: python3 use_personal_templates.py")
    print("4. Os cards serão criados na base pessoal do Notion")

if __name__ == "__main__":
    main()













