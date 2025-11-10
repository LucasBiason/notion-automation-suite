#!/usr/bin/env python3
"""
Script para listar modelos/templates da base pessoal
"""

import sys
import os
import requests
from dotenv import load_dotenv
from collections import Counter

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
TOKEN = os.getenv('NOTION_API_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_all_personal_cards():
    """Busca todos os cards da base personal"""
    
    url = f"https://api.notion.com/v1/databases/1fa962a7-693c-8032-8996-dd9cd2607dbf/query"
    
    data = {
        "page_size": 100
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar cards: {response.status_code}")
        return []
    
    return response.json().get("results", [])

def analyze_templates():
    """Analisa os cards existentes para identificar padrões/modelos"""
    
    print("🔍 Analisando cards da base pessoal...")
    cards = get_all_personal_cards()
    
    if not cards:
        print("❌ Nenhum card encontrado")
        return
    
    print(f"📋 Total de cards encontrados: {len(cards)}\n")
    
    # Analisar padrões
    activities = []
    titles = []
    status_list = []
    
    for card in cards:
        # Título
        title_property = card.get("properties", {}).get("Nome da tarefa", {})
        title = title_property.get("title", [{}])[0].get("text", {}).get("content", "")
        if title:
            titles.append(title)
        
        # Atividade
        activity_property = card.get("properties", {}).get("Atividade", {})
        activity = activity_property.get("select", {}).get("name", "")
        if activity:
            activities.append(activity)
        
        # Status
        status_property = card.get("properties", {}).get("Status", {})
        status = status_property.get("status", {}).get("name", "")
        if status:
            status_list.append(status)
    
    # Contar frequências
    activity_counts = Counter(activities)
    title_patterns = Counter(titles)
    status_counts = Counter(status_list)
    
    # Mostrar resultados
    print("📊 TIPOS DE ATIVIDADE:")
    for activity, count in activity_counts.most_common():
        print(f"  • {activity}: {count} cards")
    
    print(f"\n📝 TÍTULOS MAIS COMUNS (Top 20):")
    for title, count in title_patterns.most_common(20):
        if count > 1:  # Mostrar apenas títulos recorrentes
            print(f"  • {title}: {count}x")
    
    print(f"\n✅ STATUS UTILIZADOS:")
    for status, count in status_counts.most_common():
        print(f"  • {status}: {count} cards")
    
    # Identificar modelos/templates (títulos que se repetem)
    print(f"\n🎯 MODELOS IDENTIFICADOS (tarefas recorrentes):")
    templates = [title for title, count in title_patterns.items() if count >= 3]
    
    if templates:
        for template in sorted(templates):
            count = title_patterns[template]
            print(f"  📌 {template} ({count}x)")
    else:
        print("  ℹ️ Nenhum modelo recorrente identificado (mínimo 3 ocorrências)")

if __name__ == "__main__":
    analyze_templates()













