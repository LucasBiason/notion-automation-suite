#!/usr/bin/env python3
"""
Youtuber Cards Creator
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Criador de cards para projetos do YouTube.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from .notion_manager import NotionAPIManager, CardCreator, DatabaseType, TaskStatus, Priority
import logging

logger = logging.getLogger(__name__)

class YoutuberCardCreator(CardCreator):
    """Criador de cards para projetos do YouTube."""
    
    def __init__(self, notion_manager: NotionAPIManager):
        super().__init__(notion_manager)
        self.database_type = DatabaseType.YOUTUBER
    
    def create_metal_gear_solid_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para série Metal Gear Solid."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "Metal Gear Solid - Série Completa"
            ),
            "Status": self.create_status_property(TaskStatus.IN_PROGRESS),
            "Série": self.create_select_property("Metal Gear Solid"),
            "Episódio": self.create_rich_text_property("Em produção"),
            "Data de Gravação": self.create_date_property("2025-09-25"),
            "Data de Publicação": self.create_date_property("2025-09-30"),
            "Duração": self.create_rich_text_property("2h por episódio"),
            "Descrição": self.create_rich_text_property(
                "Série completa do Metal Gear Solid com comentários "
                "e ensinamentos sobre game design e storytelling."
            )
        }
        
        return self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🎮",
            cover=self.notion.get_default_cover("youtuber")
        )
    
    def create_pokemon_legends_za_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para série Pokémon Legends Z-A."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "Pokémon Legends Z-A - Série Completa"
            ),
            "Status": self.create_status_property(TaskStatus.TODO),
            "Série": self.create_select_property("Pokémon"),
            "Episódio": self.create_rich_text_property("A planejar"),
            "Data de Gravação": self.create_date_property("2025-10-01"),
            "Data de Publicação": self.create_date_property("2025-10-15"),
            "Duração": self.create_rich_text_property("1.5h por episódio"),
            "Descrição": self.create_rich_text_property(
                "Série do Pokémon Legends Z-A com foco em gameplay "
                "e análise de mecânicas do jogo."
            )
        }
        
        return self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🎮",
            cover=self.notion.get_default_cover("youtuber")
        )
    
    def create_ghost_of_tsushima_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para série Ghost of Tsushima."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "Ghost of Tsushima - Série Completa"
            ),
            "Status": self.create_status_property(TaskStatus.TODO),
            "Série": self.create_select_property("Ghost of Tsushima"),
            "Episódio": self.create_rich_text_property("A planejar"),
            "Data de Gravação": self.create_date_property("2025-10-10"),
            "Data de Publicação": self.create_date_property("2025-10-25"),
            "Duração": self.create_rich_text_property("2h por episódio"),
            "Descrição": self.create_rich_text_property(
                "Série do Ghost of Tsushima com foco em análise "
                "de arte, música e design de mundo."
            )
        }
        
        return self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🎮",
            cover=self.notion.get_default_cover("youtuber")
        )
    
    def create_organizacao_cronograma_card(self) -> Optional[Dict[str, Any]]:
        """Cria card para organização do cronograma."""
        properties = {
            "Nome do projeto": self.create_title_property(
                "Organização do Cronograma de Gravações"
            ),
            "Status": self.create_status_property(TaskStatus.IN_PROGRESS),
            "Série": self.create_select_property("Organização"),
            "Episódio": self.create_rich_text_property("N/A"),
            "Data de Gravação": self.create_date_property("2025-09-25"),
            "Data de Publicação": self.create_date_property("2025-09-30"),
            "Duração": self.create_rich_text_property("N/A"),
            "Descrição": self.create_rich_text_property(
                "Reorganizar cronograma de gravações para evitar "
                "sobreposição de projetos e otimizar tempo."
            )
        }
        
        return self.notion.create_page(
            self.database_type, 
            properties, 
            icon="🎮",
            cover=self.notion.get_default_cover("youtuber")
        )
    
    def create_all_youtuber_cards(self) -> Dict[str, Any]:
        """Cria todos os cards do YouTube."""
        results = {}
        
        logger.info("Criando cards do YouTube...")
        
        # Card Metal Gear Solid
        logger.info("Criando card: Metal Gear Solid...")
        mgs = self.create_metal_gear_solid_card()
        results["metal_gear_solid"] = mgs
        
        # Card Pokémon
        logger.info("Criando card: Pokémon Legends Z-A...")
        pokemon = self.create_pokemon_legends_za_card()
        results["pokemon"] = pokemon
        
        # Card Ghost of Tsushima
        logger.info("Criando card: Ghost of Tsushima...")
        ghost = self.create_ghost_of_tsushima_card()
        results["ghost_of_tsushima"] = ghost
        
        # Card organização
        logger.info("Criando card: Organização do Cronograma...")
        organizacao = self.create_organizacao_cronograma_card()
        results["organizacao"] = organizacao
        
        return results
