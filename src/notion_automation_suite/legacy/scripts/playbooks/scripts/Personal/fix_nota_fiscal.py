#!/usr/bin/env python3
"""
Atualizar Nota Fiscal Astracode para Concluído
"""

import sys
import os
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
TOKEN = os.getenv('NOTION_API_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

PERSONAL_DB_ID = "1fa962a7-693c-8032-8996-dd9cd2607dbf"

def update_nota_fiscal_status():
    """Atualiza o status da nota fiscal para Concluído"""
    
    # ID do card da nota fiscal
    card_id = "279962a7-693c-8186-b5d6-f3fda7f88de0"
    
    url = f"https://api.notion.com/v1/pages/{card_id}"
    
    data = {
        "properties": {
            "Status": {
                "status": {
                    "name": "Concluído"
                }
            }
        }
    }
    
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        print("✅ Nota Fiscal Astracode marcada como Concluída!")
        return True
    else:
        print(f"❌ Erro ao atualizar: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    print("📄 Atualizando Nota Fiscal Astracode...")
    update_nota_fiscal_status()













