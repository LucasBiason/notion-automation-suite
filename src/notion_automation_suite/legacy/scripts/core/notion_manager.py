#!/usr/bin/env python3
"""
Notion Manager - Core Module
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Gerenciador principal para integração com Notion API.
Arquitetura limpa e modular para automação de projetos.
"""

import os
import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

# Configurar logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format=os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger = logging.getLogger(__name__)

class DatabaseType(Enum):
    """Tipos de databases disponíveis."""
    WORK = "work"
    STUDIES = "studies"
    PERSONAL = "personal"
    YOUTUBER = "youtuber"

class TaskStatus(Enum):
    """Status de tarefas."""
    TODO = "A Fazer"
    IN_PROGRESS = "Em Andamento"
    DONE = "Concluído"
    PAUSED = "Pausado"
    CANCELLED = "Cancelado"

class Priority(Enum):
    """Prioridades de tarefas."""
    LOW = "Baixa"
    MEDIUM = "Média"
    HIGH = "Alta"
    URGENT = "Urgente"

@dataclass
class NotionConfig:
    """Configuração centralizada do Notion."""
    api_token: str
    version: str
    timeout: int
    databases: Dict[DatabaseType, str]
    
    def __post_init__(self):
        if not self.api_token:
            raise ValueError("NOTION_API_TOKEN é obrigatório")
        
        if not self.databases:
            raise ValueError("Database IDs são obrigatórios")
    
    @classmethod
    def from_env(cls) -> 'NotionConfig':
        """Cria configuração a partir de variáveis de ambiente."""
        return cls(
            api_token=os.getenv('NOTION_API_TOKEN'),
            version=os.getenv('NOTION_API_VERSION', '2022-06-28'),
            timeout=int(os.getenv('REQUEST_TIMEOUT', '30')),
            databases={
                DatabaseType.WORK: os.getenv('NOTION_WORK_DATABASE_ID'),
                DatabaseType.STUDIES: os.getenv('NOTION_STUDIES_DATABASE_ID'),
                DatabaseType.PERSONAL: os.getenv('NOTION_PERSONAL_DATABASE_ID'),
                DatabaseType.YOUTUBER: os.getenv('NOTION_YOUTUBE_DATABASE_ID')
            }
        )
    
    def get_headers(self) -> Dict[str, str]:
        """Retorna headers para requisições."""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Notion-Version": self.version
        }

class NotionAPIError(Exception):
    """Exceção base para erros da API do Notion."""
    pass

class NotionAPIManager:
    """Gerenciador principal da API do Notion."""
    
    def __init__(self, config: NotionConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())
        self.base_url = "https://api.notion.com/v1"
    
    def test_connection(self) -> bool:
        """Testa conexão com Notion."""
        try:
            response = self.session.get(
                f"{self.base_url}/users/me",
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"Conectado como: {user_data.get('name', 'N/A')}")
                return True
            else:
                logger.error(f"Erro de conexão: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erro na conexão: {str(e)}")
            return False
    
    def create_page(self, database_type: DatabaseType, properties: Dict[str, Any], 
                   icon: str = None, cover: str = None) -> Optional[Dict[str, Any]]:
        """Cria uma página no database especificado."""
        try:
            database_id = self.config.databases.get(database_type)
            if not database_id:
                raise NotionAPIError(f"Database {database_type.value} não configurado")
            
            data = {
                "parent": {"database_id": database_id},
                "properties": properties
            }
            
            # Adicionar ícone se fornecido
            if icon:
                data["icon"] = {"emoji": icon}
            
            # Adicionar capa se fornecida
            if cover:
                data["cover"] = {
                    "type": "external",
                    "external": {"url": cover}
                }
            
            response = self.session.post(
                f"{self.base_url}/pages",
                json=data,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Página criada: {result['id']}")
                return result
            else:
                logger.error(f"Erro ao criar página: {response.status_code}")
                logger.error(f"Resposta: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na requisição: {str(e)}")
            return None
    
    def search_pages(self, query: str = "", database_type: DatabaseType = None) -> List[Dict[str, Any]]:
        """Busca páginas no Notion."""
        try:
            data = {
                "query": query,
                "page_size": 100
            }
            
            if database_type:
                database_id = self.config.databases.get(database_type)
                if database_id:
                    data["filter"] = {
                        "property": "object",
                        "value": "page"
                    }
            
            response = self.session.post(
                f"{self.base_url}/search",
                json=data,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("results", [])
            else:
                logger.error(f"Erro na busca: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Erro na busca: {str(e)}")
            return []
    
    def get_database(self, database_type: DatabaseType) -> Optional[Dict[str, Any]]:
        """Obtém informações de um database."""
        try:
            database_id = self.config.databases.get(database_type)
            if not database_id:
                raise NotionAPIError(f"Database {database_type.value} não configurado")
            
            response = self.session.get(
                f"{self.base_url}/databases/{database_id}",
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erro ao obter database: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na requisição: {str(e)}")
            return None
    
    def update_page(self, page_id: str, properties: Dict[str, Any]) -> bool:
        """Atualiza uma página existente."""
        try:
            data = {"properties": properties}
            
            response = self.session.patch(
                f"{self.base_url}/pages/{page_id}",
                json=data,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                logger.info(f"Página atualizada: {page_id}")
                return True
            else:
                logger.error(f"Erro ao atualizar página: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erro na requisição: {str(e)}")
            return False

    def create_card_with_subitems(self, database_type: DatabaseType, main_card_data: Dict[str, Any], 
                                   subitems: List[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Motor principal de criação de cards com subitems.
        
        Args:
            database_type: Tipo do database (WORK, PERSONAL, etc)
            main_card_data: {
                'title': str,
                'emoji': str,
                'status': str,
                'priority': str (opcional),
                'cliente': str (opcional - só Work),
                'projeto': str (opcional - só Work),
                'atividade': str (opcional - só Personal),
                'categorias': list (opcional - só Studies),
                'periodo': dict (opcional),
                'description': str (opcional)
            }
            subitems: Lista de dicts com mesma estrutura + 'parent_relation'
        
        Returns:
            Dict com 'main_card' e 'subitems' criados
        """
        try:
            # 1. Criar card principal
            main_card = self._build_card_payload(database_type, main_card_data, is_main=True)
            
            response = self.session.post(
                f"{self.base_url}/pages",
                json=main_card,
                timeout=self.config.timeout
            )
            
            if response.status_code != 200:
                logger.error(f"Erro ao criar card principal: {response.status_code}")
                logger.error(f"Resposta: {response.text}")
                return None
            
            main_result = response.json()
            main_card_id = main_result['id']
            logger.info(f"✅ Card principal criado: {main_card_data['title']} ({main_card_id})")
            
            # 2. Criar subitems se fornecidos
            created_subitems = []
            if subitems:
                logger.info(f"📋 Criando {len(subitems)} subitens...")
                
                for subitem_data in subitems:
                    # Adicionar referência ao parent
                    subitem_data['parent_id'] = main_card_id
                    
                    subitem_payload = self._build_card_payload(database_type, subitem_data, is_main=False)
                    
                    sub_response = self.session.post(
                        f"{self.base_url}/pages",
                        json=subitem_payload,
                        timeout=self.config.timeout
                    )
                    
                    if sub_response.status_code == 200:
                        subitem_result = sub_response.json()
                        created_subitems.append(subitem_result)
                        logger.info(f"   ✅ {subitem_data['title']}")
                    else:
                        logger.error(f"   ❌ {subitem_data['title']}: {sub_response.text}")
            
            return {
                'main_card': main_result,
                'subitems': created_subitems
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar card com subitens: {str(e)}")
            return None
    
    def _build_card_payload(self, database_type: DatabaseType, card_data: Dict[str, Any], 
                           is_main: bool = True) -> Dict[str, Any]:
        """
        Constrói payload completo para criação de card.
        Adapta automaticamente para cada tipo de database.
        """
        database_id = self.config.databases.get(database_type)
        if not database_id:
            raise NotionAPIError(f"Database {database_type.value} não configurado")
        
        payload = {
            "parent": {"database_id": database_id},
            "properties": {}
        }
        
        # Adicionar ícone
        if card_data.get('emoji'):
            payload["icon"] = {"emoji": card_data['emoji']}
        
        # CONSTRUIR PROPRIEDADES BASEADO NO TIPO DE DATABASE
        
        if database_type == DatabaseType.WORK:
            # Base TRABALHO
            payload["properties"] = {
                "Nome do projeto": {
                    "title": [{"text": {"content": card_data['title']}}]
                },
                "Status": {
                    "status": {"name": card_data.get('status', 'Não iniciado')}
                },
                "Cliente": {
                    "select": {"name": card_data.get('cliente', 'Pessoal')}
                },
                "Projeto": {
                    "select": {"name": card_data.get('projeto', 'Automação')}
                },
                "Prioridade": {
                    "select": {"name": card_data.get('priority', 'Média')}
                }
            }
            
            # Adicionar Sprint (relação) se for subitem
            if not is_main and card_data.get('parent_id'):
                payload["properties"]["Sprint"] = {
                    "relation": [{"id": card_data['parent_id']}]
                }
        
        elif database_type == DatabaseType.PERSONAL:
            # Base PESSOAL
            payload["properties"] = {
                "Nome da tarefa": {
                    "title": [{"text": {"content": card_data['title']}}]
                },
                "Status": {
                    "status": {"name": card_data.get('status', 'Não iniciado')}
                },
                "Atividade": {
                    "select": {"name": card_data.get('atividade', 'Desenvolvimento')}
                }
            }
            
            # Adicionar Subtarefa (relação) se for subitem
            if not is_main and card_data.get('parent_id'):
                payload["properties"]["Subtarefa"] = {
                    "relation": [{"id": card_data['parent_id']}]
                }
            
            # Adicionar Data se fornecida
            if card_data.get('data'):
                payload["properties"]["Data"] = {
                    "date": {"start": card_data['data']}
                }
        
        elif database_type == DatabaseType.STUDIES:
            # Base CURSOS/ESTUDOS
            payload["properties"] = {
                "Project name": {
                    "title": [{"text": {"content": card_data['title']}}]
                },
                "Status": {
                    "status": {"name": card_data.get('status', 'Para Fazer')}
                }
            }
            
            # Categorias
            if card_data.get('categorias'):
                payload["properties"]["Categorias"] = {
                    "multi_select": [{"name": cat} for cat in card_data['categorias']]
                }
            
            # Parent item (relação) se for subitem
            if not is_main and card_data.get('parent_id'):
                payload["properties"]["Parent item"] = {
                    "relation": [{"id": card_data['parent_id']}]
                }
            
            # Período
            if card_data.get('periodo'):
                payload["properties"]["Período"] = {
                    "date": card_data['periodo']
                }
            
            # Tempo Total
            if card_data.get('tempo_total'):
                payload["properties"]["Tempo Total"] = {
                    "rich_text": [{"text": {"content": card_data['tempo_total']}}]
                }
        
        elif database_type == DatabaseType.YOUTUBER:
            # Base YOUTUBE
            payload["properties"] = {
                "Nome": {
                    "title": [{"text": {"content": card_data['title']}}]
                },
                "Status": {
                    "status": {"name": card_data.get('status', 'Para Fazer')}
                }
            }
            
            # Período
            if card_data.get('periodo'):
                payload["properties"]["Período"] = {
                    "date": card_data['periodo']
                }
            
            # Data de Lançamento
            if card_data.get('data_lancamento'):
                payload["properties"]["Data de Lançamento"] = {
                    "date": {"start": card_data['data_lancamento']}
                }
        
        # Adicionar Descrição (comum a todos)
        if card_data.get('description'):
            payload["properties"]["Descrição"] = {
                "rich_text": [{"text": {"content": card_data['description']}}]
            }
        
        return payload

class CardCreator:
    """Classe base para criação de cards."""
    
    def __init__(self, notion_manager: NotionAPIManager):
        self.notion = notion_manager
    
    def create_title_property(self, title: str) -> Dict[str, Any]:
        """Cria propriedade de título."""
        return {
            "title": [{"text": {"content": title}}]
        }
    
    def create_select_property(self, value: str) -> Dict[str, Any]:
        """Cria propriedade de seleção."""
        return {
            "select": {"name": value}
        }
    
    def create_status_property(self, status: TaskStatus) -> Dict[str, Any]:
        """Cria propriedade de status."""
        return {
            "status": {"name": status.value}
        }
    
    def create_date_property(self, start_date: str, end_date: str = None) -> Dict[str, Any]:
        """Cria propriedade de data."""
        date_prop = {"start": start_date}
        if end_date:
            date_prop["end"] = end_date
        return {"date": date_prop}
    
    def create_rich_text_property(self, text: str) -> Dict[str, Any]:
        """Cria propriedade de texto rico."""
        return {
            "rich_text": [{"text": {"content": text}}]
        }
    
    def create_relation_property(self, page_id: str) -> Dict[str, Any]:
        """Cria propriedade de relação."""
        return {
            "relation": [{"id": page_id}]
        }
    
    def create_multi_relation_property(self, page_ids: List[str]) -> Dict[str, Any]:
        """Cria propriedade de relação múltipla."""
        return {
            "relation": [{"id": page_id} for page_id in page_ids]
        }
    
    def get_default_cover(self, card_type: str) -> str:
        """Retorna URL de capa padrão baseada no tipo de card."""
        covers = {
            "work": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&h=600&fit=crop",
            "studies": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1200&h=600&fit=crop",
            "personal": "https://images.unsplash.com/photo-1515378791036-0648a814c963?w=1200&h=600&fit=crop",
            "youtuber": "https://images.unsplash.com/photo-1611162616475-46b635cb6868?w=1200&h=600&fit=crop",
            "expenseiq": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop",
            "fiap": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&h=600&fit=crop",
            "testes": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&h=600&fit=crop",
            "documentacao": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1200&h=600&fit=crop"
        }
        return covers.get(card_type.lower(), covers["work"])
