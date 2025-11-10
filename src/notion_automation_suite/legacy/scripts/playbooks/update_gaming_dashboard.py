#!/usr/bin/env python3
"""
Atualizador Automático do Gaming Dashboard

Descrição: Atualiza o Gaming Dashboard automaticamente com XP do dia
Base Acessada: MULTIPLAS
Autor: AI Notion Manager
Data: 28/10/2025
Versão: 1.0
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

# ID do Gaming Dashboard
DASHBOARD_ID = "29a962a7693c81e7846efcad5345717d"

def calculate_level(total_xp):
    """Calcula nível baseado no XP total"""
    levels = [
        (0, 1, "🌱 Iniciante"),
        (100, 2, "🌿 Aprendiz"),
        (300, 3, "🪴 Praticante"),
        (600, 4, "🌳 Experiente"),
        (1100, 5, "🦅 Competente"),
        (1850, 6, "🌟 Profissional"),
        (2850, 7, "💫 Expert"),
        (4350, 8, "🔥 Mestre"),
        (6350, 9, "👑 Grão-Mestre"),
        (9350, 10, "💎 Lenda")
    ]
    
    for i in range(len(levels) - 1, -1, -1):
        if total_xp >= levels[i][0]:
            current_level = levels[i][1]
            current_title = levels[i][2]
            
            # Calcular próximo nível
            if i < len(levels) - 1:
                next_xp = levels[i + 1][0]
                needed = next_xp - total_xp
            else:
                next_xp = total_xp
                needed = 0
            
            return current_level, current_title, next_xp, needed
    
    return 1, "🌱 Iniciante", 100, 100

def add_comment_to_dashboard(xp_today, studies, personal, work, youtube, duolingo, total_tasks):
    """Adiciona comentário com update do dia"""
    
    hoje = datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y %H:%M")
    
    comment_text = f"""📊 UPDATE AUTOMÁTICO - {hoje}

🎮 XP DO DIA: {xp_today} XP

Breakdown:
📚 Studies: {studies} XP
🏠 Personal: {personal} XP
💼 Work: {work} XP
🎥 YouTube: {youtube} XP
🦉 Duolingo: {duolingo} XP

📋 Tarefas completadas: {total_tasks}

✅ Atualização automática via script!
Próximo update: Amanhã 23:00"""
    
    url = f"https://api.notion.com/v1/comments"
    
    data = {
        "parent": {"page_id": DASHBOARD_ID},
        "rich_text": [{
            "type": "text",
            "text": {"content": comment_text}
        }]
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        print("✅ Comentário adicionado ao dashboard!")
    else:
        print(f"❌ Erro ao adicionar comentário: {response.status_code}")

def main():
    """Função principal"""
    
    print("🎮 ATUALIZADOR DE GAMING DASHBOARD")
    print("=" * 60)
    
    # Aqui você vai colocar os valores calculados do outro script
    # Por enquanto, exemplo:
    
    xp_today = int(input("💎 Digite o XP total de hoje: "))
    studies = int(input("📚 XP Studies: "))
    personal = int(input("🏠 XP Personal: "))
    work = int(input("💼 XP Work: "))
    youtube = int(input("🎥 XP YouTube: "))
    duolingo = int(input("🦉 XP Duolingo: "))
    total_tasks = int(input("📋 Total de tarefas: "))
    
    # Perguntar XP acumulado atual
    current_total = int(input("📊 XP Total Acumulado Atual: "))
    
    # Calcular novo total
    new_total = current_total + xp_today
    
    # Calcular nível
    level, title, next_xp, needed = calculate_level(new_total)
    
    print(f"\n{'=' * 60}")
    print(f"📊 RESULTADO")
    print(f"{'=' * 60}")
    print(f"\nXP Hoje: {xp_today} XP")
    print(f"XP Total: {current_total} → {new_total} XP")
    print(f"Nível: {level} - {title}")
    print(f"Próximo Nível: {next_xp} XP (falta {needed} XP)")
    
    # Verificar se subiu de nível
    old_level, _, _, _ = calculate_level(current_total)
    if level > old_level:
        print(f"\n🎉 LEVEL UP! {old_level} → {level}!")
    
    # Adicionar comentário
    add_comment_to_dashboard(xp_today, studies, personal, work, youtube, duolingo, total_tasks)
    
    print(f"\n✅ Dashboard atualizado!")
    print(f"🔗 Ver: https://www.notion.so/{DASHBOARD_ID}")

if __name__ == "__main__":
    main()

