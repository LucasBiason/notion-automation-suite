#!/usr/bin/env python3
"""
Script para corrigir as datas de lançamento de The Legend of Heroes
A partir do episódio 13, um episódio por dia às 12:00 a partir de segunda-feira
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from core.notion_manager import NotionAPIManager, NotionConfig, DatabaseType
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrailsDateFixer:
    """Classe para corrigir as datas de The Legend of Heroes."""
    
    def __init__(self, notion_manager: NotionAPIManager):
        self.notion = notion_manager
        
    def get_related_pages(self, main_page_id: str) -> List[Dict[str, Any]]:
        """Obtém todas as páginas relacionadas através da propriedade 'item principal'."""
        try:
            database_id = self.notion.config.databases.get(DatabaseType.YOUTUBER)
            if not database_id:
                logger.error("Database do YouTube não configurado")
                return []
            
            query_data = {
                "filter": {
                    "property": "item principal",
                    "relation": {
                        "contains": main_page_id
                    }
                }
            }
            
            response = self.notion.session.post(
                f"{self.notion.base_url}/databases/{database_id}/query",
                json=query_data,
                timeout=self.notion.config.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            else:
                logger.error(f"Erro ao buscar páginas relacionadas: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Erro ao buscar páginas relacionadas: {e}")
            return []
    
    def update_page_properties(self, page_id: str, properties: Dict[str, Any]) -> bool:
        """Atualiza as propriedades de uma página."""
        try:
            response = self.notion.session.patch(
                f"{self.notion.base_url}/pages/{page_id}",
                json={"properties": properties},
                timeout=self.notion.config.timeout
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Erro ao atualizar página {page_id}: {e}")
            return False
    
    def extract_episode_number(self, title: str) -> int:
        """Extrai o número do episódio do título."""
        try:
            if 'Episódio' in title:
                parts = title.split('Episódio')[1].strip()
                return int(parts.split()[0])
            return 0
        except (ValueError, IndexError):
            return 0
    
    def get_start_date(self) -> datetime:
        """Obtém a data de início: 29/09/2025 no fuso horário de São Paulo (GMT-3)."""
        # Criar timezone de São Paulo (GMT-3)
        sao_paulo_tz = timezone(timedelta(hours=-3))
        return datetime(2025, 9, 29, tzinfo=sao_paulo_tz)  # 29/09/2025 GMT-3
    
    def fix_trails_dates(self, page_id: str) -> bool:
        """Corrige as datas de lançamento de The Legend of Heroes."""
        logger.info("Corrigindo datas de The Legend of Heroes...")
        
        related_pages = self.get_related_pages(page_id)
        if not related_pages:
            logger.error("Nenhuma página relacionada encontrada para The Legend of Heroes")
            return False
        
        # Filtrar apenas episódios 13 em diante
        episodes_13_plus = []
        for page in related_pages:
            properties = page.get('properties', {})
            title_prop = properties.get('Nome do projeto', {})
            if title_prop:
                title = title_prop.get('title', [{}])[0].get('text', {}).get('content', '')
                episode_num = self.extract_episode_number(title)
                if episode_num >= 13:
                    episodes_13_plus.append((page, episode_num, title))
        
        # Ordenar por número do episódio
        episodes_13_plus.sort(key=lambda x: x[1])
        
        if not episodes_13_plus:
            logger.error("Nenhum episódio 13+ encontrado")
            return False
        
        # Calcular datas a partir de 29/09/2025
        start_date = self.get_start_date()
        logger.info(f"Data de início: {start_date.strftime('%d/%m/%Y')}")
        
        success_count = 0
        for i, (page, episode_num, title) in enumerate(episodes_13_plus):
            # Calcular data de lançamento (um episódio por dia às 12:00 GMT-3)
            release_date = start_date + timedelta(days=i)
            release_date = release_date.replace(hour=12, minute=0, second=0, microsecond=0)
            
            # Converter para UTC para o Notion (GMT-3 + 3 = UTC)
            release_date_utc = release_date.astimezone(timezone.utc)
            release_date_str = release_date_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            
            properties_update = {
                "Data de Lançamento": {
                    "date": {
                        "start": release_date_str
                    }
                }
            }
            
            if self.update_page_properties(page['id'], properties_update):
                success_count += 1
                logger.info(f"Episódio {episode_num}: {release_date.strftime('%d/%m/%Y %H:%M')} GMT-3")
            else:
                logger.error(f"Falha ao atualizar episódio {episode_num}")
        
        logger.info(f"The Legend of Heroes: {success_count} episódios corrigidos")
        return success_count > 0
    
    def fix_silent_hill_dates(self, page_id: str) -> bool:
        """Corrige as datas de lançamento de Silent Hill F."""
        logger.info("Corrigindo datas de Silent Hill F...")
        
        related_pages = self.get_related_pages(page_id)
        if not related_pages:
            logger.error("Nenhuma página relacionada encontrada para Silent Hill F")
            return False
        
        # Filtrar apenas episódios 8 em diante
        episodes_8_plus = []
        for page in related_pages:
            properties = page.get('properties', {})
            title_prop = properties.get('Nome do projeto', {})
            if title_prop:
                title = title_prop.get('title', [{}])[0].get('text', {}).get('content', '')
                episode_num = self.extract_episode_number(title)
                if episode_num >= 8:
                    episodes_8_plus.append((page, episode_num, title))
        
        # Ordenar por número do episódio
        episodes_8_plus.sort(key=lambda x: x[1])
        
        if not episodes_8_plus:
            logger.error("Nenhum episódio 8+ encontrado")
            return False
        
        # Calcular datas a partir de 29/09/2025
        start_date = self.get_start_date()
        logger.info(f"Data de início: {start_date.strftime('%d/%m/%Y')}")
        
        success_count = 0
        for i, (page, episode_num, title) in enumerate(episodes_8_plus):
            # Calcular data de lançamento (um episódio por dia às 18:00 GMT-3)
            release_date = start_date + timedelta(days=i)
            release_date = release_date.replace(hour=18, minute=0, second=0, microsecond=0)
            
            # Converter para UTC para o Notion (GMT-3 + 3 = UTC)
            release_date_utc = release_date.astimezone(timezone.utc)
            release_date_str = release_date_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            
            properties_update = {
                "Data de Lançamento": {
                    "date": {
                        "start": release_date_str
                    }
                }
            }
            
            if self.update_page_properties(page['id'], properties_update):
                success_count += 1
                logger.info(f"Episódio {episode_num}: {release_date.strftime('%d/%m/%Y %H:%M')} GMT-3")
            else:
                logger.error(f"Falha ao atualizar episódio {episode_num}")
        
        logger.info(f"Silent Hill F: {success_count} episódios corrigidos")
        return success_count > 0

def main():
    """Função principal para corrigir as datas."""
    print("=" * 60)
    print("🔧 CORRIGINDO DATAS DAS SÉRIES")
    print("=" * 60)
    
    try:
        # Carregar configuração
        config = NotionConfig.from_env()
        
        # Inicializar Notion Manager
        notion = NotionAPIManager(config)
        
        # Testar conexão
        if not notion.test_connection():
            print("❌ Falha na conexão com Notion")
            return False
        
        # Criar fixer
        fixer = TrailsDateFixer(notion)
        
        # IDs das páginas principais
        pages = {
            "The Legend of Heroes": "253962a7693c81d2b9d1f636fd4879a9",
            "Silent Hill F": "276962a7693c81228b6ade3fb06dda45"
        }
        
        results = {}
        
        # Corrigir The Legend of Heroes
        print("\n📺 Corrigindo The Legend of Heroes...")
        results["The Legend of Heroes"] = fixer.fix_trails_dates(pages["The Legend of Heroes"])
        
        # Corrigir Silent Hill F
        print("\n📺 Corrigindo Silent Hill F...")
        results["Silent Hill F"] = fixer.fix_silent_hill_dates(pages["Silent Hill F"])
        
        # Mostrar resultados
        print("\n" + "=" * 60)
        print("📊 RESULTADOS DA CORREÇÃO:")
        print("=" * 60)
        
        for series_name, success in results.items():
            status = "✅ Sucesso" if success else "❌ Falha"
            print(f"{status} - {series_name}")
        
        success_count = sum(results.values())
        total_series = len(results)
        
        if success_count == total_series:
            print("\n✅ Todas as datas foram corrigidas com sucesso!")
            print("📅 Cronograma: A partir de 29/09/2025, um episódio por dia (GMT-3 - São Paulo)")
            print("   - The Legend of Heroes: 12:00 GMT-3")
            print("   - Silent Hill F: 18:00 GMT-3")
        else:
            print(f"\n⚠️ {success_count}/{total_series} séries corrigidas")
        
        return success_count == total_series
        
    except Exception as e:
        logger.error(f"Erro na execução: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
