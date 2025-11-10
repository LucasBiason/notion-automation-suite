#!/usr/bin/env python3
"""
Script para criar cards da Fase 4 FIAP no Notion
Baseado no cronograma detalhado
"""

import sys
from pathlib import Path

# Adicionar o diretório core ao path
sys.path.append(str(Path(__file__).parent.parent))

from core.notion_manager import NotionAPIManager, NotionConfig

def create_fiap_phase4_main_card(notion):
    """Cria card principal da Fase 4 FIAP"""
    properties = {
        "Nome do projeto": {
            "title": [
                {
                    "text": {
                        "content": "FIAP Fase 4 - Análise de Dados"
                    }
                }
            ]
        },
        "Projeto": {
            "select": {
                "name": "FIAP"
            }
        },
        "Status": {
            "status": {
                "name": "Em Andamento"
            }
        },
        "Progresso": {
            "number": 0
        },
        "Prioridade": {
            "select": {
                "name": "Alta"
            }
        }
    }
    
    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "📚 Curso: PÓS TECH - FASE 4 - ANÁLISE DE DADOS"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Duração Total: 06:42:40"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Início: 06/10/2025"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Conclusão Prevista: 31/10/2025"}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "🎯 Objetivos"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Completar Fase 4 FIAP - Análise de Dados"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Finalizar Tech Challenger"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Consolidar conhecimentos em IA"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Preparar para Rocketseat"}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "📅 Cronograma"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Horário: 19:00-21:00 (Segunda a Sexta) + 19:30-21:00 (Terças)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Sábados: Revisão e exercícios práticos"}
                }]
            }
        }
    ]
    
    return create_card(notion, properties, children)

def create_section_cards(notion):
    """Cria cards para cada seção da Fase 4"""
    sections = [
        {
            "name": "Seção 1 - Análise de Dados",
            "duration": "02:48:17",
            "description": "Reconhecimento facial, análise de expressões, detecção de atividades, transcrição de áudio, classificação de tópicos e sumarização automática"
        },
        {
            "name": "Seção 2 - Textract + AWS Comprehend",
            "duration": "00:36:21",
            "description": "Introdução ao Textract e AWS Comprehend, extração de texto e análise de texto"
        },
        {
            "name": "Seção 3 - OpenAI",
            "duration": "03:18:02",
            "description": "Introdução à OpenAI, fundamentos da API, primeiros passos com GPT, API DALL-E e integração/automação"
        },
        {
            "name": "Tech Challenger",
            "duration": "1 semana",
            "description": "Projeto prático de otimização de cargas usando algoritmos genéticos"
        }
    ]
    
    created_cards = []
    
    for section in sections:
        properties = {
            "Nome do projeto": {
                "title": [
                    {
                        "text": {
                            "content": f"FIAP Fase 4 - {section['name']}"
                        }
                    }
                ]
            },
            "Projeto": {
                "select": {
                    "name": "FIAP"
                }
            },
            "Status": {
                "status": {
                    "name": "Pendente"
                }
            },
            "Progresso": {
                "number": 0
            },
            "Prioridade": {
                "select": {
                    "name": "Alta"
                }
            }
        }
        
        children = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": f"📚 {section['name']}"}
                    }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": f"Duração: {section['duration']}"}
                    }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": f"Descrição: {section['description']}"}
                    }]
                }
            }
        ]
        
        if create_card(notion, properties, children):
            created_cards.append(section['name'])
    
    return created_cards

def create_tech_challenger_card(notion):
    """Cria card específico para o Tech Challenger"""
    properties = {
        "Nome do projeto": {
            "title": [
                {
                    "text": {
                        "content": "FIAP Tech Challenger - Otimização de Cargas"
                    }
                }
            ]
        },
        "Projeto": {
            "select": {
                "name": "FIAP"
            }
        },
        "Status": {
            "status": {
                "name": "Pendente"
            }
        },
        "Progresso": {
            "number": 0
        },
        "Prioridade": {
            "select": {
                "name": "Alta"
            }
        }
    }
    
    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "🚀 Tech Challenger - Otimização de Cargas"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Projeto prático usando algoritmos genéticos para otimização de cargas em containers"}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "🎯 Objetivos"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Implementar algoritmo genético para otimização"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Criar interface para visualização dos resultados"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Documentar processo e resultados"}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "📅 Cronograma"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Início: 23/10/2025"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Conclusão: 29/10/2025"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Duração: 1 semana"}
                }]
            }
        }
    ]
    
    return create_card(notion, properties, children)

def create_card(notion, properties, children):
    """Cria um card no Notion"""
    studies_database_id = "279962a7693c800584eaca97a3bfab25"
    
    try:
        response = notion.session.post(
            f"{notion.base_url}/pages",
            json={
                "parent": {"database_id": studies_database_id},
                "properties": properties,
                "children": children
            },
            timeout=notion.config.timeout
        )
        
        if response.status_code == 200:
            print(f"✅ Card criado: {properties['Nome do projeto']['title'][0]['text']['content']}")
            return True
        else:
            print(f"❌ Erro ao criar card: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("=" * 60)
    print("CRIANDO CARDS DA FASE 4 FIAP NO NOTION")
    print("=" * 60)
    
    notion = NotionAPIManager(NotionConfig())
    
    # Criar card principal
    print("\n📝 Criando card principal da Fase 4...")
    create_fiap_phase4_main_card(notion)
    
    # Criar cards das seções
    print("\n📝 Criando cards das seções...")
    section_cards = create_section_cards(notion)
    
    # Criar card do Tech Challenger
    print("\n📝 Criando card do Tech Challenger...")
    create_tech_challenger_card(notion)
    
    print("\n" + "=" * 60)
    print("✅ CARDS DA FASE 4 FIAP CRIADOS!")
    print(f"📊 Cards criados: {len(section_cards) + 2}")
    print("=" * 60)

if __name__ == "__main__":
    main()





