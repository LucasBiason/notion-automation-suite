#!/usr/bin/env python3
"""
Verificar tarefas atrasadas e emergenciais em todas as bases do Notion
"""

import sys
import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
TOKEN = os.getenv('NOTION_API_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# IDs das bases
DATABASES = {
    "WORK": "1f9962a7-693c-80a3-b947-c471a975acb0",
    "PERSONAL": "1fa962a7-693c-8032-8996-dd9cd2607dbf",
    "YOUTUBER": "1fa962a7-693c-80ce-9f1d-ff86223d6bda",
    "STUDIES": "1fa962a7-693c-80de-b90b-eaa513dcf9d1"
}

def get_title_from_properties(properties):
    """Extrai o título do card"""
    for prop_name, prop_value in properties.items():
        if prop_value.get("type") == "title":
            title_array = prop_value.get("title", [])
            if title_array:
                return title_array[0].get("plain_text", "Sem título")
    return "Sem título"

def get_date_from_properties(properties, date_field_name):
    """Extrai a data do card"""
    date_prop = properties.get(date_field_name, {})
    if date_prop.get("type") == "date":
        date_obj = date_prop.get("date")
        if date_obj:
            return date_obj.get("start")
    return None

def get_status_from_properties(properties):
    """Extrai o status do card"""
    status_prop = properties.get("Status", {})
    
    # Tentar como campo de status
    if status_prop.get("type") == "status":
        status_obj = status_prop.get("status")
        if status_obj:
            return status_obj.get("name", "Desconhecido")
    
    # Tentar como select
    if status_prop.get("type") == "select":
        select_obj = status_prop.get("select")
        if select_obj:
            return select_obj.get("name", "Desconhecido")
    
    return "Desconhecido"

def get_priority_from_properties(properties):
    """Extrai a prioridade do card"""
    priority_prop = properties.get("Prioridade", {})
    if priority_prop.get("type") == "select":
        select_obj = priority_prop.get("select")
        if select_obj:
            return select_obj.get("name", "Normal")
    return "Normal"

def get_launch_date_from_properties(properties):
    """Extrai a data de lançamento do card (específico para YouTube)"""
    date_prop = properties.get("Data de Lançamento", {})
    if date_prop.get("type") == "date":
        date_obj = date_prop.get("date")
        if date_obj:
            return date_obj.get("start")
    return None

def check_database_overdue(database_name, database_id):
    """Verifica cards atrasados em uma base específica"""
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    # Data atual no fuso GMT-3
    now = datetime.now(timezone(timedelta(hours=-3)))
    today_str = now.strftime("%Y-%m-%d")
    
    print(f"\n{'='*70}")
    print(f"📊 BASE: {database_name}")
    print(f"{'='*70}")
    
    # Buscar todos os cards
    response = requests.post(url, headers=HEADERS, json={})
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar cards: {response.status_code}")
        return
    
    results = response.json().get("results", [])
    
    # Determinar campo de data baseado na base
    date_field_map = {
        "WORK": "Periodo",
        "PERSONAL": "Data",
        "YOUTUBER": "Periodo",
        "STUDIES": "Data de Estudo"
    }
    
    date_field = date_field_map.get(database_name, "Data")
    
    overdue_tasks = []
    urgent_tasks = []
    emergency_tasks = []
    
    for card in results:
        properties = card.get("properties", {})
        
        # Extrair informações
        title = get_title_from_properties(properties)
        date_str = get_date_from_properties(properties, date_field)
        status = get_status_from_properties(properties)
        priority = get_priority_from_properties(properties)
        card_id = card.get("id", "")
        
        # Ignorar cards concluídos, cancelados, realocados ou descartados
        ignored_statuses = [
            "Concluído", "Concluido", "Completo", "Done",
            "Cancelado", "Realocada", "Descartado", "Publicado"
        ]
        if status in ignored_statuses:
            continue
        
        # Lógica especial para YouTube: se estiver em edição, verificar data de lançamento
        card_date_str = None
        days_overdue = 0
        
        if database_name == "YOUTUBER" and status in ["Editando", "Para Edição", "Em Edição", "Revisão"]:
            launch_date_str = get_launch_date_from_properties(properties)
            if launch_date_str:
                launch_date = datetime.fromisoformat(launch_date_str.replace("Z", "+00:00"))
                card_date_str = launch_date.strftime("%Y-%m-%d")
                
                if card_date_str < today_str:
                    days_overdue = (now.date() - launch_date.date()).days
                else:
                    continue  # Não está atrasado
            else:
                continue  # Não tem data de lançamento, não pode estar atrasado
        
        # Verificar se está atrasado pelo período
        elif date_str:
            card_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            card_date_str = card_date.strftime("%Y-%m-%d")
            
            if card_date_str < today_str:
                days_overdue = (now.date() - card_date.date()).days
            else:
                continue  # Não está atrasado
        else:
            continue  # Não tem data, não pode estar atrasado
        
        # Se chegou aqui, está atrasado - adicionar à lista
        task_info = {
            "title": title,
            "date": card_date_str,
            "status": status,
            "priority": priority,
            "days_overdue": days_overdue,
            "id": card_id
        }
        
        # Classificar por emergência
        if priority == "Crítico" or days_overdue > 7:
            emergency_tasks.append(task_info)
        elif priority == "Alta" or days_overdue > 3:
            urgent_tasks.append(task_info)
        else:
            overdue_tasks.append(task_info)
    
    # Mostrar resultados
    total_overdue = len(overdue_tasks) + len(urgent_tasks) + len(emergency_tasks)
    
    if total_overdue == 0:
        print("✅ Nenhuma tarefa atrasada!")
        return
    
    print(f"\n⚠️  Total de tarefas atrasadas: {total_overdue}")
    
    # Tarefas de emergência
    if emergency_tasks:
        print(f"\n🚨 EMERGÊNCIA ({len(emergency_tasks)} tarefas):")
        for task in sorted(emergency_tasks, key=lambda x: x["days_overdue"], reverse=True):
            print(f"   • {task['title']}")
            print(f"     📅 Vencimento: {task['date']} ({task['days_overdue']} dias atrasado)")
            print(f"     ⚡ Prioridade: {task['priority']}")
            print(f"     📊 Status: {task['status']}")
            print(f"     🔗 https://www.notion.so/{task['id'].replace('-', '')}")
            print()
    
    # Tarefas urgentes
    if urgent_tasks:
        print(f"\n⚡ URGENTE ({len(urgent_tasks)} tarefas):")
        for task in sorted(urgent_tasks, key=lambda x: x["days_overdue"], reverse=True):
            print(f"   • {task['title']}")
            print(f"     📅 Vencimento: {task['date']} ({task['days_overdue']} dias atrasado)")
            print(f"     ⚡ Prioridade: {task['priority']}")
            print(f"     📊 Status: {task['status']}")
            print(f"     🔗 https://www.notion.so/{task['id'].replace('-', '')}")
            print()
    
    # Tarefas atrasadas (não urgentes)
    if overdue_tasks:
        print(f"\n⏰ ATRASADAS ({len(overdue_tasks)} tarefas):")
        for task in sorted(overdue_tasks, key=lambda x: x["days_overdue"], reverse=True):
            print(f"   • {task['title']}")
            print(f"     📅 Vencimento: {task['date']} ({task['days_overdue']} dias atrasado)")
            print(f"     ⚡ Prioridade: {task['priority']}")
            print(f"     📊 Status: {task['status']}")
            print(f"     🔗 https://www.notion.so/{task['id'].replace('-', '')}")
            print()

def main():
    """Verifica todas as bases"""
    
    print("\n🔍 VERIFICAÇÃO DE TAREFAS ATRASADAS E EMERGENCIAIS")
    print(f"📅 Data atual: {datetime.now(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M')} (GMT-3)")
    
    for db_name, db_id in DATABASES.items():
        check_database_overdue(db_name, db_id)
    
    print(f"\n{'='*70}")
    print("✅ Verificação concluída!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()

