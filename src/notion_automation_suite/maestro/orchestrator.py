"""
Maestro - Orquestrador Central do Sistema Multiagente

Este módulo coordena todos os agentes do sistema, delegando tarefas,
consolidando resultados e mantendo a knowledge base compartilhada.
"""

import os
import json
import asyncio
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


class Intent(Enum):
    """Intenções possíveis do usuário"""
    PREPARE_WEEK = "prepare_week"
    CREATE_REVIEW = "create_review"
    CHECK_DELAYS = "check_delays"
    GENERATE_REPORT = "generate_report"
    REORGANIZE_SCHEDULE = "reorganize_schedule"
    CREATE_CARDS = "create_cards"
    PLAN_YOUTUBE = "plan_youtube"
    UPDATE_GAMING = "update_gaming"
    UNKNOWN = "unknown"


@dataclass
class AgentTask:
    """Representa uma tarefa para um agente"""
    agent_id: str
    action: str
    context: Dict[str, Any]
    priority: str = "medium"  # low, medium, high, critical
    wait_for_completion: bool = True


@dataclass
class AgentResponse:
    """Resposta de um agente"""
    agent_id: str
    status: str  # success, error, partial
    result: Dict[str, Any]
    timestamp: str
    error_message: Optional[str] = None


class SharedKnowledgeBase:
    """
    Base de conhecimento compartilhada entre todos os agentes
    """
    
    def __init__(self, state_file: str = "/tmp/multiagent_state.json"):
        self.state_file = state_file
        self.state = self.load()
    
    def load(self) -> Dict[str, Any]:
        """Carrega estado do sistema"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar estado: {e}")
                return self.init_state()
        return self.init_state()
    
    def init_state(self) -> Dict[str, Any]:
        """Inicializa estado padrão"""
        return {
            "system": {
                "initialized_at": datetime.now().isoformat(),
                "timezone": "GMT-3",
                "current_date": datetime.now().strftime("%Y-%m-%d"),
                "user": {
                    "name": "Lucas Biason",
                    "level_xp": 360,
                    "duolingo_streak": 56
                }
            },
            "bases": {
                "personal": {
                    "pending_tasks": 0,
                    "late_tasks": 0,
                    "upcoming_week": []
                },
                "studies": {
                    "current_phase": "FIAP Fase 3",
                    "pending_classes": 0,
                    "next_class": None
                },
                "youtube": {
                    "active_series": 6,
                    "episodes_to_record": 0,
                    "episodes_to_edit": 0,
                    "next_launch": None
                },
                "work": {
                    "active_projects": 0,
                    "client": "Astracode",
                    "status": "maintenance"
                }
            },
            "agents": {},
            "recent_actions": [],
            "pending_decisions": []
        }
    
    def save(self):
        """Salva estado do sistema"""
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar estado: {e}")
    
    def update_agent(self, agent_id: str, data: Dict[str, Any]):
        """Atualiza estado de um agente"""
        self.state['agents'][agent_id] = {
            'last_update': datetime.now().isoformat(),
            'data': data
        }
        self.save()
    
    def add_action(self, agent_id: str, action: str, result: str):
        """Registra ação executada"""
        action_record = {
            'agent': agent_id,
            'action': action,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        self.state['recent_actions'].insert(0, action_record)
        
        # Manter apenas últimas 50 ações
        self.state['recent_actions'] = self.state['recent_actions'][:50]
        self.save()
    
    def get_agent_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Obtém estado de um agente"""
        return self.state['agents'].get(agent_id)
    
    def get_full_state(self) -> Dict[str, Any]:
        """Obtém estado completo do sistema"""
        return self.state
    
    def update_base_stats(self, base: str, stats: Dict[str, Any]):
        """Atualiza estatísticas de uma base"""
        if base in self.state['bases']:
            self.state['bases'][base].update(stats)
            self.save()


class Maestro:
    """
    Orquestrador central de todos os agentes
    """
    
    def __init__(self):
        self.knowledge_base = SharedKnowledgeBase()
        self.agents = {}
        self.intent_keywords = self._load_intent_keywords()
    
    def _load_intent_keywords(self) -> Dict[Intent, List[str]]:
        """Carrega palavras-chave para identificação de intenções"""
        return {
            Intent.PREPARE_WEEK: ["prepare", "preparar", "semana", "week"],
            Intent.CREATE_REVIEW: ["criar", "create", "revisão", "review", "resumo"],
            Intent.CHECK_DELAYS: ["verificar", "check", "atraso", "delays", "atrasadas"],
            Intent.GENERATE_REPORT: ["gerar", "generate", "relatório", "report"],
            Intent.REORGANIZE_SCHEDULE: ["reorganizar", "reorganize", "cronograma", "schedule"],
            Intent.CREATE_CARDS: ["criar", "create", "cards", "tarefas"],
            Intent.PLAN_YOUTUBE: ["planejar", "plan", "youtube", "episódios", "gravar"],
            Intent.UPDATE_GAMING: ["atualizar", "update", "gaming", "gamificação", "xp"],
        }
    
    def understand_intent(self, request: str) -> Intent:
        """
        Entende a intenção do usuário baseado no texto
        """
        request_lower = request.lower()
        
        # Procura por palavras-chave
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                return intent
        
        return Intent.UNKNOWN
    
    def decide_agents(self, intent: Intent, context: Dict[str, Any] = None) -> List[AgentTask]:
        """
        Decide quais agentes acionar baseado na intenção
        """
        tasks = []
        
        if intent == Intent.PREPARE_WEEK:
            # Preparar semana: Weekly Cards + Monitor + Reports
            tasks.extend([
                AgentTask(
                    agent_id="weekly_cards",
                    action="create_weekly_cards",
                    context={"date": datetime.now().strftime("%Y-%m-%d")},
                    priority="high"
                ),
                AgentTask(
                    agent_id="monitor",
                    action="check_delays",
                    context={},
                    priority="high"
                ),
                AgentTask(
                    agent_id="reports",
                    action="generate_weekly_report",
                    context={},
                    priority="medium"
                )
            ])
        
        elif intent == Intent.CREATE_REVIEW:
            # Criar revisão: Coach de Estudos + Notion Manager
            aula = context.get('aula', 'Unknown') if context else 'Unknown'
            tasks.extend([
                AgentTask(
                    agent_id="coach_estudos",
                    action="create_review",
                    context={"aula": aula},
                    priority="high"
                ),
                AgentTask(
                    agent_id="notion_manager",
                    action="create_review_card",
                    context={"aula": aula},
                    priority="medium",
                    wait_for_completion=False  # Aguarda coach terminar
                )
            ])
        
        elif intent == Intent.CHECK_DELAYS:
            # Verificar atrasos: Monitor
            tasks.append(
                AgentTask(
                    agent_id="monitor",
                    action="check_all_delays",
                    context={},
                    priority="high"
                )
            )
        
        elif intent == Intent.GENERATE_REPORT:
            # Gerar relatório: Reports
            report_type = context.get('type', 'weekly') if context else 'weekly'
            tasks.append(
                AgentTask(
                    agent_id="reports",
                    action=f"generate_{report_type}_report",
                    context={},
                    priority="medium"
                )
            )
        
        elif intent == Intent.REORGANIZE_SCHEDULE:
            # Reorganizar: Study Coach + Notion Manager
            tasks.extend([
                AgentTask(
                    agent_id="study_coach",
                    action="reorganize_schedule",
                    context=context or {},
                    priority="high"
                ),
                AgentTask(
                    agent_id="notion_manager",
                    action="update_schedule_cards",
                    context={},
                    priority="medium",
                    wait_for_completion=False
                )
            ])
        
        elif intent == Intent.PLAN_YOUTUBE:
            # Planejar YouTube: YouTube Organizer
            tasks.append(
                AgentTask(
                    agent_id="youtube",
                    action="plan_production",
                    context=context or {},
                    priority="high"
                )
            )
        
        elif intent == Intent.UPDATE_GAMING:
            # Atualizar Gaming: Scripts de gamificação
            tasks.append(
                AgentTask(
                    agent_id="gaming",
                    action="update_dashboard",
                    context=context or {},
                    priority="medium"
                )
            )
        
        return tasks
    
    async def delegate_tasks(self, tasks: List[AgentTask]) -> List[AgentResponse]:
        """
        Delega tarefas para agentes (paralelo quando possível)
        """
        responses = []
        
        # Separar tarefas que podem ser executadas em paralelo
        high_priority = [t for t in tasks if t.priority in ["critical", "high"]]
        medium_low = [t for t in tasks if t.priority in ["medium", "low"]]
        
        # Executar tarefas de alta prioridade primeiro
        for task in high_priority:
            response = await self.execute_task(task)
            responses.append(response)
        
        # Executar tarefas de média/baixa prioridade em paralelo
        if medium_low:
            parallel_responses = await asyncio.gather(
                *[self.execute_task(task) for task in medium_low],
                return_exceptions=True
            )
            responses.extend([r for r in parallel_responses if isinstance(r, AgentResponse)])
        
        return responses
    
    async def execute_task(self, task: AgentTask) -> AgentResponse:
        """
        Executa uma tarefa em um agente específico
        """
        try:
            # TODO: Implementar execução real dos agentes
            # Por enquanto, simula execução
            
            print(f"[MAESTRO] Executando {task.action} no agente {task.agent_id}")
            
            # Simular delay de execução
            await asyncio.sleep(0.5)
            
            response = AgentResponse(
                agent_id=task.agent_id,
                status="success",
                result={"message": f"Tarefa {task.action} executada com sucesso"},
                timestamp=datetime.now().isoformat()
            )
            
            # Registrar ação na knowledge base
            self.knowledge_base.add_action(
                agent_id=task.agent_id,
                action=task.action,
                result="success"
            )
            
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_id=task.agent_id,
                status="error",
                result={},
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def consolidate_results(self, responses: List[AgentResponse]) -> str:
        """
        Consolida resultados de múltiplos agentes em uma resposta única
        """
        success_count = sum(1 for r in responses if r.status == "success")
        error_count = sum(1 for r in responses if r.status == "error")
        
        result_text = f"✅ **Operação Concluída**\n\n"
        result_text += f"**Resumo:** {success_count} agentes executados com sucesso"
        
        if error_count > 0:
            result_text += f", {error_count} com erros"
        
        result_text += "\n\n**Detalhes:**\n"
        
        for response in responses:
            emoji = "✅" if response.status == "success" else "❌"
            result_text += f"{emoji} **{response.agent_id}**: {response.result.get('message', 'Concluído')}\n"
        
        # Adicionar ações recomendadas se houver
        pending_decisions = self.knowledge_base.state.get('pending_decisions', [])
        if pending_decisions:
            result_text += "\n**⚠️ Ações Recomendadas:**\n"
            for decision in pending_decisions:
                result_text += f"- {decision.get('issue')}\n"
        
        return result_text
    
    async def handle_request(self, request: str, context: Dict[str, Any] = None) -> str:
        """
        Processa uma requisição do usuário
        
        Esta é a função principal que coordena todo o fluxo:
        1. Entende a intenção
        2. Decide quais agentes acionar
        3. Delega tarefas
        4. Consolida resultados
        """
        print(f"[MAESTRO] Recebida requisição: {request}")
        
        # 1. Entender intenção
        intent = self.understand_intent(request)
        print(f"[MAESTRO] Intenção identificada: {intent.value}")
        
        if intent == Intent.UNKNOWN:
            return "❌ Não entendi a requisição. Tente reformular ou peça ajuda."
        
        # 2. Decidir quais agentes acionar
        tasks = self.decide_agents(intent, context)
        print(f"[MAESTRO] {len(tasks)} tarefas identificadas")
        
        # 3. Delegar tarefas
        responses = await self.delegate_tasks(tasks)
        
        # 4. Consolidar resultados
        result = self.consolidate_results(responses)
        
        return result


# Função helper para uso via CLI
async def main():
    """Função principal para testes via CLI"""
    maestro = Maestro()
    
    # Exemplos de requisições
    test_requests = [
        "Prepare minha semana",
        "Verificar tarefas atrasadas",
        "Gerar relatório semanal"
    ]
    
    for request in test_requests:
        print(f"\n{'='*60}")
        print(f"Requisição: {request}")
        print('='*60)
        
        result = await maestro.handle_request(request)
        print(result)
        print()


if __name__ == "__main__":
    asyncio.run(main())






