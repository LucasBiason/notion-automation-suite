#!/usr/bin/env python3
"""Verificar propriedades do database de Estudos"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('NOTION_API_TOKEN')
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def get_database_properties():
    """Busca propriedades do database"""
    url = f'https://api.notion.com/v1/databases/{ESTUDOS_DB}'
    
    response = requests.get(url, headers=headers, timeout=60)
    
    if response.status_code == 200:
        db = response.json()
        print('📋 PROPRIEDADES DO DATABASE ESTUDOS:')
        print('=' * 80)
        print('')
        
        for prop_name, prop_data in db['properties'].items():
            prop_type = prop_data['type']
            print(f'• {prop_name}: {prop_type}')
            
            if prop_type == 'status' and 'status' in prop_data:
                print(f'  Opções: {[opt["name"] for opt in prop_data["status"]["options"]]}')
            elif prop_type == 'select' and 'select' in prop_data:
                print(f'  Opções: {[opt["name"] for opt in prop_data["select"]["options"]]}')
        
        print('')
        print('=' * 80)
    else:
        print(f'Erro: {response.text}')

if __name__ == '__main__':
    get_database_properties()










