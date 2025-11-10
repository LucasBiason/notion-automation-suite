#!/usr/bin/env python3
"""
Script para atualizar o card da Aula 1 com TODO o resumo criado
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('NOTION_API_TOKEN')
AULA1_ID = '27f962a7-693c-8173-b9e6-da148221fcb6'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def adicionar_conteudo_aula1():
    """Adiciona conteúdo completo ao card da Aula 1"""
    
    print('📝 Adicionando resumo completo ao card da Aula 1...')
    print('')
    
    # Blocos do Notion com todo o resumo
    blocos = [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "📚 Resumo Completo - Aula 1"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "✅"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Status: Concluída • Data: 13/10/2025 • Duração: 1h30min (14:30-16:00)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Objetivos de Aprendizagem"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Compreender os diferentes tipos de aprendizado de IA"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Entender a evolução dos modelos GPT (GPT-3 → GPT-4 → GPT-5)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Conhecer a plataforma OpenAI e suas APIs"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Entender conceitos de Machine Learning, Deep Learning e Transformers"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📖 Conceitos Fundamentais"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "1. Tipos de Aprendizado de IA"}}]
            }
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Aprendizado Supervisionado"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "O que é: Modelo recebe dados com rótulos (input + resposta esperada)"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Exemplo: Classificar números escritos à mão (imagem do '4' → resposta '4')"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Aplicação: Classificação, regressão, previsão"}
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
                "rich_text": [{"type": "text", "text": {"content": "🔍 Aprendizado Não Supervisionado"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "O que é: Modelo encontra padrões em dados sem rótulos"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Exemplo: Agrupar músicas por gênero no Spotify (sem classificação prévia)"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Aplicação: Clustering, redução de dimensionalidade"}
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
                "rich_text": [{"type": "text", "text": {"content": "🎮 Aprendizado por Reforço"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "O que é: Modelo aprende através de recompensas/penalizações"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Exemplo: Jogo de corrida (ação certa = +1, ação errada = -1)"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Aplicação: Games, robótica, trading"}
                            }]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "2. Deep Learning e Redes Neurais 🧠"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Inspiração: Neurônios biológicos"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Estrutura: Camadas de neurônios interconectados"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Pesos: Linhas que conectam neurônios (influência entre eles)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "3. Transformers - A Revolução (2018) 🚀"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Ano: 2018 (Google)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Revolução: Mudou completamente a IA"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Base: GPT, BERT, T5"}
                }]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "💡"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Por que revolucionaram? Processamento paralelo (não sequencial) + melhor compreensão de contexto + geração de linguagem natural"}
                }]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Conceitos-Chave Dominados"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "✅ 3 tipos de aprendizado: Supervisionado, Não Supervisionado, Reforço"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "✅ Evolução GPT: GPT-3 (175B parâmetros) → GPT-4 (trilhões) → GPT-5 (desenvolvimento)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "✅ Transformers (2018): Revolução que possibilitou GPT"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "✅ OpenAI Platform: Chat, Assistants, DALL-E, Whisper"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "✅ Pricing: Por tokens, rate limits, monitoramento necessário"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📚 Material Criado"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "✅ Resumo completo (template v2.0 - 11 seções)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "✅ 12 flashcards para revisão"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "✅ Card de revisão (agendado 18/10 19:00)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "✅ Exercícios práticos conceituais"}
                }]
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎴 Flashcards (12 cards)"}}]
            }
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "Flashcard 1: Aprendizado Supervisionado"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Pergunta: O que caracteriza o aprendizado supervisionado?"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Resposta: Usa dados etiquetados (input + resposta esperada) para treinar o modelo. Exemplo: classificar números escritos à mão."}
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
                "rich_text": [{"type": "text", "text": {"content": "Flashcard 2: Aprendizado Não Supervisionado"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Pergunta: Qual a diferença do aprendizado não supervisionado?"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Resposta: Encontra padrões em dados sem rótulos. Exemplo: agrupar músicas por gênero automaticamente."}
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
                "rich_text": [{"type": "text", "text": {"content": "Flashcard 3: Aprendizado por Reforço"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Pergunta: Como funciona o aprendizado por reforço?"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Resposta: Modelo aprende através de recompensas (+) e penalizações (-). Exemplo: jogos, onde ações corretas são recompensadas."}
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
                "rich_text": [{"type": "text", "text": {"content": "Flashcard 4: Redes Neurais - Pesos"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Pergunta: O que são pesos em redes neurais?"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Resposta: São as conexões entre neurônios que determinam a influência de um neurônio sobre outro. Inspirados em sinapses biológicas."}
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
                "rich_text": [{"type": "text", "text": {"content": "Flashcard 5: Transformers"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Pergunta: Por que os Transformers revolucionaram a IA?"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Resposta: Permitem processamento paralelo de texto, melhor compreensão de contexto e geração de linguagem natural mais eficiente."}
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
                "rich_text": [{"type": "text", "text": {"content": "Flashcard 6: GPT-4 vs GPT-3"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Pergunta: Qual a principal diferença entre GPT-3 e GPT-4?"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Resposta: GPT-3: 175 bilhões de parâmetros. GPT-4: trilhões de parâmetros, muito maior capacidade."}
                            }]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "💡 Insights e Conexões"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "🚀"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Aplicações nos seus projetos:"}
                }],
                "children": [
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "ExpenseIQ: Function Calling para consultas ao banco em linguagem natural"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "HubTravel: Fine-tuning para recomendações personalizadas"}
                            }]
                        }
                    },
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": "Agentes Notion: Integração com OpenAI para automação inteligente"}
                            }]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📝 Exercícios Práticos"}}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Explique com suas palavras a diferença entre os 3 tipos de aprendizado de IA"}
                }]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Compare GPT-3 e GPT-4 em termos de capacidade e custo"}
                }]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Como você aplicaria Function Calling no ExpenseIQ?"}
                }]
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
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
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "📅 18/10 (sexta) 19:00: Revisão da Aula 1"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "📅 20/10 (segunda) 19:00: Aula 4 - API DALL-E"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "📚 Explorar documentação OpenAI"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "🧪 Testar TensorFlow Playground"}
                }]
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "✅"},
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Aula concluída com sucesso! Base sólida construída para próximas aulas práticas. 🎉"}
                }]
            }
        }
    ]
    
    # Adicionar blocos ao card
    url = f'https://api.notion.com/v1/blocks/{AULA1_ID}/children'
    payload = {"children": blocos}
    
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        print('✅ Resumo completo adicionado ao card!')
        print('')
        print('📋 Conteúdo adicionado:')
        print('  ✅ Objetivos de Aprendizagem')
        print('  ✅ Conceitos Fundamentais (3 tipos de IA)')
        print('  ✅ Deep Learning e Redes Neurais')
        print('  ✅ Transformers (2018)')
        print('  ✅ Conceitos-Chave Dominados')
        print('  ✅ 6 Flashcards (em formato toggle)')
        print('  ✅ Insights para seus projetos')
        print('  ✅ Exercícios práticos')
        print('  ✅ Próximos passos')
        return True
    else:
        print(f'❌ Erro ao adicionar conteúdo: {response.text}')
        return False

if __name__ == '__main__':
    print('🤖 ATUALIZANDO CARD DA AULA 1 COM RESUMO COMPLETO')
    print('='*70)
    print('')
    
    success = adicionar_conteudo_aula1()
    
    if success:
        print('')
        print('='*70)
        print('🎉 CARD DA AULA 1 COMPLETAMENTE ATUALIZADO!')
        print('='*70)
        print('')
        print('🔗 Ver no Notion:')
        print('https://www.notion.so/Aula-1-Introduo-OpenAI-e-Inteligncia-Artificial-27f962a7693c8173b9e6da148221fcb6')
        print('')
        print('📝 Conteúdo incluído:')
        print('  • Status: Concluído ✅')
        print('  • Data: 13/10/2025 14:30-16:00')
        print('  • Resumo completo com 11 seções')
        print('  • 6 flashcards interativos')
        print('  • Insights para projetos')
        print('  • Exercícios práticos')
        print('  • Próximos passos')
    else:
        print('❌ Falha na atualização')











