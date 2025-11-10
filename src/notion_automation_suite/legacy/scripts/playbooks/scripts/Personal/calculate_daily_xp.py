#!/usr/bin/env python3
"""
Calculadora Automática de XP Diário

Descrição: Busca cards concluídos hoje e calcula XP total automaticamente
Base Acessada: MULTIPLAS (todas as 4 bases)
Autor: AI Notion Manager
Data: 28/10/2025
Versão: 1.0
"""

import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

# Configurações
TOKEN = os.getenv('NOTION_API_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# IDs das bases
BASES = {
    'STUDIES': '1fa962a7-693c-80de-b90b-eaa513dcf9d1',
    'PERSONAL': '1fa962a7-693c-8032-8996-dd9cd2607dbf',
    'WORK': '1f9962a7-693c-80a3-b947-c471a975acb0',
    'YOUTUBER': '1fa962a7-693c-80ce-9f1d-ff86223d6bda'
}

# Tabela de XP
XP_TABLE = {
    'STUDIES': {
        'aula': 10,
        'projeto_1h': 10,
        'projeto_2h': 25,
        'secao': 50,
        'projeto_completo': 500,
        'resumo': 25,
        'exercicio': 15
    },
    'PERSONAL': {
        'tarefa_simples': 10,
        'compromisso': 20,
        'pagamento': 15,
        'planejamento': 25,
        'revisao_financeira': 50
    },
    'WORK': {
        'tarefa_pequena': 25,
        'tarefa_media': 50,
        'tarefa_grande': 100,
        'projeto': 500,
        'deploy': 200
    },
    'YOUTUBER': {
        'gravou': 50,
        'editou': 75,
        'publicou': 100,
        'serie': 500
    }
}

def get_completed_tasks_today(database_id):
    """Busca tasks concluídas hoje"""
    
    hoje = datetime.now(timezone(timedelta(hours=-3))).date()
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    # Buscar cards concluídos
    data = {
        "filter": {
            "or": [
                {"property": "Status", "status": {"equals": "Concluído"}},
                {"property": "Status", "status": {"equals": "Concluido"}},
                {"property": "Status", "status": {"equals": "Completo"}},
                {"property": "Status", "status": {"equals": "Done"}},
                {"property": "Status", "status": {"equals": "Publicado"}}
            ]
        },
        "page_size": 100
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar: {response.status_code}")
        return []
    
    results = response.json().get("results", [])
    
    # Filtrar apenas os de hoje (editados hoje)
    tasks_today = []
    for task in results:
        last_edited = task.get("last_edited_time", "")
        if last_edited:
            edited_date = datetime.fromisoformat(last_edited.replace('Z', '+00:00')).date()
            if edited_date == hoje:
                tasks_today.append(task)
    
    return tasks_today

def calculate_xp_studies(task):
    """Calcula XP de uma task de Studies"""
    props = task.get("properties", {})
    title = props.get("Project name", {}).get("title", [{}])[0].get("plain_text", "").lower()
    categorias = props.get("Categorias", {}).get("multi_select", [])
    
    xp = 0
    tipo = "Tarefa"
    
    # Verificar tipo
    if any("aula" in c.get("name", "").lower() for c in categorias):
        xp = 10
        tipo = "Aula"
    elif any("seção" in c.get("name", "").lower() or "secao" in c.get("name", "").lower() for c in categorias):
        xp = 50
        tipo = "Seção"
    elif any("projeto" in c.get("name", "").lower() or "portfolio" in c.get("name", "").lower() for c in categorias):
        # Verificar tempo ou assumir 2h+
        xp = 25
        tipo = "Projeto (2h+)"
    else:
        xp = 10
        tipo = "Tarefa"
    
    return xp, tipo

def calculate_xp_personal(task):
    """Calcula XP de uma task Personal"""
    props = task.get("properties", {})
    atividade = props.get("Atividade", {}).get("select", {}).get("name", "")
    title = props.get("Nome da tarefa", {}).get("title", [{}])[0].get("plain_text", "").lower()
    
    xp = 10  # Padrão
    tipo = "Tarefa"
    
    if "tratamento" in title or "médico" in title or "consulta" in title:
        xp = 20
        tipo = "Compromisso Médico"
    elif "pagamento" in title:
        xp = 15
        tipo = "Pagamento"
    elif "planejamento" in title:
        xp = 25
        tipo = "Planejamento"
    elif "revisão" in title or "revisao" in title:
        xp = 50
        tipo = "Revisão Financeira"
    elif atividade == "Saúde":
        xp = 20
        tipo = "Saúde"
    elif atividade == "Financeiro" or atividade == "Finanças":
        xp = 15
        tipo = "Financeiro"
    
    return xp, tipo

def calculate_xp_youtuber(task):
    """Calcula XP de uma task YouTube"""
    props = task.get("properties", {})
    status = props.get("Status", {}).get("status", {}).get("name", "")
    title = props.get("Nome do projeto", {}).get("title", [{}])[0].get("plain_text", "")
    
    xp = 0
    tipo = "Tarefa"
    
    if status == "Publicado":
        xp = 100
        tipo = "Episódio Publicado"
    elif "gravando" in status.lower() or "para gravar" in status.lower():
        xp = 50
        tipo = "Episódio Gravado"
    elif "editando" in status.lower() or "para edição" in status.lower():
        xp = 75
        tipo = "Episódio Editado"
    
    return xp, tipo

def calculate_xp_work(task):
    """Calcula XP de uma task Work"""
    props = task.get("properties", {})
    prioridade = props.get("Prioridade", {}).get("select", {}).get("name", "")
    
    xp = 50  # Padrão
    tipo = "Tarefa Média"
    
    if prioridade == "Alta":
        xp = 100
        tipo = "Tarefa Alta Prioridade"
    elif prioridade == "Média":
        xp = 50
        tipo = "Tarefa Média"
    else:
        xp = 25
        tipo = "Tarefa"
    
    return xp, tipo

def main():
    """Função principal"""
    
    print("🎮 CALCULADORA DE XP DIÁRIO")
    print("=" * 60)
    
    hoje = datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y")
    print(f"📅 Data: {hoje}\n")
    
    total_xp = 0
    total_tasks = 0
    breakdown = []
    
    # STUDIES
    print("📚 Analisando base STUDIES...")
    tasks = get_completed_tasks_today(BASES['STUDIES'])
    studies_xp = 0
    for task in tasks:
        xp, tipo = calculate_xp_studies(task)
        title = task.get("properties", {}).get("Project name", {}).get("title", [{}])[0].get("plain_text", "Sem título")
        studies_xp += xp
        breakdown.append(f"  ✅ {title[:40]} ({tipo}) = {xp} XP")
        total_tasks += 1
    
    print(f"  Total: {len(tasks)} tasks = {studies_xp} XP\n")
    total_xp += studies_xp
    
    # PERSONAL
    print("🏠 Analisando base PERSONAL...")
    tasks = get_completed_tasks_today(BASES['PERSONAL'])
    personal_xp = 0
    for task in tasks:
        xp, tipo = calculate_xp_personal(task)
        title = task.get("properties", {}).get("Nome da tarefa", {}).get("title", [{}])[0].get("plain_text", "Sem título")
        personal_xp += xp
        breakdown.append(f"  ✅ {title[:40]} ({tipo}) = {xp} XP")
        total_tasks += 1
    
    print(f"  Total: {len(tasks)} tasks = {personal_xp} XP\n")
    total_xp += personal_xp
    
    # WORK
    print("💼 Analisando base WORK...")
    tasks = get_completed_tasks_today(BASES['WORK'])
    work_xp = 0
    for task in tasks:
        xp, tipo = calculate_xp_work(task)
        title = task.get("properties", {}).get("Nome do projeto", {}).get("title", [{}])[0].get("plain_text", "Sem título")
        work_xp += xp
        breakdown.append(f"  ✅ {title[:40]} ({tipo}) = {xp} XP")
        total_tasks += 1
    
    print(f"  Total: {len(tasks)} tasks = {work_xp} XP\n")
    total_xp += work_xp
    
    # YOUTUBER
    print("🎥 Analisando base YOUTUBER...")
    tasks = get_completed_tasks_today(BASES['YOUTUBER'])
    youtube_xp = 0
    for task in tasks:
        xp, tipo = calculate_xp_youtuber(task)
        title = task.get("properties", {}).get("Nome do projeto", {}).get("title", [{}])[0].get("plain_text", "Sem título")
        if xp > 0:  # Só contar se ganhou XP
            youtube_xp += xp
            breakdown.append(f"  ✅ {title[:40]} ({tipo}) = {xp} XP")
            total_tasks += 1
    
    print(f"  Total: {len(tasks)} tasks com XP = {youtube_xp} XP\n")
    total_xp += youtube_xp
    
    # RESUMO
    print("=" * 60)
    print("📊 RESUMO DO DIA")
    print("=" * 60)
    print(f"\n📚 Studies: {studies_xp} XP")
    print(f"🏠 Personal: {personal_xp} XP")
    print(f"💼 Work: {work_xp} XP")
    print(f"🎥 YouTube: {youtube_xp} XP")
    print(f"\n{'─' * 60}")
    print(f"🎯 TOTAL: {total_xp} XP")
    print(f"📋 Tarefas: {total_tasks}")
    print(f"{'─' * 60}\n")
    
    # Breakdown detalhado
    if breakdown:
        print("📝 DETALHAMENTO:")
        for item in breakdown:
            print(item)
        print()
    
    # Verificar badges
    print("🏆 BADGES POSSÍVEIS:")
    if total_tasks >= 5:
        print("  ⚡ Sprint - 5 tarefas em 1 dia (+150 XP)")
    if total_tasks >= 10:
        print("  🎯 Sniper - 10 tarefas em 1 dia (+300 XP)")
    if studies_xp > 0 and personal_xp > 0 and youtube_xp > 0:
        print("  🦸 Multitarefa - 1 tarefa cada base (+100 XP)")
    
    # Sugestão para dashboard
    print(f"\n💡 COPIAR PARA O DASHBOARD:")
    print(f"   XP Hoje: {total_xp} XP")
    print(f"   Tarefas: {total_tasks}")
    print(f"   Streak: +1 dia")
    
    # Salvar em arquivo para referência
    report_file = f"gaming_report_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"GAMING REPORT - {hoje}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"XP Total: {total_xp} XP\n")
        f.write(f"Tarefas: {total_tasks}\n\n")
        f.write("Breakdown:\n")
        for item in breakdown:
            f.write(item + "\n")
    
    print(f"\n📄 Relatório salvo: {report_file}")

if __name__ == "__main__":
    main()

