#!/usr/bin/env python3
"""
Exemplo de Criação de Subitens
Versão: 3.0
Data: 25/09/2025
Status: Ativo - Reestruturado

Exemplo de como usar o sistema para criar subitens facilmente.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from core import NotionAPIManager, NotionConfig, WorkCardCreator, TaskStatus, Priority
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def exemplo_criacao_subitens():
    """Exemplo de como criar subitens facilmente."""
    print("=" * 60)
    print("📋 EXEMPLO DE CRIAÇÃO DE SUBITENS")
    print("=" * 60)
    
    try:
        # Carregar configuração
        config = NotionConfig.from_env()
        
        # Criar gerenciador
        notion_manager = NotionAPIManager(config)
        
        # Testar conexão
        if not notion_manager.test_connection():
            print("❌ Falha na conexão com Notion")
            return False
        
        # Criar criador de cards
        creator = WorkCardCreator(notion_manager)
        
        # ID do card principal (ExpenseIQ - Release 1.0.2)
        parent_id = "24e962a7-693c-801e-aaca-d17f17960378"
        
        print(f"\n🎯 Criando subitens para o card principal: {parent_id}")
        
        # Exemplo 1: Subitem simples
        print("\n1. Criando subitem simples...")
        subitem1 = creator.create_subitem_card(
            title="ExpenseIQ - Teste de Integração WhatsApp",
            parent_id=parent_id,
            icon="📱",
            status=TaskStatus.TODO,
            priority=Priority.HIGH,
            cover_type="expenseiq"
        )
        
        if subitem1:
            print(f"✅ Subitem criado: {subitem1['id']}")
        else:
            print("❌ Falha ao criar subitem")
        
        # Exemplo 2: Subitem com configurações personalizadas
        print("\n2. Criando subitem personalizado...")
        subitem2 = creator.create_subitem_card(
            title="ExpenseIQ - Validação de Performance",
            parent_id=parent_id,
            icon="⚡",
            status=TaskStatus.IN_PROGRESS,
            priority=Priority.MEDIUM,
            cover_type="testes"
        )
        
        if subitem2:
            print(f"✅ Subitem criado: {subitem2['id']}")
        else:
            print("❌ Falha ao criar subitem")
        
        # Exemplo 3: Múltiplos subitens
        print("\n3. Criando múltiplos subitens...")
        subitens = [
            ("ExpenseIQ - Documentação API Reports", "📊", "documentacao"),
            ("ExpenseIQ - Documentação API Receipts", "🧾", "documentacao"),
            ("ExpenseIQ - Documentação API Auth", "🔐", "documentacao"),
            ("ExpenseIQ - Documentação API Users", "👥", "documentacao")
        ]
        
        for title, icon, cover_type in subitens:
            subitem = creator.create_subitem_card(
                title=title,
                parent_id=parent_id,
                icon=icon,
                status=TaskStatus.TODO,
                priority=Priority.MEDIUM,
                cover_type=cover_type
            )
            
            if subitem:
                print(f"✅ {title}: {subitem['id']}")
            else:
                print(f"❌ Falha: {title}")
        
        print("\n" + "=" * 60)
        print("🎉 Exemplo concluído!")
        print("=" * 60)
        print("\n💡 Dicas de uso:")
        print("1. Use create_subitem_card() para criar subitens facilmente")
        print("2. Ícones são aplicados automaticamente")
        print("3. Capas são geradas automaticamente baseadas no tipo")
        print("4. Relacionamento com item principal é criado automaticamente")
        print("5. Propriedades Cliente e Projeto são preenchidas automaticamente")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro na execução: {str(e)}")
        return False

if __name__ == "__main__":
    success = exemplo_criacao_subitens()
    sys.exit(0 if success else 1)
