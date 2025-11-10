#!/usr/bin/env python3
"""
Notion Projects - Main Script
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Script principal para executar todo o sistema Notion Projects.
"""

import os
import sys
import argparse
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

from core import NotionAPIManager, NotionConfig
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Testa conexão com Notion."""
    print("🔍 Testando conexão com Notion...")
    
    try:
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

def create_work_cards():
    """Cria cards de trabalho."""
    print("\n🎯 Criando cards de trabalho...")
    
    try:
        from scripts.Work.create_work_cards import main as create_work
        return create_work()
    except Exception as e:
        logger.error(f"Erro ao criar cards de trabalho: {e}")
        return False

def create_studies_cards():
    """Cria cards de estudos."""
    print("\n📚 Criando cards de estudos...")
    
    try:
        from scripts.Studies.create_studies_cards import main as create_studies
        return create_studies()
    except Exception as e:
        logger.error(f"Erro ao criar cards de estudos: {e}")
        return False

def create_personal_cards():
    """Cria cards pessoais."""
    print("\n👤 Criando cards pessoais...")
    
    try:
        from scripts.Personal.create_personal_cards import main as create_personal
        return create_personal()
    except Exception as e:
        logger.error(f"Erro ao criar cards pessoais: {e}")
        return False

def create_youtuber_cards():
    """Cria cards do YouTube."""
    print("\n🎬 Criando cards do YouTube...")
    
    try:
        from scripts.Youtuber.create_youtuber_cards import main as create_youtuber
        return create_youtuber()
    except Exception as e:
        logger.error(f"Erro ao criar cards do YouTube: {e}")
        return False

def create_all_cards():
    """Cria todos os cards."""
    print("=" * 60)
    print("🚀 CRIANDO TODOS OS CARDS - NOTION")
    print("=" * 60)
    
    # Testar conexão primeiro
    if not test_connection():
        print("❌ Falha na conexão. Verifique suas configurações.")
        return False
    
    # Criar cards de cada frente
    results = {}
    
    # Trabalho
    results['work'] = create_work_cards()
    
    # Estudos
    results['studies'] = create_studies_cards()
    
    # Pessoal
    results['personal'] = create_personal_cards()
    
    # YouTube
    results['youtuber'] = create_youtuber_cards()
    
    # Mostrar resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO FINAL:")
    print("=" * 60)
    
    success_count = 0
    total_count = len(results)
    
    for front, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {front.upper()}: {'Sucesso' if success else 'Falha'}")
        if success:
            success_count += 1
    
    print(f"\n🎉 Processo concluído! {success_count}/{total_count} frentes executadas com sucesso")
    
    if success_count == total_count:
        print("\n📋 Todos os cards foram criados com sucesso!")
        print("🔗 Acesse seu Notion para ver os cards!")
    
    return success_count == total_count

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description='Notion Projects - Sistema de Automação')
    parser.add_argument('--test', action='store_true', help='Apenas testar conexão')
    parser.add_argument('--work', action='store_true', help='Criar apenas cards de trabalho')
    parser.add_argument('--studies', action='store_true', help='Criar apenas cards de estudos')
    parser.add_argument('--personal', action='store_true', help='Criar apenas cards pessoais')
    parser.add_argument('--youtuber', action='store_true', help='Criar apenas cards do YouTube')
    parser.add_argument('--all', action='store_true', help='Criar todos os cards (padrão)')
    
    args = parser.parse_args()
    
    # Se nenhum argumento foi passado, criar todos os cards
    if not any([args.test, args.work, args.studies, args.personal, args.youtuber, args.all]):
        args.all = True
    
    try:
        if args.test:
            success = test_connection()
        elif args.work:
            success = create_work_cards()
        elif args.studies:
            success = create_studies_cards()
        elif args.personal:
            success = create_personal_cards()
        elif args.youtuber:
            success = create_youtuber_cards()
        elif args.all:
            success = create_all_cards()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⏹️  Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
