"""
Agente 4: Organizador YouTube

Funcionalidades:
- 48h antes do lançamento: Cria cards de Gravar, Editar e Upload
- Verifica se episódio foi gravado 24h antes
- Reorganiza cronograma se houver atrasos
- Diferencia: Data de Lançamento vs Período (quando gravar)

Base: YouTube
Horários: 21:00-23:30 (gravação)
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pytz
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.notion_client import NotionClient

load_dotenv()


class YouTubeOrganizer:
    """Organizador de Episódios YouTube"""
    
    def __init__(self):
        self.notion = NotionClient()
        self.youtube_db_id = os.getenv('YOUTUBER_DB_ID')
        self.sp_tz = pytz.timezone('America/Sao_Paulo')
    
    def get_upcoming_episodes(self, days_ahead: int = 3) -> List[Dict]:
        """Busca episódios com lançamento nos próximos X dias"""
        today = datetime.now(self.sp_tz)
        future_date = today + timedelta(days=days_ahead)
        
        filter_obj = {
            "and": [
                {
                    "property": "Data de Lançamento",
                    "date": {
                        "on_or_after": today.strftime('%Y-%m-%d')
                    }
                },
                {
                    "property": "Data de Lançamento",
                    "date": {
                        "on_or_before": future_date.strftime('%Y-%m-%d')
                    }
                },
                {
                    "property": "Status",
                    "status": {"equals": "Para Lançar"}
                }
            ]
        }
        
        return self.notion.query_database(self.youtube_db_id, filter_obj)
    
    def check_if_production_cards_exist(self, episode_id: str) -> Dict[str, bool]:
        """Verifica se cards de produção já foram criados"""
        # Buscar cards relacionados ao episódio
        filter_obj = {
            "property": "Série Principal",
            "relation": {"contains": episode_id}
        }
        
        related_cards = self.notion.query_database(self.youtube_db_id, filter_obj)
        
        exists = {
            'gravar': False,
            'editar': False,
            'upload': False
        }
        
        for card in related_cards:
            nome = card['properties']['Nome']['title'][0]['text']['content'].lower()
            
            if 'gravar' in nome:
                exists['gravar'] = True
            elif 'editar' in nome:
                exists['editar'] = True
            elif 'upload' in nome:
                exists['upload'] = True
        
        return exists
    
    def create_recording_card(self, episode: Dict, recording_date: datetime) -> Optional[str]:
        """Cria card de Gravação"""
        episode_title = episode['properties']['Nome']['title'][0]['text']['content']
        
        # Período de gravação: 21:00-23:30
        recording_start = recording_date.replace(hour=21, minute=0, second=0)
        recording_end = recording_date.replace(hour=23, minute=30, second=0)
        
        properties = {
            "Nome": {
                "title": [{"text": {"content": f"Gravar - {episode_title}"}}]
            },
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(recording_start, include_time=True),
                    "end": self.notion.format_date_gmt3(recording_end, include_time=True)
                }
            },
            "Status": {
                "status": {"name": "Para Gravar"}
            },
            "Série Principal": {
                "relation": [{"id": episode['id']}]
            }
        }
        
        card_id = self.notion.create_page(self.youtube_db_id, properties, icon="🎥")
        print(f"  ✅ Criado: Gravar - {episode_title} ({recording_start.date()} 21:00)")
        return card_id
    
    def create_editing_card(self, episode: Dict, editing_date: datetime) -> Optional[str]:
        """Cria card de Edição"""
        episode_title = episode['properties']['Nome']['title'][0]['text']['content']
        
        # Edição: Após gravação (21:30-23:30 ou dia seguinte)
        editing_start = editing_date.replace(hour=21, minute=30, second=0)
        editing_end = editing_date.replace(hour=23, minute=30, second=0)
        
        properties = {
            "Nome": {
                "title": [{"text": {"content": f"Editar - {episode_title}"}}]
            },
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(editing_start, include_time=True),
                    "end": self.notion.format_date_gmt3(editing_end, include_time=True)
                }
            },
            "Status": {
                "status": {"name": "Para Editar"}
            },
            "Série Principal": {
                "relation": [{"id": episode['id']}]
            }
        }
        
        card_id = self.notion.create_page(self.youtube_db_id, properties, icon="✂️")
        print(f"  ✅ Criado: Editar - {episode_title}")
        return card_id
    
    def create_upload_card(self, episode: Dict, launch_date: datetime) -> Optional[str]:
        """Cria card de Upload (2h antes do lançamento)"""
        episode_title = episode['properties']['Nome']['title'][0]['text']['content']
        
        # Upload: 2h antes do lançamento
        upload_time = launch_date - timedelta(hours=2)
        
        properties = {
            "Nome": {
                "title": [{"text": {"content": f"Upload - {episode_title}"}}]
            },
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(upload_time, include_time=True)
                }
            },
            "Status": {
                "status": {"name": "Para Publicar"}
            },
            "Série Principal": {
                "relation": [{"id": episode['id']}]
            }
        }
        
        card_id = self.notion.create_page(self.youtube_db_id, properties, icon="📤")
        print(f"  ✅ Criado: Upload - {episode_title}")
        return card_id
    
    def create_production_cards(self, episode: Dict):
        """Cria todos os cards de produção para um episódio"""
        launch_date_str = episode['properties']['Data de Lançamento']['date']['start']
        launch_date = datetime.fromisoformat(launch_date_str.replace('Z', '+00:00'))
        launch_date = launch_date.astimezone(self.sp_tz)
        
        episode_title = episode['properties']['Nome']['title'][0]['text']['content']
        
        # Verificar se já existem
        exists = self.check_if_production_cards_exist(episode['id'])
        
        if all(exists.values()):
            print(f"  ⏭️  Cards de produção já existem para: {episode_title}")
            return
        
        print(f"📺 Criando cards de produção para: {episode_title}")
        print(f"   Lançamento: {launch_date}")
        
        # Data de gravação: 2 dias antes do lançamento
        recording_date = launch_date - timedelta(days=2)
        
        # Pular finais de semana para gravação
        while recording_date.weekday() in [5, 6]:
            recording_date -= timedelta(days=1)
        
        # Criar cards
        if not exists['gravar']:
            self.create_recording_card(episode, recording_date)
        
        if not exists['editar']:
            # Edição no mesmo dia ou dia seguinte
            editing_date = recording_date + timedelta(days=1)
            self.create_editing_card(episode, editing_date)
        
        if not exists['upload']:
            self.create_upload_card(episode, launch_date)
        
        print()
    
    def check_recordings_status(self):
        """Verifica se episódios foram gravados 24h antes do lançamento"""
        print("\n🔍 Verificando status de gravações...\n")
        
        # Episódios que lançam amanhã
        tomorrow = datetime.now(self.sp_tz) + timedelta(days=1)
        
        filter_obj = {
            "and": [
                {
                    "property": "Data de Lançamento",
                    "date": {"equals": tomorrow.strftime('%Y-%m-%d')}
                },
                {
                    "property": "Status",
                    "status": {"equals": "Para Lançar"}
                }
            ]
        }
        
        episodes = self.notion.query_database(self.youtube_db_id, filter_obj)
        
        if not episodes:
            print("✅ Nenhum episódio lança amanhã")
            return
        
        for episode in episodes:
            title = episode['properties']['Nome']['title'][0]['text']['content']
            
            # Verificar se foi gravado
            exists = self.check_if_production_cards_exist(episode['id'])
            
            if not exists['gravar']:
                print(f"⚠️  ALERTA: {title} lança amanhã mas não tem card de gravação!")
            else:
                # Buscar status do card de gravação
                filter_gravar = {
                    "and": [
                        {
                            "property": "Nome",
                            "title": {"contains": f"Gravar - {title}"}
                        },
                        {
                            "property": "Série Principal",
                            "relation": {"contains": episode['id']}
                        }
                    ]
                }
                
                gravar_cards = self.notion.query_database(self.youtube_db_id, filter_gravar)
                
                if gravar_cards:
                    status = gravar_cards[0]['properties']['Status']['status']['name']
                    
                    if status != "Gravado":
                        print(f"🚨 CRÍTICO: {title} lança amanhã e ainda não foi gravado!")
                    else:
                        print(f"✅ {title} já foi gravado")
    
    def run(self, mode='create'):
        """
        Executa organizador
        
        Args:
            mode: 'create' para criar cards, 'check' para verificar status
        """
        print("🤖 Agent 4: Organizador YouTube")
        print(f"⏰ Timezone: GMT-3 (São Paulo)")
        print(f"📺 Base: YouTube\n")
        
        if mode == 'create':
            # Buscar episódios dos próximos 3 dias
            upcoming = self.get_upcoming_episodes(days_ahead=3)
            
            if not upcoming:
                print("✅ Nenhum episódio para lançar nos próximos 3 dias")
                return
            
            print(f"📋 Encontrados {len(upcoming)} episódio(s) próximo(s)\n")
            
            for episode in upcoming:
                self.create_production_cards(episode)
        
        elif mode == 'check':
            self.check_recordings_status()
        
        else:
            print(f"❌ Modo inválido: {mode}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Organizador YouTube')
    parser.add_argument('--mode', choices=['create', 'check'], default='create',
                        help='Modo de execução')
    
    args = parser.parse_args()
    
    agent = YouTubeOrganizer()
    agent.run(mode=args.mode)













