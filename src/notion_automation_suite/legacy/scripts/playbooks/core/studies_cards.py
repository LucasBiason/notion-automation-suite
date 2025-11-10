#!/usr/bin/env python3
"""
Studies Cards Creator
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Criador de cards para projetos de estudos.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from .notion_manager import NotionAPIManager, CardCreator, DatabaseType, TaskStatus, Priority
import logging

logger = logging.getLogger(__name__)

class StudiesCardCreator(CardCreator):
    """Criador de cards para projetos de estudos."""
    
    def __init__(self, notion_manager: NotionAPIManager):
        super().__init__(notion_manager)
        self.database_type = DatabaseType.STUDIES
    
    def create_fiap_fine_tuning_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para projeto Fine Tuning FIAP."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "FIAP - Fine Tuning Tech Challenge Fase 3"
            ),
            "Status": self.create_status_property(TaskStatus.DONE),
            "Prioridade": self.create_select_property(Priority.URGENT.value),
            "Periodo": self.create_date_property("2025-09-15", "2025-09-25"),
            "Tipo": self.create_select_property("FIAP")
        }
        
        # Criar página com ícone e capa
        result = self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🤖",
            cover=self.notion.get_default_cover("fiap")
        )
        
        return result
    
    def create_ia_knowledge_base_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para base de conhecimento IA."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "IA Knowledge Base - Construção de Base de Conhecimento"
            ),
            "Status": self.create_status_property(TaskStatus.IN_PROGRESS),
            "Prioridade": self.create_select_property(Priority.MEDIUM.value),
            "Periodo": self.create_date_property("2025-09-01", "2025-12-31"),
            "Tipo": self.create_select_property("Pessoal")
        }
        
        # Criar página com ícone e capa
        result = self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🧠",
            cover=self.notion.get_default_cover("studies")
        )
        
        return result
    
    def create_fiap_fase4_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para Fase 4 do FIAP."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "FIAP - Fase 4 - Aulas e Projetos"
            ),
            "Status": self.create_status_property(TaskStatus.TODO),
            "Prioridade": self.create_select_property(Priority.HIGH.value),
            "Periodo": self.create_date_property("2025-10-01", "2025-11-30"),
            "Tipo": self.create_select_property("FIAP")
        }
        
        # Criar página com ícone e capa
        result = self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🎓",
            cover=self.notion.get_default_cover("fiap")
        )
        
        return result
    
    def create_all_studies_cards(self) -> Dict[str, Any]:
        """Cria todos os cards de estudos."""
        results = {}
        
        logger.info("Criando cards de estudos...")
        
        # Card Fine Tuning
        logger.info("Criando card: Fine Tuning FIAP...")
        fine_tuning = self.create_fiap_fine_tuning_card()
        results["fine_tuning"] = fine_tuning
        
        # Card IA Knowledge Base
        logger.info("Criando card: IA Knowledge Base...")
        ia_kb = self.create_ia_knowledge_base_card()
        results["ia_knowledge_base"] = ia_kb
        
        # Card Fase 4
        logger.info("Criando card: FIAP Fase 4...")
        fase4 = self.create_fiap_fase4_card()
        results["fase4"] = fase4
        
        return results
