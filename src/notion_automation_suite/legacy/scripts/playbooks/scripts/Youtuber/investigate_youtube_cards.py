#!/usr/bin/env python3
"""
Investigar cards do YouTube em detalhes para identificar quais estão realmente atrasados
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

YOUTUBE_DB_ID = "1fa962a7-693c-80ce-9f1d-ff86223d6bda"

def get_property_value(properties, prop_name):
    """Extrai valor de uma propriedade genérica"""
    prop = properties.get(prop_name, {})
    prop_type = prop.get("type")
    
    if prop_type == "title":
        title_array = prop.get("title", [])
        if title_array:
            return title_array[0].get("plain_text", "")
    elif prop_type == "rich_text":
        text_array = prop.get("rich_text", [])
        if text_array:
            return text_array[0].get("plain_text", "")
    elif prop_type == "select":
        select_obj = prop.get("select")
        if select_obj:
            return select_obj.get("name", "")
    elif prop_type == "status":
        status_obj = prop.get("status")
        if status_obj:
            return status_obj.get("name", "")
    elif prop_type == "date":
        date_obj = prop.get("date")
        if date_obj:
            return date_obj.get("start", "")
    
    return None

def investigate_youtube_cards():
    """Investiga todos os cards do YouTube e mostra detalhes"""
    
    url = f"https://api.notion.com/v1/databases/{YOUTUBE_DB_ID}/query"
    
    # Data atual no fuso GMT-3
    now = datetime.now(timezone(timedelta(hours=-3)))
    today_str = now.strftime("%Y-%m-%d")
    
    print(f"\n{'='*80}")
    print(f"🔍 INVESTIGAÇÃO DETALHADA - BASE YOUTUBER")
    print(f"📅 Data atual: {now.strftime('%d/%m/%Y %H:%M')} (GMT-3)")
    print(f"{'='*80}\n")
    
    # Buscar todos os cards
    response = requests.post(url, headers=HEADERS, json={})
    
    if response.status_code != 200:
        print(f"❌ Erro ao buscar cards: {response.status_code}")
        return
    
    results = response.json().get("results", [])
    
    print(f"📊 Total de cards encontrados: {len(results)}\n")
    
    # Primeiro, vamos ver todos os status possíveis
    status_list = {}
    
    for card in results:
        properties = card.get("properties", {})
        status = get_property_value(properties, "Status")
        
        if status:
            if status not in status_list:
                status_list[status] = 0
            status_list[status] += 1
    
    print("📋 STATUS DISPONÍVEIS NA BASE:")
    for status, count in sorted(status_list.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {status}: {count} cards")
    
    print(f"\n{'='*80}\n")
    
    # Agora vamos analisar cards por status
    cards_to_review = []
    truly_overdue = []
    
    for card in results:
        properties = card.get("properties", {})
        
        # Extrair informações
        title = get_property_value(properties, "Nome")
        status = get_property_value(properties, "Status")
        periodo = get_property_value(properties, "Periodo")
        data_lancamento = get_property_value(properties, "Data de Lançamento")
        card_id = card.get("id", "")
        
        # Verificar se está em status de revisão/edição
        if status in ["Editando", "Para Edição", "Em Edição", "Revisão"]:
            # Para estes, só considerar atrasado se data de lançamento for anterior a hoje
            if data_lancamento:
                try:
                    lancamento_date = datetime.fromisoformat(data_lancamento.replace("Z", "+00:00"))
                    lancamento_str = lancamento_date.strftime("%Y-%m-%d")
                    
                    if lancamento_str < today_str:
                        days_overdue = (now.date() - lancamento_date.date()).days
                        cards_to_review.append({
                            "title": title,
                            "status": status,
                            "periodo": periodo,
                            "data_lancamento": lancamento_str,
                            "days_overdue": days_overdue,
                            "id": card_id
                        })
                except:
                    pass
        
        # Para outros status (exceto Publicado e Concluído), verificar pelo período
        elif status not in ["Publicado", "Concluído", "Concluido"]:
            if periodo:
                try:
                    periodo_date = datetime.fromisoformat(periodo.replace("Z", "+00:00"))
                    periodo_str = periodo_date.strftime("%Y-%m-%d")
                    
                    if periodo_str < today_str:
                        days_overdue = (now.date() - periodo_date.date()).days
                        truly_overdue.append({
                            "title": title,
                            "status": status,
                            "periodo": periodo_str,
                            "data_lancamento": data_lancamento if data_lancamento else "N/A",
                            "days_overdue": days_overdue,
                            "id": card_id
                        })
                except:
                    pass
    
    # Mostrar resultados
    print("🎬 CARDS EM REVISÃO/EDIÇÃO COM DATA DE LANÇAMENTO ATRASADA:")
    if cards_to_review:
        print(f"   Total: {len(cards_to_review)}\n")
        for card in sorted(cards_to_review, key=lambda x: x["days_overdue"], reverse=True):
            print(f"   📺 {card['title']}")
            print(f"      Status: {card['status']}")
            print(f"      Período: {card['periodo']}")
            print(f"      Data Lançamento: {card['data_lancamento']} ({card['days_overdue']} dias atrasado)")
            print(f"      🔗 https://www.notion.so/{card['id'].replace('-', '')}")
            print()
    else:
        print("   ✅ Nenhum card em revisão atrasado!\n")
    
    print(f"{'='*80}\n")
    
    print("⚠️  CARDS REALMENTE ATRASADOS (Status diferente de Publicado/Concluído):")
    if truly_overdue:
        print(f"   Total: {len(truly_overdue)}\n")
        for card in sorted(truly_overdue, key=lambda x: x["days_overdue"], reverse=True):
            print(f"   📺 {card['title']}")
            print(f"      Status: {card['status']}")
            print(f"      Período: {card['periodo']} ({card['days_overdue']} dias atrasado)")
            print(f"      Data Lançamento: {card['data_lancamento']}")
            print(f"      🔗 https://www.notion.so/{card['id'].replace('-', '')}")
            print()
    else:
        print("   ✅ Nenhum card realmente atrasado!\n")
    
    print(f"{'='*80}\n")
    
    # Resumo
    print("📊 RESUMO:")
    print(f"   • Cards em Revisão/Edição atrasados: {len(cards_to_review)}")
    print(f"   • Cards realmente atrasados: {len(truly_overdue)}")
    print(f"   • Total de cards que precisam atenção: {len(cards_to_review) + len(truly_overdue)}")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    investigate_youtube_cards()













