#!/usr/bin/env python3
"""
Script para criar card do projeto Sphinx no Notion
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from core import NotionAPIManager, NotionConfig, WorkCardCreator, TaskStatus, Priority, DatabaseType
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sphinx_card():
    """Cria card para o projeto Sphinx."""
    print("=" * 60)
    print("📚 CRIANDO CARD DO PROJETO SPHINX - NOTION")
    print("=" * 60)
    
    try:
        # Carregar configuração
        config = NotionConfig.from_env()
        
        # Criar gerenciador
        notion_manager = NotionAPIManager(config)
        
        # Testar conexão
        logger.info("Testando conexão com Notion...")
        if not notion_manager.test_connection():
            logger.error("Falha na conexão com Notion")
            return False
        
        # Criar criador de cards
        creator = WorkCardCreator(notion_manager)
        
        # Propriedades do card Sphinx
        properties = {
            "Nome do projeto": creator.create_title_property(
                "ExpenseIQ - Documentação Sphinx Completa"
            ),
            "Cliente": creator.create_select_property("Astracode"),
            "Projeto": creator.create_select_property("Expense IQ"),
            "Status": creator.create_status_property(TaskStatus.IN_PROGRESS),
            "Prioridade": creator.create_select_property(Priority.HIGH.value),
            "Periodo": creator.create_date_property("2025-09-26", "2025-10-05"),
            "item principal": creator.create_relation_property("24e962a7-693c-801e-aaca-d17f17960378")
        }
        
        # Criar página com ícone e capa
        result = notion_manager.create_page(
            DatabaseType.WORK, 
            properties, 
            icon="📚"
        )
        
        if result:
            print(f"✅ Card criado com sucesso!")
            print(f"📋 ID: {result['id']}")
            print(f"🔗 URL: {result.get('url', 'N/A')}")
            
            # Adicionar conteúdo detalhado ao card
            add_detailed_content(notion_manager, result['id'])
            
            return result
        else:
            print("❌ Falha ao criar card")
            return False
            
    except Exception as e:
        logger.error(f"Erro na execução: {str(e)}")
        return False

def add_detailed_content(notion_manager, page_id):
    """Adiciona conteúdo detalhado ao card criado."""
    try:
        # Conteúdo detalhado sobre o projeto Sphinx
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "📚 Projeto Sphinx - Documentação Completa ExpenseIQ"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "Criação de documentação completa e automatizada usando Sphinx para compilar todas as APIs e fluxos do sistema ExpenseIQ."}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🎯 Objetivos"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Compilar todas as documentações das APIs em um único local"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Integrar com Redoc para atualização automática"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Incluir fluxos de uso e diagramas"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Servir documentação via nginx em porta separada"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📋 Estrutura do Projeto"}}]
                }
            },
            {
                "object": "block",
                "type": "code",
                "code": {
                    "language": "text",
                    "rich_text": [{"type": "text", "text": {"content": "docs/\n├── sphinx/\n│   ├── conf.py\n│   ├── index.rst\n│   ├── requirements.txt\n│   ├── source/\n│   │   ├── api/\n│   │   │   ├── index.rst\n│   │   │   ├── user-service.rst\n│   │   │   ├── company-service.rst\n│   │   │   ├── advance-service.rst\n│   │   │   ├── reports-service.rst\n│   │   │   ├── receipt-service.rst\n│   │   │   ├── ocr-service.rst\n│   │   │   └── documents-service.rst\n│   │   ├── flows/\n│   │   │   ├── index.rst\n│   │   │   ├── implementation-flow.rst\n│   │   │   ├── receipt-management-flow.rst\n│   │   │   ├── report-management-flow.rst\n│   │   │   └── advance-management-flow.rst\n│   │   └── diagrams/\n│   │       ├── index.rst\n│   │       └── *.md\n│   ├── build/\n│   └── static/\n└── nginx/\n    └── sphinx.conf"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🔧 Configuração Sphinx"}}]
                }
            },
            {
                "object": "block",
                "type": "code",
                "code": {
                    "language": "python",
                    "rich_text": [{"type": "text", "text": {"content": "# conf.py\nextensions = [\n    'sphinxcontrib.redoc',\n    'myst_parser',\n    'sphinxcontrib.mermaid'\n]\n\n# Configuração Redoc\nredoc = [\n    {\n        'name': 'User Service API',\n        'page': 'api/user-service',\n        'spec': 'http://0.0.0.0:8001/openapi.json',\n        'embed': True,\n    },\n    {\n        'name': 'Company Service API', \n        'page': 'api/company-service',\n        'spec': 'http://0.0.0.0:8003/openapi.json',\n        'embed': True,\n    }\n]"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🔄 Integração Automática"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Redoc embebido para cada serviço"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Webhooks para atualização automática"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Scripts de build automatizado"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📊 Conteúdo Incluído"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Todas as APIs dos 7 serviços (131 endpoints)"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Fluxos de uso completos"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Diagramas Mermaid para visualização"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Exemplos de uso e validações"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "⏱️ Tempo Estimado"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "🕒 Tempo total estimado: 2-3 dias"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Setup inicial: 4 horas"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Configuração Redoc: 6 horas"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Integração fluxos: 8 horas"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Configuração nginx: 2 horas"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🚀 Próximos Passos"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "1. Completar tarefas pendentes da documentação atual"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "2. Implementar projeto Sphinx base"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "3. Configurar integração com Redoc"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "4. Integrar fluxos e diagramas"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "5. Configurar nginx e deploy"}}]
                }
            }
        ]
        
        # Adicionar blocos à página
        response = notion_manager.session.post(
            f"{notion_manager.base_url}/blocks/{page_id}/children",
            json={"children": blocks},
            timeout=notion_manager.config.timeout
        )
        
        if response.status_code == 200:
            print("✅ Conteúdo detalhado adicionado ao card")
        else:
            print(f"❌ Erro ao adicionar conteúdo: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao adicionar conteúdo: {str(e)}")

def main():
    """Função principal."""
    result = create_sphinx_card()
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 CARD SPHINX CRIADO COM SUCESSO!")
        print("=" * 60)
        print(f"📋 ID: {result['id']}")
        print(f"🔗 URL: {result.get('url', 'N/A')}")
        print("\n💡 O card contém toda a especificação do projeto Sphinx")
        print("📚 Inclui estrutura, configuração, tempo estimado e próximos passos")
        return True
    else:
        print("\n❌ Falha ao criar card")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
