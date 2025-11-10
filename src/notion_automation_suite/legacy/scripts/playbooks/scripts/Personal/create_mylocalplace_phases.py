#!/usr/bin/env python3
"""
Cria subtarefas (fases) do MyLocalPlace
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.notion_engine import NotionEngine

TOKEN = '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'
PARENT_ID = '287962a7-693c-8103-acf9-c6d4fa5883cf'

SUBTASKS = [
    {'title': 'FASE 1: Implementar Segurança', 'emoji': '🔐', 'atividade': 'Desenvolvimento'},
    {'title': 'FASE 2: Atualizar Stack Docker', 'emoji': '📦', 'atividade': 'Desenvolvimento'},
    {'title': 'FASE 3: Implementar Novas Features', 'emoji': '📱', 'atividade': 'Desenvolvimento'},
    {'title': 'FASE 4: Otimização e Performance', 'emoji': '⚡', 'atividade': 'Desenvolvimento'},
    {'title': 'FASE 5: Testes e Qualidade', 'emoji': '🧪', 'atividade': 'Desenvolvimento'},
    {'title': 'FASE 6: Deploy e Produção', 'emoji': '🚀', 'atividade': 'Desenvolvimento'},
    {'title': 'FASE 7: Monitoramento', 'emoji': '📊', 'atividade': 'Desenvolvimento'},
    {'title': 'FASE 8: Documentação', 'emoji': '📚', 'atividade': 'Desenvolvimento'},
    {'title': 'FASE 9: Melhorias UX/UI', 'emoji': '🎨', 'atividade': 'Desenvolvimento'}
]

def main():
    engine = NotionEngine(TOKEN)
    result = engine.create_subitems_only('PERSONAL', PARENT_ID, SUBTASKS)
    
    print(f"MyLocalPlace: {result['created']}/{len(SUBTASKS)} criados")
    if result['failed'] > 0:
        print(f"Falhas: {result['failed']}")
    
    return result['created'] == len(SUBTASKS)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

