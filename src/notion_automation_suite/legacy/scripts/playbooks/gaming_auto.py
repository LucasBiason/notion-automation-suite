#!/usr/bin/env python3
"""
Gaming Auto - Script Automático Completo

Descrição: Calcula XP, verifica badges e atualiza dashboard AUTOMATICAMENTE
Base Acessada: MULTIPLAS
Autor: AI Notion Manager
Data: 28/10/2025
Versão: 1.0

USO: python3 gaming_auto.py
"""

import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('NOTION_API_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

BASES = {
    'STUDIES': '1fa962a7-693c-80de-b90b-eaa513dcf9d1',
    'PERSONAL': '1fa962a7-693c-8032-8996-dd9cd2607dbf',
    'WORK': '1f9962a7-693c-80a3-b947-c471a975acb0',
    'YOUTUBER': '1fa962a7-693c-80ce-9f1d-ff86223d6bda'
}

DASHBOARD_ID = "29a962a7693c81e7846efcad5345717d"

def get_completed_today(database_id):
    """Busca cards concluídos hoje"""
    hoje = datetime.now(timezone(timedelta(hours=-3))).date()
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    data = {
        "filter": {
            "or": [
                {"property": "Status", "status": {"equals": "Concluído"}},
                {"property": "Status", "status": {"equals": "Concluido"}},
                {"property": "Status", "status": {"equals": "Publicado"}},
                {"property": "Status", "status": {"equals": "Em Andamento"}}
            ]
        },
        "page_size": 100
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code != 200:
        return []
    
    results = response.json().get("results", [])
    
    # Filtrar editados hoje
    tasks_today = []
    for task in results:
        last_edited = task.get("last_edited_time", "")
        if last_edited:
            edited_date = datetime.fromisoformat(last_edited.replace('Z', '+00:00')).date()
            if edited_date == hoje:
                tasks_today.append(task)
    
    return tasks_today

def calculate_xp_smart(base_name, task):
    """Calcula XP de forma inteligente"""
    
    props = task.get("properties", {})
    
    if base_name == 'STUDIES':
        categorias = [c.get("name", "") for c in props.get("Categorias", {}).get("multi_select", [])]
        if "Aula" in categorias:
            return 10, "Aula"
        elif "Projeto" in categorias or "Portfolio" in categorias:
            return 25, "Projeto"
        elif "Seção" in categorias:
            return 50, "Seção"
        return 10, "Tarefa"
    
    elif base_name == 'PERSONAL':
        title = props.get("Nome da tarefa", {}).get("title", [{}])[0].get("plain_text", "").lower()
        if "tratamento" in title or "médico" in title:
            return 20, "Compromisso Médico"
        elif "pagamento" in title:
            return 15, "Pagamento"
        elif "planejamento" in title:
            return 25, "Planejamento"
        elif "revisão" in title:
            return 50, "Revisão"
        return 10, "Tarefa"
    
    elif base_name == 'YOUTUBER':
        status = props.get("Status", {}).get("status", {}).get("name", "")
        if status == "Publicado":
            return 100, "Episódio Publicado"
        elif "Editando" in status:
            return 75, "Episódio Editado"
        return 50, "Tarefa YouTube"
    
    elif base_name == 'WORK':
        return 50, "Tarefa Trabalho"
    
    return 0, "Desconhecido"

def add_comment(xp_breakdown, total_xp):
    """Adiciona comentário no dashboard"""
    
    hoje = datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y %H:%M")
    
    text = f"""🤖 UPDATE AUTOMÁTICO - {hoje}

🎮 XP DO DIA: {total_xp} XP

Breakdown:
{xp_breakdown}

✅ Calculado automaticamente!
Próximo update: Amanhã 23:00"""
    
    url = "https://api.notion.com/v1/comments"
    data = {
        "parent": {"page_id": DASHBOARD_ID},
        "rich_text": [{"type": "text", "text": {"content": text}}]
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    return response.status_code == 200

def main():
    """Função principal AUTOMÁTICA"""
    
    print("🤖 GAMING AUTO - ATUALIZAÇÃO AUTOMÁTICA")
    print("=" * 70)
    
    hoje_str = datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y")
    print(f"📅 Data: {hoje_str}\n")
    
    total_xp = 0
    total_tasks = 0
    breakdown_lines = []
    
    xp_por_base = {}
    
    # Processar cada base
    for base_name, base_id in BASES.items():
        print(f"🔍 Analisando {base_name}...")
        
        tasks = get_completed_today(base_id)
        base_xp = 0
        base_count = 0
        
        for task in tasks:
            xp, tipo = calculate_xp_smart(base_name, task)
            if xp > 0:
                base_xp += xp
                base_count += 1
                total_tasks += 1
        
        xp_por_base[base_name] = base_xp
        total_xp += base_xp
        
        emoji = {
            'STUDIES': '📚',
            'PERSONAL': '🏠', 
            'WORK': '💼',
            'YOUTUBER': '🎥'
        }.get(base_name, '📋')
        
        print(f"  {emoji} {base_count} tasks = {base_xp} XP\n")
    
    # Adicionar Duolingo manualmente (não está nas bases)
    duolingo_xp = int(input("\n🦉 XP Duolingo hoje (digite 0 se não fez): ") or "0")
    total_xp += duolingo_xp
    xp_por_base['DUOLINGO'] = duolingo_xp
    
    # Criar breakdown
    breakdown_text = "\n".join([
        f"📚 Studies: {xp_por_base.get('STUDIES', 0)} XP",
        f"🏠 Personal: {xp_por_base.get('PERSONAL', 0)} XP",
        f"💼 Work: {xp_por_base.get('WORK', 0)} XP",
        f"🎥 YouTube: {xp_por_base.get('YOUTUBER', 0)} XP",
        f"🦉 Duolingo: {xp_por_base.get('DUOLINGO', 0)} XP"
    ])
    
    # RESUMO
    print("\n" + "=" * 70)
    print("📊 RESUMO DO DIA")
    print("=" * 70)
    print(f"\n{breakdown_text}")
    print(f"\n{'─' * 70}")
    print(f"🎯 TOTAL: {total_xp} XP")
    print(f"📋 Tarefas: {total_tasks}")
    print(f"{'─' * 70}\n")
    
    # Adicionar comentário
    if add_comment(breakdown_text, total_xp):
        print("✅ Dashboard atualizado com comentário!")
    
    # Salvar em arquivo
    report_file = f"gaming_report_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"GAMING REPORT - {hoje_str}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"XP Total: {total_xp} XP\n")
        f.write(f"Tarefas: {total_tasks}\n\n")
        f.write(breakdown_text)
    
    print(f"📄 Relatório salvo: {report_file}")
    print(f"\n🔗 Dashboard: https://www.notion.so/{DASHBOARD_ID}")
    
    # Instruções finais
    print(f"\n{'=' * 70}")
    print("💡 PRÓXIMOS PASSOS MANUAIS:")
    print(f"{'=' * 70}")
    print(f"\n1. Atualizar XP Total no dashboard: +{total_xp} XP")
    print(f"2. Marcar dia na tabela semanal: {total_xp} XP")
    print(f"3. Streak +1 dia")
    print(f"4. Verificar se desbloqueou badges")
    print(f"5. Celebrar! 🎉\n")

if __name__ == "__main__":
    main()

