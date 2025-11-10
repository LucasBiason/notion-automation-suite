#!/usr/bin/env python3
"""
Script para Reorganizar Cronograma das Séries do YouTube
Versão: 1.0
Data: 27/01/2025
Status: Ativo

Script para reorganizar o cronograma das séries do YouTube no Notion:
- The Legend of Heroes: Trails in the Sky FC - horário 12:00 a partir do episódio 13
- Ghost of Yōtei - horário 15:00, intercalado com Digimon
- Digimon Story: Time Stranger - horário 15:00, intercalado com Ghost of Yōtei
- Silent Hill F - horário 18:00 a partir do episódio 8
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from core.notion_manager import NotionAPIManager, NotionConfig
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeriesScheduler:
    """Classe para reorganizar o cronograma das séries do YouTube."""
    
    def __init__(self, notion_manager: NotionAPIManager):
        self.notion = notion_manager
        
    def get_page_children(self, page_id: str) -> List[Dict[str, Any]]:
        """Obtém todos os subitens de uma página."""
        try:
            response = self.notion.session.get(
                f"{self.notion.base_url}/blocks/{page_id}/children",
                timeout=self.notion.config.timeout
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            else:
                logger.error(f"Erro ao obter subitens: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Erro ao obter subitens da página {page_id}: {e}")
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
    
    def update_legend_of_heroes_schedule(self, page_id: str) -> bool:
        """Atualiza o cronograma de The Legend of Heroes: Trails in the Sky FC."""
        logger.info("Atualizando cronograma de The Legend of Heroes...")
        
        children = self.get_page_children(page_id)
        if not children:
            logger.error("Nenhum subitem encontrado para The Legend of Heroes")
            return False
        
        success_count = 0
        for child in children:
            if child.get('type') == 'child_page':
                child_id = child['id']
                child_title = child.get('child_page', {}).get('title', '')
                
                # Verificar se é a partir do episódio 13
                if 'Episódio' in child_title:
                    try:
                        # Extrair número do episódio
                        episode_num = int(child_title.split('Episódio')[1].split()[0])
                        if episode_num >= 13:
                            # Atualizar para 12:00
                            properties = {
                                "Data de Lançamento": {
                                    "date": {
                                        "start": "2025-01-27T12:00:00.000Z"  # Será ajustado com data real
                                    }
                                }
                            }
                            
                            if self.update_page_properties(child_id, properties):
                                success_count += 1
                                logger.info(f"Atualizado {child_title} para 12:00")
                    except (ValueError, IndexError):
                        logger.warning(f"Não foi possível extrair número do episódio de {child_title}")
        
        logger.info(f"The Legend of Heroes: {success_count} episódios atualizados")
        return success_count > 0
    
    def create_interleaved_schedule(self, ghost_start: str, digimon_start: str) -> List[Dict[str, str]]:
        """Cria cronograma intercalado para Ghost of Yōtei e Digimon."""
        ghost_date = datetime.strptime(ghost_start, "%d/%m/%Y")
        digimon_date = datetime.strptime(digimon_start, "%d/%m/%Y")
        
        schedule = []
        current_date = ghost_date
        
        # Intercalar por 30 dias (aproximadamente 1 mês)
        for i in range(20):  # 20 episódios para cada série
            if i % 2 == 0:  # Ghost of Yōtei
                schedule.append({
                    "series": "Ghost of Yōtei",
                    "episode": (i // 2) + 1,
                    "date": current_date.strftime("%Y-%m-%d"),
                    "time": "15:00"
                })
            else:  # Digimon
                schedule.append({
                    "series": "Digimon",
                    "episode": (i // 2) + 1,
                    "date": current_date.strftime("%Y-%m-%d"),
                    "time": "15:00"
                })
            
            current_date += timedelta(days=1)
        
        return schedule
    
    def update_ghost_of_yotei_schedule(self, page_id: str) -> bool:
        """Atualiza o cronograma de Ghost of Yōtei."""
        logger.info("Atualizando cronograma de Ghost of Yōtei...")
        
        children = self.get_page_children(page_id)
        if not children:
            logger.error("Nenhum subitem encontrado para Ghost of Yōtei")
            return False
        
        # Criar cronograma intercalado
        schedule = self.create_interleaved_schedule("02/10/2025", "03/10/2025")
        ghost_schedule = [s for s in schedule if s["series"] == "Ghost of Yōtei"]
        
        success_count = 0
        for i, child in enumerate(children):
            if child.get('type') == 'child_page':
                child_id = child['id']
                child_title = child.get('child_page', {}).get('title', '')
                
                if 'Episódio' in child_title:
                    try:
                        episode_num = int(child_title.split('Episódio')[1].split()[0])
                        if episode_num <= len(ghost_schedule):
                            schedule_item = ghost_schedule[episode_num - 1]
                            
                            # Definir período baseado no episódio
                            if episode_num == 1:
                                # Episódio 1: 7:00 às 9:00
                                start_time = f"{schedule_item['date']}T07:00:00.000Z"
                                end_time = f"{schedule_item['date']}T09:00:00.000Z"
                            else:
                                # Outros episódios: 21:00 às 23:50 do dia anterior
                                prev_date = datetime.strptime(schedule_item['date'], "%Y-%m-%d") - timedelta(days=1)
                                start_time = f"{prev_date.strftime('%Y-%m-%d')}T21:00:00.000Z"
                                end_time = f"{prev_date.strftime('%Y-%m-%d')}T23:50:00.000Z"
                            
                            properties = {
                                "Data de Lançamento": {
                                    "date": {
                                        "start": f"{schedule_item['date']}T{schedule_item['time']}:00.000Z"
                                    }
                                },
                                "Período": {
                                    "date": {
                                        "start": start_time,
                                        "end": end_time
                                    }
                                }
                            }
                            
                            if self.update_page_properties(child_id, properties):
                                success_count += 1
                                logger.info(f"Atualizado {child_title} para {schedule_item['date']} {schedule_item['time']}")
                    except (ValueError, IndexError):
                        logger.warning(f"Não foi possível extrair número do episódio de {child_title}")
        
        logger.info(f"Ghost of Yōtei: {success_count} episódios atualizados")
        return success_count > 0
    
    def update_digimon_schedule(self, page_id: str) -> bool:
        """Atualiza o cronograma de Digimon Story: Time Stranger."""
        logger.info("Atualizando cronograma de Digimon...")
        
        children = self.get_page_children(page_id)
        if not children:
            logger.error("Nenhum subitem encontrado para Digimon")
            return False
        
        # Criar cronograma intercalado
        schedule = self.create_interleaved_schedule("02/10/2025", "03/10/2025")
        digimon_schedule = [s for s in schedule if s["series"] == "Digimon"]
        
        success_count = 0
        for i, child in enumerate(children):
            if child.get('type') == 'child_page':
                child_id = child['id']
                child_title = child.get('child_page', {}).get('title', '')
                
                if 'Episódio' in child_title:
                    try:
                        episode_num = int(child_title.split('Episódio')[1].split()[0])
                        if episode_num <= len(digimon_schedule):
                            schedule_item = digimon_schedule[episode_num - 1]
                            
                            # Definir período baseado no episódio
                            if episode_num == 2:  # Episódio 2 mantém o dia mas 7:00 às 9:00
                                start_time = f"{schedule_item['date']}T07:00:00.000Z"
                                end_time = f"{schedule_item['date']}T09:00:00.000Z"
                            else:
                                # Outros episódios: 21:00 às 23:50 do dia anterior
                                prev_date = datetime.strptime(schedule_item['date'], "%Y-%m-%d") - timedelta(days=1)
                                start_time = f"{prev_date.strftime('%Y-%m-%d')}T21:00:00.000Z"
                                end_time = f"{prev_date.strftime('%Y-%m-%d')}T23:50:00.000Z"
                            
                            properties = {
                                "Data de Lançamento": {
                                    "date": {
                                        "start": f"{schedule_item['date']}T{schedule_item['time']}:00.000Z"
                                    }
                                },
                                "Período": {
                                    "date": {
                                        "start": start_time,
                                        "end": end_time
                                    }
                                }
                            }
                            
                            if self.update_page_properties(child_id, properties):
                                success_count += 1
                                logger.info(f"Atualizado {child_title} para {schedule_item['date']} {schedule_item['time']}")
                    except (ValueError, IndexError):
                        logger.warning(f"Não foi possível extrair número do episódio de {child_title}")
        
        logger.info(f"Digimon: {success_count} episódios atualizados")
        return success_count > 0
    
    def update_silent_hill_schedule(self, page_id: str) -> bool:
        """Atualiza o cronograma de Silent Hill F."""
        logger.info("Atualizando cronograma de Silent Hill F...")
        
        children = self.get_page_children(page_id)
        if not children:
            logger.error("Nenhum subitem encontrado para Silent Hill F")
            return False
        
        success_count = 0
        for child in children:
            if child.get('type') == 'child_page':
                child_id = child['id']
                child_title = child.get('child_page', {}).get('title', '')
                
                if 'Episódio' in child_title:
                    try:
                        episode_num = int(child_title.split('Episódio')[1].split()[0])
                        if episode_num >= 8:
                            # Atualizar para 18:00
                            properties = {
                                "Data de Lançamento": {
                                    "date": {
                                        "start": "2025-01-27T18:00:00.000Z"  # Será ajustado com data real
                                    }
                                }
                            }
                            
                            if self.update_page_properties(child_id, properties):
                                success_count += 1
                                logger.info(f"Atualizado {child_title} para 18:00")
                    except (ValueError, IndexError):
                        logger.warning(f"Não foi possível extrair número do episódio de {child_title}")
        
        logger.info(f"Silent Hill F: {success_count} episódios atualizados")
        return success_count > 0

def main():
    """Função principal para reorganizar as séries."""
    print("=" * 60)
    print("🎬 REORGANIZANDO CRONOGRAMA DAS SÉRIES DO YOUTUBE")
    print("=" * 60)
    
    try:
        # Carregar configuração
        config = NotionConfig.from_env()
        
        # Inicializar Notion Manager
        notion = NotionAPIManager(config)
        
        # Criar scheduler
        scheduler = SeriesScheduler(notion)
        
        # URLs das páginas
        pages = {
            "The Legend of Heroes": "253962a7693c81d2b9d1f636fd4879a9",
            "Ghost of Yōtei": "253962a7693c81aeb8f5d5e4e32a19ad",
            "Digimon Story": "26e962a7693c80fc8f0bd8f6b9aaf282",
            "Silent Hill F": "276962a7693c81228b6ade3fb06dda45"
        }
        
        results = {}
        
        # Atualizar cada série
        for series_name, page_id in pages.items():
            print(f"\n📺 Processando {series_name}...")
            
            if series_name == "The Legend of Heroes":
                results[series_name] = scheduler.update_legend_of_heroes_schedule(page_id)
            elif series_name == "Ghost of Yōtei":
                results[series_name] = scheduler.update_ghost_of_yotei_schedule(page_id)
            elif series_name == "Digimon Story":
                results[series_name] = scheduler.update_digimon_schedule(page_id)
            elif series_name == "Silent Hill F":
                results[series_name] = scheduler.update_silent_hill_schedule(page_id)
        
        # Mostrar resultados
        print("\n" + "=" * 60)
        print("📊 RESULTADOS DA REORGANIZAÇÃO:")
        print("=" * 60)
        
        for series_name, success in results.items():
            status = "✅ Sucesso" if success else "❌ Falha"
            print(f"{status} - {series_name}")
        
        success_count = sum(results.values())
        total_series = len(results)
        
        print(f"\n🎉 Processo concluído! {success_count}/{total_series} séries reorganizadas com sucesso")
        
        return success_count == total_series
        
    except Exception as e:
        logger.error(f"Erro na execução: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
