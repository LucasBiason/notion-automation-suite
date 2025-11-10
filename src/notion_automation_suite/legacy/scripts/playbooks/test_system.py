#!/usr/bin/env python3
"""
Test System Script
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Script para testar todo o sistema Notion Projects.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("🔍 Testando imports...")
    
    try:
        from core import (
            NotionAPIManager, NotionConfig, DatabaseType, 
            TaskStatus, Priority, NotionAPIError,
            WorkCardCreator, StudiesCardCreator, 
            PersonalCardCreator, YoutuberCardCreator
        )
        print("✅ Imports do core OK")
        
        # Testar imports dos scripts
        from scripts.Work.create_work_cards import main as work_main
        from scripts.Studies.create_studies_cards import main as studies_main
        from scripts.Personal.create_personal_cards import main as personal_main
        from scripts.Youtuber.create_youtuber_cards import main as youtuber_main
        print("✅ Imports dos scripts OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False

def test_config():
    """Testa configuração."""
    print("\n🔧 Testando configuração...")
    
    try:
        from core import NotionConfig
        
        # Verificar se .env existe
        env_file = Path(".env")
        if not env_file.exists():
            print("⚠️  Arquivo .env não encontrado")
            print("Crie o arquivo .env com suas configurações")
            return False
        
        # Carregar .env
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ Arquivo .env carregado")
        except ImportError:
            print("⚠️  python-dotenv não instalado")
            print("Execute: pip install python-dotenv")
            return False
        
        # Verificar configuração
        try:
            config = NotionConfig.from_env()
            print("✅ Configuração carregada")
            
            # Verificar token
            if not config.api_token:
                print("❌ NOTION_API_TOKEN não configurado")
                return False
            print("✅ Token configurado")
            
            # Verificar databases
            for db_type, db_id in config.databases.items():
                if not db_id:
                    print(f"⚠️  {db_type.value} database ID não configurado")
                else:
                    print(f"✅ {db_type.value}: {db_id[:8]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na configuração: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de configuração: {e}")
        return False

def test_connection():
    """Testa conexão com Notion."""
    print("\n🌐 Testando conexão com Notion...")
    
    try:
        from core import NotionAPIManager, NotionConfig
        
        config = NotionConfig.from_env()
        notion_manager = NotionAPIManager(config)
        
        if notion_manager.test_connection():
            print("✅ Conexão estabelecida!")
            return True
        else:
            print("❌ Falha na conexão")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_card_creators():
    """Testa criadores de cards."""
    print("\n🎯 Testando criadores de cards...")
    
    try:
        from core import NotionAPIManager, NotionConfig, WorkCardCreator
        
        config = NotionConfig.from_env()
        notion_manager = NotionAPIManager(config)
        
        # Testar WorkCardCreator
        work_creator = WorkCardCreator(notion_manager)
        print("✅ WorkCardCreator criado")
        
        # Testar métodos (sem executar)
        methods = [
            'create_title_property',
            'create_select_property',
            'create_status_property',
            'create_date_property'
        ]
        
        for method in methods:
            if hasattr(work_creator, method):
                print(f"✅ Método {method} disponível")
            else:
                print(f"❌ Método {method} não encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de criadores: {e}")
        return False

def main():
    """Função principal."""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA NOTION PROJECTS")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuração", test_config),
        ("Conexão", test_connection),
        ("Criadores de Cards", test_card_creators)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            print(f"✅ {test_name}: PASSOU")
            passed += 1
        else:
            print(f"❌ {test_name}: FALHOU")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADO: {passed}/{total} testes passaram")
    print("=" * 60)
    
    if passed == total:
        print("🎉 Todos os testes passaram!")
        print("✅ Sistema pronto para uso")
        print("\n🚀 Próximos passos:")
        print("1. python3 main.py --test")
        print("2. python3 main.py --work")
        print("3. python3 main.py --all")
    else:
        print("❌ Alguns testes falharam")
        print("🔧 Verifique as configurações e dependências")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
