#!/usr/bin/env python3
"""
Reorganizar ROADMAP completo:
1. FIAP Fase 4 - Semana 1 (27/10-31/10) 8h-20h
2. Tech Challenge - Semana 2 (03/11-09/11)
3. Projetos Portfolio - Documentação
"""

import requests
from datetime import datetime, timedelta
import pytz

# Configuração
NOTION_TOKEN = input("Cole seu Notion Token: ").strip()
NOTION_VERSION = '2022-06-28'

# Database e Cards IDs
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'
FASE4_CARD_ID = '279962a7-693c-8000-84ea-ca97a3bfab25'
PROJETOS_PORTFOLIO_ID = '294962a7-693c-81be-afc2-e098c9ac8b92'
ROADMAP_PRINCIPAL_ID = '294962a7-693c-816a-8bd9-d1284b212549'

# Timezone
gmt3 = pytz.timezone('America/Sao_Paulo')

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

def format_date_gmt3(dt):
    """Formata datetime para GMT-3"""
    if isinstance(dt, datetime):
        return dt.astimezone(gmt3).strftime('%Y-%m-%dT%H:%M:%S-03:00')
    return dt

def get_page_children(parent_id):
    """Busca todos os subitens de um card"""
    url = f'https://api.notion.com/v1/databases/{ESTUDOS_DB}/query'
    
    payload = {
        "filter": {
            "property": "Parent item",
            "relation": {"contains": parent_id}
        },
        "sorts": [{"property": "Período", "direction": "ascending"}]
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"❌ Erro ao buscar subitens: {response.status_code}")
        print(response.text)
        return []

def update_page_period(page_id, start_dt, end_dt):
    """Atualiza o período de um card"""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    
    payload = {
        "properties": {
            "Período": {
                "date": {
                    "start": format_date_gmt3(start_dt),
                    "end": format_date_gmt3(end_dt)
                }
            }
        }
    }
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    return response.status_code == 200

def create_tech_challenge_card():
    """Cria card do Tech Challenge como subitem da Fase 4"""
    url = 'https://api.notion.com/v1/pages'
    
    # Tech Challenge: Semana 2 (03/11-09/11)
    inicio = gmt3.localize(datetime(2025, 11, 3, 8, 0))
    fim = gmt3.localize(datetime(2025, 11, 9, 20, 0))
    
    payload = {
        "parent": {"database_id": ESTUDOS_DB},
        "icon": {"type": "emoji", "emoji": "🏆"},
        "properties": {
            "Project name": {
                "title": [{"text": {"content": "Tech Challenge Fase 4 - Video Analysis IA"}}]
            },
            "Status": {"status": {"name": "Para Fazer"}},
            "Parent item": {"relation": [{"id": FASE4_CARD_ID}]},
            "Categorias": {
                "multi_select": [
                    {"name": "FIAP"},
                    {"name": "Tech Challenge"},
                    {"name": "IA"},
                    {"name": "Projeto Final"}
                ]
            },
            "Prioridade": {"select": {"name": "Crítica"}},
            "Período": {
                "date": {
                    "start": format_date_gmt3(inicio),
                    "end": format_date_gmt3(fim)
                }
            },
            "Tempo Total": {"rich_text": [{"text": {"content": "60:00:00"}}]},
            "Descrição": {
                "rich_text": [{
                    "text": {
                        "content": "Projeto final da Fase 4: Sistema de análise de vídeos com IA (reconhecimento facial, detecção de emoções e atividades). Prazo: 09/12/2025. Peso: 30% da nota."
                    }
                }]
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        card_id = response.json()['id']
        print(f"✅ Tech Challenge criado: {card_id}")
        return card_id
    else:
        print(f"❌ Erro ao criar Tech Challenge: {response.status_code}")
        print(response.text)
        return None

def create_portfolio_projects():
    """Cria cards dos projetos de portfolio"""
    
    projetos = [
        {
            "nome": "Notion MCP Server",
            "emoji": "🤖",
            "descricao": "Model Context Protocol Server customizado para Notion com regras de negócio embutidas para 4 databases diferentes. Não é apenas proxy - conhece regras específicas de cada database.",
            "periodo": (datetime(2025, 10, 23), datetime(2025, 11, 15)),
            "tempo": "40:00:00",
            "prioridade": "Alta",
            "categorias": ["Portfolio", "MCP", "Notion", "Python"]
        },
        {
            "nome": "MyLocalPlace v2.0 - DevTools Dashboard",
            "emoji": "🏠",
            "descricao": "Ambiente completo de desenvolvimento local com dashboard Streamlit para observabilidade. Controle de serviços (Docker), monitoramento de recursos, backup/restore databases.",
            "periodo": (datetime(2025, 10, 23), datetime(2025, 11, 10)),
            "tempo": "30:00:00",
            "prioridade": "Alta",
            "categorias": ["Portfolio", "DevOps", "Docker", "Streamlit"]
        },
        {
            "nome": "FastAPI Microservice Framework",
            "emoji": "🔧",
            "descricao": "Biblioteca reutilizável para criar microserviços FastAPI com CQRS + Event Sourcing. Baseada em padrões do ExpenseIQ mas genérica e open source.",
            "periodo": (datetime(2025, 11, 10), datetime(2025, 12, 7)),
            "tempo": "80:00:00",
            "prioridade": "Alta",
            "categorias": ["Portfolio", "FastAPI", "CQRS", "Event Sourcing", "Biblioteca"]
        },
        {
            "nome": "IntelliCart E-commerce CQRS + IA",
            "emoji": "🛒",
            "descricao": "E-commerce backend com arquitetura CQRS, Event Sourcing e AI Agents. 4 microserviços + IA integrada. Demonstra maestria arquitetural.",
            "periodo": (datetime(2025, 12, 8), datetime(2025, 12, 30)),
            "tempo": "120:00:00",
            "prioridade": "Crítica",
            "categorias": ["Portfolio", "E-commerce", "CQRS", "IA", "Microserviços"]
        }
    ]
    
    created = []
    
    for projeto in projetos:
        url = 'https://api.notion.com/v1/pages'
        
        inicio = gmt3.localize(projeto["periodo"][0])
        fim = gmt3.localize(projeto["periodo"][1])
        
        payload = {
            "parent": {"database_id": ESTUDOS_DB},
            "icon": {"type": "emoji", "emoji": projeto["emoji"]},
            "properties": {
                "Project name": {
                    "title": [{"text": {"content": projeto["nome"]}}]
                },
                "Status": {"status": {"name": "Para Fazer"}},
                "Parent item": {"relation": [{"id": PROJETOS_PORTFOLIO_ID}]},
                "Categorias": {
                    "multi_select": [{"name": cat} for cat in projeto["categorias"]]
                },
                "Prioridade": {"select": {"name": projeto["prioridade"]}},
                "Período": {
                    "date": {
                        "start": format_date_gmt3(inicio),
                        "end": format_date_gmt3(fim)
                    }
                },
                "Tempo Total": {"rich_text": [{"text": {"content": projeto["tempo"]}}]},
                "Descrição": {
                    "rich_text": [{"text": {"content": projeto["descricao"]}}]
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            card_id = response.json()['id']
            print(f"✅ {projeto['nome']}: {card_id}")
            created.append({"nome": projeto["nome"], "id": card_id})
        else:
            print(f"❌ Erro ao criar {projeto['nome']}: {response.status_code}")
            print(response.text)
    
    return created

def reorganizar_fase4_semana1():
    """
    Reorganiza FIAP Fase 4 para SEMANA 1 (27/10-31/10):
    - Início: 27/10/2025 8:00
    - Aulas sequenciais com 50min revisão
    - 8h-20h (terça até 15h)
    """
    
    print("\n📚 Reorganizando FIAP Fase 4 para Semana 1 (27/10-31/10)...")
    
    # Buscar aulas da Seção 3 (OpenAI)
    aulas = get_page_children(FASE4_CARD_ID)
    
    # Filtrar apenas aulas OpenAI (as 6 aulas)
    aulas_openai = [
        a for a in aulas 
        if 'OpenAI' in a['properties']['Project name']['title'][0]['text']['content']
        and 'Aula' in a['properties']['Project name']['title'][0]['text']['content']
    ]
    
    # Ordenar por número da aula
    def get_aula_number(aula):
        titulo = aula['properties']['Project name']['title'][0]['text']['content']
        try:
            # Extrair número após "Aula"
            num_str = titulo.split('Aula')[1].split(':')[0].strip()
            return int(num_str)
        except:
            return 999
    
    aulas_openai.sort(key=get_aula_number)
    
    print(f"Encontradas {len(aulas_openai)} aulas OpenAI")
    
    # Durações aproximadas (em minutos)
    duracoes = {
        1: 62,  # Aula 1 (já foi)
        2: 29,  # Aula 2
        3: 47,  # Aula 3
        4: 48,  # Aula 4
        5: 58,  # Aula 5
        6: 30   # Aula 6 (estimada)
    }
    
    # Cronograma
    # Segunda 27/10: Aulas 2, 3
    # Terça 28/10: Aula 4 (até 15h)
    # Quarta 29/10: Aula 5
    # Quinta 30/10: Aula 6
    # Sexta 31/10: Revisão geral
    
    cronograma = [
        # Segunda 27/10
        {"dia": datetime(2025, 10, 27), "aulas": [2, 3], "limite": 20},
        # Terça 28/10 (até 15h)
        {"dia": datetime(2025, 10, 28), "aulas": [4], "limite": 15},
        # Quarta 29/10
        {"dia": datetime(2025, 10, 29), "aulas": [5], "limite": 20},
        # Quinta 30/10
        {"dia": datetime(2025, 10, 30), "aulas": [6], "limite": 20},
    ]
    
    reorganizadas = 0
    
    for dia_config in cronograma:
        dia = dia_config["dia"]
        aulas_do_dia = dia_config["aulas"]
        limite_hora = dia_config["limite"]
        
        hora_atual = 8  # Começa às 8h
        
        for num_aula in aulas_do_dia:
            # Encontrar a aula
            aula_card = None
            for aula in aulas_openai:
                if get_aula_number(aula) == num_aula:
                    aula_card = aula
                    break
            
            if not aula_card:
                print(f"⚠️ Aula {num_aula} não encontrada")
                continue
            
            # Duração da aula
            duracao = duracoes.get(num_aula, 60)
            duracao_horas = duracao / 60.0
            
            # Calcular horários
            inicio = gmt3.localize(dia.replace(hour=int(hora_atual), minute=int((hora_atual % 1) * 60)))
            fim = inicio + timedelta(hours=duracao_horas)
            
            # Verificar se passa do limite
            if fim.hour >= limite_hora:
                print(f"⚠️ Aula {num_aula} passaria do limite ({limite_hora}h). Não agendando.")
                continue
            
            # Atualizar período da aula
            if update_page_period(aula_card['id'], inicio, fim):
                titulo = aula_card['properties']['Project name']['title'][0]['text']['content']
                print(f"✅ Aula {num_aula}: {dia.strftime('%d/%m')} {inicio.strftime('%H:%M')}-{fim.strftime('%H:%M')} ({int(duracao)}min)")
                reorganizadas += 1
            else:
                print(f"❌ Erro ao atualizar Aula {num_aula}")
            
            # Próxima aula: fim atual + 50min revisão
            hora_atual = fim.hour + (fim.minute / 60.0) + (50 / 60.0)
    
    print(f"\n✅ {reorganizadas} aulas reorganizadas para Semana 1!")
    return reorganizadas

def main():
    print("🚀 Reorganização Completa do Roadmap 2025-2026")
    print("=" * 60)
    
    # 1. Reorganizar FIAP Fase 4 - Semana 1
    print("\n📅 ETAPA 1: FIAP Fase 4 - Semana 1 (27-31/10)")
    aulas_reorganizadas = reorganizar_fase4_semana1()
    
    # 2. Criar Tech Challenge - Semana 2
    print("\n🏆 ETAPA 2: Criar Tech Challenge - Semana 2 (03-09/11)")
    tc_id = create_tech_challenge_card()
    
    # 3. Criar Projetos de Portfolio
    print("\n📦 ETAPA 3: Criar Projetos de Portfolio")
    projetos = create_portfolio_projects()
    
    print("\n" + "=" * 60)
    print("✅ REORGANIZAÇÃO COMPLETA!")
    print(f"   - {aulas_reorganizadas} aulas FIAP reorganizadas")
    print(f"   - Tech Challenge: {'✅' if tc_id else '❌'}")
    print(f"   - Projetos Portfolio: {len(projetos)} criados")
    
    print("\n📋 Próximos Passos:")
    print("1. Verificar aulas no Notion")
    print("2. Verificar Tech Challenge criado")
    print("3. Verificar Projetos Portfolio criados")
    print("4. Adicionar conteúdo detalhado aos cards")
    print("5. Planejar IA Master")

if __name__ == "__main__":
    main()










