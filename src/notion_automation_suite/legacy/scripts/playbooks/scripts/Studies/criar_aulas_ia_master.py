#!/usr/bin/env python3
"""
Criar todas as aulas do curso IA Master como sub-itens das sessões
"""

import requests
from datetime import datetime, timedelta
import pytz

# Configuração
NOTION_TOKEN = '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'
NOTION_VERSION = '2022-06-28'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

# Timezone
gmt3 = pytz.timezone('America/Sao_Paulo')

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

def format_date_gmt3(dt):
    """Formata datetime para GMT-3."""
    if dt.tzinfo is None:
        dt = gmt3.localize(dt)
    return dt.isoformat()

def query_database(database_id, filter_data=None):
    """Query Notion database."""
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    payload = {'filter': filter_data} if filter_data else {}
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"❌ Erro ao consultar database: {response.status_code} - {response.text}")
        return []

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
        print(f"❌ Erro ao criar página: {response.status_code} - {response.text}")
        return None

def find_session_by_title(title):
    """Encontra uma sessão pelo título."""
    filter_data = {
        "property": "Project name",
        "title": {
            "contains": title
        }
    }
    results = query_database(ESTUDOS_DB, filter_data)
    return results[0]['id'] if results else None

# Estrutura completa das sessões e aulas
SESSOES = {
    "01 - Introdução à serviços de Inteligência Artificial": [
        "[IMPORTANTE] - Comunidade no WhatsApp",
        "001 - Entendendo serviços, modelos e demandas de IA",
        "002 - Formas de consumir modelos de IA"
    ],
    "02 - Integrando com a OpenAI (GPT)": [
        "003 - Criando conta e analisando modelo de cobrança",
        "004 - Api Key e primeira integração",
        "005 - Resposta em formato de stream",
        "006 - Contexto e Agentes",
        "007 - Explorando mais parâmetros",
        "008 - Modelo para gerar imagens",
        "009 - Modelo para gerar áudios",
        "010 - Modelo para transcrever áudios"
    ],
    "03 - Introdução ao LangChain": [
        "CÓDIGOS E PROJETOS - MÓDULO 03",
        "011 - O que é LangChain? Vantagens de uso",
        "012 - Ecossistema e pacotes do LangChain",
        "013 - Primeiro exemplo com LangChain",
        "014 - Caching de prompts",
        "015 - Prompt Templates",
        "016 - Chat Prompt Templates",
        "017 - Simple Chains",
        "018 - Router Chains",
        "019 - Loaders (txt, pdf e csv)"
    ],
    "04 - Agentes e Ferramentas": [
        "CÓDIGOS E PROJETOS - MÓDULO 04",
        "020 - Introdução à Agents e Tools",
        "021 - Sobre Tools",
        "022 - Tools nativas",
        "023 - Criando um agent com search tool",
        "024 - Criando um agent com Python REPL tool",
        "025 - Criando um agent assistente financeiro",
        "026 - Criando um agent com banco de dados SQL"
    ],
    "05 - RAG (Retrieval-Augmented Generation)": [
        "CÓDIGOS E PROJETOS - MÓDULO 05",
        "027 - RAG e vetores (como um modelo de IA funciona)",
        "028 - Embedding, chunk e overlap",
        "029 - Sobre vector stores",
        "030 - RAG com pdf (criando banco de vetores)",
        "031 - RAG com pdf (executando o modelo)",
        "032 - RAG com pdf (vector store persistido)",
        "033 - Usando vector store persistido",
        "034 - RAG com csv",
        "035 - Assistentes com RAG na OpenAI"
    ],
    "06 - Aplicações de IA com Streamlit": [
        "CÓDIGOS E PROJETOS - MÓDULO 06",
        "036 - Sobre Streamlit e IA",
        "037 - Construindo a interface do app (parte 1)",
        "038 - Construindo a interface do app (parte 2)",
        "039 - Criando o agente de estoque",
        "040 - Ajuste de variável de ambiente"
    ],
    "07 - ChatBot com IA": [
        "CÓDIGOS E PROJETOS - MÓDULO 07",
        "041 - Introdução à ChatBots com IA",
        "042 - Criando a interface do ChatBot",
        "043 - Implementando RAG no ChatBot",
        "044 - Configurando vector store no ChatBot",
        "045 - Implementando histórico de mensagens",
        "046 - Testando o ChatBot"
    ],
    "08 - Dicas, Truques e Ferramentas": [
        "047 - Groq e modelos grátis",
        "048 - Usando Groq nos seus projetos",
        "049 - Ollama e IAs locais",
        "050 - Usando Ollama nos seus projetos",
        "051 - Usando a API do Ollama",
        "052 - Open WebUI"
    ],
    "09 - ChatBot com IA para WhatsApp": [
        "053 - Conhecendo o nosso projeto",
        "054 - Subindo o EvolutionAPI",
        "055 - Conectando instância do WhatsApp e enviando mensagens",
        "056 - Criando a API e Webhook com FastAPI",
        "057 - Configurando Webhooks de eventos",
        "058 - Respondendo mensagens recebidas",
        "059 - RAG (treinando o chatbot com seus dados)",
        "060 - Variáveis de ambiente e ajustes de config",
        "061 - Prompts e chains",
        "062 - Chain principal e finalização",
        "063 - Dicas para usar o projeto",
        "064 - Implementando debounce/buffer",
        "065 - Criando nosso buffer message",
        "066 - Criando a task do debounce",
        "067 - Finalizando e testando o buffer"
    ],
    "10 - MCP": [
        "01 - Entendendo MCP",
        "02 - MCP Server e MCP Client",
        "03 - A grande vantagem",
        "04 - Agente sem MCP",
        "05 - Agente com MCP",
        "06 - MCP Servers com FastMCP",
        "07 - Deploy do MCP Server",
        "CERTIFICADO"
    ],
    "11 - IA para Devs": [
        "01 - Introdução ao módulo",
        "02 - Ferramentas e formas de uso",
        "03 - Setup de IA, planos e limites",
        "04 - Instalando o Claude Code",
        "05 - Instalando e configurando MCP Servers",
        "06 - Sub agentes",
        "07 - Usando os agentes no projeto",
        "08 - Frontend completo com IA",
        "09 - Ajustes de design com IA",
        "10 - Novas features com IA",
        "11 - Comando init",
        "12 - Comandos compact e clear",
        "13 - Programador VS Desenvolvedor",
        "14 - Spec-Driven Development",
        "15 - Criando o Finanpy",
        "16 - Criando e refinando o PRD",
        "17 - Gerando a documentação com IA",
        "18 - Criando os agentes do projeto",
        "19 - Fluxo de trabalho com IA",
        "20 - Contornando os limites das IAs",
        "21 - Trabalhando com Codex"
    ]
}

def main():
    print("🚀 Criando aulas do IA Master...\n")
    
    total_criadas = 0
    
    for sessao_titulo, aulas in SESSOES.items():
        print(f"\n📚 Buscando sessão: {sessao_titulo}")
        
        # Buscar a sessão
        session_id = find_session_by_title(sessao_titulo)
        
        if not session_id:
            print(f"   ⚠️  Sessão não encontrada: {sessao_titulo}")
            continue
        
        print(f"   ✅ Sessão encontrada! Criando {len(aulas)} aulas...")
        
        # Criar cada aula como sub-item
        for idx, aula_titulo in enumerate(aulas, 1):
            # Determinar duração (15 min para aulas normais)
            duracao_minutos = 15
            
            # Aulas especiais sem tempo de estudo
            if aula_titulo.startswith("[IMPORTANTE]") or aula_titulo.startswith("CÓDIGOS") or aula_titulo == "CERTIFICADO":
                duracao_minutos = 0
            
            aula_props = {
                "Project name": {"title": [{"text": {"content": aula_titulo}}]},
                "Status": {"status": {"name": "Para Fazer"}},
                "Prioridade": {"select": {"name": "Média"}},
                "Categorias": {"multi_select": [{"name": "IA"}, {"name": "Curso"}]},
                "Tempo Total": {"rich_text": [{"text": {"content": f"{duracao_minutos} min"}}]}
            }
            
            aula = create_page(ESTUDOS_DB, aula_props, parent_id=session_id, icon={"type": "emoji", "emoji": "📝"})
            
            if aula:
                print(f"      ✅ {idx}/{len(aulas)}: {aula_titulo}")
                total_criadas += 1
            else:
                print(f"      ❌ {idx}/{len(aulas)}: {aula_titulo}")
    
    print(f"\n\n{'='*60}")
    print(f"✅ CONCLUÍDO! {total_criadas} aulas criadas com sucesso!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()

