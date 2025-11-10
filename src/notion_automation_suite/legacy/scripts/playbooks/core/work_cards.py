#!/usr/bin/env python3
"""
Work Cards Creator
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Criador de cards para projetos de trabalho.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from .notion_manager import NotionAPIManager, CardCreator, DatabaseType, TaskStatus, Priority
import logging

logger = logging.getLogger(__name__)

class WorkCardCreator(CardCreator):
    """Criador de cards para projetos de trabalho."""
    
    def __init__(self, notion_manager: NotionAPIManager):
        super().__init__(notion_manager)
        self.database_type = DatabaseType.WORK
    
    def create_expenseiq_campo_number_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para feature Campo Number do ExpenseIQ."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "ExpenseIQ - Feature Campo Number para Agente IA"
            ),
            "Cliente": self.create_select_property("Astracode"),
            "Projeto": self.create_select_property("Expense IQ"),
            "Status": self.create_status_property(TaskStatus.DONE),
            "Prioridade": self.create_select_property(Priority.HIGH.value),
            "Periodo": self.create_date_property("2025-09-20", "2025-09-25"),
            "item principal": self.create_relation_property("24e962a7-693c-801e-aaca-d17f17960378")
        }
        
        # Criar página com ícone
        result = self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🔢"
        )
        
        return result
    
    def create_advance_number_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para implementação do campo Number no Advance Service."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "ExpenseIQ - Implementação Campo Number: Advance Service"
            ),
            "Cliente": self.create_select_property("Astracode"),
            "Projeto": self.create_select_property("Expense IQ"),
            "Status": self.create_status_property(TaskStatus.IN_PROGRESS),
            "Prioridade": self.create_select_property(Priority.HIGH.value),
            "Periodo": self.create_date_property("2025-09-26", "2025-09-27"),
            "item principal": self.create_relation_property("24e962a7-693c-801e-aaca-d17f17960378")
        }
        
        # Criar página com ícone
        result = self.notion.create_page(
            self.database_type, 
            properties, 
            icon="💰"
        )
        
        return result
    
    def create_expenseiq_testes_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para revisão de testes do ExpenseIQ."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "ExpenseIQ - Revisão de Testes Unitários"
            ),
            "Cliente": self.create_select_property("Astracode"),
            "Projeto": self.create_select_property("Expense IQ"),
            "Status": self.create_status_property(TaskStatus.IN_PROGRESS),
            "Prioridade": self.create_select_property(Priority.HIGH.value),
            "Periodo": self.create_date_property("2025-09-25", "2025-09-30"),
            "item principal": self.create_relation_property("24e962a7-693c-801e-aaca-d17f17960378")
        }
        
        # Criar página com ícone
        result = self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🧪"
        )
        
        return result
    
    def create_expenseiq_documentacao_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para documentação unificada do ExpenseIQ."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "ExpenseIQ - Documentação Unificada API"
            ),
            "Cliente": self.create_select_property("Astracode"),
            "Projeto": self.create_select_property("Expense IQ"),
            "Status": self.create_status_property(TaskStatus.IN_PROGRESS),
            "Prioridade": self.create_select_property(Priority.MEDIUM.value),
            "Periodo": self.create_date_property("2025-09-25", "2025-10-05"),
            "item principal": self.create_relation_property("24e962a7-693c-801e-aaca-d17f17960378")
        }
        
        # Criar página com ícone
        result = self.notion.create_page(
            self.database_type, 
            properties, 
            icon="📚"
        )
        
        return result
    
    def create_subitem_card(self, title: str, parent_id: str, icon: str = None, 
                           status: TaskStatus = TaskStatus.TODO, 
                           priority: Priority = Priority.MEDIUM,
                           cover_type: str = "expenseiq") -> Optional[Dict[str, Any]]:
        """Cria um subitem genérico relacionado a um card principal."""
        properties = {
            "Nome do projeto": self.create_title_property(title),
            "Cliente": self.create_select_property("Astracode"),
            "Projeto": self.create_select_property("Expense IQ"),
            "Status": self.create_status_property(status),
            "Prioridade": self.create_select_property(priority.value),
            "item principal": self.create_relation_property(parent_id)
        }
        
        # Definir ícone padrão se não fornecido
        if not icon:
            icon = "📋"
        
        # Criar página com ícone
        result = self.notion.create_page(
            self.database_type, 
            properties, 
            icon=icon
        )
        
        return result
    
    def create_all_expenseiq_cards(self) -> Dict[str, Any]:
        """Cria todos os cards do ExpenseIQ."""
        results = {}
        
        logger.info("Criando cards do ExpenseIQ...")
        
        # Card principal - Campo Number
        logger.info("Criando card: Feature Campo Number...")
        campo_number = self.create_expenseiq_campo_number_card()
        results["campo_number"] = campo_number
        
        # Card de testes
        logger.info("Criando card: Testes Unitários...")
        testes = self.create_expenseiq_testes_card()
        results["testes"] = testes
        
        # Card de documentação
        logger.info("Criando card: Documentação Unificada...")
        documentacao = self.create_expenseiq_documentacao_card()
        results["documentacao"] = documentacao
        
        # Card Advance Number
        logger.info("Criando card: Advance Number...")
        advance_number = self.create_advance_number_card()
        results["advance_number"] = advance_number
        
        return results
    
