#!/usr/bin/env python3
"""
Script para criar cards dos cursos Rocketseat no Notion
Baseado no cronograma detalhado
"""

import sys
from pathlib import Path

# Adicionar o diretório core ao path
sys.path.append(str(Path(__file__).parent.parent))

from core.notion_manager import NotionAPIManager, NotionConfig

def create_rocketseat_main_card(notion):
    """Cria card principal dos cursos Rocketseat"""
    properties = {
        "Nome do projeto": {
            "title": [
                {
                    "text": {
                        "content": "Rocketseat - IA na Prática: do Zero à Automação"
                    }
                }
            ]
        },
        "Projeto": {
            "select": {
                "name": "Rocketseat"
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
                    "text": {"content": "🚀 Curso: IA na Prática: do Zero à Automação"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Duração Total: 06:16:01"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Início: 01/11/2025"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Conclusão Prevista: 30/11/2025"}
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
                    "text": {"content": "Dominar ferramentas de IA generativa"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Aprender engenharia de prompts"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Criar agentes de IA personalizados"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Implementar automações práticas"}
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
                    "text": {"content": "Sábados: Revisão e projetos práticos"}
                }]
            }
        }
    ]
    
    return create_card(notion, properties, children)

def create_module_cards(notion):
    """Cria cards para cada módulo da Rocketseat"""
    modules = [
        {
            "name": "Módulo 1 - IA Generativa",
            "duration": "02:26:07",
            "description": "Dominando IA Generativa, ferramentas, prompts eficientes, NotebookLM, Gemini, criação de imagens e integrações"
        },
        {
            "name": "Módulo 2 - ChatGPT",
            "duration": "00:44:11",
            "description": "Introdução ao ChatGPT, interface, modelos, planos, prompts e elementos de prompt excelente"
        },
        {
            "name": "Módulo 3 - Integrações ChatGPT",
            "duration": "00:27:00",
            "description": "Trabalhando com imagens, arquivos, Google Drive, OneDrive, modo ditar e modo de voz"
        },
        {
            "name": "Módulo 4 - Modelos ChatGPT",
            "duration": "01:00:13",
            "description": "Comparando retornos, modelo de busca, criação de imagens, reflexão, investigação e escrita"
        },
        {
            "name": "Módulo 5 - Personalização ChatGPT",
            "duration": "00:52:01",
            "description": "Personalizar ChatGPT, projetos, GPTs personalizados, configuração e compartilhamento"
        },
        {
            "name": "Módulo 6 - Engenharia de Prompt",
            "duration": "01:04:19",
            "description": "Zero-Shot, Few-Shot, Follow-Up, refinamento, verificação cognitiva, role prompting e cadeia de pensamento"
        },
        {
            "name": "Módulo 7 - Maker Primeiros Passos",
            "duration": "00:27:01",
            "description": "Possibilidades GPT Maker, chatbot x agente, conta, créditos, dashboards e projeto prático"
        },
        {
            "name": "Módulo 8 - Maker Agentes",
            "duration": "00:42:13",
            "description": "Criando agente de vendas, perfil do agente, cenários de treinamento e refinamento"
        },
        {
            "name": "Módulo 9 - Maker Intenções",
            "duration": "00:46:16",
            "description": "Compreendendo intenções, planilhas, webhooks, Make, dados e integração"
        },
        {
            "name": "Módulo 10 - Maker Canais (Parte 1)",
            "duration": "00:48:02",
            "description": "Web Chat, demonstração, configuração, status, monitoramento e transferência"
        },
        {
            "name": "Módulo 11 - Maker Canais (Parte 2)",
            "duration": "00:41:43",
            "description": "WhatsApp, modelos IA, agente barbearia, Google Calendar e agendamento"
        }
    ]
    
    created_cards = []
    
    for module in modules:
        properties = {
            "Nome do projeto": {
                "title": [
                    {
                        "text": {
                            "content": f"Rocketseat - {module['name']}"
                        }
                    }
                ]
            },
            "Projeto": {
                "select": {
                    "name": "Rocketseat"
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
                        "text": {"content": f"📚 {module['name']}"}
                    }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": f"Duração: {module['duration']}"}
                    }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": f"Descrição: {module['description']}"}
                    }]
                }
            }
        ]
        
        if create_card(notion, properties, children):
            created_cards.append(module['name'])
    
    return created_cards

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
    print("CRIANDO CARDS DOS CURSOS ROCKETSEAT NO NOTION")
    print("=" * 60)
    
    notion = NotionAPIManager(NotionConfig())
    
    # Criar card principal
    print("\n📝 Criando card principal da Rocketseat...")
    create_rocketseat_main_card(notion)
    
    # Criar cards dos módulos
    print("\n📝 Criando cards dos módulos...")
    module_cards = create_module_cards(notion)
    
    print("\n" + "=" * 60)
    print("✅ CARDS DA ROCKETSEAT CRIADOS!")
    print(f"📊 Cards criados: {len(module_cards) + 1}")
    print("=" * 60)

if __name__ == "__main__":
    main()





