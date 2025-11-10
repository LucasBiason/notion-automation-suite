#!/usr/bin/env python3
"""
Cronograma Master Completo
- Reorganiza FIAP Fase 4 (Semana 1)
- Cria Tech Challenge (Semana 2)
- Cria fases dos projetos de portfolio
- Organiza cronograma dos demais cursos
"""

import requests
from datetime import datetime, timedelta
import pytz

# Configuração
NOTION_TOKEN = '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'
NOTION_VERSION = '2022-06-28'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

# IDs importantes
FASE4_CARD_ID = '279962a7-693c-8005-84ea-ca97a3bfab25'
PORTFOLIO_CARD_ID = '294962a7-693c-81be-afc2-e098c9ac8b92'

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

tz = pytz.timezone('America/Sao_Paulo')

def format_date_gmt3(dt):
    """Formata data para GMT-3 (São Paulo)."""
    if dt.tzinfo is None:
        dt = tz.localize(dt)
    return dt.isoformat()

def query_database(database_id, filter_params=None):
    """Consulta database do Notion."""
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    payload = {}
    if filter_params:
        payload['filter'] = filter_params
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao consultar: {response.status_code} - {response.text}")
        return None

def update_page(page_id, properties):
    """Atualiza uma página no Notion."""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    payload = {'properties': properties}
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao atualizar: {response.status_code} - {response.text}")
        return None

def create_page(database_id, properties, parent_id=None, icon=None):
    """Cria uma página no Notion."""
    url = 'https://api.notion.com/v1/pages'
    
    payload = {
        'parent': {'database_id': database_id},
        'properties': properties
    }
    
    if parent_id:
        payload['properties']['Parent item'] = {"relation": [{"id": parent_id}]}
    
    if icon:
        payload['icon'] = icon
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao criar: {response.status_code} - {response.text}")
        return None

print("="*70)
print("🚀 CRONOGRAMA MASTER - ROADMAP 2025-2026")
print("="*70)

# ============================================================
# PARTE 1: REORGANIZAR FIAP FASE 4 (SEMANA 1)
# ============================================================
print("\n📚 PARTE 1: Reorganizando FIAP Fase 4 (Semana 1: 27/10-31/10)...\n")

# Buscar todas as aulas da Fase 4
filter_fase4 = {
    "property": "Parent item",
    "relation": {
        "contains": FASE4_CARD_ID
    }
}

aulas_fase4 = query_database(ESTUDOS_DB, filter_fase4)

if not aulas_fase4 or len(aulas_fase4['results']) == 0:
    print("❌ Nenhuma aula da Fase 4 encontrada!")
else:
    aulas = []
    for page in aulas_fase4['results']:
        titulo = page['properties']['Project name']['title'][0]['text']['content']
        page_id = page['id']
        
        # Extrair duração se existir
        tempo_prop = page['properties'].get('Tempo Total', {})
        tempo_text = tempo_prop.get('rich_text', [])
        duracao_str = tempo_text[0]['text']['content'] if tempo_text else "1h"
        
        # Converter duração para minutos
        if 'h' in duracao_str:
            horas = int(duracao_str.split('h')[0].strip())
            duracao_min = horas * 60
        elif 'min' in duracao_str or 'm' in duracao_str:
            duracao_min = int(duracao_str.replace('min', '').replace('m', '').strip())
        else:
            duracao_min = 60  # padrão 1h
        
        aulas.append({
            'id': page_id,
            'titulo': titulo,
            'duracao_min': duracao_min
        })
    
    print(f"✅ {len(aulas)} aulas encontradas na Fase 4\n")
    
    # Reorganizar cronograma
    data_atual = datetime(2025, 10, 27, 8, 0)  # Segunda 27/10 às 8:00
    REVISAO_MIN = 50  # 50 min de revisão após cada aula
    
    aulas_reorganizadas = 0
    
    for aula in aulas:
        # Pular terça-feira após 15:00 (médico)
        if data_atual.weekday() == 1 and data_atual.hour >= 15:  # Terça (1) às 15:00
            # Pular para quarta 8:00
            data_atual = data_atual.replace(day=29, hour=8, minute=0)
        
        # Pular fins de semana
        if data_atual.weekday() >= 5:  # Sábado (5) ou Domingo (6)
            # Pular para segunda 8:00
            dias_ate_segunda = 7 - data_atual.weekday()
            data_atual = data_atual + timedelta(days=dias_ate_segunda)
            data_atual = data_atual.replace(hour=8, minute=0)
        
        # Calcular fim da aula
        data_fim = data_atual + timedelta(minutes=aula['duracao_min'])
        
        # Se ultrapassar 20:00, mover para o próximo dia
        if data_fim.hour >= 20:
            data_atual = data_atual + timedelta(days=1)
            data_atual = data_atual.replace(hour=8, minute=0)
            data_fim = data_atual + timedelta(minutes=aula['duracao_min'])
        
        # Atualizar aula no Notion
        props = {
            "Período": {
                "date": {
                    "start": format_date_gmt3(data_atual),
                    "end": format_date_gmt3(data_fim)
                }
            }
        }
        
        resultado = update_page(aula['id'], props)
        if resultado:
            print(f"   ✅ {aula['titulo']}")
            print(f"      📅 {data_atual.strftime('%d/%m %H:%M')} - {data_fim.strftime('%H:%M')}")
            aulas_reorganizadas += 1
        
        # Avançar para próxima aula (aula + revisão)
        data_atual = data_fim + timedelta(minutes=REVISAO_MIN)
    
    print(f"\n✅ {aulas_reorganizadas} aulas da Fase 4 reorganizadas!\n")

# ============================================================
# PARTE 2: CRIAR TECH CHALLENGE (SEMANA 2)
# ============================================================
print("\n🎯 PARTE 2: Criando Tech Challenge (Semana 2)...\n")

# Criar card do Tech Challenge
tech_props = {
    "Project name": {"title": [{"text": {"content": "Tech Challenge - Fase 4"}}]},
    "Status": {"status": {"name": "Para Fazer"}},
    "Prioridade": {"select": {"name": "Crítica"}},
    "Categorias": {"multi_select": [{"name": "Projeto"}, {"name": "FIAP"}]},
    "Período": {
        "date": {
            "start": format_date_gmt3(datetime(2025, 11, 3, 8, 0)),
            "end": format_date_gmt3(datetime(2025, 11, 7, 20, 0))
        }
    },
    "Descrição": {"rich_text": [{"text": {"content": "Projeto Tech Challenge da Fase 4 - Análise de Dados com IA"}}]}
}

tech_card = create_page(
    ESTUDOS_DB,
    tech_props,
    parent_id=FASE4_CARD_ID,
    icon={"type": "emoji", "emoji": "🎯"}
)

if tech_card:
    print(f"✅ Tech Challenge criado!")
    print(f"   📅 Semana 2: 03/11 a 07/11 (8:00-20:00)\n")
else:
    print("❌ Erro ao criar Tech Challenge!\n")

# ============================================================
# PARTE 3: CRIAR FASES DOS PROJETOS DE PORTFOLIO
# ============================================================
print("\n💼 PARTE 3: Criando fases dos projetos de portfolio...\n")

# Definir projetos e suas fases
PROJETOS_PORTFOLIO = [
    {
        "nome": "MyLocalPlace v2.0",
        "icon": {"type": "emoji", "emoji": "🏠"},
        "fases": [
            "Fase 1: Análise e Documentação",
            "Fase 2: Modernização Docker Compose",
            "Fase 3: Dashboard Streamlit",
            "Fase 4: Automação e Scripts",
            "Fase 5: Documentação e Deploy"
        ]
    },
    {
        "nome": "Notion MCP Server",
        "icon": {"type": "emoji", "emoji": "🔌"},
        "fases": [
            "Fase 1: Core MCP Protocol",
            "Fase 2: Notion Service Layer",
            "Fase 3: Custom Notion Classes",
            "Fase 4: Testes e Validação",
            "Fase 5: Documentação e Deploy"
        ]
    },
    {
        "nome": "FastAPI Microservice Framework",
        "icon": {"type": "emoji", "emoji": "⚡"},
        "fases": [
            "Fase 1: Core Framework",
            "Fase 2: Middlewares (Auth, Log, Error)",
            "Fase 3: Database Layer (Singleton)",
            "Fase 4: Cache e Queue Tools",
            "Fase 5: Publicação GitHub Packages"
        ]
    },
    {
        "nome": "IntelliCart E-commerce",
        "icon": {"type": "emoji", "emoji": "🛒"},
        "fases": [
            "Fase 1: Arquitetura CQRS + Event Sourcing",
            "Fase 2: Gestão de Produtos e Estoque",
            "Fase 3: API Carrinho e Buscas",
            "Fase 4: Integração IA (Recomendações)",
            "Fase 5: Deploy Local (Minikube)"
        ]
    }
]

# Buscar projetos existentes ou criar
for projeto_data in PROJETOS_PORTFOLIO:
    print(f"📦 Processando: {projeto_data['nome']}...")
    
    # Buscar projeto
    filter_projeto = {
        "property": "Project name",
        "title": {
            "contains": projeto_data['nome']
        }
    }
    
    resultado_busca = query_database(ESTUDOS_DB, filter_projeto)
    
    if resultado_busca and len(resultado_busca['results']) > 0:
        projeto_id = resultado_busca['results'][0]['id']
        print(f"   ✅ Projeto encontrado!")
    else:
        # Criar projeto
        projeto_props = {
            "Project name": {"title": [{"text": {"content": projeto_data['nome']}}]},
            "Status": {"status": {"name": "Para Fazer"}},
            "Prioridade": {"select": {"name": "Alta"}},
            "Categorias": {"multi_select": [{"name": "Projeto"}, {"name": "Portfolio"}]},
        }
        
        projeto_criado = create_page(
            ESTUDOS_DB,
            projeto_props,
            parent_id=PORTFOLIO_CARD_ID,
            icon=projeto_data['icon']
        )
        
        if not projeto_criado:
            print(f"   ❌ Erro ao criar projeto!")
            continue
        
        projeto_id = projeto_criado['id']
        print(f"   ✅ Projeto criado!")
    
    # Criar fases
    for fase_nome in projeto_data['fases']:
        fase_props = {
            "Project name": {"title": [{"text": {"content": fase_nome}}]},
            "Status": {"status": {"name": "Para Fazer"}},
            "Prioridade": {"select": {"name": "Alta"}},
            "Categorias": {"multi_select": [{"name": "Fase"}, {"name": "Portfolio"}]},
        }
        
        fase_criada = create_page(
            ESTUDOS_DB,
            fase_props,
            parent_id=projeto_id,
            icon={"type": "emoji", "emoji": "📋"}
        )
        
        if fase_criada:
            print(f"      ✅ {fase_nome}")
        else:
            print(f"      ❌ {fase_nome}")
    
    print()

print("\n" + "="*70)
print("✅ CRONOGRAMA MASTER COMPLETO!")
print("="*70)
print("\n📊 Próximos passos:")
print("   1. FIAP Fase 4: 27/10-31/10 (Semana 1)")
print("   2. Tech Challenge: 03/11-07/11 (Semana 2)")
print("   3. IA Master + demais cursos: a partir de 10/11")
print("   4. Projetos Portfolio: paralelo aos estudos")
print("\n")

