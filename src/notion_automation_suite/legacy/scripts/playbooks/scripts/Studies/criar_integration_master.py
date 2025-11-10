#!/usr/bin/env python3
"""
Criar curso Integration Master no Notion
- Card principal
- Seções como sub-itens
- Aulas como sub-itens das seções
"""

import requests
from datetime import datetime
import pytz

# Configuração
NOTION_TOKEN = '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'
NOTION_VERSION = '2022-06-28'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'
FORMACOES_CURSOS_ID = '294962a7-693c-814c-867d-c81836cece10'  # ID do card "Formações e Cursos"

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

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

# Estrutura COMPLETA do curso Integration Master
CURSO = {
    "titulo": "Integration Master",
    "icon": {"type": "emoji", "emoji": "🔌"},
    "secoes": [
        {
            "titulo": "01 - Introdução",
            "aulas": [
                "001 - Boas-vindas e recados importantes [NÃO PULAR]",
                "[IMPORTANTE] - Comunidade no WhatsApp",
            ]
        },
        {
            "titulo": "02 - Configuração de ambiente",
            "aulas": [
                "002 - Instalando o Python no Windows",
                "003 - Instalando e configurando o VS Code (temas e extensões)",
                "004 - [AVISO IMPORTANTE] PIP e VENV",
                "005 - Configurando ambiente Linux",
                "006 - Política de execução Powershell [Windows]",
            ]
        },
        {
            "titulo": "03 - Começando pelo começo",
            "aulas": [
                "007 - Strings e seus Métodos",
                "008 - Operadores Lógicos no Python",
                "009 - Funções em Python",
                "010 - Laços de Repetição (FOR / WHILE)",
                "011 - Dicionários e seus Métodos",
                "012 - Listas e seus Métodos",
                "013 - Compreensão de Listas",
                "014 - Variáveis de Ambiente",
            ]
        },
        {
            "titulo": "04 - Alguns conceitos importantes",
            "aulas": [
                "015 - O que é PIP?",
                "016 - Ambientes Virtuais (venv)",
                "017 - Conceito de POO com Python",
            ]
        },
        {
            "titulo": "05 - Introdução à integrações",
            "aulas": [
                "018 - Sobre integrações de sistemas",
                "019 - Sobre API Rest e HTTP",
                "020 - Sobre métodos HTTP",
                "021 - Sobre status code",
                "022 - Sobre autenticações de APIs",
            ]
        },
        {
            "titulo": "06 - Integrações com Python",
            "aulas": [
                "023 - Integrações com Python requests",
                "024 - API de cotação de moedas",
                "025 - Sobre clients e services",
                "026 - API de envio de mensagens no WhatsApp",
            ]
        },
        {
            "titulo": "07 - Webhooks",
            "aulas": [
                "027 - O que são webhooks?",
                "028 - Rodando o SGE",
                "029 - Gerando e enviando eventos",
                "030 - Boas práticas de eventos",
                "031 - Ajustando dados do evento",
                "032 - Criando sistema para processar eventos",
                "033 - Completando o ciclo do evento",
                "034 - Armazenando eventos (parte 1)",
                "035 - Armazenando eventos (parte 2)",
                "036 - Integrando Api do WhatsApp ao sistema",
                "037 - Configurando variáveis de ambiente da Api",
                "038 - Montando e enviando a mensagem",
                "039 - Enviando emails automáticos no sistema",
                "040 - Criando template de email",
                "041 - Ajustando o signals do evento",
            ]
        },
        {
            "titulo": "08 - Introdução à serviços de Inteligência Artificial",
            "aulas": [
                "042 - Entendendo serviços, modelos e demandas de IA",
                "043 - Formas de consumir modelos de IA",
            ]
        },
        {
            "titulo": "09 - Integrando com a OpenAI (GPT)",
            "aulas": [
                "044 - Criando conta e analisando modelo de cobrança",
                "045 - Api Key e primeira integração",
                "046 - Resposta em formato de stream",
                "047 - Contexto e agentes",
                "048 - Explorando mais parâmetros",
                "049 - Demonstração de integração com sistema de gestão",
                "050 - Criando nosso agente",
                "051 - Ajustando os prompts",
                "052 - Alimentando agente com dados (RAG)",
                "053 - Armazenando resultados do agente",
                "054 - Criando comando para invocar agente",
                "055 - Mostrando resultados do agente no dashboard",
            ]
        },
        {
            "titulo": "10 - Integração com API de emissão de NF-e/NFS-e",
            "aulas": [
                "056 - NF-e x NFS-e",
                "057 - Certificado digital A1",
                "058 - Sobre APIs de emissão",
                "059 - Conhecendo a Webmania API",
                "060 - Conhecendo o painel e configurando a empresa",
                "061 - Emitindo a primeira NFS via API",
                "062 - Consultando um lote de NFS",
                "063 - Baixando o PDF da NFS",
                "064 - Baixando o XML da NFS",
                "065 - Criando o client da API",
                "066 - Correção do client e métodos",
                "067 - Implementando busca de NFS",
                "068 - Implementando download de PDFs",
                "069 - Implementando download de XMLS",
                "070 - Emissão simplificada para MEI",
            ]
        },
        {
            "titulo": "11 - Integração com API de pagamentos",
            "aulas": [
                "071 - Configurações iniciais Mercado Pago",
                "072 - API vs SDK",
                "073 - Gerando Pix",
                "074 - Gerando Boleto",
                "075 - Pagamentos com Cartão de Crédito",
                "076 - Criando nosso checkout",
                "077 - Criando o client da Api",
                "078 - Implementando métodos privados",
                "079 - Finalizando o client",
                "080 - Utilizando o client na aplicação",
                "081 - Finalizando nosso checkout",
                "CERTIFICADO",
            ]
        },
    ]
}

def main():
    print("🚀 Criando curso Integration Master no Notion...\n")
    
    # 1. Criar card principal do curso
    print("📚 Criando card principal 'Integration Master'...")
    curso_props = {
        "Project name": {"title": [{"text": {"content": CURSO["titulo"]}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Média"}},
        "Categorias": {"multi_select": [{"name": "Curso"}, {"name": "Integração"}]},
    }
    
    curso_card = create_page(
        ESTUDOS_DB, 
        curso_props, 
        parent_id=FORMACOES_CURSOS_ID, 
        icon=CURSO["icon"]
    )
    
    if not curso_card:
        print("❌ Falha ao criar card principal do curso!")
        return
    
    curso_card_id = curso_card['id']
    print(f"✅ Card principal criado! ID: {curso_card_id}\n")
    
    # 2. Criar seções e aulas
    total_secoes = 0
    total_aulas = 0
    
    for secao_data in CURSO["secoes"]:
        secao_titulo = secao_data["titulo"]
        print(f"\n📂 Criando seção: {secao_titulo}")
        
        # Criar seção
        secao_props = {
            "Project name": {"title": [{"text": {"content": secao_titulo}}]},
            "Status": {"status": {"name": "Para Fazer"}},
            "Prioridade": {"select": {"name": "Média"}},
            "Categorias": {"multi_select": [{"name": "Seção"}, {"name": "Integração"}]},
        }
        
        secao_card = create_page(
            ESTUDOS_DB,
            secao_props,
            parent_id=curso_card_id,
            icon={"type": "emoji", "emoji": "📁"}
        )
        
        if not secao_card:
            print(f"   ❌ Falha ao criar seção: {secao_titulo}")
            continue
        
        secao_card_id = secao_card['id']
        total_secoes += 1
        print(f"   ✅ Seção criada! Criando {len(secao_data['aulas'])} aulas...")
        
        # Criar aulas da seção
        for idx, aula_titulo in enumerate(secao_data['aulas'], 1):
            aula_props = {
                "Project name": {"title": [{"text": {"content": aula_titulo}}]},
                "Status": {"status": {"name": "Para Fazer"}},
                "Prioridade": {"select": {"name": "Média"}},
                "Categorias": {"multi_select": [{"name": "Aula"}, {"name": "Integração"}]},
            }
            
            aula_card = create_page(
                ESTUDOS_DB,
                aula_props,
                parent_id=secao_card_id,
                icon={"type": "emoji", "emoji": "📝"}
            )
            
            if aula_card:
                print(f"      ✅ {idx}/{len(secao_data['aulas'])}: {aula_titulo}")
                total_aulas += 1
            else:
                print(f"      ❌ {idx}/{len(secao_data['aulas'])}: {aula_titulo}")
    
    print(f"\n\n{'='*60}")
    print(f"✅ INTEGRATION MASTER CRIADO COM SUCESSO!")
    print(f"📊 Total de seções criadas: {total_secoes}")
    print(f"📝 Total de aulas criadas: {total_aulas}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()










