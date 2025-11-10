"""
Agente 2: Coach de Estudos

Funcionalidades:
1. Reorganizador de Cronogramas
   - Detecta aulas puladas/adiadas
   - Recalcula TODAS as datas subsequentes
   - Respeita horários: 19:00-21:00 (seg-sex), 19:30-21:00 (ter)
   - Pula finais de semana

2. Professor Particular IA
   - Gera resumos de aulas
   - Cria exercícios práticos
   - Acompanha progresso
   
Base: Estudos
Contextos: @01-Estudos/, @ia-ml-knowledge-base/, @Apostilas e Materiais de Cursos/
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


class StudyCoach:
    """Coach de Estudos - Reorganizador + Professor IA"""
    
    def __init__(self):
        self.notion = NotionClient()
        self.estudos_db_id = os.getenv('ESTUDOS_DB_ID')
        self.sp_tz = pytz.timezone('America/Sao_Paulo')
        
        # Horários de estudo
        self.study_hours = {
            'monday': (19, 0, 21, 0),      # 19:00-21:00
            'tuesday': (19, 30, 21, 0),    # 19:30-21:00
            'wednesday': (19, 0, 21, 0),   # 19:00-21:00
            'thursday': (19, 0, 21, 0),    # 19:00-21:00
            'friday': (19, 0, 21, 0),      # 19:00-21:00
        }
    
    def get_next_study_day(self, current_date: datetime) -> datetime:
        """Retorna próximo dia de estudo (pula finais de semana)"""
        next_day = current_date + timedelta(days=1)
        
        # Pula sábado e domingo
        while next_day.weekday() in [5, 6]:  # 5=sábado, 6=domingo
            next_day += timedelta(days=1)
        
        return next_day
    
    def get_study_hours_for_day(self, date: datetime) -> tuple:
        """Retorna horários de estudo para o dia"""
        weekday = date.weekday()
        
        if weekday == 1:  # Terça
            return self.study_hours['tuesday']
        elif weekday in [0, 2, 3, 4]:  # Seg, Qua, Qui, Sex
            return self.study_hours['monday']
        else:
            # Fim de semana - pular
            return None
    
    def calculate_class_times(self, start_date: datetime, duration_minutes: int) -> tuple:
        """
        Calcula horários de aula respeitando limite de 21:00
        
        Returns:
            (start_time, end_time, overflows) - overflows=True se passa das 21:00
        """
        hours = self.get_study_hours_for_day(start_date)
        if not hours:
            return None, None, True
        
        start_h, start_m, end_h, end_m = hours
        
        # Horário de início
        class_start = start_date.replace(hour=start_h, minute=start_m, second=0)
        
        # Horário de término
        class_end = class_start + timedelta(minutes=duration_minutes)
        
        # Verifica se passa das 21:00
        limit = start_date.replace(hour=21, minute=0, second=0)
        overflows = class_end > limit
        
        return class_start, class_end, overflows
    
    def find_skipped_classes(self) -> List[Dict]:
        """Encontra aulas marcadas como 'Pulada' ou 'Adiada'"""
        filter_obj = {
            "or": [
                {
                    "property": "Status",
                    "status": {"equals": "Pulada"}
                },
                {
                    "property": "Status",
                    "status": {"equals": "Adiada"}
                }
            ]
        }
        
        return self.notion.query_database(self.estudos_db_id, filter_obj)
    
    def get_subsequent_classes(self, after_date: datetime) -> List[Dict]:
        """Busca todas as aulas APÓS uma data"""
        filter_obj = {
            "property": "Data",
            "date": {
                "after": after_date.strftime('%Y-%m-%d')
            }
        }
        
        results = self.notion.query_database(self.estudos_db_id, filter_obj)
        
        # Ordenar por data
        results.sort(key=lambda x: x['properties']['Data']['date']['start'])
        
        return results
    
    def reschedule_class(self, page_id: str, new_date: datetime, duration: int = 45):
        """Reagenda uma aula"""
        class_start, class_end, overflows = self.calculate_class_times(new_date, duration)
        
        if overflows:
            # Mover para próximo dia
            new_date = self.get_next_study_day(new_date)
            class_start, class_end, _ = self.calculate_class_times(new_date, duration)
        
        properties = {
            "Data": {
                "date": {
                    "start": self.notion.format_date_gmt3(class_start, include_time=True),
                    "end": self.notion.format_date_gmt3(class_end, include_time=True)
                }
            }
        }
        
        return self.notion.update_page(page_id, properties)
    
    def reorganize_schedule_after_skip(self, skipped_class: Dict):
        """Reorganiza cronograma após aula pulada"""
        # Data da aula pulada
        skipped_date_str = skipped_class['properties']['Data']['date']['start']
        skipped_date = datetime.fromisoformat(skipped_date_str.replace('Z', '+00:00'))
        skipped_date = skipped_date.astimezone(self.sp_tz)
        
        # Buscar aulas subsequentes
        subsequent = self.get_subsequent_classes(skipped_date)
        
        if not subsequent:
            print(f"  ✅ Nenhuma aula subsequente para reorganizar")
            return
        
        print(f"  📅 Reorganizando {len(subsequent)} aulas subsequentes...")
        
        # Calcular nova data para aula pulada (próximo dia disponível)
        new_date = self.get_next_study_day(skipped_date)
        
        # Reagendar aula pulada
        self.reschedule_class(skipped_class['id'], new_date)
        print(f"  ✅ Aula pulada reagendada para {new_date.date()}")
        
        # Empurrar todas as subsequentes
        current_date = new_date
        for aula in subsequent:
            current_date = self.get_next_study_day(current_date)
            self.reschedule_class(aula['id'], current_date)
        
        print(f"  ✅ {len(subsequent)} aulas reorganizadas!")
    
    def check_and_reorganize(self):
        """Verifica aulas puladas e reorganiza automaticamente"""
        print("\n📚 Verificando aulas puladas/adiadas...\n")
        
        skipped = self.find_skipped_classes()
        
        if not skipped:
            print("✅ Nenhuma aula pulada encontrada!")
            return
        
        print(f"⚠️  Encontradas {len(skipped)} aula(s) pulada(s)\n")
        
        for aula in skipped:
            title = aula['properties']['Project name']['title'][0]['text']['content']
            print(f"📖 Reorganizando: {title}")
            
            self.reorganize_schedule_after_skip(aula)
            
            # Marcar como reagendada
            properties = {
                "Status": {
                    "status": {"name": "Não iniciado"}
                }
            }
            self.notion.update_page(aula['id'], properties)
            
            print()
        
        print(f"✅ {len(skipped)} cronograma(s) reorganizado(s)!")
    
    def generate_class_summary(self, class_id: str):
        """
        Gera resumo de aula usando IA
        
        TODO: Integrar com OpenAI
        TODO: Buscar prompt da Galeria de Prompts no Notion
        TODO: Buscar transcrição + apostila
        """
        print(f"🤖 Gerando resumo para aula {class_id}...")
        print("⚠️  Integração OpenAI pendente")
        
        # Placeholder - será implementado com OpenAI
        pass
    
    def create_practice_exercises(self, class_id: str):
        """
        Cria exercícios práticos
        
        TODO: Integrar com OpenAI
        TODO: Criar cards de exercícios no Notion
        """
        print(f"📝 Criando exercícios para aula {class_id}...")
        print("⚠️  Integração OpenAI pendente")
        
        # Placeholder - será implementado com OpenAI
        pass
    
    def run(self, mode='reorganize'):
        """
        Executa coach
        
        Args:
            mode: 'reorganize' ou 'summary' ou 'exercises'
        """
        print("🤖 Agent 2: Coach de Estudos")
        print(f"⏰ Timezone: GMT-3 (São Paulo)")
        print(f"📚 Base: Estudos\n")
        
        if mode == 'reorganize':
            self.check_and_reorganize()
        elif mode == 'summary':
            print("⚠️  Modo 'summary' requer integração OpenAI (pendente)")
        elif mode == 'exercises':
            print("⚠️  Modo 'exercises' requer integração OpenAI (pendente)")
        else:
            print(f"❌ Modo inválido: {mode}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Coach de Estudos')
    parser.add_argument('--mode', choices=['reorganize', 'summary', 'exercises'],
                        default='reorganize', help='Modo de execução')
    
    args = parser.parse_args()
    
    agent = StudyCoach()
    agent.run(mode=args.mode)













