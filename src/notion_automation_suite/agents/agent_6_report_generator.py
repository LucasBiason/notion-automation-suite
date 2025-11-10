"""
Agente 6: Gerador de Relatórios

Funcionalidades:
- Segunda 07:00: Relatório Semanal
- Dia 1 do mês: Relatório Mensal
- Sob demanda: Status Atual

Bases: Todas (Trabalho, Pessoal, Estudos, YouTube)
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict
from collections import Counter
import pytz
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.notion_client import NotionClient

load_dotenv()


class ReportGenerator:
    """Gerador de Relatórios"""
    
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
        """Retorna range da semana passada"""
        today = datetime.now(self.sp_tz)
        days_since_monday = (today.weekday() - 0) % 7
        last_monday = today - timedelta(days=days_since_monday + 7)
        last_sunday = last_monday + timedelta(days=6)
        
        return last_monday, last_sunday
    
    def get_completed_cards_last_week(self, db_id: str) -> List[Dict]:
        """Busca cards concluídos na semana passada"""
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
                    "property": "Status",
                    "status": {"equals": "Concluído"}
                }
            ]
        }
        
        return self.notion.query_database(db_id, filter_obj)
    
    def get_in_progress_courses(self) -> List[Dict]:
        """Busca cursos em andamento"""
        filter_obj = {
            "property": "Status",
            "status": {"equals": "Em andamento"}
        }
        
        return self.notion.query_database(self.databases['Estudos'], filter_obj)
    
    def get_upcoming_commitments(self, days_ahead: int = 7) -> List[Dict]:
        """Busca compromissos dos próximos X dias"""
        today = datetime.now(self.sp_tz)
        future_date = today + timedelta(days=days_ahead)
        
        all_commitments = []
        
        for db_id in self.databases.values():
            filter_obj = {
                "and": [
                    {
                        "property": "Data",
                        "date": {
                            "on_or_after": today.strftime('%Y-%m-%d')
                        }
                    },
                    {
                        "property": "Data",
                        "date": {
                            "on_or_before": future_date.strftime('%Y-%m-%d')
                        }
                    },
                    {
                        "property": "Status",
                        "status": {"does_not_equal": "Concluído"}
                    }
                ]
            }
            
            cards = self.notion.query_database(db_id, filter_obj)
            all_commitments.extend(cards)
        
        # Ordenar por data
        all_commitments.sort(key=lambda x: x['properties']['Data']['date']['start'])
        
        return all_commitments
    
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
    
    def weekly_report(self):
        """Gera relatório semanal"""
        last_monday, last_sunday = self.get_last_week_range()
        
        report = f"""
# 📊 Relatório Semanal - {last_monday.strftime('%d/%m')} a {last_sunday.strftime('%d/%m/%Y')}

## ✅ Concluído na Semana Passada

"""
        total_completed = 0
        
        for db_name, db_id in self.databases.items():
            completed = self.get_completed_cards_last_week(db_id)
            
            if completed:
                report += f"### {db_name} ({len(completed)} cards)\n\n"
                total_completed += len(completed)
                
                for card in completed:
                    title = self.get_card_title(card)
                    report += f"- [x] {title}\n"
                
                report += "\n"
        
        if total_completed == 0:
            report += "Nenhum card concluído na semana passada.\n\n"
        
        # Cursos em andamento
        courses = self.get_in_progress_courses()
        
        report += "## 📚 Cursos em Andamento\n\n"
        
        if courses:
            for course in courses:
                title = self.get_card_title(course)
                # TODO: Calcular % de conclusão
                report += f"- {title}: Em andamento\n"
        else:
            report += "Nenhum curso em andamento.\n"
        
        report += "\n"
        
        # Próximos compromissos
        upcoming = self.get_upcoming_commitments(days_ahead=7)
        
        report += "## 📅 Próximos Compromissos (Esta Semana)\n\n"
        
        if upcoming:
            current_day = None
            
            for card in upcoming:
                title = self.get_card_title(card)
                date_str = card['properties']['Data']['date']['start']
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                date = date.astimezone(self.sp_tz)
                
                day_str = date.strftime('%A, %d/%m')
                
                if day_str != current_day:
                    report += f"\n### {day_str}\n\n"
                    current_day = day_str
                
                time_str = date.strftime('%H:%M') if date.hour != 0 else ""
                report += f"- {time_str} {title}\n"
        else:
            report += "Nenhum compromisso agendado.\n"
        
        report += "\n"
        
        # YouTube
        youtube_filter = {
            "property": "Status",
            "status": {"equals": "Para Gravar"}
        }
        to_record = self.notion.query_database(self.databases['YouTube'], youtube_filter)
        
        report += "## 🎬 YouTube\n\n"
        report += f"- {len(to_record)} episódio(s) para gravar\n"
        
        report += "\n---\n\n"
        report += f"**Gerado em:** {datetime.now(self.sp_tz).strftime('%d/%m/%Y %H:%M')}\n"
        
        return report
    
    def monthly_report(self):
        """Gera relatório mensal"""
        today = datetime.now(self.sp_tz)
        last_month = today - timedelta(days=30)
        
        report = f"""
# 📊 Relatório Mensal - {last_month.strftime('%B/%Y')}

## 📊 Estatísticas

"""
        
        # TODO: Implementar estatísticas mensais
        # - Horas estudadas
        # - Cards concluídos
        # - Episódios publicados
        # - Cursos completados
        
        report += "⚠️ Estatísticas mensais: Em desenvolvimento\n\n"
        
        report += "## 📚 Progresso de Cursos\n\n"
        
        courses = self.get_in_progress_courses()
        for course in courses:
            title = self.get_card_title(course)
            report += f"- {title}: Em andamento\n"
        
        report += "\n---\n\n"
        report += f"**Gerado em:** {datetime.now(self.sp_tz).strftime('%d/%m/%Y %H:%M')}\n"
        
        return report
    
    def status_report(self):
        """Gera relatório de status atual"""
        today = datetime.now(self.sp_tz)
        
        report = f"""
# 📊 Status Atual - {today.strftime('%d/%m/%Y %H:%M')}

## ⏰ Próximas 24 Horas

"""
        
        # Compromissos de hoje
        today_cards = self.get_upcoming_commitments(days_ahead=1)
        
        if today_cards:
            for card in today_cards:
                title = self.get_card_title(card)
                date_str = card['properties']['Data']['date']['start']
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                date = date.astimezone(self.sp_tz)
                
                time_str = date.strftime('%H:%M') if date.hour != 0 else ""
                status = card['properties']['Status']['status']['name']
                
                report += f"- {time_str} {title} ({status})\n"
        else:
            report += "Nenhum compromisso nas próximas 24h.\n"
        
        report += "\n## 📋 Cards Pendentes Urgentes\n\n"
        
        # TODO: Implementar detecção de urgentes
        report += "⚠️ Detecção de urgentes: Em desenvolvimento\n"
        
        report += "\n---\n\n"
        report += f"**Gerado em:** {datetime.now(self.sp_tz).strftime('%d/%m/%Y %H:%M')}\n"
        
        return report
    
    def run(self, mode='weekly'):
        """
        Gera relatório
        
        Args:
            mode: 'weekly', 'monthly' ou 'status'
        """
        print("🤖 Agent 6: Gerador de Relatórios")
        print(f"⏰ Timezone: GMT-3 (São Paulo)\n")
        
        if mode == 'weekly':
            report = self.weekly_report()
        elif mode == 'monthly':
            report = self.monthly_report()
        elif mode == 'status':
            report = self.status_report()
        else:
            print(f"❌ Modo inválido: {mode}")
            return
        
        print(report)
        
        # Salvar relatório em arquivo
        filename = f"report_{mode}_{datetime.now(self.sp_tz).strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join('logs', filename)
        
        os.makedirs('logs', exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n💾 Relatório salvo em: {filepath}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Gerador de Relatórios')
    parser.add_argument('--mode', choices=['weekly', 'monthly', 'status'],
                        default='weekly', help='Tipo de relatório')
    
    args = parser.parse_args()
    
    agent = ReportGenerator()
    agent.run(mode=args.mode)













