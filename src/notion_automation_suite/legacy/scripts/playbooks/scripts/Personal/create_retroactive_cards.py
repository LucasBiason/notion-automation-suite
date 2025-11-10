#!/usr/bin/env python3
"""
Criar cards retroativos da semana atual (20-22/10/2025)
"""

import sys
import os
from dotenv import load_dotenv

# Adicionar o diretório models ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from personal_templates import PersonalTemplates

def create_retroactive_cards():
    """Cria cards retroativos da semana atual"""
    
    # Carregar token
    load_dotenv()
    TOKEN = os.getenv('NOTION_API_TOKEN')
    
    if not TOKEN:
        print("❌ Token do Notion não configurado")
        return
    
    # Inicializar classe
    templates = PersonalTemplates(TOKEN)
    
    print("📅 Criando cards retroativos da semana...")
    print("=" * 60)
    
    # 1. Segunda (20/10) - Planejamento Semanal (Concluído)
    print("\n📝 Segunda (20/10): Planejamento Semanal")
    planejamento_id = templates.create_card_from_template(
        "planejamento_semanal",
        "2025-10-20",
        status="Concluído"
    )
    
    # 2. Segunda (20/10) - Pagamento Hamilton (Concluído)
    print("\n💰 Segunda (20/10): Pagamento Hamilton (Médico)")
    pagamento_id = templates.create_card_from_template(
        "pagamento_hamilton",
        "2025-10-20",
        status="Concluído"
    )
    
    # 3. Terça (21/10) - Tratamento Médico (Concluído)
    print("\n🏥 Terça (21/10): Tratamento Médico")
    tratamento_id = templates.create_card_from_template(
        "tratamento_medico",
        "2025-10-21",
        status="Concluído"
    )
    
    # 4. Terça (21/10) - Consulta Médica Emergencial - Dr. Mario Otorino
    print("\n🚨 Terça (21/10): Consulta Médica Emergencial - Dr. Mario Otorino")
    consulta_id = templates.create_consulta_medica(
        medico="Doutor Mario",
        especialidade="Otorino",
        date="2025-10-21",
        hora_inicio="",  # Não informado
        hora_fim="",     # Não informado
        status="Concluído"
    )
    
    # 5. Quarta (22/10) - Planejamento Semanal (Em andamento - hoje)
    print("\n📝 Quarta (22/10): Revisão Semanal (Hoje)")
    revisao_id = templates.create_card_from_template(
        "planejamento_semanal",
        "2025-10-22",
        status="Em andamento"
    )
    
    print("\n" + "=" * 60)
    print("✅ Todos os cards retroativos foram criados!")
    
    # Retornar IDs para adicionar ícones depois
    return {
        "planejamento": planejamento_id,
        "pagamento": pagamento_id,
        "tratamento": tratamento_id,
        "consulta": consulta_id,
        "revisao": revisao_id
    }

if __name__ == "__main__":
    card_ids = create_retroactive_cards()
    
    # Adicionar ícones
    if card_ids:
        print("\n🎨 Adicionando ícones aos cards...")
        
        import requests
        from dotenv import load_dotenv
        
        load_dotenv()
        TOKEN = os.getenv('NOTION_API_TOKEN')
        HEADERS = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Mapeamento de ícones
        icons = {
            "planejamento": "📝",
            "pagamento": "💰",
            "tratamento": "🏥",
            "consulta": "🏥",
            "revisao": "📝"
        }
        
        for key, card_id in card_ids.items():
            if card_id:
                url = f"https://api.notion.com/v1/pages/{card_id}"
                data = {"icon": {"type": "emoji", "emoji": icons[key]}}
                response = requests.patch(url, headers=HEADERS, json=data)
                if response.status_code == 200:
                    print(f"  ✅ Ícone {icons[key]} adicionado ao card {key}")
        
        print("\n🎉 Processo concluído!")













