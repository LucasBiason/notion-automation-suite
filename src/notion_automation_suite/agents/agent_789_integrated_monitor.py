"""
Agente 7-8-9: Monitor Integrado

Combina 3 funcionalidades:
1. Monitor de Prazos - Alerta cursos/projetos próximos do fim
2. Otimizador de Cronograma - Detecta sobrecarga, sugere redistribuição
3. Integrador de Bases - Verifica conflitos entre bases

Bases: Todas (Trabalho, Pessoal, Estudos, YouTube)
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import defaultdict
import pytz
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.notion_client import NotionClient

load_dotenv()


class IntegratedMonitor:
    """Monitor Integrado - Prazos + Otimização + Integração"""
    
    def __init__(self):
        self.notion = NotionClient()
        self.sp_tz = pytz.timezone('America/Sao_Paulo')
        
        self.databases = {
            'Trabalho': os.getenv('TRABALHO_DB_ID'),
            'Pessoal': os.getenv('PESSOAL_DB_ID'),
            'Estudos': os.getenv('ESTUDOS_DB_ID'),
            'YouTube': os.getenv('YOUTUBER_DB_ID')
        }
    
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
    
    # ========== MONITOR DE PRAZOS ==========
    
    def check_deadlines(self, days_threshold: int = 7) -> List[Dict]:
        """Verifica prazos próximos"""
        today = datetime.now(self.sp_tz)
        threshold_date = today + timedelta(days=days_threshold)
        
        alerts = []
        
        for db_name, db_id in self.databases.items():
            filter_obj = {
                "and": [
                    {
                        "property": "Data",
                        "date": {
                            "on_or_before": threshold_date.strftime('%Y-%m-%d')
                        }
                    },
                    {
                        "property": "Status",
                        "status": {"does_not_equal": "Concluído"}
                    }
                ]
            }
            
            cards = self.notion.query_database(db_id, filter_obj)
            
            for card in cards:
                date_str = card['properties']['Data']['date']['start']
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                date = date.astimezone(self.sp_tz)
                
                days_left = (date - today).days
                
                if days_left <= days_threshold:
                    alerts.append({
                        'database': db_name,
                        'title': self.get_card_title(card),
                        'date': date,
                        'days_left': days_left,
                        'urgency': 'critical' if days_left <= 2 else 'warning'
                    })
        
        return sorted(alerts, key=lambda x: x['days_left'])
    
    def check_overdue_cards(self) -> List[Dict]:
        """Verifica cards vencidos não concluídos"""
        today = datetime.now(self.sp_tz)
        
        overdue = []
        
        for db_name, db_id in self.databases.items():
            filter_obj = {
                "and": [
                    {
                        "property": "Data",
                        "date": {
                            "before": today.strftime('%Y-%m-%d')
                        }
                    },
                    {
                        "property": "Status",
                        "status": {"does_not_equal": "Concluído"}
                    }
                ]
            }
            
            cards = self.notion.query_database(db_id, filter_obj)
            
            for card in cards:
                date_str = card['properties']['Data']['date']['start']
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                date = date.astimezone(self.sp_tz)
                
                days_overdue = (today - date).days
                
                overdue.append({
                    'database': db_name,
                    'title': self.get_card_title(card),
                    'date': date,
                    'days_overdue': days_overdue
                })
        
        return sorted(overdue, key=lambda x: x['days_overdue'], reverse=True)
    
    # ========== OTIMIZADOR DE CRONOGRAMA ==========
    
    def analyze_workload(self, start_date: datetime, end_date: datetime) -> Dict:
        """Analisa carga de trabalho em um período"""
        workload = defaultdict(lambda: {'hours': 0, 'cards': []})
        
        for db_name, db_id in self.databases.items():
            filter_obj = {
                "and": [
                    {
                        "property": "Data",
                        "date": {
                            "on_or_after": start_date.strftime('%Y-%m-%d')
                        }
                    },
                    {
                        "property": "Data",
                        "date": {
                            "on_or_before": end_date.strftime('%Y-%m-%d')
                        }
                    },
                    {
                        "property": "Status",
                        "status": {"does_not_equal": "Concluído"}
                    }
                ]
            }
            
            cards = self.notion.query_database(db_id, filter_obj)
            
            for card in cards:
                date_str = card['properties']['Data']['date']['start']
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                date = date.astimezone(self.sp_tz)
                
                day_key = date.strftime('%Y-%m-%d')
                
                # Estimar horas (padrão: 2h por card, ajustar conforme necessário)
                estimated_hours = 2
                
                # Se tem horário de fim, calcular duração real
                if 'end' in card['properties']['Data']['date']:
                    end_str = card['properties']['Data']['date']['end']
                    end_date = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                    end_date = end_date.astimezone(self.sp_tz)
                    
                    duration = (end_date - date).total_seconds() / 3600
                    estimated_hours = duration
                
                workload[day_key]['hours'] += estimated_hours
                workload[day_key]['cards'].append({
                    'database': db_name,
                    'title': self.get_card_title(card),
                    'hours': estimated_hours
                })
        
        return dict(workload)
    
    def detect_overload(self, threshold_hours: int = 10) -> List[Dict]:
        """Detecta dias com sobrecarga"""
        today = datetime.now(self.sp_tz)
        next_week = today + timedelta(days=7)
        
        workload = self.analyze_workload(today, next_week)
        
        overloaded_days = []
        
        for day_str, data in workload.items():
            if data['hours'] > threshold_hours:
                overloaded_days.append({
                    'date': day_str,
                    'total_hours': data['hours'],
                    'cards_count': len(data['cards']),
                    'cards': data['cards']
                })
        
        return sorted(overloaded_days, key=lambda x: x['total_hours'], reverse=True)
    
    # ========== INTEGRADOR DE BASES ==========
    
    def detect_conflicts(self, date: datetime) -> List[Dict]:
        """Detecta conflitos de horário em um dia"""
        conflicts = []
        
        day_str = date.strftime('%Y-%m-%d')
        
        # Buscar todos os cards do dia
        all_cards = []
        
        for db_name, db_id in self.databases.items():
            filter_obj = {
                "property": "Data",
                "date": {"equals": day_str}
            }
            
            cards = self.notion.query_database(db_id, filter_obj)
            
            for card in cards:
                date_prop = card['properties']['Data']['date']
                
                start_str = date_prop['start']
                start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                start = start.astimezone(self.sp_tz)
                
                end = None
                if 'end' in date_prop and date_prop['end']:
                    end_str = date_prop['end']
                    end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                    end = end.astimezone(self.sp_tz)
                
                all_cards.append({
                    'database': db_name,
                    'title': self.get_card_title(card),
                    'start': start,
                    'end': end
                })
        
        # Verificar sobreposições
        for i, card1 in enumerate(all_cards):
            for card2 in all_cards[i+1:]:
                # Se ambos têm horário de fim, verificar sobreposição
                if card1['end'] and card2['end']:
                    # Conflito se:
                    # - card1 começa durante card2
                    # - card2 começa durante card1
                    if (card1['start'] < card2['end'] and card1['end'] > card2['start']):
                        conflicts.append({
                            'card1': f"{card1['database']}: {card1['title']}",
                            'card2': f"{card2['database']}: {card2['title']}",
                            'time1': f"{card1['start'].strftime('%H:%M')}-{card1['end'].strftime('%H:%M')}",
                            'time2': f"{card2['start'].strftime('%H:%M')}-{card2['end'].strftime('%H:%M')}"
                        })
        
        return conflicts
    
    # ========== EXECUÇÃO ==========
    
    def monitor_deadlines(self):
        """Monitora prazos"""
        print("\n🚨 Monitor de Prazos\n")
        
        # Prazos próximos
        alerts = self.check_deadlines(days_threshold=7)
        
        if alerts:
            print(f"⚠️  {len(alerts)} prazo(s) próximo(s):\n")
            
            for alert in alerts:
                emoji = "🔴" if alert['urgency'] == 'critical' else "🟡"
                days_text = f"{alert['days_left']} dia(s)" if alert['days_left'] > 0 else "HOJE"
                
                print(f"{emoji} {alert['database']}: {alert['title']}")
                print(f"   Prazo: {alert['date'].strftime('%d/%m/%Y')} ({days_text})")
                print()
        else:
            print("✅ Nenhum prazo próximo nos próximos 7 dias\n")
        
        # Cards vencidos
        overdue = self.check_overdue_cards()
        
        if overdue:
            print(f"🔴 {len(overdue)} card(s) vencido(s):\n")
            
            for card in overdue[:5]:  # Mostrar apenas os 5 mais atrasados
                print(f"   - {card['database']}: {card['title']}")
                print(f"     Venceu há {card['days_overdue']} dia(s)")
                print()
        else:
            print("✅ Nenhum card vencido\n")
    
    def optimize_schedule(self):
        """Otimiza cronograma"""
        print("\n📊 Otimizador de Cronograma\n")
        
        overloaded = self.detect_overload(threshold_hours=10)
        
        if overloaded:
            print(f"⚠️  {len(overloaded)} dia(s) com sobrecarga:\n")
            
            for day in overloaded:
                date = datetime.strptime(day['date'], '%Y-%m-%d')
                
                print(f"🔴 {date.strftime('%d/%m/%Y (%A)')}")
                print(f"   Total: {day['total_hours']:.1f}h ({day['cards_count']} cards)")
                print(f"   Detalhes:")
                
                for card in day['cards']:
                    print(f"     - {card['database']}: {card['title']} ({card['hours']:.1f}h)")
                
                print(f"\n   💡 Sugestão: Redistribuir cards para outros dias")
                print()
        else:
            print("✅ Nenhum dia com sobrecarga detectada\n")
    
    def integrate_bases(self):
        """Integra e verifica conflitos"""
        print("\n🔗 Integrador de Bases\n")
        
        # Verificar próximos 3 dias
        today = datetime.now(self.sp_tz)
        
        total_conflicts = 0
        
        for i in range(3):
            check_date = today + timedelta(days=i)
            conflicts = self.detect_conflicts(check_date)
            
            if conflicts:
                print(f"⚠️  {check_date.strftime('%d/%m/%Y (%A)')}: {len(conflicts)} conflito(s)\n")
                total_conflicts += len(conflicts)
                
                for conflict in conflicts:
                    print(f"   🔴 Conflito detectado:")
                    print(f"      - {conflict['card1']} ({conflict['time1']})")
                    print(f"      - {conflict['card2']} ({conflict['time2']})")
                    print()
        
        if total_conflicts == 0:
            print("✅ Nenhum conflito de horário detectado nos próximos 3 dias\n")
    
    def run(self, mode='all'):
        """
        Executa monitor
        
        Args:
            mode: 'deadlines', 'optimize', 'integrate' ou 'all'
        """
        print("🤖 Agent 7-8-9: Monitor Integrado")
        print(f"⏰ Timezone: GMT-3 (São Paulo)\n")
        
        if mode in ['deadlines', 'all']:
            self.monitor_deadlines()
        
        if mode in ['optimize', 'all']:
            self.optimize_schedule()
        
        if mode in ['integrate', 'all']:
            self.integrate_bases()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor Integrado')
    parser.add_argument('--mode', choices=['deadlines', 'optimize', 'integrate', 'all'],
                        default='all', help='Modo de execução')
    
    args = parser.parse_args()
    
    agent = IntegratedMonitor()
    agent.run(mode=args.mode)













