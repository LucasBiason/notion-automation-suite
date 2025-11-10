#!/usr/bin/env python3
"""
Modelos/Templates para Cards Pessoais - Notion
Classe reutilizável para criar cards baseados nos templates da base pessoal
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
import sys
import os

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from notion_engine import NotionEngine

class PersonalTemplates:
    """
    Classe para criar cards pessoais baseados nos templates do Notion
    """
    
    def __init__(self, token: str):
        """Inicializa com o token do Notion"""
        self.engine = NotionEngine(token)
        
        # Templates exatos baseados nas imagens do Notion
        self.templates = {
            "planejamento_semanal": {
                "title": "Planejamento Semanal",
                "emoji": "📝",
                "atividade": "Gestão",
                "description": "Revisão do planejamento de tarefas para a semana."
            },
            "pagamento_hamilton": {
                "title": "Pagamento Hamilton (Médico)",
                "emoji": "💰",
                "atividade": "Finanças",
                "description": "Realizar a transferência bancária e o envio do comprovante"
            },
            "tratamento_medico": {
                "title": "Tratamento Médico",
                "emoji": "🏥",
                "atividade": "Saúde",
                "description": "Sessão de tratamento sempre as terças das 16:00 as 18:00"
            },
            "revisao_financeira_recebimentos": {
                "title": "Revisão Financeira - Recebimento e Pagamentos",
                "emoji": "📊",
                "atividade": "Finanças",
                "description": "Revisão Financeira dos gastos até o momento no mês. Atualizar a Planilha de Controle."
            },
            "revisao_financeira_fechamento": {
                "title": "Revisão Financeira - Fechamento do Mês",
                "emoji": "📊",
                "atividade": "Finanças",
                "description": "Revisão Financeira dos gastos até o momento no mês. Atualizar a Planilha de Controle."
            },
            "pagamento_contadora_impostos": {
                "title": "Pagamento Contadora e Impostos",
                "emoji": "💸",
                "atividade": "Finanças",
                "description": "Verificar impostos na plataforma\nLink: https://app.contabilizei.com.br/\nVerificar valores e atualizar na planilha de controle contábil"
            },
            "nota_fiscal_astracode": {
                "title": "Emissão de Nota Fiscal Astracode",
                "emoji": "📄",
                "atividade": "Finanças",
                "description": "Emitir Nota Fiscal para Astracode"
            },
            "consulta_medica": {
                "title": "Consulta Médica: <Preencher medico>",
                "emoji": "🏥",
                "atividade": "Saúde",
                "description": "Consulta médica com especialista"
            }
        }
    
    def create_card_from_template(self, template_name: str, date: str, 
                                status: str = "Não iniciado", 
                                custom_data: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Cria um card baseado em um template
        
        Args:
            template_name: Nome do template (ex: "planejamento_semanal")
            date: Data no formato YYYY-MM-DD
            status: Status do card (padrão: "Não iniciado")
            custom_data: Dados customizados para sobrescrever o template
        
        Returns:
            ID do card criado ou None
        """
        if template_name not in self.templates:
            print(f"❌ Template '{template_name}' não encontrado")
            return None
        
        template = self.templates[template_name].copy()
        
        # Aplicar dados customizados se fornecidos
        if custom_data:
            template.update(custom_data)
        
        # Preparar dados para o NotionEngine
        card_data = {
            "title": template["title"],
            "status": status,
            "periodo": {"start": date},
            "atividade": template["atividade"],
            "description": template["description"],
            "emoji": template["emoji"]
        }
        
        return self.engine.create_card("PERSONAL", card_data)
    
    def create_weekly_events(self, week_start_date: str, 
                           mark_completed: bool = False) -> Dict[str, str]:
        """
        Cria todos os eventos recorrentes da semana
        
        Args:
            week_start_date: Data de início da semana (YYYY-MM-DD)
            mark_completed: Se True, marca todos como concluídos
        
        Returns:
            Dict com template_name -> card_id
        """
        start_date = datetime.strptime(week_start_date, "%Y-%m-%d")
        
        # Calcular datas
        monday = start_date
        tuesday = start_date + timedelta(days=1)
        fifteenth = start_date.replace(day=15)
        twenty_fifth = start_date.replace(day=25)
        
        status = "Concluído" if mark_completed else "Não iniciado"
        
        created_cards = {}
        
        # Segunda-feira: Planejamento Semanal + Pagamento Hamilton
        if monday.month == start_date.month:
            created_cards["planejamento_semanal"] = self.create_card_from_template(
                "planejamento_semanal", monday.strftime("%Y-%m-%d"), status
            )
            created_cards["pagamento_hamilton"] = self.create_card_from_template(
                "pagamento_hamilton", monday.strftime("%Y-%m-%d"), status
            )
        
        # Terça-feira: Tratamento
        if tuesday.month == start_date.month:
            created_cards["tratamento_medico"] = self.create_card_from_template(
                "tratamento_medico", tuesday.strftime("%Y-%m-%d"), status
            )
        
        # Dia 15: Revisão Financeira + Gestão de Pagamento + Pagamento de Impostos
        if start_date.day >= 15:
            created_cards["revisao_financeira"] = self.create_card_from_template(
                "revisao_financeira", fifteenth.strftime("%Y-%m-%d"), status
            )
            created_cards["gestao_pagamento"] = self.create_card_from_template(
                "gestao_pagamento", fifteenth.strftime("%Y-%m-%d"), status
            )
            created_cards["pagamento_impostos"] = self.create_card_from_template(
                "pagamento_impostos", fifteenth.strftime("%Y-%m-%d"), status
            )
        
        # Dia 25: Geração de Nota Fiscal
        if start_date.day >= 25:
            created_cards["nota_fiscal_astracode"] = self.create_card_from_template(
                "nota_fiscal_astracode", twenty_fifth.strftime("%Y-%m-%d"), status
            )
        
        return created_cards
    
    def create_monthly_events(self, year: int, month: int, 
                            mark_completed: bool = False) -> Dict[str, str]:
        """
        Cria todos os eventos recorrentes do mês
        
        Args:
            year: Ano (ex: 2025)
            month: Mês (ex: 10)
            mark_completed: Se True, marca todos como concluídos
        
        Returns:
            Dict com template_name -> card_id
        """
        status = "Concluído" if mark_completed else "Não iniciado"
        created_cards = {}
        
        # Calcular primeira segunda-feira do mês
        first_day = datetime(year, month, 1)
        days_until_monday = (7 - first_day.weekday()) % 7
        if first_day.weekday() != 0:  # Se não é segunda
            days_until_monday = (7 - first_day.weekday()) % 7
        first_monday = first_day + timedelta(days=days_until_monday)
        
        # Segunda-feira: Planejamento Semanal + Pagamento Hamilton
        created_cards["planejamento_semanal"] = self.create_card_from_template(
            "planejamento_semanal", first_monday.strftime("%Y-%m-%d"), status
        )
        created_cards["pagamento_hamilton"] = self.create_card_from_template(
            "pagamento_hamilton", first_monday.strftime("%Y-%m-%d"), status
        )
        
        # Terça-feira: Tratamento
        tuesday = first_monday + timedelta(days=1)
        created_cards["tratamento_medico"] = self.create_card_from_template(
            "tratamento_medico", tuesday.strftime("%Y-%m-%d"), status
        )
        
        # Dia 15: Eventos financeiros
        fifteenth = datetime(year, month, 15)
        created_cards["revisao_financeira"] = self.create_card_from_template(
            "revisao_financeira", fifteenth.strftime("%Y-%m-%d"), status
        )
        created_cards["gestao_pagamento"] = self.create_card_from_template(
            "gestao_pagamento", fifteenth.strftime("%Y-%m-%d"), status
        )
        created_cards["pagamento_impostos"] = self.create_card_from_template(
            "pagamento_impostos", fifteenth.strftime("%Y-%m-%d"), status
        )
        
        # Dia 25: Nota Fiscal
        twenty_fifth = datetime(year, month, 25)
        created_cards["nota_fiscal_astracode"] = self.create_card_from_template(
            "nota_fiscal_astracode", twenty_fifth.strftime("%Y-%m-%d"), status
        )
        
        return created_cards
    
    def list_available_templates(self) -> Dict[str, Dict[str, str]]:
        """
        Lista todos os templates disponíveis
        
        Returns:
            Dict com template_name -> template_data
        """
        return self.templates.copy()
    
    def get_template_info(self, template_name: str) -> Optional[Dict[str, str]]:
        """
        Obtém informações de um template específico
        
        Args:
            template_name: Nome do template
        
        Returns:
            Dict com dados do template ou None
        """
        return self.templates.get(template_name)
    
    def create_consulta_medica(self, medico: str, especialidade: str, date: str, 
                             hora_inicio: str = "", hora_fim: str = "", 
                             status: str = "Não iniciado") -> Optional[str]:
        """
        Cria um card de consulta médica com médico e especialidade personalizados
        
        Args:
            medico: Nome do médico (ex: "Doutora Andrea")
            especialidade: Especialidade (ex: "Endocrino")
            date: Data no formato YYYY-MM-DD
            hora_inicio: Hora de início (ex: "8:00")
            hora_fim: Hora de fim (ex: "10:20")
            status: Status do card
        
        Returns:
            ID do card criado ou None
        """
        # Construir título personalizado
        title = f"Consulta Médica: {medico} {especialidade}"
        
        # Construir descrição com horários se fornecidos
        description = f"Consulta médica com {medico} - {especialidade}"
        if hora_inicio and hora_fim:
            description += f"\nHorário: {hora_inicio} às {hora_fim}"
        
        # Dados customizados
        custom_data = {
            "title": title,
            "description": description
        }
        
        return self.create_card_from_template("consulta_medica", date, status, custom_data)

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de como usar a classe
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    TOKEN = os.getenv('NOTION_API_TOKEN')
    
    if TOKEN:
        templates = PersonalTemplates(TOKEN)
        
        # Listar templates disponíveis
        print("📋 Templates disponíveis:")
        for name, data in templates.list_available_templates().items():
            print(f"  • {name}: {data['title']} ({data['emoji']})")
        
        # Exemplo: criar um card específico
        # card_id = templates.create_card_from_template(
        #     "planejamento_semanal", 
        #     "2025-10-21", 
        #     "Não iniciado"
        # )
        
        # Exemplo: criar eventos da semana
        # cards = templates.create_weekly_events("2025-10-21", mark_completed=False)
    else:
        print("❌ Token do Notion não configurado")
