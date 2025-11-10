#!/usr/bin/env python3
"""
Criar card para ia-ml-knowledge-base no cronograma
"""

import requests
from datetime import datetime
import pytz

NOTION_TOKEN = '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'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'
PORTFOLIO_CARD_ID = '294962a7-693c-81be-afc2-e098c9ac8b92'  # Projetos de Portfolio

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

gmt3 = pytz.timezone('America/Sao_Paulo')

def format_date_gmt3(dt):
    """Formata data para GMT-3."""
    return gmt3.localize(dt).isoformat()

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

def add_content_to_page(page_id, blocks):
    """Adiciona conteúdo a uma página."""
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    payload = {'children': blocks}
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    return response.status_code == 200

def get_ia_knowledge_base_content():
    """Conteúdo detalhado do ia-ml-knowledge-base."""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "📚 IA/ML Knowledge Base - Snippets & Receitas"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "🎯"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Projeto de revisão e consolidação de conhecimento em IA/ML através de snippets práticos e receitas de código."}
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
                "rich_text": [{"type": "text", "text": {"content": "Consolidar conhecimento dos cursos de IA/ML"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Criar snippets práticos e reutilizáveis"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Documentar receitas de código para problemas comuns"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Aproveitar conteúdo dos tutoriais do Instagram"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📁 Estrutura do Projeto"}}]
            }
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "🤖 OpenAI & GPT"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "Snippets para integração com OpenAI API"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "Function Calling, Assistants, DALL-E"}}]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "⛓️ LangChain"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "Receitas para LangChain"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "Agents, Tools, RAG, Memory"}}]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "🧠 Machine Learning"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "Snippets de scikit-learn, pandas, numpy"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "Preprocessing, modelagem, avaliação"}}]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "📱 Integrações"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "WhatsApp, Telegram, Discord"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "APIs externas, webhooks"}}]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📸 Fonte de Conteúdo"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "📱 Tutoriais do Instagram: "}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Screenshots de posts educativos"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Códigos e exemplos práticos"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Dicas e truques de IA"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🚀 Fases do Projeto"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Fase 1: Estruturação e Organização"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Fase 2: Coleta de Conteúdo (Instagram)"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Fase 3: Criação de Snippets"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Fase 4: Documentação e Testes"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Fase 5: Publicação e Manutenção"}}]
            }
        }
    ]

def main():
    print("\n" + "="*70)
    print("📚 CRIANDO CARD IA-ML-KNOWLEDGE-BASE")
    print("="*70 + "\n")
    
    # Propriedades do card principal
    properties = {
        "Project name": {"title": [{"text": {"content": "IA/ML Knowledge Base - Snippets & Receitas"}}]},
        "Status": {"status": {"name": "Para Fazer"}},
        "Prioridade": {"select": {"name": "Alta"}},
        "Categorias": {"multi_select": [{"name": "Portfolio"}, {"name": "IA/ML"}, {"name": "Documentação"}]},
        "Período": {
            "date": {
                "start": format_date_gmt3(datetime(2025, 11, 4)),  # Início após outros projetos
                "end": format_date_gmt3(datetime(2025, 12, 15))    # Final antes do fim do ano
            }
        },
        "Tempo Total": {"rich_text": [{"text": {"content": "40 horas"}}]},
        "Descrição": {"rich_text": [{"text": {"content": "Projeto de consolidação de conhecimento em IA/ML através de snippets práticos e receitas de código, aproveitando conteúdo dos tutoriais do Instagram."}}]}
    }
    
    # Criar card principal
    print("📝 Criando card principal...")
    main_card = create_page(
        ESTUDOS_DB, 
        properties, 
        parent_id=PORTFOLIO_CARD_ID,
        icon={"type": "emoji", "emoji": "📚"}
    )
    
    if not main_card:
        print("❌ Falha ao criar card principal!")
        return
    
    main_card_id = main_card['id']
    print(f"✅ Card principal criado: {main_card_id}")
    
    # Adicionar conteúdo detalhado
    print("📄 Adicionando conteúdo detalhado...")
    content_blocks = get_ia_knowledge_base_content()
    
    if add_content_to_page(main_card_id, content_blocks):
        print("✅ Conteúdo adicionado com sucesso!")
    else:
        print("❌ Erro ao adicionar conteúdo")
    
    # Criar fases como subitens
    print("🏗️ Criando fases do projeto...")
    
    fases = [
        {
            "title": "Fase 1: Estruturação e Organização",
            "desc": "Definir estrutura de pastas, templates e padrões",
            "duracao": "8 horas",
            "data_inicio": datetime(2025, 11, 4),
            "data_fim": datetime(2025, 11, 8)
        },
        {
            "title": "Fase 2: Coleta de Conteúdo (Instagram)",
            "desc": "Processar screenshots e extrair códigos dos tutoriais",
            "duracao": "10 horas", 
            "data_inicio": datetime(2025, 11, 9),
            "data_fim": datetime(2025, 11, 15)
        },
        {
            "title": "Fase 3: Criação de Snippets",
            "desc": "Desenvolver snippets práticos e reutilizáveis",
            "duracao": "12 horas",
            "data_inicio": datetime(2025, 11, 16),
            "data_fim": datetime(2025, 11, 25)
        },
        {
            "title": "Fase 4: Documentação e Testes",
            "desc": "Documentar e testar todos os snippets",
            "duracao": "6 horas",
            "data_inicio": datetime(2025, 11, 26),
            "data_fim": datetime(2025, 12, 2)
        },
        {
            "title": "Fase 5: Publicação e Manutenção",
            "desc": "Publicar no GitHub e configurar manutenção",
            "duracao": "4 horas",
            "data_inicio": datetime(2025, 12, 3),
            "data_fim": datetime(2025, 12, 8)
        }
    ]
    
    fases_criadas = 0
    
    for i, fase in enumerate(fases, 1):
        fase_properties = {
            "Project name": {"title": [{"text": {"content": fase["title"]}}]},
            "Status": {"status": {"name": "Para Fazer"}},
            "Categorias": {"multi_select": [{"name": "Portfolio"}, {"name": "IA/ML"}, {"name": "Fase"}]},
            "Período": {
                "date": {
                    "start": format_date_gmt3(fase["data_inicio"]),
                    "end": format_date_gmt3(fase["data_fim"])
                }
            },
            "Tempo Total": {"rich_text": [{"text": {"content": fase["duracao"]}}]},
            "Descrição": {"rich_text": [{"text": {"content": fase["desc"]}}]}
        }
        
        fase_card = create_page(
            ESTUDOS_DB,
            fase_properties,
            parent_id=main_card_id,
            icon={"type": "emoji", "emoji": f"{i}️⃣"}
        )
        
        if fase_card:
            print(f"   ✅ {fase['title']}")
            fases_criadas += 1
        else:
            print(f"   ❌ Erro: {fase['title']}")
    
    print(f"\n{'='*70}")
    print(f"✅ IA/ML Knowledge Base criado com sucesso!")
    print(f"📚 Card principal: {main_card_id}")
    print(f"🏗️ Fases criadas: {fases_criadas}/5")
    print(f"📅 Período: 04/11/2025 → 15/12/2025")
    print(f"⏱️ Tempo total: 40 horas")
    print(f"{'='*70}\n")
    
    print("🔗 Ver no Notion:")
    print(f"https://www.notion.so/{main_card_id.replace('-', '')}")

if __name__ == "__main__":
    main()









