#!/usr/bin/env python3
"""
Criar Estrutura Completa HubTravel no Notion
Versão: 1.0
Data: 09/10/2025

Cria:
- 5 subitens principais (Flight, Hotel, Vehicle, Common, Docs)
- 9-10 sub-tarefas para cada subitem
- Documentação completa como blocos
- Períodos com data/hora GMT-3
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
load_dotenv()

from core.notion_manager import NotionAPIManager, NotionConfig, DatabaseType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PARENT_ID = '287962a7-693c-815f-b835-c0b46026a5d8'
WORK_DB_ID = '1f9962a7-693c-80a3-b947-c471a975acb0'
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

def format_notion_date(dt):
    """Formata data para Notion (GMT-3)"""
    return dt.strftime('%Y-%m-%dT%H:%M:%S.000-03:00')

def create_notion_period(start_dt, end_dt):
    """Cria objeto de período para Notion"""
    return {
        "date": {
            "start": format_notion_date(start_dt),
            "end": format_notion_date(end_dt)
        }
    }

def get_existing_subitems(notion, parent_id):
    """Verifica se já existem subitens vinculados ao parent"""
    try:
        response = notion.session.post(
            f"{notion.base_url}/databases/{WORK_DB_ID}/query",
            json={
                "filter": {
                    "property": "Sprint",
                    "relation": {
                        "contains": parent_id
                    }
                }
            },
            timeout=notion.config.timeout
        )
        
        if response.status_code == 200:
            results = response.json()['results']
            logger.info(f"Encontrados {len(results)} subitens existentes")
            return results
        else:
            logger.warning(f"Erro ao buscar subitens: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Erro ao verificar subitens: {e}")
        return []

def create_subitem_with_blocks(notion, parent_id, subitem_data, blocks):
    """Cria subitem com blocos de documentação"""
    
    payload = {
        "parent": {"database_id": WORK_DB_ID},
        "icon": {"emoji": subitem_data['emoji']},
        "properties": {
            "Nome do projeto": {
                "title": [{"text": {"content": subitem_data['title']}}]
            },
            "Status": {
                "status": {"name": subitem_data['status']}
            },
            "Cliente": {
                "select": {"name": "Astracode"}
            },
            "Projeto": {
                "select": {"name": "HubTravel"}
            },
            "Prioridade": {
                "select": {"name": subitem_data['priority']}
            },
            "Sprint": {
                "relation": [{"id": parent_id}]
            },
            "Periodo": subitem_data.get('periodo', {})
        }
    }
    
    if blocks:
        payload["children"] = blocks
    
    try:
        response = notion.session.post(
            f"{notion.base_url}/pages",
            json=payload,
            timeout=notion.config.timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ {subitem_data['title']}: {result['id']}")
            return result
        else:
            logger.error(f"❌ {subitem_data['title']}: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Erro ao criar {subitem_data['title']}: {e}")
        return None

def get_flight_service_blocks():
    """Blocos de documentação para Flight Service"""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Flight Service Connector"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Microservico proxy para API Aereo da Wooba. Responsavel por todo o fluxo de voos desde pesquisa ate emissao de bilhetes."}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "RESPONSABILIDADES"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Pesquisa de disponibilidade (3 endpoints)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Detalhamento e regras tarifarias (3 endpoints)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Reserva e consulta (2 endpoints)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Gestao de assentos (3 endpoints)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Emissao de bilhetes (4 endpoints)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Pos-venda: alteracao e cancelamento (4 endpoints)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Listagens e buscas (4 endpoints)"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "TOTAL: 23 endpoints Wooba mapeados"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "STACK TECNICA"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "FastAPI + PostgreSQL + Redis + httpx"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "DATABASE"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "flights_db (PostgreSQL) com 3 tabelas: flight_searches, flight_bookings, flight_tickets"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "ENDPOINTS PROXY"}}]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "language": "plain text",
                "rich_text": [{"type": "text", "text": {"content": "POST   /api/flights/availability\nPOST   /api/flights/availability/multiple\nGET    /api/flights/systems\nGET    /api/flights/{id}/fare-rules\nGET    /api/flights/{id}/family-details\nPOST   /api/flights/{id}/price\nPOST   /api/bookings\nGET    /api/bookings/{locator}\nGET    /api/bookings/{locator}/seats\nPOST   /api/bookings/{locator}/seats\nDELETE /api/bookings/{locator}/seats\nPOST   /api/bookings/{locator}/issue/start\nGET    /api/bookings/{locator}/payment-methods\nPOST   /api/bookings/{locator}/issue\nGET    /api/tickets/{number}\nDELETE /api/bookings/{locator}\nDELETE /api/tickets/{number}"}}]
            }
        }
    ]

def get_hotel_service_blocks():
    """Blocos de documentação para Hotel Service"""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Hotel Service Connector"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Microservico proxy para API Hotel da Wooba. Fluxo completo de hospedagem."}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "RESPONSABILIDADES"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Busca de destinos e hoteis"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Disponibilidade de quartos"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Detalhes e amenities"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Reserva de hospedagem"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Confirmacao e voucher"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Cancelamento"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "TOTAL: 7 endpoints Wooba mapeados"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "DATABASE"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "hotels_db (PostgreSQL) com 2 tabelas: hotel_searches, hotel_reservations"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "ENDPOINTS PROXY"}}]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "language": "plain text",
                "rich_text": [{"type": "text", "text": {"content": "POST   /api/hotels/destinations\nPOST   /api/hotels/availability\nGET    /api/hotels/{id}/info\nPOST   /api/hotels/{id}/price\nPOST   /api/reservations\nGET    /api/reservations/{id}\nDELETE /api/reservations/{id}"}}]
            }
        }
    ]

def get_vehicle_service_blocks():
    """Blocos de documentação para Vehicle Service"""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Vehicle Service Connector"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Microservico proxy para API Carro da Wooba. Fluxo completo de locacao de veiculos."}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "RESPONSABILIDADES"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Disponibilidade de veiculos"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Detalhes e categorias"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Tarifacao (com extras)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Reserva de locacao"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Retirada (pickup) e Devolucao (return)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Cancelamento"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "TOTAL: 6 endpoints Wooba mapeados"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "DATABASE"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "vehicles_db (PostgreSQL) com 2 tabelas: vehicle_searches, vehicle_rentals"}}]
            }
        }
    ]

def get_common_connector_blocks():
    """Blocos de documentação para Common Connector"""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Common Wooba Connector"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Infraestrutura comum compartilhada por todos os microservicos."}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "COMPONENTES"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "1. WOOBA ADAPTER SERVICE (:8010)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Autenticacao RSA/PKCS1 com Developer Token"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Cliente HTTP base para API Wooba"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Gerenciamento de sessao e headers"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "2. HUBTRAVEL SHARED LIBRARY"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "hubtravel_shared.auth - Middleware autenticacao (bypass)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "hubtravel_shared.wooba - Cliente Wooba base"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "hubtravel_shared.validators - Validacoes compartilhadas"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "3. API GATEWAY (:8000)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Roteamento para Flight/Hotel/Vehicle"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Middleware de autenticacao (bypass temporario)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Rate limiting e throttling"}}]
            }
        }
    ]

def get_documentation_blocks():
    """Blocos de documentação para Documentação"""
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Documentacao e Planejamento"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Documentacao completa do projeto HubTravel Wooba Connector."}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "DOCUMENTACAO TECNICA"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "README.md principal"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "README.md por servico (6 arquivos)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "CHANGELOG.md"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "ARCHITECTURE.md"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "DOCUMENTACAO API"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "OpenAPI/Swagger por servico (6 specs)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Postman Collections atualizadas"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Guia de integracao"}}]
            }
        }
    ]

def main():
    """Função principal"""
    print("=" * 80)
    print("CRIANDO ESTRUTURA COMPLETA HUBTRAVEL NO NOTION")
    print("=" * 80)
    
    # Inicializar Notion
    config = NotionConfig.from_env()
    notion = NotionAPIManager(config)
    
    if not notion.test_connection():
        logger.error("Falha na conexao com Notion")
        return False
    
    # Verificar subitens existentes
    print("\n1. Verificando subitens existentes...")
    existing = get_existing_subitems(notion, PARENT_ID)
    
    if existing:
        print(f"   Encontrados {len(existing)} subitens. Deletando para recriar...")
        for item in existing:
            notion.session.patch(
                f"{notion.base_url}/pages/{item['id']}",
                json={"archived": True},
                timeout=notion.config.timeout
            )
    
    # Definir períodos (GMT-3)
    start_date = datetime(2025, 10, 10, 19, 0, tzinfo=SAO_PAULO_TZ)
    
    # Definir os 5 componentes principais
    components = [
        {
            'title': 'Flight Service Connector',
            'emoji': '✈️',
            'status': 'Em Andamento',
            'priority': 'Alta',
            'periodo': create_notion_period(
                start_date,
                start_date + timedelta(days=7)
            ),
            'blocks': get_flight_service_blocks(),
            'subtasks': [
                {'title': 'Analise - Estudar 23 endpoints API Aereo', 'emoji': '📋', 'hours': 8},
                {'title': 'Estrutura Base - Setup FastAPI padrao ExpenseIQ', 'emoji': '🏗️', 'hours': 6},
                {'title': 'Disponibilidade - 3 endpoints de pesquisa', 'emoji': '🔍', 'hours': 10},
                {'title': 'Detalhamento - Regras e tarifas', 'emoji': '💰', 'hours': 8},
                {'title': 'Reserva - Booking endpoints', 'emoji': '📝', 'hours': 10},
                {'title': 'Assentos - Gestao de assentos', 'emoji': '💺', 'hours': 6},
                {'title': 'Emissao - Ticketing endpoints', 'emoji': '🎫', 'hours': 12},
                {'title': 'Pos-venda - Alteracao e cancelamento', 'emoji': '🔄', 'hours': 8},
                {'title': 'Testes - 95%+ cobertura com mocking Wooba', 'emoji': '🧪', 'hours': 12},
                {'title': 'Documentacao - OpenAPI + README + Diagramas', 'emoji': '📚', 'hours': 6}
            ]
        },
        {
            'title': 'Hotel Service Connector',
            'emoji': '🏨',
            'status': 'Não iniciado',
            'priority': 'Alta',
            'periodo': create_notion_period(
                start_date + timedelta(days=8),
                start_date + timedelta(days=12)
            ),
            'blocks': get_hotel_service_blocks(),
            'subtasks': [
                {'title': 'Analise - Estudar 7 endpoints API Hotel', 'emoji': '📋', 'hours': 4},
                {'title': 'Estrutura Base - Setup FastAPI', 'emoji': '🏗️', 'hours': 4},
                {'title': 'Pesquisa - Destinations e Avail', 'emoji': '🔍', 'hours': 8},
                {'title': 'Detalhamento - Descriptive Info', 'emoji': '📄', 'hours': 6},
                {'title': 'Reserva - Criar e consultar', 'emoji': '📝', 'hours': 8},
                {'title': 'Confirmacao - Confirmar e voucher', 'emoji': '✅', 'hours': 6},
                {'title': 'Cancelamento - Cancel endpoint', 'emoji': '❌', 'hours': 4},
                {'title': 'Testes - 95%+ cobertura', 'emoji': '🧪', 'hours': 8},
                {'title': 'Documentacao - OpenAPI + README', 'emoji': '📚', 'hours': 4}
            ]
        },
        {
            'title': 'Vehicle Service Connector',
            'emoji': '🚗',
            'status': 'Não iniciado',
            'priority': 'Média',
            'periodo': create_notion_period(
                start_date + timedelta(days=13),
                start_date + timedelta(days=17)
            ),
            'blocks': get_vehicle_service_blocks(),
            'subtasks': [
                {'title': 'Analise - Estudar 6 endpoints API Carro', 'emoji': '📋', 'hours': 4},
                {'title': 'Estrutura Base - Setup FastAPI', 'emoji': '🏗️', 'hours': 4},
                {'title': 'Disponibilidade - Shopping endpoint', 'emoji': '🔍', 'hours': 6},
                {'title': 'Detalhamento - Details endpoint', 'emoji': '📄', 'hours': 4},
                {'title': 'Reserva - Book endpoints', 'emoji': '📝', 'hours': 8},
                {'title': 'Retirada/Devolucao - Pickup/Return', 'emoji': '🔄', 'hours': 6},
                {'title': 'Cancelamento - Cancel endpoint', 'emoji': '❌', 'hours': 4},
                {'title': 'Testes - 95%+ cobertura', 'emoji': '🧪', 'hours': 8},
                {'title': 'Documentacao - OpenAPI + README', 'emoji': '📚', 'hours': 4}
            ]
        },
        {
            'title': 'Common Wooba Connector',
            'emoji': '🔧',
            'status': 'Não iniciado',
            'priority': 'Alta',
            'periodo': create_notion_period(
                start_date + timedelta(days=18),
                start_date + timedelta(days=22)
            ),
            'blocks': get_common_connector_blocks(),
            'subtasks': [
                {'title': 'Auth RSA - Implementar criptografia RSA/PKCS1', 'emoji': '🔐', 'hours': 8},
                {'title': 'Cliente HTTP - Wooba HTTP client base', 'emoji': '🌐', 'hours': 6},
                {'title': 'Wooba Adapter - Service completo', 'emoji': '🔌', 'hours': 10},
                {'title': 'Shared Library - Codigo comum', 'emoji': '📦', 'hours': 8},
                {'title': 'API Gateway - Roteamento unificado', 'emoji': '🚪', 'hours': 8},
                {'title': 'Docker Compose - Infraestrutura completa', 'emoji': '🐳', 'hours': 6},
                {'title': 'Makefile - Comandos automatizados', 'emoji': '⚙️', 'hours': 4},
                {'title': 'Testes Integracao - End-to-end', 'emoji': '🧪', 'hours': 10},
                {'title': 'Documentacao - README raiz', 'emoji': '📚', 'hours': 4}
            ]
        },
        {
            'title': 'Documentacao e Planejamento',
            'emoji': '📚',
            'status': 'Em Andamento',
            'priority': 'Alta',
            'periodo': create_notion_period(
                start_date,
                start_date + timedelta(days=2)
            ),
            'blocks': get_documentation_blocks(),
            'subtasks': [
                {'title': 'README Principal', 'emoji': '📄', 'hours': 3},
                {'title': 'OpenAPI Specs - 6 arquivos', 'emoji': '📋', 'hours': 4},
                {'title': 'Diagramas Mermaid - 5 arquivos', 'emoji': '📊', 'hours': 4},
                {'title': 'Guia Integracao Wooba', 'emoji': '📖', 'hours': 3},
                {'title': 'Postman Collections', 'emoji': '📮', 'hours': 2}
            ]
        }
    ]
    
    print("\n2. Criando 5 componentes principais...\n")
    
    created_components = []
    
    for component in components:
        print(f"\n   Criando: {component['title']}...")
        
        # Criar componente principal
        result = create_subitem_with_blocks(
            notion,
            PARENT_ID,
            component,
            component['blocks']
        )
        
        if result:
            component_id = result['id']
            created_components.append({
                'id': component_id,
                'title': component['title'],
                'subtasks': component['subtasks']
            })
            
            # Criar sub-tarefas
            print(f"      Criando {len(component['subtasks'])} sub-tarefas...")
            
            current_time = datetime.now(SAO_PAULO_TZ).replace(hour=19, minute=0, second=0, microsecond=0)
            
            for idx, subtask in enumerate(component['subtasks']):
                # Calcular período da sub-tarefa
                task_start = current_time
                task_end = task_start + timedelta(hours=subtask['hours'])
                
                # Se passar das 21:00, mover para próximo dia
                if task_end.hour >= 21:
                    current_time = (current_time + timedelta(days=1)).replace(hour=19, minute=0)
                    task_start = current_time
                    task_end = task_start + timedelta(hours=subtask['hours'])
                
                subtask_data = {
                    'title': f"{component['title']} - {subtask['title']}",
                    'emoji': subtask['emoji'],
                    'status': 'Não iniciado',
                    'priority': 'Média',
                    'periodo': create_notion_period(task_start, task_end)
                }
                
                subtask_result = create_subitem_with_blocks(
                    notion,
                    component_id,
                    subtask_data,
                    []
                )
                
                if subtask_result:
                    print(f"         ✅ {subtask['title']}")
                else:
                    print(f"         ❌ {subtask['title']}")
                
                current_time = task_end
    
    # Salvar IDs criados
    print("\n3. Salvando IDs dos cards criados...")
    
    ids_file = Path(__file__).parent.parent.parent / "hubtravel_card_ids.txt"
    with open(ids_file, 'w') as f:
        f.write(f"PARENT_ID: {PARENT_ID}\n\n")
        for comp in created_components:
            f.write(f"{comp['title']}: {comp['id']}\n")
    
    print(f"   ✅ IDs salvos em: {ids_file}")
    
    print("\n" + "=" * 80)
    print(f"CONCLUIDO: {len(created_components)} componentes + sub-tarefas criados!")
    print("=" * 80)
    print(f"\nVerifique: https://notion.so/{PARENT_ID.replace('-', '')}")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

