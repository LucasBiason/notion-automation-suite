"""
Agente 3: Finalizador Semanal

Responsável por:
- Segunda 07:00: Buscar cards da semana anterior não concluídos
- Perguntar se deve marcar como "Concluído" ou "Cancelado"
- Diariamente 23:00: Notificar cards pendentes de hoje

Base: Todas (Trabalho, Pessoal, Estudos, YouTube)
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict
import pytz
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.notion_client import NotionClient

load_dotenv()


class WeeklyFinalizer:
    """Finalizador Semanal de Cards"""
    
    def __init__(self):
        self.notion = NotionClient()
        self.sp_tz = pytz.timezone('America/Sao_Paulo')
        
        self.databases = {
            'Trabalho': os.getenv('TRABALHO_DB_ID'),
            'Pessoal': os.getenv('PESSOAL_DB_ID'),
            'Estudos': os.getenv('ESTUDOS_DB_ID'),
            'YouTube': os.getenv('YOUTUBER_DB_ID')
        }
    
    def get_last_week_range(self):
        """Retorna range da semana passada (seg-dom)"""
        today = datetime.now(self.sp_tz)
        
        # Última segunda
        days_since_monday = (today.weekday() - 0) % 7
        last_monday = today - timedelta(days=days_since_monday + 7)
        last_monday = last_monday.replace(hour=0, minute=0, second=0)
        
        # Último domingo
        last_sunday = last_monday + timedelta(days=6)
        last_sunday = last_sunday.replace(hour=23, minute=59, second=59)
        
        return last_monday, last_sunday
    
    def get_pending_cards_last_week(self, database_id: str) -> List[Dict]:
        """Busca cards da semana passada não concluídos"""
        last_monday, last_sunday = self.get_last_week_range()
        
        filter_obj = {
            "and": [
                {
                    "property": "Data",
                    "date": {
                        "on_or_after": last_monday.strftime('%Y-%m-%d')
                    }
                },
                {
                    "property": "Data",
                    "date": {
                        "on_or_before": last_sunday.strftime('%Y-%m-%d')
                    }
                },
                {
                    "or": [
                        {
                            "property": "Status",
                            "status": {"equals": "Não iniciado"}
                        },
                        {
                            "property": "Status",
                            "status": {"equals": "Em andamento"}
                        }
                    ]
                }
            ]
        }
        
        return self.notion.query_database(database_id, filter_obj)
    
    def get_pending_cards_today(self, database_id: str) -> List[Dict]:
        """Busca cards de hoje não concluídos"""
        today = datetime.now(self.sp_tz).strftime('%Y-%m-%d')
        
        filter_obj = {
            "and": [
                {
                    "property": "Data",
                    "date": {"equals": today}
                },
                {
                    "or": [
                        {
                            "property": "Status",
                            "status": {"equals": "Não iniciado"}
                        },
                        {
                            "property": "Status",
                            "status": {"equals": "Em andamento"}
                        }
                    ]
                }
            ]
        }
        
        return self.notion.query_database(database_id, filter_obj)
    
    def mark_as_completed(self, page_id: str) -> bool:
        """Marca card como Concluído"""
        properties = {
            "Status": {
                "status": {"name": "Concluído"}
            }
        }
        return self.notion.update_page(page_id, properties)
    
    def mark_as_cancelled(self, page_id: str) -> bool:
        """Marca card como Cancelado"""
        properties = {
            "Status": {
                "status": {"name": "Cancelado"}
            }
        }
        return self.notion.update_page(page_id, properties)
    
    def reschedule_card(self, page_id: str, new_date: datetime) -> bool:
        """Reagenda card para nova data"""
        properties = {
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(new_date, include_time=False)
                }
            }
        }
        return self.notion.update_page(page_id, properties)
    
    def get_card_title(self, page: Dict) -> str:
        """Extrai título do card"""
        title_prop = page['properties'].get('Nome do projeto') or \
                     page['properties'].get('Nome da tarefa') or \
                     page['properties'].get('Project name') or \
                     page['properties'].get('Nome')
        
        if title_prop and 'title' in title_prop:
            texts = title_prop['title']
            if texts:
                return texts[0]['text']['content']
        
        return "Sem título"
    
    def weekly_cleanup(self):
        """Limpeza semanal - segunda 07:00"""
        print("\n🧹 Limpeza Semanal - Cards Pendentes da Semana Passada\n")
        
        last_monday, last_sunday = self.get_last_week_range()
        print(f"📅 Período: {last_monday.date()} a {last_sunday.date()}\n")
        
        total_pending = 0
        
        for db_name, db_id in self.databases.items():
            pending_cards = self.get_pending_cards_last_week(db_id)
            
            if pending_cards:
                print(f"📋 {db_name}: {len(pending_cards)} cards pendentes")
                total_pending += len(pending_cards)
                
                for card in pending_cards:
                    title = self.get_card_title(card)
                    card_id = card['id']
                    
                    print(f"  - {title}")
                    print(f"    ID: {card_id}")
                    print(f"    Ações disponíveis:")
                    print(f"      1. Marcar como Concluído")
                    print(f"      2. Marcar como Cancelado")
                    print(f"      3. Reagendar para esta semana")
                    print()
        
        if total_pending == 0:
            print("✅ Nenhum card pendente da semana passada!")
        else:
            print(f"\n📊 Total: {total_pending} cards pendentes")
            print("\n💡 Execute ações manualmente ou configure auto-finalização")
    
    def daily_reminder(self):
        """Lembrete diário - 23:00"""
        print("\n⏰ Lembrete Diário - Cards Pendentes de Hoje\n")
        
        today = datetime.now(self.sp_tz)
        print(f"📅 Data: {today.date()}\n")
        
        total_pending = 0
        
        for db_name, db_id in self.databases.items():
            pending_cards = self.get_pending_cards_today(db_id)
            
            if pending_cards:
                print(f"📋 {db_name}: {len(pending_cards)} cards pendentes")
                total_pending += len(pending_cards)
                
                for card in pending_cards:
                    title = self.get_card_title(card)
                    status = card['properties']['Status']['status']['name']
                    
                    print(f"  - {title}")
                    print(f"    Status: {status}")
                    print()
        
        if total_pending == 0:
            print("✅ Todos os cards de hoje foram concluídos! Ótimo trabalho!")
        else:
            print(f"\n📊 Total: {total_pending} cards pendentes hoje")
            print("💡 Lembre-se de finalizá-los antes de dormir!")
    
    def run(self, mode='weekly'):
        """
        Executa finalizador
        
        Args:
            mode: 'weekly' para limpeza semanal, 'daily' para lembrete diário
        """
        print("🤖 Agent 3: Finalizador Semanal")
        print(f"⏰ Timezone: GMT-3 (São Paulo)\n")
        
        if mode == 'weekly':
            self.weekly_cleanup()
        elif mode == 'daily':
            self.daily_reminder()
        else:
            print(f"❌ Modo inválido: {mode}")
            print("   Use 'weekly' ou 'daily'")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Finalizador Semanal de Cards')
    parser.add_argument('--mode', choices=['weekly', 'daily'], default='weekly',
                        help='Modo de execução')
    
    args = parser.parse_args()
    
    agent = WeeklyFinalizer()
    agent.run(mode=args.mode)













