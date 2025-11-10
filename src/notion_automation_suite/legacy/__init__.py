"""
Core Module - Notion Projects
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Módulo principal para integração com Notion API.
"""

from .notion_manager import (
    NotionAPIManager,
    NotionConfig,
    DatabaseType,
    TaskStatus,
    Priority,
    NotionAPIError
)

from .work_cards import WorkCardCreator
from .studies_cards import StudiesCardCreator
from .personal_cards import PersonalCardCreator
from .youtuber_cards import YoutuberCardCreator

__all__ = [
    'NotionAPIManager',
    'NotionConfig',
    'DatabaseType',
    'TaskStatus',
    'Priority',
    'NotionAPIError',
    'WorkCardCreator',
    'StudiesCardCreator',
    'PersonalCardCreator',
    'YoutuberCardCreator'
]
