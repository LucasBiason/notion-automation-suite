"""
Agente 1: Gerenciador de Cards Semanais

Responsável por criar automaticamente:
- Cards semanais: Planejamento, Pagamento Hamilton, Tratamento Médico
- Cards mensais: Revisão Financeira (15), Nota Fiscal (25), Fechamento (30)

Timezone: SEMPRE GMT-3
Base: Pessoal (Personal)
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


class WeeklyCardsManager:
    """Gerenciador de Cards Semanais e Mensais"""
    
    def __init__(self):
        self.notion = NotionClient()
        self.personal_db_id = os.getenv('PESSOAL_DB_ID')
        self.sp_tz = pytz.timezone('America/Sao_Paulo')
    
    def get_next_monday(self) -> datetime:
        """Retorna a próxima segunda-feira"""
        today = datetime.now(self.sp_tz)
        days_ahead = 0 - today.weekday()  # Segunda = 0
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    
    def get_next_tuesday(self) -> datetime:
        """Retorna a próxima terça-feira"""
        today = datetime.now(self.sp_tz)
        days_ahead = 1 - today.weekday()  # Terça = 1
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    
    def check_if_card_exists(self, title: str, date: datetime) -> bool:
        """Verifica se card já existe para evitar duplicação"""
        date_str = date.strftime('%Y-%m-%d')
        
        filter_obj = {
            "and": [
                {
                    "property": "Nome da tarefa",
                    "title": {
                        "contains": title
                    }
                },
                {
                    "property": "Data",
                    "date": {
                        "equals": date_str
                    }
                }
            ]
        }
        
        results = self.notion.query_database(self.personal_db_id, filter_obj)
        return len(results) > 0
    
    def create_weekly_planning(self) -> Optional[str]:
        """Cria card de Planejamento Semanal (segunda 07:00)"""
        monday = self.get_next_monday().replace(hour=7, minute=0, second=0)
        
        if self.check_if_card_exists("Planejamento Semanal", monday):
            print(f"⏭️  Card 'Planejamento Semanal' já existe para {monday.date()}")
            return None
        
        properties = {
            "Nome da tarefa": {
                "title": [{"text": {"content": "Planejamento Semanal"}}]
            },
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(monday, include_time=True)
                }
            },
            "Status": {
                "status": {"name": "Não iniciado"}
            },
            "Atividade": {
                "select": {"name": "Gestão"}
            }
        }
        
        card_id = self.notion.create_page(self.personal_db_id, properties, icon="📋")
        print(f"✅ Criado: Planejamento Semanal - {monday.date()} 07:00")
        return card_id
    
    def create_hamilton_payment(self) -> Optional[str]:
        """Cria card de Pagamento Hamilton (toda segunda)"""
        monday = self.get_next_monday().replace(hour=9, minute=0, second=0)
        
        if self.check_if_card_exists("Pagamento Hamilton (Médico)", monday):
            print(f"⏭️  Card 'Pagamento Hamilton' já existe para {monday.date()}")
            return None
        
        properties = {
            "Nome da tarefa": {
                "title": [{"text": {"content": "Pagamento Hamilton (Médico)"}}]
            },
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(monday, include_time=False)
                }
            },
            "Status": {
                "status": {"name": "Não iniciado"}
            },
            "Atividade": {
                "select": {"name": "Finanças"}
            }
        }
        
        card_id = self.notion.create_page(self.personal_db_id, properties, icon="💰")
        print(f"✅ Criado: Pagamento Hamilton - {monday.date()}")
        return card_id
    
    def create_medical_treatment(self) -> Optional[str]:
        """Cria card de Tratamento Médico (terça 16:00-18:00)"""
        tuesday = self.get_next_tuesday().replace(hour=16, minute=0, second=0)
        tuesday_end = tuesday.replace(hour=18, minute=0, second=0)
        
        if self.check_if_card_exists("Tratamento Médico", tuesday):
            print(f"⏭️  Card 'Tratamento Médico' já existe para {tuesday.date()}")
            return None
        
        properties = {
            "Nome da tarefa": {
                "title": [{"text": {"content": "Tratamento Médico"}}]
            },
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(tuesday, include_time=True),
                    "end": self.notion.format_date_gmt3(tuesday_end, include_time=True)
                }
            },
            "Status": {
                "status": {"name": "Não iniciado"}
            },
            "Atividade": {
                "select": {"name": "Saúde"}
            }
        }
        
        card_id = self.notion.create_page(self.personal_db_id, properties, icon="🏥")
        print(f"✅ Criado: Tratamento Médico - {tuesday.date()} 16:00-18:00")
        return card_id
    
    def create_monthly_financial_review(self, day: int) -> Optional[str]:
        """Cria card de Revisão Financeira (dias 15 e 30)"""
        today = datetime.now(self.sp_tz)
        
        # Calcular próximo dia do mês
        if today.day >= day:
            # Próximo mês
            if today.month == 12:
                target_date = datetime(today.year + 1, 1, day, tzinfo=self.sp_tz)
            else:
                target_date = datetime(today.year, today.month + 1, day, tzinfo=self.sp_tz)
        else:
            # Este mês
            target_date = datetime(today.year, today.month, day, tzinfo=self.sp_tz)
        
        title = f"Revisão Financeira - {target_date.strftime('%d/%m')}"
        if day == 30:
            title = f"Revisão Financeira - Fechamento {target_date.strftime('%m/%Y')}"
        
        if self.check_if_card_exists(title, target_date):
            print(f"⏭️  Card '{title}' já existe")
            return None
        
        properties = {
            "Nome da tarefa": {
                "title": [{"text": {"content": title}}]
            },
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(target_date, include_time=False)
                }
            },
            "Status": {
                "status": {"name": "Não iniciado"}
            },
            "Atividade": {
                "select": {"name": "Finanças"}
            }
        }
        
        card_id = self.notion.create_page(self.personal_db_id, properties, icon="📊")
        print(f"✅ Criado: {title}")
        return card_id
    
    def create_nota_fiscal(self) -> Optional[str]:
        """Cria card de Emissão de Nota Fiscal (dia 25)"""
        today = datetime.now(self.sp_tz)
        
        # Calcular próximo dia 25
        if today.day >= 25:
            # Próximo mês
            if today.month == 12:
                target_date = datetime(today.year + 1, 1, 25, tzinfo=self.sp_tz)
            else:
                target_date = datetime(today.year, today.month + 1, 25, tzinfo=self.sp_tz)
        else:
            # Este mês
            target_date = datetime(today.year, today.month, 25, tzinfo=self.sp_tz)
        
        title = f"Emissão de Nota Fiscal - {target_date.strftime('%m/%Y')}"
        
        if self.check_if_card_exists(title, target_date):
            print(f"⏭️  Card '{title}' já existe")
            return None
        
        properties = {
            "Nome da tarefa": {
                "title": [{"text": {"content": title}}]
            },
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(target_date, include_time=False)
                }
            },
            "Status": {
                "status": {"name": "Não iniciado"}
            },
            "Atividade": {
                "select": {"name": "Finanças"}
            }
        }
        
        card_id = self.notion.create_page(self.personal_db_id, properties, icon="📄")
        print(f"✅ Criado: {title}")
        return card_id
    
    def create_all_weekly_cards(self) -> Dict[str, str]:
        """Cria todos os cards semanais"""
        print("\n📅 Criando Cards Semanais...")
        results = {}
        
        results['planning'] = self.create_weekly_planning()
        results['hamilton'] = self.create_hamilton_payment()
        results['treatment'] = self.create_medical_treatment()
        
        return results
    
    def create_all_monthly_cards(self) -> Dict[str, str]:
        """Cria todos os cards mensais"""
        print("\n📅 Criando Cards Mensais...")
        results = {}
        
        results['review_15'] = self.create_monthly_financial_review(15)
        results['nota_fiscal'] = self.create_nota_fiscal()
        results['review_30'] = self.create_monthly_financial_review(30)
        
        return results
    
    def run(self):
        """Executa criação de todos os cards"""
        print("🤖 Agent 1: Gerenciador de Cards Semanais")
        print(f"⏰ Timezone: GMT-3 (São Paulo)")
        print(f"📋 Base: Pessoal\n")
        
        weekly = self.create_all_weekly_cards()
        monthly = self.create_all_monthly_cards()
        
        total_created = sum(1 for v in {**weekly, **monthly}.values() if v is not None)
        
        print(f"\n✅ Concluído! {total_created} cards criados.")


if __name__ == "__main__":
    agent = WeeklyCardsManager()
    agent.run()













