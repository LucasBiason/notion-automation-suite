"""
Notion API Client - Cliente centralizado para todas as operações com Notion
"""

import requests
import os
from datetime import datetime
from typing import Dict, List, Optional
import pytz


class NotionClient:
    """Cliente para interagir com a API do Notion"""
    
    def __init__(self):
        self.token = os.getenv('NOTION_TOKEN')
        self.version = os.getenv('NOTION_VERSION', '2022-06-28')
        self.base_url = 'https://api.notion.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Notion-Version': self.version
        }
        self.sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    
    def format_date_gmt3(self, dt: datetime, include_time: bool = True) -> str:
        """Formata data para GMT-3 (SEMPRE)"""
        if include_time:
            return dt.strftime('%Y-%m-%dT%H:%M:%S.000-03:00')
        else:
            return dt.strftime('%Y-%m-%d')
    
    def query_database(self, database_id: str, filter_obj: Optional[Dict] = None) -> List[Dict]:
        """Consulta um database do Notion"""
        url = f'{self.base_url}/databases/{database_id}/query'
        
        payload = {}
        if filter_obj:
            payload['filter'] = filter_obj
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            return response.json()['results']
        else:
            raise Exception(f"Erro ao consultar database: {response.text}")
    
    def create_page(self, database_id: str, properties: Dict, icon: Optional[str] = None) -> str:
        """Cria uma página no Notion"""
        url = f'{self.base_url}/pages'
        
        payload = {
            'parent': {'database_id': database_id},
            'properties': properties
        }
        
        if icon:
            payload['icon'] = {'emoji': icon}
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            return response.json()['id']
        else:
            raise Exception(f"Erro ao criar página: {response.text}")
    
    def update_page(self, page_id: str, properties: Dict) -> bool:
        """Atualiza uma página do Notion"""
        url = f'{self.base_url}/pages/{page_id}'
        
        payload = {'properties': properties}
        
        response = requests.patch(url, headers=self.headers, json=payload)
        
        return response.status_code == 200
    
    def get_page(self, page_id: str) -> Dict:
        """Obtém informações de uma página"""
        url = f'{self.base_url}/pages/{page_id}'
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro ao obter página: {response.text}")
    
    def get_database_properties(self, database_id: str) -> Dict:
        """Obtém propriedades de um database"""
        url = f'{self.base_url}/databases/{database_id}'
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()['properties']
        else:
            raise Exception(f"Erro ao obter propriedades: {response.text}")

