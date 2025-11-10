#!/usr/bin/env python3
"""
Notion Engine - Motor de Criação de Cards
Versão: 5.0
Data: 10/10/2025

Motor centralizado para criar cards no Notion.
Recebe JSONs simples e adapta automaticamente para cada base.
"""

import requests
from typing import Dict, Any, List, Optional

class NotionEngine:
    """Motor principal para criação de cards no Notion."""
    
    BASES = {
        'WORK': {
            'id': '1f9962a7-693c-80a3-b947-c471a975acb0',
            'title_field': 'Nome do projeto',
            'relation_field': 'Sprint'
        },
        'PERSONAL': {
            'id': '1fa962a7-693c-8032-8996-dd9cd2607dbf',
            'title_field': 'Nome da tarefa',
            'relation_field': 'Subtarefa'
        },
        'STUDIES': {
            'id': '1fa962a7-693c-80de-b90b-eaa513dcf9d1',
            'title_field': 'Project name',
            'relation_field': 'Parent item'
        },
        'YOUTUBER': {
            'id': '1fa962a7-693c-80ce-9f1d-ff86223d6bda',
            'title_field': 'Nome do projeto',
            'relation_field': 'item principal'
        }
    }
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = 'https://api.notion.com/v1'
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
    
    def create_card(self, base: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Cria um card no Notion.
        
        Args:
            base: 'WORK', 'PERSONAL', 'STUDIES' ou 'YOUTUBER'
            data: Dict com dados do card
        
        Returns:
            ID do card criado ou None
        """
        payload = self._build_payload(base, data)
        
        response = requests.post(
            f'{self.base_url}/pages',
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['id']
        return None
    
    def create_subitems_only(self, base: str, parent_id: str, 
                            subitems: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Cria subitens para um card existente.
        
        Args:
            base: Tipo da base
            parent_id: ID do card pai
            subitems: Lista de dicts com dados dos subitens
        
        Returns:
            {'created': int, 'failed': int, 'ids': List[str]}
        """
        created_ids = []
        failed = 0
        
        for subitem_data in subitems:
            subitem_data['parent_id'] = parent_id
            card_id = self.create_card(base, subitem_data)
            
            if card_id:
                created_ids.append(card_id)
            else:
                failed += 1
        
        return {
            'created': len(created_ids),
            'failed': failed,
            'ids': created_ids
        }
    
    def _build_payload(self, base: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Constrói payload adaptado para cada base."""
        base_config = self.BASES[base]
        
        payload = {
            "parent": {"database_id": base_config['id']},
            "properties": {}
        }
        
        if data.get('emoji'):
            payload["icon"] = {"emoji": data['emoji']}
        
        if base == 'WORK':
            payload["properties"] = {
                "Nome do projeto": {"title": [{"text": {"content": data['title']}}]},
                "Status": {"status": {"name": data.get('status', 'Não iniciado')}},
                "Cliente": {"select": {"name": data.get('cliente', 'Pessoal')}},
                "Projeto": {"select": {"name": data.get('projeto', 'Automação')}},
                "Prioridade": {"select": {"name": data.get('priority', 'Normal')}}
            }
            
            if data.get('parent_id'):
                payload["properties"]["Sprint"] = {"relation": [{"id": data['parent_id']}]}
            elif data.get('item_principal'):
                payload["properties"]["item principal"] = {"relation": [{"id": data['item_principal']}]}
            
            if data.get('periodo'):
                payload["properties"]["Periodo"] = {"date": data['periodo']}
        
        elif base == 'PERSONAL':
            payload["properties"] = {
                "Nome da tarefa": {"title": [{"text": {"content": data['title']}}]},
                "Status": {"status": {"name": data.get('status', 'Não iniciado')}},
                "Atividade": {"select": {"name": data.get('atividade', 'Desenvolvimento')}}
            }
            
            if data.get('parent_id'):
                payload["properties"]["Subtarefa"] = {"relation": [{"id": data['parent_id']}]}
            elif data.get('tarefa_principal'):
                payload["properties"]["tarefa principal"] = {"relation": [{"id": data['tarefa_principal']}]}
            
            if data.get('periodo'):
                payload["properties"]["Data"] = {"date": data['periodo']}
            
            if data.get('description'):
                payload["properties"]["Descrição"] = {"rich_text": [{"text": {"content": data['description']}}]}
        
        elif base == 'STUDIES':
            payload["properties"] = {
                "Project name": {"title": [{"text": {"content": data['title']}}]},
                "Status": {"status": {"name": data.get('status', 'Para Fazer')}}
            }
            
            if data.get('categorias'):
                payload["properties"]["Categorias"] = {"multi_select": [{"name": cat} for cat in data['categorias']]}
            
            if data.get('parent_id'):
                payload["properties"]["Parent item"] = {"relation": [{"id": data['parent_id']}]}
            elif data.get('parent_item'):
                payload["properties"]["Parent item"] = {"relation": [{"id": data['parent_item']}]}
            
            if data.get('periodo'):
                payload["properties"]["Período"] = {"date": data['periodo']}
            
            if data.get('tempo_total'):
                payload["properties"]["Tempo Total"] = {"rich_text": [{"text": {"content": data['tempo_total']}}]}
        
        elif base == 'YOUTUBER':
            payload["properties"] = {
                "Nome do projeto": {"title": [{"text": {"content": data['title']}}]},
                "Status": {"status": {"name": data.get('status', 'Não iniciado')}}
            }
            
            if data.get('parent_id'):
                payload["properties"]["item principal"] = {"relation": [{"id": data['parent_id']}]}
            elif data.get('item_principal'):
                payload["properties"]["item principal"] = {"relation": [{"id": data['item_principal']}]}
            
            if data.get('periodo'):
                payload["properties"]["Periodo"] = {"date": data['periodo']}
            
            if data.get('data_lancamento'):
                payload["properties"]["Data de Lançamento"] = {"date": {"start": data['data_lancamento']}}
            
            if data.get('resumo_episodio'):
                payload["properties"]["Resumo do Episodio"] = {"rich_text": [{"text": {"content": data['resumo_episodio']}}]}
        
        return payload
