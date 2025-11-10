#!/usr/bin/env python3
"""
Script para obter TODOs diários de todas as bases do Notion (versão corrigida)
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from core.notion_manager import NotionAPIManager, NotionConfig, DatabaseType
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_rich_text(rich_text):
    """Extrai texto de rich_text."""
    if not rich_text:
        return ""
    return "".join([item.get('text', {}).get('content', '') for item in rich_text])

def get_database_properties(notion, database_id):
    """Obtém propriedades de uma database."""
    try:
        response = notion.session.get(
            f"{notion.base_url}/databases/{database_id}",
            timeout=notion.config.timeout
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('properties', {})
    except Exception as e:
        logger.error(f"Erro ao obter propriedades: {e}")
    return {}

def get_today_todos():
    """Obtém TODOs de hoje de todas as bases."""
    print("=" * 60)
    print("📅 TODOs DE HOJE - 29 DE SETEMBRO DE 2025")
    print("=" * 60)
    
    try:
        # Carregar configuração
        config = NotionConfig.from_env()
        
        # Inicializar Notion Manager
        notion = NotionAPIManager(config)
        
        # Testar conexão
        if not notion.test_connection():
            print("❌ Falha na conexão com Notion")
            return False
        
        # Data de hoje
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"📅 Data: {today}")
        
        # Bases para verificar
        databases = {
            "Pessoal": DatabaseType.PERSONAL,
            "Cursos": DatabaseType.STUDIES,
            "Trabalho": DatabaseType.WORK,
            "Youtuber": DatabaseType.YOUTUBER
        }
        
        all_todos = {}
        
        for db_name, db_type in databases.items():
            print(f"\n📊 Verificando {db_name}...")
            
            database_id = config.databases.get(db_type)
            if not database_id:
                print(f"   ❌ Database {db_name} não configurado")
                continue
            
            # Obter propriedades da database
            properties = get_database_properties(notion, database_id)
            print(f"   Propriedades: {list(properties.keys())}")
            
            # Buscar propriedade de data
            date_property = None
            for prop_name, prop_info in properties.items():
                if prop_info.get('type') == 'date':
                    date_property = prop_name
                    break
            
            if not date_property:
                print(f"   ⚠️ Nenhuma propriedade de data encontrada")
                # Buscar todos os itens sem filtro de data
                query_response = notion.session.post(
                    f"{notion.base_url}/databases/{database_id}/query",
                    json={},
                    timeout=notion.config.timeout
                )
            else:
                print(f"   📅 Usando propriedade de data: {date_property}")
                # Consultar database com filtro de data
                query_response = notion.session.post(
                    f"{notion.base_url}/databases/{database_id}/query",
                    json={
                        "filter": {
                            "property": date_property,
                            "date": {
                                "equals": today
                            }
                        }
                    },
                    timeout=notion.config.timeout
                )
            
            if query_response.status_code == 200:
                query_data = query_response.json()
                items = query_data.get('results', [])
                print(f"   ✅ {len(items)} itens encontrados")
                
                todos = []
                for item in items:
                    properties = item.get('properties', {})
                    
                    # Extrair informações do item
                    todo_info = {}
                    
                    # Título/Nome
                    for prop_name, prop_value in properties.items():
                        if prop_value.get('type') == 'title':
                            if prop_value.get('title'):
                                todo_info['titulo'] = extract_text_from_rich_text(prop_value.get('title', []))
                            break
                    
                    # Status
                    for prop_name, prop_value in properties.items():
                        if 'status' in prop_name.lower():
                            if prop_value.get('select'):
                                todo_info['status'] = prop_value['select'].get('name', 'N/A')
                            break
                    
                    # Data
                    for prop_name, prop_value in properties.items():
                        if prop_value.get('type') == 'date':
                            if prop_value.get('date'):
                                todo_info['data'] = prop_value['date'].get('start', 'N/A')
                            break
                    
                    # Hora (se existir)
                    for prop_name, prop_value in properties.items():
                        if 'hora' in prop_name.lower() or 'time' in prop_name.lower():
                            if prop_value.get('rich_text'):
                                todo_info['hora'] = extract_text_from_rich_text(prop_value.get('rich_text', []))
                            break
                    
                    # Descrição
                    for prop_name, prop_value in properties.items():
                        if 'desc' in prop_name.lower() or 'description' in prop_name.lower():
                            if prop_value.get('rich_text'):
                                todo_info['descricao'] = extract_text_from_rich_text(prop_value.get('rich_text', []))
                            break
                    
                    # Responsável
                    for prop_name, prop_value in properties.items():
                        if 'resp' in prop_name.lower() or 'responsible' in prop_name.lower():
                            if prop_value.get('rich_text'):
                                todo_info['responsavel'] = extract_text_from_rich_text(prop_value.get('rich_text', []))
                            break
                    
                    todos.append(todo_info)
                
                all_todos[db_name] = todos
            else:
                print(f"   ❌ Erro ao consultar {db_name}: {query_response.status_code}")
                if query_response.status_code == 400:
                    try:
                        error_data = query_response.json()
                        print(f"   Detalhes do erro: {error_data}")
                    except:
                        print(f"   Resposta: {query_response.text}")
        
        # Mostrar resumo
        print("\n" + "=" * 60)
        print("📋 RESUMO DOS TODOs DE HOJE")
        print("=" * 60)
        
        total_todos = 0
        for db_name, todos in all_todos.items():
            print(f"\n🎯 {db_name.upper()}:")
            if todos:
                for i, todo in enumerate(todos, 1):
                    print(f"   {i}. {todo.get('titulo', 'Sem título')}")
                    if todo.get('hora'):
                        print(f"      ⏰ {todo['hora']}")
                    if todo.get('status'):
                        print(f"      📊 Status: {todo['status']}")
                    if todo.get('descricao'):
                        desc = todo['descricao']
                        if len(desc) > 100:
                            desc = desc[:100] + "..."
                        print(f"      📝 {desc}")
                    print()
                total_todos += len(todos)
            else:
                print("   ✅ Nenhuma tarefa para hoje")
        
        print(f"\n📊 Total de tarefas: {total_todos}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro na execução: {str(e)}")
        return False

if __name__ == "__main__":
    success = get_today_todos()
    sys.exit(0 if success else 1)

