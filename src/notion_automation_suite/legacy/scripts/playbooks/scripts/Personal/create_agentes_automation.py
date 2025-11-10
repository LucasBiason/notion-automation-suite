#!/usr/bin/env python3
"""
Cria subtarefas dos Agentes de Automação
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.notion_engine import NotionEngine

TOKEN = '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'
PARENT_ID = '287962a7-693c-8171-982f-f9b13993df67'

SUBTASKS = [
    {'title': 'Agente 1: Gerenciador de Cards Semanais', 'emoji': '📅', 'atividade': 'Desenvolvimento'},
    {'title': 'Agente 2: Coach de Estudos', 'emoji': '📚', 'atividade': 'Desenvolvimento'},
    {'title': 'Agente 3: Finalizador Semanal', 'emoji': '✅', 'atividade': 'Desenvolvimento'},
    {'title': 'Agente 4: Organizador YouTube', 'emoji': '🎬', 'atividade': 'Desenvolvimento'},
    {'title': 'Agente 6: Gerador de Relatórios', 'emoji': '📊', 'atividade': 'Desenvolvimento'},
    {'title': 'Agente 7-8-9: Monitor Integrado', 'emoji': '🚨', 'atividade': 'Desenvolvimento'}
]

def main():
    engine = NotionEngine(TOKEN)
    result = engine.create_subitems_only('PERSONAL', PARENT_ID, SUBTASKS)
    
    print(f"Agentes: {result['created']}/{len(SUBTASKS)} criados")
    if result['failed'] > 0:
        print(f"Falhas: {result['failed']}")
    
    return result['created'] == len(SUBTASKS)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

