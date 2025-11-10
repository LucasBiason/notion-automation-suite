#!/usr/bin/env python3
"""
Cria todos os subitens da base Personal (Agentes + MyLocalPlace)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.notion_engine import NotionEngine

TOKEN = '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'

def main():
    engine = NotionEngine(TOKEN)
    
    print("🤖 Criando subtarefas Personal...")
    print("")
    
    # 1. Agentes
    agentes_id = '287962a7-693c-8171-982f-f9b13993df67'
    agentes_tasks = [
        {'title': 'Agente 1: Gerenciador de Cards Semanais', 'emoji': '📅', 'atividade': 'Desenvolvimento'},
        {'title': 'Agente 2: Coach de Estudos', 'emoji': '📚', 'atividade': 'Desenvolvimento'},
        {'title': 'Agente 3: Finalizador Semanal', 'emoji': '✅', 'atividade': 'Desenvolvimento'},
        {'title': 'Agente 4: Organizador YouTube', 'emoji': '🎬', 'atividade': 'Desenvolvimento'},
        {'title': 'Agente 6: Gerador de Relatórios', 'emoji': '📊', 'atividade': 'Desenvolvimento'},
        {'title': 'Agente 7-8-9: Monitor Integrado', 'emoji': '🚨', 'atividade': 'Desenvolvimento'}
    ]
    
    print("1. Agentes de Automação:")
    r1 = engine.create_subitems_only('PERSONAL', agentes_id, agentes_tasks)
    print(f"   {r1['created']}/6 criados")
    print("")
    
    # 2. MyLocalPlace
    mylocalplace_id = '287962a7-693c-8103-acf9-c6d4fa5883cf'
    mylocalplace_tasks = [
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
    
    print("2. MyLocalPlace:")
    r2 = engine.create_subitems_only('PERSONAL', mylocalplace_id, mylocalplace_tasks)
    print(f"   {r2['created']}/9 criados")
    print("")
    
    total = r1['created'] + r2['created']
    print(f"Total: {total}/15 cards criados")
    
    return total == 15

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

