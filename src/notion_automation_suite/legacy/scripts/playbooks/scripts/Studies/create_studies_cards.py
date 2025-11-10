#!/usr/bin/env python3
"""
Create Studies Cards Script
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Script para criar cards de estudos no Notion.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from core import NotionAPIManager, NotionConfig, StudiesCardCreator
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Função principal para criar cards de estudos."""
    print("=" * 60)
    print("📚 CRIANDO CARDS DE ESTUDOS - NOTION")
    print("=" * 60)
    
    try:
        # Carregar configuração
        config = NotionConfig.from_env()
        
        # Criar gerenciador
        notion_manager = NotionAPIManager(config)
        
        # Testar conexão
        logger.info("Testando conexão com Notion...")
        if not notion_manager.test_connection():
            logger.error("Falha na conexão com Notion")
            return False
        
        # Criar cards
        creator = StudiesCardCreator(notion_manager)
        
        # Cards de estudos
        logger.info("Criando cards de estudos...")
        results = creator.create_all_studies_cards()
        
        # Mostrar resultados
        print("\n" + "=" * 60)
        print("📊 RESULTADOS - ESTUDOS:")
        print("=" * 60)
        
        success_count = 0
        for card_type, result in results.items():
            if result:
                print(f"✅ {card_type.upper()}: {result['id']}")
                print(f"   URL: {result.get('url', 'N/A')}")
                success_count += 1
            else:
                print(f"❌ {card_type.upper()}: Falha na criação")
        
        total_cards = len(results)
        print(f"\n🎉 Processo concluído! {success_count}/{total_cards} cards criados com sucesso")
        
        if success_count == total_cards:
            print("\n📋 Cards criados:")
            print("1. FIAP - Fine Tuning Tech Challenge")
            print("2. IA Knowledge Base")
            print("3. FIAP - Fase 4")
            print("\n🔗 Acesse seu Notion para ver os cards!")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro na execução: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
