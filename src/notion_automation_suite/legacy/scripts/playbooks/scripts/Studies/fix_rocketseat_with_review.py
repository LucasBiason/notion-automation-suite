#!/usr/bin/env python3
"""
Script para corrigir completamente a estrutura do Rocketseat no Notion
- Remove emojis dos títulos
- Adiciona emojis como ícones das páginas
- Cria módulos e aulas como sub-itens
- Define períodos corretos em GMT-3
- Respeita limite de 21:00 e adiciona períodos de revisão
"""

import requests
import os
from datetime import datetime, timezone, timedelta

# Configurações
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_VERSION = '2022-06-28'
BASE_URL = 'https://api.notion.com/v1'
HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

STUDIES_DB_ID = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

# Estrutura do curso
COURSE_STRUCTURE = {
    'title': 'Rocketseat - IA na Prática: do Zero à Automação',
    'description': 'Formação completa em Inteligência Artificial prática, do básico ao avançado, com foco em automação e aplicações reais.',
    'categories': ['Cursos', 'IA', 'Rocketseat', 'Formação Completa'],
    'start_date': datetime(2025, 11, 1, 19, 0),  # 01/11/2025 19:00 GMT-3
    'total_duration': '06:16:01',
    'modules': [
        {
            'title': 'Módulo 1: Inteligência Artificial de zero - Dominando IA Generativa',
            'duration': '02:26:07',
            'description': 'Fundamentos da IA Generativa, ferramentas e aplicações práticas.',
            'lessons': [
                {'title': 'Boas vindas', 'duration': '01:39'},
                {'title': 'O que é Inteligência Artificial', 'duration': '07:39'},
                {'title': 'Evolução da IA até a IA Generativa', 'duration': '08:16'},
                {'title': 'Compreendendo IA Generativa', 'duration': '07:50'},
                {'title': 'IA Generativa por dentro', 'duration': '13:33'},
                {'title': 'Ferramentas de IA Generativa', 'duration': '13:29'},
                {'title': 'Comparando modelos de IA', 'duration': '07:14'},
                {'title': 'Prompts eficientes com ChatGPT', 'duration': '07:45'},
                {'title': 'Analisando Arquivo', 'duration': '08:54'},
                {'title': 'Conversando com fontes', 'duration': '12:17'},
                {'title': 'Cocriando um Podcast', 'duration': '05:00'},
                {'title': 'Outras ferramentas do NotebookLM', 'duration': '05:38'},
                {'title': 'Escrevendo um eBook com Gemini', 'duration': '08:42'},
                {'title': 'Transcrever vídeo com IA', 'duration': '08:59'},
                {'title': 'Ferramentas para criar imagem', 'duration': '09:30'},
                {'title': 'Gerando imagens com IA', 'duration': '10:54'},
                {'title': 'Criando o #Rock', 'duration': '10:36'},
                {'title': 'Integrações', 'duration': '07:39'},
                {'title': 'Agente com Manus AI', 'duration': '14:59'},
                {'title': 'Resumo e orçamentos com Manus AI', 'duration': '04:36'},
                {'title': 'Criando um Dashboard com Manus AI', 'duration': '07:58'},
                {'title': 'Cuidados e boas práticas', 'duration': '15:18'},
                {'title': 'Encerramento', 'duration': '01:15'}
            ]
        },
        {
            'title': 'Módulo 2: Introdução ao ChatGPT',
            'duration': '00:44:11',
            'description': 'Domine a interface e funcionalidades básicas do ChatGPT.',
            'lessons': [
                {'title': 'Boas vindas', 'duration': '03:03'},
                {'title': 'Possibilidades de uso', 'duration': '03:20'},
                {'title': 'Conhecendo a interface', 'duration': '04:42'},
                {'title': 'Comparando as interfaces', 'duration': '02:43'},
                {'title': 'Modelos e planos', 'duration': '03:38'},
                {'title': 'Criando seu primeiro prompt', 'duration': '03:58'},
                {'title': 'Gerenciando histórico', 'duration': '03:44'},
                {'title': 'Interagir com a resposta', 'duration': '07:54'},
                {'title': 'Compartilhar', 'duration': '03:12'},
                {'title': 'Elementos de Prompt Excelente', 'duration': '08:08'},
                {'title': 'Sendo claro com IA', 'duration': '09:17'},
                {'title': 'Habilitar', 'duration': '02:26'},
                {'title': 'Pausar', 'duration': '02:16'}
            ]
        },
        {
            'title': 'Módulo 3: Integrações do ChatGPT',
            'duration': '00:27:00',
            'description': 'Aprenda a integrar o ChatGPT com outras ferramentas.',
            'lessons': [
                {'title': 'Trabalhando com imagens', 'duration': '07:22'},
                {'title': 'Trabalhando com arquivos', 'duration': '10:24'},
                {'title': 'Conectar com Google Drive', 'duration': '00:31'},
                {'title': 'Conectar com OneDrive', 'duration': '01:10'},
                {'title': 'Modo ditar', 'duration': '01:50'},
                {'title': 'Modo de voz', 'duration': '06:23'}
            ]
        },
        {
            'title': 'Módulo 4: Modelos do ChatGPT',
            'duration': '01:00:13',
            'description': 'Explore os diferentes modelos e suas capacidades.',
            'lessons': [
                {'title': 'Comparando retornos', 'duration': '03:29'},
                {'title': 'Modelo de busca na Web', 'duration': '04:58'},
                {'title': 'Modelo de criação de imagens', 'duration': '05:34'},
                {'title': 'Editando imagem', 'duration': '03:46'},
                {'title': 'Modelo de reflexão', 'duration': '07:59'},
                {'title': 'Modelo de investigação', 'duration': '12:59'},
                {'title': 'Modelo de escrita', 'duration': '07:20'},
                {'title': 'Escritos com mais produtividade', 'duration': '10:43'},
                {'title': 'Pensar por mais tempo', 'duration': '03:38'},
                {'title': 'Comparativo entre os modelos', 'duration': '05:01'}
            ]
        },
        {
            'title': 'Módulo 5: Personalização e Automação do ChatGPT',
            'duration': '00:52:01',
            'description': 'Personalize e automatize seu uso do ChatGPT.',
            'lessons': [
                {'title': 'Personalizar o ChatGPT', 'duration': '08:00'},
                {'title': 'Criando projetos', 'duration': '04:08'},
                {'title': 'Projeto com instruções e arquivos', 'duration': '07:51'},
                {'title': 'Organizar conversas em projetos', 'duration': '05:15'},
                {'title': 'GPTs personalizados', 'duration': '10:30'},
                {'title': 'Tirando GPTs da barra', 'duration': '00:47'},
                {'title': 'Criando o GPT Personalizado', 'duration': '02:33'},
                {'title': 'Configurando o GPT Personalizado', 'duration': '13:55'},
                {'title': 'Compartilhando e testando GPT Personalizado', 'duration': '06:02'},
                {'title': 'Avaliando GPT Personalizado', 'duration': '04:48'},
                {'title': 'Diferença entre GPTs e Projetos', 'duration': '01:52'},
                {'title': 'Encerramento', 'duration': '00:51'}
            ]
        },
        {
            'title': 'Módulo 6: Engenharia de Prompt',
            'duration': '01:04:19',
            'description': 'Domine técnicas avançadas de engenharia de prompt.',
            'lessons': [
                {'title': 'Boas vindas', 'duration': '01:34'},
                {'title': 'O que é Engenharia de Prompt e por que ela importa', 'duration': '04:54'},
                {'title': 'Zero-Shot Prompting', 'duration': '03:40'},
                {'title': 'Few-Shot Prompting', 'duration': '03:22'},
                {'title': 'Prompts de Follow-Up', 'duration': '04:31'},
                {'title': 'Prompts de Follow-Up', 'duration': '04:51'},
                {'title': 'Refinamento de Perguntas', 'duration': '04:38'},
                {'title': 'Verificação Cognitiva', 'duration': '07:47'},
                {'title': 'Persona do usuário', 'duration': '03:50'},
                {'title': 'Role Prompting', 'duration': '04:23'},
                {'title': 'Ancoragem de Memória', 'duration': '04:59'},
                {'title': 'Cadeia de Pensamento', 'duration': '03:37'},
                {'title': 'Prompts de Dois Passos', 'duration': '01:56'},
                {'title': 'Empilhamento de prompts', 'duration': '04:01'},
                {'title': 'Autoconsciência', 'duration': '03:18'},
                {'title': 'Prompts Iterativos', 'duration': '03:53'},
                {'title': 'Temperatura', 'duration': '05:23'},
                {'title': 'Comparativo entre as técnicas', 'duration': '07:48'},
                {'title': 'Encerramento', 'duration': '01:04'}
            ]
        },
        {
            'title': 'Módulo 7: Maker: Primeiros passos',
            'duration': '00:27:01',
            'description': 'Introdução ao GPT Maker e suas possibilidades.',
            'lessons': [
                {'title': 'Boas vindas', 'duration': '01:59'},
                {'title': 'Possibilidades com GPT Maker', 'duration': '05:24'},
                {'title': 'Chatbot x Agente de IA', 'duration': '04:40'},
                {'title': 'Criando sua conta', 'duration': '02:31'},
                {'title': 'Sistema de créditos', 'duration': '04:53'},
                {'title': 'Dashboards e Workspaces', 'duration': '06:23'},
                {'title': 'Projeto prático da Pizzaria Forno & Sabor', 'duration': '05:39'}
            ]
        },
        {
            'title': 'Módulo 8: Maker: Agentes',
            'duration': '00:42:13',
            'description': 'Crie e configure agentes de IA personalizados.',
            'lessons': [
                {'title': 'Criando um agente de vendas', 'duration': '08:47'},
                {'title': 'Perfil do Agente', 'duration': '03:30'},
                {'title': 'Dica para criar perfil do agente', 'duration': '02:16'},
                {'title': 'Cenários para treinar seus agentes', 'duration': '07:19'},
                {'title': 'Testando nosso agente', 'duration': '04:11'},
                {'title': 'Testando e refinando o comportamento', 'duration': '07:38'},
                {'title': 'Treinamento com instruções', 'duration': '09:05'}
            ]
        },
        {
            'title': 'Módulo 9: Maker: Intenções',
            'duration': '00:46:16',
            'description': 'Configure intenções e integrações avançadas.',
            'lessons': [
                {'title': 'Compreendendo Intenções', 'duration': '02:10'},
                {'title': 'Criando a planilha', 'duration': '02:24'},
                {'title': 'Integração com Make e compreendendo Webhooks', 'duration': '03:58'},
                {'title': 'Criando Webhook no Make', 'duration': '05:30'},
                {'title': 'Utilizando Webhook', 'duration': '08:34'},
                {'title': 'Definindo os dados', 'duration': '04:52'},
                {'title': 'Passando dados via Webhook', 'duration': '04:51'},
                {'title': 'Salvando dados na planilha', 'duration': '08:18'},
                {'title': 'Testando com o agente', 'duration': '07:38'},
                {'title': 'Criando intenções para consultar cadastro do cliente', 'duration': '15:18'}
            ]
        },
        {
            'title': 'Módulo 10: Maker: Canais (Parte 1)',
            'duration': '00:48:02',
            'description': 'Configure canais de comunicação para seus agentes.',
            'lessons': [
                {'title': 'Recapitulando e próximos passos', 'duration': '04:09'},
                {'title': 'Conectar Web Chat', 'duration': '05:13'},
                {'title': 'Demonstração de uso em site', 'duration': '07:41'},
                {'title': 'Configurar Chat Web e Review do Chat', 'duration': '10:16'},
                {'title': 'Definindo status da conversa', 'duration': '05:14'},
                {'title': 'Monitoramento do atendimento', 'duration': '05:40'},
                {'title': 'Assumir o atendimento do agente', 'duration': '03:29'},
                {'title': 'Regras de transferência', 'duration': '04:23'}
            ]
        },
        {
            'title': 'Módulo 11: Maker: Canais (Parte 2)',
            'duration': '00:41:43',
            'description': 'Avançado em canais e integrações.',
            'lessons': [
                {'title': 'Ações do moderador', 'duration': '04:40'},
                {'title': 'Disparo de Webhooks', 'duration': '00:51'},
                {'title': 'Status do Agente de IA', 'duration': '00:53'},
                {'title': 'Agente em Treinamento', 'duration': '03:11'},
                {'title': 'Conectando ao WhatsApp', 'duration': '07:59'},
                {'title': 'Modelos da IA utilizados pelo agente', 'duration': '03:56'},
                {'title': 'Criando o agente para barbearia', 'duration': '05:04'},
                {'title': 'Criando agendas no Google Calendar', 'duration': '03:01'},
                {'title': 'Integração com agenda', 'duration': '04:35'},
                {'title': 'Mais configurações da Agenda', 'duration': '02:06'},
                {'title': 'Múltiplas agendas', 'duration': '02:53'},
                {'title': 'Configurações de agendamento', 'duration': '03:56'},
                {'title': 'Testando o Agente', 'duration': '07:44'},
                {'title': 'Encerramento', 'duration': '00:51'}
            ]
        }
    ]
}

def parse_duration(duration_str):
    """Converte string de duração para minutos"""
    parts = duration_str.split(':')
    if len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        return hours * 60 + minutes + seconds / 60
    elif len(parts) == 2:  # MM:SS
        minutes, seconds = map(int, parts)
        return minutes + seconds / 60
    else:
        return 0

def calculate_periods_with_review(start_date, course_structure):
    """Calcula os períodos respeitando limite de 21:00 e adicionando revisão"""
    # Timezone GMT-3
    sao_paulo_tz = timezone(timedelta(hours=-3))
    
    # Data de início
    current_date = start_date.replace(tzinfo=sao_paulo_tz)
    
    module_periods = {}
    lesson_periods = {}
    
    for i, module in enumerate(course_structure['modules']):
        # Período do módulo (sem horário específico)
        module_start = current_date.replace(hour=19, minute=0, second=0)
        module_end = current_date.replace(hour=21, minute=0, second=0)
        
        module_periods[module['title']] = {
            'start': module_start,
            'end': module_end
        }
        
        # Calcular períodos das aulas
        current_lesson_time = module_start
        
        for j, lesson in enumerate(module['lessons']):
            lesson_duration = parse_duration(lesson['duration'])
            lesson_start = current_lesson_time
            lesson_end = lesson_start + timedelta(minutes=lesson_duration)
            
            # Se a aula passa das 21:00, mover para o próximo dia
            if lesson_end.hour >= 21:
                # Mover para o próximo dia às 19:00
                next_day = current_date + timedelta(days=1)
                lesson_start = next_day.replace(hour=19, minute=0, second=0)
                lesson_end = lesson_start + timedelta(minutes=lesson_duration)
                current_date = next_day
                current_lesson_time = lesson_start
            
            lesson_key = f"{module['title']} - {lesson['title']}"
            lesson_periods[lesson_key] = {
                'start': lesson_start,
                'end': lesson_end
            }
            
            # Próxima aula começa após a atual + 15 min de revisão
            current_lesson_time = lesson_end + timedelta(minutes=15)
            
            # Se passou das 21:00, mover para o próximo dia
            if current_lesson_time.hour >= 21:
                next_day = current_date + timedelta(days=1)
                current_lesson_time = next_day.replace(hour=19, minute=0, second=0)
                current_date = next_day
        
        # Próximo módulo começa após o atual + 30 min de revisão
        next_module_date = current_date + timedelta(days=1)
        current_date = next_module_date
    
    return module_periods, lesson_periods

def format_notion_date(dt, include_time=True):
    """Formata data para o formato do Notion (mantendo GMT-3)"""
    if include_time:
        return dt.strftime('%Y-%m-%dT%H:%M:%S.000-03:00')
    else:
        return dt.strftime('%Y-%m-%d')

def create_notion_period(start_dt, end_dt, include_time=True):
    """Cria objeto de período para o Notion"""
    return {
        "date": {
            "start": format_notion_date(start_dt, include_time),
            "end": format_notion_date(end_dt, include_time)
        }
    }

def main():
    print("🚀 Iniciando correção completa da estrutura do Rocketseat com revisão...")
    
    if not NOTION_TOKEN:
        print("❌ NOTION_TOKEN não encontrado!")
        return
    
    # Calcular períodos
    print("📅 Calculando períodos com revisão...")
    module_periods, lesson_periods = calculate_periods_with_review(
        COURSE_STRUCTURE['start_date'], 
        COURSE_STRUCTURE
    )
    
    # 1. Deletar card antigo
    print("\n1. Deletando card antigo...")
    response = requests.post(f'{BASE_URL}/databases/{STUDIES_DB_ID}/query', headers=HEADERS, json={
        'filter': {
            'property': 'Project name',
            'title': {
                'contains': 'Rocketseat - IA na Prática'
            }
        }
    })
    
    if response.status_code == 200:
        results = response.json()['results']
        for card in results:
            delete_response = requests.delete(f'{BASE_URL}/pages/{card["id"]}', headers=HEADERS)
            if delete_response.status_code == 200:
                print(f"✅ Card antigo deletado: {card['id']}")
            else:
                print(f"❌ Erro ao deletar card: {delete_response.text}")
    
    # 2. Criar card principal
    print("\n2. Criando card principal...")
    course_end = max([period['end'] for period in module_periods.values()])
    
    main_properties = {
        'Project name': {
            'title': [{'text': {'content': COURSE_STRUCTURE['title']}}]
        },
        'Status': {'status': {'name': 'Para Fazer'}},
        'Categorias': {'multi_select': [{'name': cat} for cat in COURSE_STRUCTURE['categories']]},
        'Período': create_notion_period(COURSE_STRUCTURE['start_date'], course_end, include_time=False),
        'Tempo Total': {'rich_text': [{'text': {'content': COURSE_STRUCTURE['total_duration']}}]},
        'Descrição': {'rich_text': [{'text': {'content': COURSE_STRUCTURE['description']}}]}
    }
    
    response = requests.post(
        f'{BASE_URL}/pages',
        headers=HEADERS,
        json={
            'parent': {'database_id': STUDIES_DB_ID},
            'properties': main_properties,
            'icon': {'type': 'emoji', 'emoji': '🚀'}
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Erro ao criar card principal: {response.text}")
        return
    
    main_card_id = response.json()['id']
    print(f"✅ Card principal criado: {main_card_id}")
    
    # 3. Criar módulos e aulas
    print("\n3. Criando módulos e aulas...")
    
    for i, module in enumerate(COURSE_STRUCTURE['modules']):
        module_period = module_periods[module['title']]
        
        # Criar módulo
        module_properties = {
            'Project name': {
                'title': [{'text': {'content': module['title']}}]
            },
            'Status': {'status': {'name': 'Para Fazer'}},
            'Categorias': {'multi_select': [{'name': 'Cursos'}, {'name': 'IA'}, {'name': 'Rocketseat'}, {'name': 'Módulo'}]},
            'Parent item': {'relation': [{'id': main_card_id}]},
            'Período': create_notion_period(module_period['start'], module_period['end'], include_time=False),
            'Tempo Total': {'rich_text': [{'text': {'content': module['duration']}}]},
            'Descrição': {'rich_text': [{'text': {'content': module['description']}}]}
        }
        
        response = requests.post(
            f'{BASE_URL}/pages',
            headers=HEADERS,
            json={
                'parent': {'database_id': STUDIES_DB_ID},
                'properties': module_properties,
                'icon': {'type': 'emoji', 'emoji': '🧠'}
            }
        )
        
        if response.status_code != 200:
            print(f"❌ Erro ao criar módulo {i+1}: {response.text}")
            continue
        
        module_id = response.json()['id']
        print(f"✅ Módulo {i+1} criado: {module['title']}")
        
        # Criar aulas
        print(f"   Criando aulas do módulo {i+1}...")
        
        for j, lesson in enumerate(module['lessons']):
            lesson_key = f"{module['title']} - {lesson['title']}"
            lesson_period = lesson_periods[lesson_key]
            lesson_description = f'Aula {j+1} do {module["title"]}'
            
            lesson_properties = {
                'Project name': {
                    'title': [{'text': {'content': lesson['title']}}]
                },
                'Status': {'status': {'name': 'Para Fazer'}},
                'Categorias': {'multi_select': [{'name': 'Cursos'}, {'name': 'IA'}, {'name': 'Rocketseat'}, {'name': 'Aula'}]},
                'Parent item': {'relation': [{'id': module_id}]},
                'Período': create_notion_period(lesson_period['start'], lesson_period['end'], include_time=True),
                'Tempo Total': {'rich_text': [{'text': {'content': lesson['duration']}}]},
                'Descrição': {'rich_text': [{'text': {'content': lesson_description}}]}
            }
            
            response = requests.post(
                f'{BASE_URL}/pages',
                headers=HEADERS,
                json={
                    'parent': {'database_id': STUDIES_DB_ID},
                    'properties': lesson_properties,
                    'icon': {'type': 'emoji', 'emoji': '📚'}
                }
            )
            
            if response.status_code == 200:
                print(f"     ✅ Aula {j+1}: {lesson['title']} ({lesson['duration']})")
            else:
                print(f"     ❌ Erro ao criar aula {j+1}: {response.text}")
    
    print(f"\n🎉 Estrutura do Rocketseat corrigida com sucesso!")
    print(f"📅 Período total: {COURSE_STRUCTURE['start_date'].strftime('%d/%m/%Y %H:%M')} GMT-3 até {course_end.strftime('%d/%m/%Y %H:%M')} GMT-3")
    print(f"📚 Total de módulos: {len(COURSE_STRUCTURE['modules'])}")
    print(f"📖 Total de aulas: {sum(len(m['lessons']) for m in COURSE_STRUCTURE['modules'])}")
    print(f"⏰ Revisão incluída: 15 min entre aulas, 30 min entre módulos")

if __name__ == "__main__":
    main()





