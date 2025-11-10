"""
Maestro - Sistema de Orquestração Multiagente

Este módulo fornece a coordenação central para todos os agentes do sistema.
"""

from .orchestrator import Maestro, Intent, AgentTask, AgentResponse, SharedKnowledgeBase

__all__ = ['Maestro', 'Intent', 'AgentTask', 'AgentResponse', 'SharedKnowledgeBase']
__version__ = '1.0.0'






