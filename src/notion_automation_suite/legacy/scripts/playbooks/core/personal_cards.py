#!/usr/bin/env python3
"""
Personal Cards Creator
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Criador de cards para tarefas pessoais.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from .notion_manager import NotionAPIManager, CardCreator, DatabaseType, TaskStatus, Priority
import logging

logger = logging.getLogger(__name__)

class PersonalCardCreator(CardCreator):
    """Criador de cards para tarefas pessoais."""
    
    def __init__(self, notion_manager: NotionAPIManager):
        super().__init__(notion_manager)
        self.database_type = DatabaseType.PERSONAL
    
    def create_organizacao_projetos_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para organização de projetos."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "Organização de Projetos e Estrutura"
            ),
            "Status": self.create_status_property(TaskStatus.IN_PROGRESS),
            "Prioridade": self.create_select_property(Priority.HIGH.value),
            "Data de Vencimento": self.create_date_property("2025-09-30"),
            "Categoria": self.create_select_property("Organização"),
            "Descrição": self.create_rich_text_property(
                "Reorganizar estrutura de projetos, limpar Limbo dos Projetos "
                "e implementar sistema unificado de gestão."
            )
        }
        
        return self.notion.create_page(
            self.database_type, 
            properties, 
            icon="📁",
            cover=self.notion.get_default_cover("personal")
        )
    
    def create_limpeza_limbo_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para limpeza do Limbo dos Projetos."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "Limpeza do Limbo dos Projetos"
            ),
            "Status": self.create_status_property(TaskStatus.TODO),
            "Prioridade": self.create_select_property(Priority.MEDIUM.value),
            "Data de Vencimento": self.create_date_property("2025-10-15"),
            "Categoria": self.create_select_property("Organização"),
            "Descrição": self.create_rich_text_property(
                "Eliminar projetos desnecessários do Limbo dos Projetos "
                "e organizar arquivos importantes."
            )
        }
        
        return self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🧹",
            cover=self.notion.get_default_cover("personal")
        )
    
    def create_sistema_contexto_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para sistema de controle de contexto."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "Sistema de Controle de Contexto"
            ),
            "Status": self.create_status_property(TaskStatus.TODO),
            "Prioridade": self.create_select_property(Priority.MEDIUM.value),
            "Data de Vencimento": self.create_date_property("2025-10-10"),
            "Categoria": self.create_select_property("Desenvolvimento"),
            "Descrição": self.create_rich_text_property(
                "Criar sistema para controle de contexto e andamento "
                "para treinamento de assistentes de IA."
            )
        }
        
        return self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🤖",
            cover=self.notion.get_default_cover("personal")
        )
    
    def create_all_personal_cards(self) -> Dict[str, Any]:
        """Cria todos os cards pessoais."""
        results = {}
        
        logger.info("Criando cards pessoais...")
        
        # Card organização
        logger.info("Criando card: Organização de Projetos...")
        organizacao = self.create_organizacao_projetos_card()
        results["organizacao"] = organizacao
        
        # Card limpeza
        logger.info("Criando card: Limpeza do Limbo...")
        limpeza = self.create_limpeza_limbo_card()
        results["limpeza"] = limpeza
        
        # Card sistema contexto
        logger.info("Criando card: Sistema de Contexto...")
        contexto = self.create_sistema_contexto_card()
        results["contexto"] = contexto
        
        return results
