#!/usr/bin/env python3
"""
Script para estruturar o Roadmap Completo no Notion
Cria card principal + subitens com estrutura correta (Parent/Sub-item)
"""

import os
import requests
from datetime import datetime, timedelta
import pytz
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

# Database ID (Base de Cursos)
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

# Timezone GMT-3
gmt3 = pytz.timezone('America/Sao_Paulo')

def format_date_gmt3(date_obj, hour=19, minute=0):
    """Formata data para GMT-3."""
    return gmt3.localize(date_obj).isoformat()

def create_page(database_id, properties, parent_id=None):
    """Cria uma página no Notion."""
    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    
    if parent_id:
        payload["properties"]["Parent item"] = {"relation": [{"id": parent_id}]}
    
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao criar página: {response.status_code} - {response.text}")
        return None

def update_page(page_id, properties):
    """Atualiza uma página existente."""
    response = requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=HEADERS,
        json={"properties": properties}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao atualizar página: {response.status_code} - {response.text}")
        return None

def add_content_to_page(page_id, blocks):
    """Adiciona conteúdo (blocos) a uma página."""
    response = requests.patch(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers=HEADERS,
        json={"children": blocks}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao adicionar conteúdo: {response.status_code} - {response.text}")
        return None

def get_roadmap_main_content():
    """Conteúdo detalhado para o card principal do Roadmap."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Visão Geral do Roadmap"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Este roadmap foi criado para transformar Lucas em um Engenheiro de Software Sênior especializado em IA, com foco em:"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Desenvolvimento de habilidades técnicas avançadas"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Construção de portfolio robusto com projetos reais"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Especialização em IA e Machine Learning"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Preparação para mercado de trabalho competitivo"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📊 Métricas de Sucesso"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "🎯"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Meta: 1000+ horas de estudo e desenvolvimento até dezembro de 2026"}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🚀 Próximos Passos Imediatos"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Finalizar FIAP Fase 4 + Tech Challenge (Prioridade #1)"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Modernizar MyLocalPlace v2.0 (Portfolio rápido)"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Desenvolver FastAPI Microservice Framework"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Construir IntelliCart com CQRS + Event Sourcing"}}]
            }
        }
    ]

def get_formacoes_content():
    """Conteúdo detalhado para Formações e Cursos."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "📚 Estratégia de Formação"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Combinação estratégica de formações para maximizar aprendizado e minimizar sobreposição de conteúdo."}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Prioridades"}}]
            }
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "🥇 FIAP - IA para Devs (ATIVA)"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Formação principal e mais completa. Fase 4 em andamento com foco em OpenAI, AWS e projetos práticos."}
                            }]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "🥈 Udemy - IA e ML (COMPLEMENTAR)"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Reforço e aprofundamento em conceitos fundamentais de IA e Machine Learning."}
                            }]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "🥉 Rocketseat - IA Prática (PROJETOS)"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Foco em projetos práticos e aplicações reais de IA no desenvolvimento."}
                            }]
                        }
                    }
                ]
            }
        }
    ]

def get_portfolio_content():
    """Conteúdo detalhado para Projetos de Portfolio."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "💼 Estratégia de Portfolio"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Portfolio progressivo com projetos de complexidade crescente, demonstrando evolução técnica e capacidade de entrega."}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🚀 Sequência de Desenvolvimento"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "MyLocalPlace v2.0 (Q4 2025) - Portfolio rápido"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "FastAPI Framework (Q1 2026) - Biblioteca reutilizável"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "IntelliCart (Q2-Q3 2026) - Projeto principal com CQRS"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Objetivos por Projeto"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "⚡"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Demonstrar capacidade de modernização e melhoria de sistemas existentes"}
                }]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "🔧"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Mostrar habilidade em criar ferramentas reutilizáveis e bibliotecas"}
                }]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "🏗️"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Aplicar arquiteturas avançadas (CQRS, Event Sourcing) em projetos reais"}
                }]
            }
        }
    ]

def get_mylocalplace_content():
    """Conteúdo detalhado para MyLocalPlace v2.0."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🏠 MyLocalPlace v2.0 - Modernização Completa"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Modernização do ambiente local de desenvolvimento com foco em observabilidade, facilidade de uso e gestão de serviços."
                }]
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
                "rich_text": [{"type": "text", "text": {"content": "Dashboard Streamlit para observabilidade completa"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Gestão individual de serviços (start/stop/monitor)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Adicionar RabbitMQ e ChromaDB"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Makefile melhorado com comandos intuitivos"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🛠️ Tecnologias"}}]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "language": "yaml",
                "rich_text": [{"type": "text", "text": {"content": "Serviços:\n  - PostgreSQL\n  - MongoDB\n  - Redis\n  - RabbitMQ (novo)\n  - ChromaDB (novo)\n  - Ollama\n  - OpenWebUI\n  - LangFlow\n\nFerramentas:\n  - Docker Compose\n  - Streamlit Dashboard\n  - Makefile\n  - Python Scripts"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📋 Fases de Desenvolvimento"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Fase 1: Dashboard Streamlit básico"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Fase 2: Adicionar RabbitMQ e ChromaDB"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Fase 3: Melhorar Makefile e automações"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Fase 4: Documentação e testes"}}]
            }
        }
    ]

def get_fastapi_framework_content():
    """Conteúdo detalhado para FastAPI Microservice Framework."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🔧 FastAPI Microservice Framework"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Biblioteca reutilizável para criação rápida de microserviços FastAPI com padrões de arquitetura, middlewares e ferramentas essenciais."
                }]
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
                "rich_text": [{"type": "text", "text": {"content": "Criar biblioteca reutilizável para microserviços"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Encapsular middlewares essenciais (auth, logging, errors)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Padrão Singleton para acesso a banco de dados"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Ferramentas para cache e filas"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🏗️ Arquitetura"}}]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "language": "python",
                "rich_text": [{"type": "text", "text": {"content": "fastapi-framework/\n├── core/\n│   ├── builder.py          # FastAPI Builder\n│   ├── middlewares.py      # Auth, Logging, Errors\n│   └── database.py         # Singleton DB Access\n├── utils/\n│   ├── cache.py            # Redis Cache\n│   ├── queue.py            # RabbitMQ Queue\n│   └── validators.py       # Pydantic Validators\n├── examples/\n│   └── basic_service.py    # Exemplo de uso\n└── tests/                  # Testes unitários"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📦 Publicação"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "📚"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Será publicado no GitHub Packages como biblioteca Python reutilizável"}
                }]
            }
        }
    ]

def get_intellicart_content():
    """Conteúdo detalhado para IntelliCart."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🛒 IntelliCart - E-commerce com CQRS + Event Sourcing"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "E-commerce completo demonstrando arquiteturas avançadas com CQRS, Event Sourcing e integração de IA para recomendações e busca inteligente."
                }]
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
                "rich_text": [{"type": "text", "text": {"content": "Demonstrar domínio de arquiteturas avançadas (CQRS + Event Sourcing)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Integrar IA para busca inteligente e recomendações"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Criar API completa para carrinho e produtos"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Simular compras (sem gateway de pagamento)"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🏗️ Arquitetura"}}]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "language": "yaml",
                "rich_text": [{"type": "text", "text": {"content": "Microserviços:\n  - Product Service (CQRS)\n  - Cart Service (Event Sourcing)\n  - Order Service (Saga Pattern)\n  - Search Service (IA + Elasticsearch)\n  - Recommendation Service (IA)\n\nTecnologias:\n  - FastAPI + Pydantic\n  - PostgreSQL + EventStore\n  - Redis (Cache)\n  - RabbitMQ (Events)\n  - Elasticsearch (Search)\n  - OpenAI API (IA)\n  - Docker + Kubernetes"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🤖 Funcionalidades de IA"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Busca semântica de produtos"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Recomendações personalizadas"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Análise de sentimento de reviews"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Chatbot para suporte ao cliente"}}]
            }
        }
    ]

def get_ia_knowledge_base_content():
    """Conteúdo detalhado para IA Knowledge Base."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🧠 IA Knowledge Base"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Base de conhecimento estruturada com resumos, exercícios práticos e flashcards para maximizar o aprendizado em IA e Machine Learning."
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📚 Estrutura"}}]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "language": "yaml",
                "rich_text": [{"type": "text", "text": {"content": "ia-ml-knowledge-base/\n├── resumos/\n│   ├── fiap-fase4/\n│   ├── udemy-ia-ml/\n│   └── rocketseat-ia/\n├── exercicios/\n│   ├── openai/\n│   ├── aws/\n│   └── projetos-praticos/\n├── flashcards/\n│   ├── conceitos-fundamentais/\n│   ├── algoritmos-ml/\n│   └── frameworks-ia/\n└── projetos/\n    ├── tech-challenge-fiap/\n    └── portfolio-projects/"}}]
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
                "rich_text": [{"type": "text", "text": {"content": "Centralizar todo conhecimento de IA em um local"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Criar exercícios práticos para cada conceito"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Sistema de flashcards para revisão"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Documentar projetos e aprendizados"}}]
            }
        }
    ]

def main():
    """Função principal - Estrutura o Roadmap Completo."""
    
    print("🚀 ESTRUTURANDO ROADMAP COMPLETO NO NOTION")
    print("="*60)
    
    # 1. CRIAR CARD PRINCIPAL
    print("\n📋 1. Criando card principal...")
    
    main_card_properties = {
        "Project name": {"title": [{"text": {"content": "Roadmap Engenheiro de Software com IA 2025-2026"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Portfolio"}, {"name": "Desenvolvimento"}, {"name": "IA"}]},
        "Período": {
            "date": {
                "start": "2025-10-23T00:00:00.000-03:00",
                "end": "2026-12-31T23:59:59.000-03:00"
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "1000+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Roadmap completo para se tornar Engenheiro de Software com especialização em IA. Inclui formações, projetos de portfolio e desenvolvimento de habilidades técnicas."}}]}
    }
    
    main_card = create_page(ESTUDOS_DB, main_card_properties)
    
    if not main_card:
        print("❌ Falha ao criar card principal!")
        return
    
    main_card_id = main_card['id']
    print(f"✅ Card principal criado: {main_card_id}")
    
    # Adicionar conteúdo detalhado ao card principal
    print("📝 Adicionando conteúdo detalhado ao card principal...")
    add_content_to_page(main_card_id, get_roadmap_main_content())
    
    # 2. CRIAR SUBITENS PRINCIPAIS
    print("\n📋 2. Criando subitens principais...")
    
    # Subitem: Formações e Cursos
    formacoes_properties = {
        "Project name": {"title": [{"text": {"content": "Formações e Cursos"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Estudos"}, {"name": "Formação"}]},
        "Período": {
            "date": {
                "start": "2025-10-23T00:00:00.000-03:00",
                "end": "2026-06-30T23:59:59.000-03:00"
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "400+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Todas as formações e cursos relacionados a IA, desenvolvimento e tecnologias modernas."}}]}
    }
    
    formacoes_card = create_page(ESTUDOS_DB, formacoes_properties, main_card_id)
    if formacoes_card:
        formacoes_id = formacoes_card['id']
        print(f"✅ Formações e Cursos: {formacoes_id}")
        
        # Adicionar conteúdo detalhado
        print("📝 Adicionando conteúdo detalhado às Formações...")
        add_content_to_page(formacoes_id, get_formacoes_content())
    
    # Subitem: Projetos de Portfolio
    portfolio_properties = {
        "Project name": {"title": [{"text": {"content": "Projetos de Portfolio"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Portfolio"}, {"name": "Desenvolvimento"}]},
        "Período": {
            "date": {
                "start": "2025-10-23T00:00:00.000-03:00",
                "end": "2026-12-31T23:59:59.000-03:00"
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "600+ horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Projetos práticos para demonstrar habilidades e construir portfolio profissional."}}]}
    }
    
    portfolio_card = create_page(ESTUDOS_DB, portfolio_properties, main_card_id)
    if portfolio_card:
        portfolio_id = portfolio_card['id']
        print(f"✅ Projetos de Portfolio: {portfolio_id}")
        
        # Adicionar conteúdo detalhado
        print("📝 Adicionando conteúdo detalhado ao Portfolio...")
        add_content_to_page(portfolio_id, get_portfolio_content())
    
    # 3. CRIAR CARDS DE FORMAÇÕES
    print("\n📚 3. Criando cards de formações...")
    
    formacoes_list = [
        {
            "name": "Pós Tech FIAP - IA para Devs",
            "status": "Em andamento",
            "periodo": ("2025-03-27T00:00:00.000-03:00", "2026-02-28T23:59:59.000-03:00"),
            "tempo": "200+ horas",
            "desc": "Formação principal em IA para desenvolvedores - Fase 4 em andamento"
        },
        {
            "name": "Udemy - Formação Completa IA e ML",
            "status": "Para Fazer",
            "periodo": ("2025-11-01T00:00:00.000-03:00", "2026-03-31T23:59:59.000-03:00"),
            "tempo": "100+ horas",
            "desc": "Formação complementar em IA e Machine Learning"
        },
        {
            "name": "Rocketseat - IA na Prática do Zero",
            "status": "Para Fazer",
            "periodo": ("2025-12-01T00:00:00.000-03:00", "2026-02-28T23:59:59.000-03:00"),
            "tempo": "80+ horas",
            "desc": "Formação prática em IA com projetos reais"
        },
        {
            "name": "Rocketseat - IA para Devs",
            "status": "Para Fazer",
            "periodo": ("2026-03-01T00:00:00.000-03:00", "2026-05-31T23:59:59.000-03:00"),
            "tempo": "60+ horas",
            "desc": "Aprofundamento em IA para desenvolvedores"
        }
    ]
    
    for formacao in formacoes_list:
        formacao_properties = {
            "Project name": {"title": [{"text": {"content": formacao["name"]}}]},
            "Status": {"status": {"name": formacao["status"]}},
            "Prioridade": {"select": {"name": "Alta"}},
            "Categorias": {"multi_select": [{"name": "Formação"}, {"name": "IA"}]},
            "Período": {
                "date": {
                    "start": formacao["periodo"][0],
                    "end": formacao["periodo"][1]
                }
            },
            "Tempo Total": {"rich_text": [{"text": {"content": formacao["tempo"]}}]},
            "Descrição": {"rich_text": [{"text": {"content": formacao["desc"]}}]}
        }
        
        formacao_card = create_page(ESTUDOS_DB, formacao_properties, formacoes_id)
        if formacao_card:
            print(f"✅ {formacao['name']}: {formacao_card['id']}")
    
    # 4. CRIAR CARDS DE PROJETOS
    print("\n💼 4. Criando cards de projetos...")
    
    projetos_list = [
        {
            "name": "MyLocalPlace v2.0",
            "status": "Para Fazer",
            "periodo": ("2025-10-23T00:00:00.000-03:00", "2025-12-31T23:59:59.000-03:00"),
            "tempo": "120+ horas",
            "desc": "Modernização do ambiente local de desenvolvimento com dashboard Streamlit"
        },
        {
            "name": "FastAPI Microservice Framework",
            "status": "Para Fazer",
            "periodo": ("2025-11-01T00:00:00.000-03:00", "2026-02-28T23:59:59.000-03:00"),
            "tempo": "200+ horas",
            "desc": "Biblioteca reutilizável para criação de microserviços FastAPI"
        },
        {
            "name": "IntelliCart - E-commerce com CQRS",
            "status": "Para Fazer",
            "periodo": ("2026-01-01T00:00:00.000-03:00", "2026-08-31T23:59:59.000-03:00"),
            "tempo": "300+ horas",
            "desc": "E-commerce completo com CQRS, Event Sourcing e IA"
        },
        {
            "name": "IA Knowledge Base",
            "status": "Em andamento",
            "periodo": ("2025-09-01T00:00:00.000-03:00", "2026-12-31T23:59:59.000-03:00"),
            "tempo": "100+ horas",
            "desc": "Base de conhecimento em IA com resumos e exercícios"
        }
    ]
    
    for projeto in projetos_list:
        projeto_properties = {
            "Project name": {"title": [{"text": {"content": projeto["name"]}}]},
            "Status": {"status": {"name": projeto["status"]}},
            "Prioridade": {"select": {"name": "Alta"}},
            "Categorias": {"multi_select": [{"name": "Portfolio"}, {"name": "Desenvolvimento"}]},
            "Período": {
                "date": {
                    "start": projeto["periodo"][0],
                    "end": projeto["periodo"][1]
                }
            },
            "Tempo Total": {"rich_text": [{"text": {"content": projeto["tempo"]}}]},
            "Descrição": {"rich_text": [{"text": {"content": projeto["desc"]}}]}
        }
        
        projeto_card = create_page(ESTUDOS_DB, projeto_properties, portfolio_id)
        if projeto_card:
            print(f"✅ {projeto['name']}: {projeto_card['id']}")
            
            # Adicionar conteúdo detalhado baseado no projeto
            print(f"📝 Adicionando conteúdo detalhado ao {projeto['name']}...")
            
            if "MyLocalPlace" in projeto['name']:
                add_content_to_page(projeto_card['id'], get_mylocalplace_content())
            elif "FastAPI" in projeto['name']:
                add_content_to_page(projeto_card['id'], get_fastapi_framework_content())
            elif "IntelliCart" in projeto['name']:
                add_content_to_page(projeto_card['id'], get_intellicart_content())
            elif "IA Knowledge" in projeto['name']:
                add_content_to_page(projeto_card['id'], get_ia_knowledge_base_content())
    
    print("\n" + "="*60)
    print("🎉 ESTRUTURA COMPLETA CRIADA NO NOTION!")
    print("="*60)
    print(f"📋 Card principal: {main_card_id}")
    print(f"📚 Formações: {formacoes_id}")
    print(f"💼 Portfolio: {portfolio_id}")
    print("\n🔗 Ver no Notion:")
    print(f"https://www.notion.so/{main_card_id.replace('-', '')}")

if __name__ == "__main__":
    main()
