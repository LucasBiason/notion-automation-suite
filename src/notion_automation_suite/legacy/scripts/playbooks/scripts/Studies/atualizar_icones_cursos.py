#!/usr/bin/env python3
"""
Atualizar ícones dos cursos e seções
"""

import requests

# Configuração
NOTION_TOKEN = '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'
NOTION_VERSION = '2022-06-28'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'
FORMACOES_CURSOS_ID = '294962a7-693c-814c-867d-c81836cece10'

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

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
        return None

def update_page_icon(page_id, emoji):
    """Atualiza apenas o ícone de uma página."""
    url = f'https://api.notion.com/v1/pages/{page_id}'
    payload = {
        'icon': {'type': 'emoji', 'emoji': emoji}
    }
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    return response.status_code == 200

print("\n" + "="*70)
print("🎨 ATUALIZANDO ÍCONES DOS CURSOS E SEÇÕES")
print("="*70 + "\n")

# Ícones específicos para cada curso
ICONES_CURSOS = {
    "IA Master": "🎓",
    "Algoritmos Genéticos": "🧬",
    "Pós Tech FIAP": "🎯",
}

# Ícones para seções do IA Master
ICONES_SECOES_IA_MASTER = {
    "01 - Introdução": "👋",
    "02 - Integrando com a OpenAI (GPT)": "🤖",
    "03 - Chamadas de função e Tools (OpenAI)": "🔧",
    "04 - Introdução ao LangChain": "⛓️",
    "05 - LangChain com Modelos de Chat": "💬",
    "06 - LangChain com Agents e Tools": "🔨",
    "07 - RAG com LangChain": "📚",
    "08 - Integrando WhatsApp ao ChatBot": "📱",
    "09 - Criando Buffer e Debounce": "⏱️",
}

# Buscar todos os cursos
filter_cursos = {
    "property": "Parent item",
    "relation": {"contains": FORMACOES_CURSOS_ID}
}

cursos = query_database(ESTUDOS_DB, filter_cursos)

if not cursos or len(cursos['results']) == 0:
    print("❌ Nenhum curso encontrado!\n")
    exit(1)

print(f"📚 {len(cursos['results'])} cursos encontrados\n")

for curso in cursos['results']:
    titulo = curso['properties']['Project name']['title'][0]['text']['content']
    curso_id = curso['id']
    
    # Verificar se precisa atualizar ícone
    icone_novo = None
    
    for nome_curso, emoji in ICONES_CURSOS.items():
        if nome_curso.lower() in titulo.lower():
            icone_novo = emoji
            break
    
    if icone_novo:
        if update_page_icon(curso_id, icone_novo):
            print(f"✅ {icone_novo} {titulo}")
        else:
            print(f"❌ Erro ao atualizar: {titulo}")
    
    # Se for IA Master, atualizar seções também
    if "IA Master" in titulo:
        print(f"   🔍 Atualizando seções do IA Master...\n")
        
        # Buscar seções do IA Master
        filter_secoes = {
            "property": "Parent item",
            "relation": {"contains": curso_id}
        }
        
        secoes = query_database(ESTUDOS_DB, filter_secoes)
        
        if secoes and len(secoes['results']) > 0:
            for secao in secoes['results']:
                secao_titulo = secao['properties']['Project name']['title'][0]['text']['content']
                secao_id = secao['id']
                
                # Buscar ícone específico para esta seção
                icone_secao = ICONES_SECOES_IA_MASTER.get(secao_titulo, "📁")
                
                if update_page_icon(secao_id, icone_secao):
                    print(f"      ✅ {icone_secao} {secao_titulo}")
                else:
                    print(f"      ❌ {secao_titulo}")
        
        print()

print("="*70)
print("✅ Ícones atualizados com sucesso!")
print("="*70 + "\n")










