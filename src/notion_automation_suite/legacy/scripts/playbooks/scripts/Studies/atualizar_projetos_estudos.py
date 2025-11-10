#!/usr/bin/env python3
"""
Criar cards no Notion para projetos de estudos reorganizados
"""

import requests

NOTION_TOKEN = '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'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'
PORTFOLIO_CARD_ID = '294962a7-693c-81be-afc2-e098c9ac8b92'

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def create_page(database_id, properties, parent_id=None, icon=None):
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
        print(f"❌ Erro: {response.status_code} - {response.text}")
        return None

def main():
    print("\n" + "="*70)
    print("📚 CRIANDO CARDS PARA PROJETOS DE ESTUDO")
    print("="*70 + "\n")
    
    projetos = [
        {
            "nome": "RAG Recipe Assistant",
            "icone": "🍳",
            "descricao": "Projeto educacional completo de RAG com LangChain, ChromaDB e 118 receitas. Sistema de recomendação inteligente com busca semântica.",
            "repo": "https://github.com/LucasBiason/rag-recipe-assistant",
            "categorias": ["Portfolio", "IA/ML", "RAG", "LangChain"],
            "tempo": "Completo",
            "status": "Concluido"
        },
        {
            "nome": "ML Spam Classifier API",
            "icone": "📧",
            "descricao": "API de classificação de spam com FastAPI e Naive Bayes. 98.5% accuracy, 100% test coverage, Docker ready.",
            "repo": "https://github.com/LucasBiason/ml-spam-classifier-api",
            "categorias": ["Portfolio", "ML", "NLP", "FastAPI"],
            "tempo": "Completo",
            "status": "Concluido"
        },
        {
            "nome": "ML House Price Predictor",
            "icone": "🏠",
            "descricao": "Predição de preços de imóveis com regressão linear. API FastAPI, feature importance analysis, R² 0.87.",
            "repo": "https://github.com/LucasBiason/ml-house-price-predictor",
            "categorias": ["Portfolio", "ML", "Regression", "FastAPI"],
            "tempo": "Completo",
            "status": "Concluido"
        },
        {
            "nome": "ML Sales Forecasting",
            "icone": "📈",
            "descricao": "API de forecasting de vendas com Prophet e ARIMA. Multi-horizon (7, 30, 90 dias), confidence intervals.",
            "repo": "https://github.com/LucasBiason/ml-sales-forecasting",
            "categorias": ["Portfolio", "ML", "Time Series", "FastAPI"],
            "tempo": "Completo",
            "status": "Concluido"
        },
        {
            "nome": "Python ML Toolkit",
            "icone": "🧰",
            "descricao": "Toolkit privado de utilitários reutilizáveis: audio processing (Whisper), YouTube downloader, OCR, integrações.",
            "repo": "https://github.com/LucasBiason/python-ml-toolkit (PRIVATE)",
            "categorias": ["Portfolio", "Ferramentas", "Reutilizável"],
            "tempo": "40 horas",
            "status": "Concluido"
        }
    ]
    
    criados = []
    
    for projeto in projetos:
        print(f"📝 Criando {projeto['nome']}...")
        
        properties = {
            "Project name": {"title": [{"text": {"content": projeto['nome']}}]},
            "Status": {"status": {"name": projeto['status']}},
            "Prioridade": {"select": {"name": "Alta"}},
            "Categorias": {"multi_select": [{"name": cat} for cat in projeto['categorias']]},
            "Tempo Total": {"rich_text": [{"text": {"content": projeto['tempo']}}]},
            "Descrição": {"rich_text": [{"text": {"content": f"{projeto['descricao']}\n\nRepositório: {projeto['repo']}"}}]}
        }
        
        card = create_page(
            ESTUDOS_DB,
            properties,
            parent_id=PORTFOLIO_CARD_ID,
            icon={"type": "emoji", "emoji": projeto['icone']}
        )
        
        if card:
            criados.append((projeto['nome'], card['id']))
            print(f"✅ {projeto['nome']}")
            print(f"   https://www.notion.so/{card['id'].replace('-', '')}")
        print()
    
    print("="*70)
    print(f"✅ {len(criados)}/5 PROJETOS CRIADOS NO NOTION")
    print("="*70)
    print("\nTodos os projetos estão como 'Concluido' pois já existem")
    print("e foram reorganizados/melhorados.\n")

if __name__ == "__main__":
    main()
