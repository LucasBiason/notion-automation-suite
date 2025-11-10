#!/usr/bin/env python3
"""
Script para deletar cards de teste existentes
"""

import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.notion_engine import NotionEngine

def delete_test_cards():
    """Deleta os cards de teste criados anteriormente"""
    
    # Credenciais
    TOKEN = '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'
    
    # Headers para API do Notion
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    
    # IDs dos cards principais criados anteriormente
    cards_to_delete = [
        # WORK base - card principal
        "288962a7693c81c59439e58ad031512e",
        # PERSONAL base - card principal  
        "288962a7693c817fa419c2ce0a27e693",
        # STUDIES base - card principal
        "288962a7693c81ebbdb7d19387c4dbf0"
    ]
    
    print("🗑️  Iniciando deleção dos cards de teste...")
    
    for card_id in cards_to_delete:
        try:
            # Para deletar, vamos arquivar o card (Notion não permite deletar diretamente)
            url = f'https://api.notion.com/v1/pages/{card_id}'
            data = {"archived": True}
            
            response = requests.patch(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"✅ Card {card_id} arquivado com sucesso")
            else:
                print(f"❌ Erro ao arquivar card {card_id}: {response.status_code}")
                print(f"   Resposta: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro ao deletar card {card_id}: {e}")
    
    print("\n🎯 Cards de teste deletados! Agora vou recriar apenas WORK e PERSONAL.")

if __name__ == "__main__":
    delete_test_cards()
