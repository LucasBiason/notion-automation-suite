#!/usr/bin/env python3
"""
Atualizar TODOS os Cards HubTravel com Documentação Detalhada
Versão otimizada com blocos menores
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
load_dotenv()

from core.notion_manager import NotionAPIManager, NotionConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CARDS = {
    'flight': '287962a7-693c-8160-9214-e242dbb534ee',
    'hotel': '287962a7-693c-815e-8360-dd5236967520',
    'vehicle': '287962a7-693c-81be-b58a-f37de3c1da7c',
    'common': '287962a7-693c-812a-8da4-ea2d3284dc8b',
    'docs': '287962a7-693c-8154-83be-c06276f3e3d6'
}

def add_blocks_to_card(notion, card_id, blocks):
    """Adiciona blocos ao card"""
    try:
        response = notion.session.patch(
            f"{notion.base_url}/blocks/{card_id}/children",
            json={"children": blocks},
            timeout=60
        )
        
        if response.status_code == 200:
            return True
        else:
            logger.error(f"Erro {response.status_code}: {response.text[:200]}")
            return False
    except Exception as e:
        logger.error(f"Erro: {e}")
        return False

def get_flight_blocks():
    """Blocos Flight Service (versao compacta)"""
    return [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "ENDPOINTS PRINCIPAIS"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/flights/availability - Buscar voos"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/flights/availability/multiple - Buscar em multiplos sistemas"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "GET /api/flights/systems - Recuperar sistemas disponiveis"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/flights/{id}/price - Tarifar voo"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/bookings - Criar reserva"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "GET /api/bookings/{locator} - Consultar reserva"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/bookings/{locator}/issue - Emitir bilhetes"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "GET /api/tickets/{number} - Consultar bilhete"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "DELETE /api/bookings/{locator} - Cancelar reserva"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "STACK TECNICA"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "FastAPI + PostgreSQL (flights_db) + Redis + httpx"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "3 tabelas: flight_searches, flight_bookings, flight_tickets"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "EXEMPLO BUSCA"}}]}},
        {"object": "block", "type": "code", "code": {"language": "python", "rich_text": [{"type": "text", "text": {"content": "@router.post(\"/api/flights/availability\")\nasync def search_flights(search: FlightSearchRequest):\n    cache_key = f\"flights:{search.origin}:{search.destination}\"\n    cached = await cache_service.get(cache_key)\n    if cached:\n        return cached\n    \n    wooba_request = {\n        \"Login\": settings.WOOBA_LOGIN,\n        \"Senha\": settings.WOOBA_PASSWORD,\n        \"Origem\": search.origin,\n        \"Destino\": search.destination,\n        \"DataIda\": convert_date(search.departure_date),\n        \"Sistema\": 0\n    }\n    \n    response = await wooba_adapter.post(\n        \"/aereo/disponibilidade\", wooba_request\n    )\n    \n    flights = parse_wooba_flights(response)\n    await cache_service.set(cache_key, flights, ttl=600)\n    return flights"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "EXEMPLO RESERVA"}}]}},
        {"object": "block", "type": "code", "code": {"language": "python", "rich_text": [{"type": "text", "text": {"content": "@router.post(\"/api/bookings\")\nasync def create_booking(booking: BookingCreateRequest):\n    wooba_request = {\n        \"Login\": settings.WOOBA_LOGIN,\n        \"Senha\": settings.WOOBA_PASSWORD,\n        \"IdentificacaoDaViagem\": booking.flight_id,\n        \"Passageiros\": build_passengers(booking.passengers),\n        \"Contatos\": build_contacts(booking.contacts),\n        \"Pagamento\": build_payment(booking.payment)\n    }\n    \n    response = await wooba_adapter.post(\n        \"/aereo/reservar\", wooba_request\n    )\n    \n    booking_entity = await booking_repository.create(\n        parse_wooba_booking(response)\n    )\n    \n    return booking_entity"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "EXEMPLO EMISSAO"}}]}},
        {"object": "block", "type": "code", "code": {"language": "python", "rich_text": [{"type": "text", "text": {"content": "@router.post(\"/api/bookings/{locator}/issue\")\nasync def issue_tickets(locator: str, payment: PaymentRequest):\n    # 1. Iniciar emissao\n    start_response = await wooba_adapter.post(\n        \"/aereo/iniciar-emissao\",\n        {\"Login\": settings.WOOBA_LOGIN, \"Senha\": settings.WOOBA_PASSWORD, \"Localizador\": locator}\n    )\n    \n    # 2. Emitir\n    tickets_response = await wooba_adapter.post(\n        \"/aereo/emitir\",\n        {\n            \"Login\": settings.WOOBA_LOGIN,\n            \"Senha\": settings.WOOBA_PASSWORD,\n            \"Localizador\": locator,\n            \"Pagamento\": build_payment(payment)\n        }\n    )\n    \n    tickets = parse_wooba_tickets(tickets_response)\n    await ticket_repository.save_all(tickets)\n    return tickets"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "DATABASE"}}]}},
        {"object": "block", "type": "code", "code": {"language": "sql", "rich_text": [{"type": "text", "text": {"content": "CREATE TABLE flight_searches (\n    id VARCHAR(36) PRIMARY KEY,\n    origin VARCHAR(3) NOT NULL,\n    destination VARCHAR(3) NOT NULL,\n    departure_date TIMESTAMP,\n    results JSONB,\n    created_at TIMESTAMP DEFAULT NOW()\n);\n\nCREATE TABLE flight_bookings (\n    id VARCHAR(36) PRIMARY KEY,\n    locator VARCHAR(10) UNIQUE NOT NULL,\n    status VARCHAR(20) DEFAULT 'CONFIRMED',\n    passengers JSONB,\n    total_price DECIMAL(10,2),\n    created_at TIMESTAMP DEFAULT NOW()\n);\n\nCREATE TABLE flight_tickets (\n    id VARCHAR(36) PRIMARY KEY,\n    ticket_number VARCHAR(13) UNIQUE NOT NULL,\n    booking_id VARCHAR(36),\n    passenger_name VARCHAR(255),\n    status VARCHAR(20) DEFAULT 'ACTIVE'\n);"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "VARIAVEIS DE AMBIENTE"}}]}},
        {"object": "block", "type": "code", "code": {"language": "bash", "rich_text": [{"type": "text", "text": {"content": "PORT=8001\nDB_HOST=flights-db\nDB_NAME=flights_db\nREDIS_URL=redis://redis:6379/1\nWOOBA_ADAPTER_URL=http://wooba-adapter:8010\nWOOBA_LOGIN=usuario_sandbox\nWOOBA_PASSWORD=senha_sandbox"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "REFERENCIAS"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Doc Wooba: /Contextos de IA/02-Trabalho/HubTravel/WOOBA_API_COMPLETA.md"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Postman: /Trabalho/Documentacoes/Wooba/Travellink Web API - Aereo.postman_collection.json"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Base ExpenseIQ: /Trabalho/expenseiq/"}}]}}
    ]

def get_hotel_blocks():
    """Blocos Hotel Service"""
    return [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "ENDPOINTS PRINCIPAIS"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/hotels/destinations - Buscar destinos"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/hotels/availability - Buscar hoteis disponiveis"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "GET /api/hotels/{id}/info - Detalhes do hotel"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/reservations - Criar reserva de hotel"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "GET /api/reservations/{id} - Consultar reserva"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "DELETE /api/reservations/{id} - Cancelar reserva"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "STACK"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "FastAPI + PostgreSQL (hotels_db) + Redis"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "2 tabelas: hotel_searches, hotel_reservations"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "EXEMPLO CODIGO"}}]}},
        {"object": "block", "type": "code", "code": {"language": "python", "rich_text": [{"type": "text", "text": {"content": "@router.post(\"/api/hotels/availability\")\nasync def search_hotels(search: HotelSearchRequest):\n    wooba_request = {\n        \"Login\": settings.WOOBA_LOGIN,\n        \"Senha\": settings.WOOBA_PASSWORD,\n        \"Destination\": search.destination,\n        \"CheckIn\": convert_date(search.checkin),\n        \"CheckOut\": convert_date(search.checkout),\n        \"Rooms\": search.rooms\n    }\n    \n    response = await wooba_adapter.post(\n        \"/hotel/avail\", wooba_request\n    )\n    \n    hotels = parse_wooba_hotels(response)\n    return hotels"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "DATABASE"}}]}},
        {"object": "block", "type": "code", "code": {"language": "sql", "rich_text": [{"type": "text", "text": {"content": "CREATE TABLE hotel_searches (\n    id VARCHAR(36) PRIMARY KEY,\n    destination VARCHAR(100),\n    checkin_date DATE,\n    checkout_date DATE,\n    results JSONB,\n    created_at TIMESTAMP DEFAULT NOW()\n);\n\nCREATE TABLE hotel_reservations (\n    id VARCHAR(36) PRIMARY KEY,\n    confirmation_code VARCHAR(20) UNIQUE,\n    hotel_id VARCHAR(50),\n    hotel_name VARCHAR(255),\n    status VARCHAR(20),\n    total_price DECIMAL(10,2),\n    created_at TIMESTAMP DEFAULT NOW()\n);"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Doc: /Trabalho/Documentacoes/Wooba/Travellink Web API - Hotel - Documentation.postman_collection.json"}}]}}
    ]

def get_vehicle_blocks():
    """Blocos Vehicle Service"""
    return [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "ENDPOINTS PRINCIPAIS"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/vehicles/availability - Buscar veiculos"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "GET /api/vehicles/{id}/details - Detalhes do veiculo"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/rentals - Criar reserva de locacao"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "GET /api/rentals/{id} - Consultar reserva"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POST /api/rentals/{id}/pickup - Confirmar retirada"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "DELETE /api/rentals/{id} - Cancelar reserva"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "STACK"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "FastAPI + PostgreSQL (vehicles_db) + Redis"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "2 tabelas: vehicle_searches, vehicle_rentals"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "EXEMPLO CODIGO"}}]}},
        {"object": "block", "type": "code", "code": {"language": "python", "rich_text": [{"type": "text", "text": {"content": "@router.post(\"/api/vehicles/availability\")\nasync def search_vehicles(search: VehicleSearchRequest):\n    wooba_request = {\n        \"Login\": settings.WOOBA_LOGIN,\n        \"Senha\": settings.WOOBA_PASSWORD,\n        \"PickupLocation\": search.pickup_location,\n        \"DropoffLocation\": search.dropoff_location,\n        \"PickupDate\": convert_date(search.pickup_date),\n        \"DropoffDate\": convert_date(search.dropoff_date)\n    }\n    \n    response = await wooba_adapter.post(\n        \"/carro/shopping\", wooba_request\n    )\n    \n    vehicles = parse_wooba_vehicles(response)\n    return vehicles"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Doc: /Trabalho/Documentacoes/Wooba/Travellink Web API - CARRO - Documentacao.postman_collection.json"}}]}}
    ]

def get_common_blocks():
    """Blocos Common Connector"""
    return [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "COMPONENTES"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "1. Wooba Adapter Service (:8010) - Auth RSA + Cliente HTTP"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "2. HubTravel Shared Library - Codigo compartilhado"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "3. API Gateway (:8000) - Roteamento unificado"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "AUTH RSA/PKCS1"}}]}},
        {"object": "block", "type": "code", "code": {"language": "python", "rich_text": [{"type": "text", "text": {"content": "from cryptography.hazmat.primitives import serialization\nfrom cryptography.hazmat.primitives.asymmetric import padding\nimport base64\n\ndef encrypt_access_code(text: str, date: str, public_key_xml: str) -> str:\n    value = f\"{text}|{date}\"\n    public_key = parse_xml_public_key(public_key_xml)\n    \n    encrypted = public_key.encrypt(\n        value.encode('utf-8'),\n        padding.PKCS1v15()\n    )\n    \n    return base64.b64encode(encrypted).decode('utf-8')"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "CLIENTE WOOBA BASE"}}]}},
        {"object": "block", "type": "code", "code": {"language": "python", "rich_text": [{"type": "text", "text": {"content": "class WoobaClient:\n    def __init__(self):\n        self.base_url = settings.WOOBA_BASE_URL\n        self.dev_token = settings.WOOBA_DEV_TOKEN\n        self.dev_access_code = encrypt_access_code(\n            \"HUBTRAVEL\", datetime.now().strftime(\"%d/%m/%Y\"), PUBLIC_KEY\n        )\n    \n    async def post(self, endpoint: str, data: Dict):\n        headers = {\n            \"Developer-Token\": self.dev_token,\n            \"Developer-Access-Code\": self.dev_access_code,\n            \"Content-Type\": \"application/json\"\n        }\n        \n        async with httpx.AsyncClient() as client:\n            response = await client.post(\n                f\"{self.base_url}{endpoint}\",\n                json=data,\n                headers=headers,\n                timeout=30.0\n            )\n            return response.json()"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "API GATEWAY"}}]}},
        {"object": "block", "type": "code", "code": {"language": "python", "rich_text": [{"type": "text", "text": {"content": "# api-gateway/app/main.py\nfrom fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\n\napp = FastAPI(title=\"HubTravel API Gateway\")\n\n# Rotas para Flight Service\napp.include_router(\n    flight_router,\n    prefix=\"/api/v1/flights\",\n    tags=[\"flights\"]\n)\n\n# Rotas para Hotel Service\napp.include_router(\n    hotel_router,\n    prefix=\"/api/v1/hotels\",\n    tags=[\"hotels\"]\n)\n\n# Rotas para Vehicle Service\napp.include_router(\n    vehicle_router,\n    prefix=\"/api/v1/vehicles\",\n    tags=[\"vehicles\"]\n)"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Doc: /Contextos de IA/02-Trabalho/HubTravel/HUBTRAVEL_CONTEXTO.md"}}]}}
    ]

def get_docs_blocks():
    """Blocos Documentation"""
    return [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "DOCUMENTACAO CRIADA"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "1. HUBTRAVEL_CONTEXTO.md (9.4KB) - Visao geral"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "2. WOOBA_API_COMPLETA.md (21KB) - API completa"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "3. ENDPOINTS_RESUMO.md (1.3KB) - Lista rapida"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "4. CARDS_NOTION_CRIADOS.md (6KB) - IDs e URLs"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "5. RESUMO_EXECUCAO.md - Este resumo"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "PROXIMOS DOCUMENTOS"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "README.md - Documentacao principal do projeto"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "ARCHITECTURE.md - Diagrama de arquitetura completo"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "API_SPECS/ - 6 arquivos OpenAPI (um por servico)"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "DIAGRAMS/ - 5 diagramas Mermaid de fluxos"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "POSTMAN/ - Collections atualizadas"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "LOCALIZACAO"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Toda documentacao em: /home/lucas-biason/Projetos/Contextos de IA/02-Trabalho/HubTravel/"}}]}}
    ]

def main():
    """Atualizar todos os cards"""
    print("=" * 80)
    print("ATUALIZANDO TODOS OS CARDS HUBTRAVEL COM DOCUMENTACAO")
    print("=" * 80)
    
    config = NotionConfig.from_env()
    notion = NotionAPIManager(config)
    
    if not notion.test_connection():
        return False
    
    updates = [
        ('Flight Service', CARDS['flight'], get_flight_blocks()),
        ('Hotel Service', CARDS['hotel'], get_hotel_blocks()),
        ('Vehicle Service', CARDS['vehicle'], get_vehicle_blocks()),
        ('Common Connector', CARDS['common'], get_common_blocks()),
        ('Documentation', CARDS['docs'], get_docs_blocks())
    ]
    
    success_count = 0
    
    for name, card_id, blocks in updates:
        print(f"\nAtualizando: {name}...")
        print(f"   ID: {card_id}")
        print(f"   Blocos: {len(blocks)}")
        
        if add_blocks_to_card(notion, card_id, blocks):
            print(f"   ✅ {name} atualizado")
            success_count += 1
        else:
            print(f"   ❌ {name} falhou")
    
    print("\n" + "=" * 80)
    print(f"RESULTADO: {success_count}/5 cards atualizados com sucesso")
    print("=" * 80)
    
    if success_count == 5:
        print("\n✅ Todos os cards foram atualizados!")
        print(f"   Verifique: https://notion.so/287962a7693c815fb835c0b46026a5d8")
        return True
    else:
        print(f"\n⚠️ Alguns cards falharam. Verifique os logs acima.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)



