#!/usr/bin/env python3
"""
Criar estrutura completa de cards para Deploy Render + Supabase
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.notion_manager import NotionAPIManager, NotionConfig
from core import DatabaseType

config = NotionConfig.from_env()
notion = NotionAPIManager(config)

print("=" * 80)
print("🚀 CRIANDO CARDS: DEPLOY RENDER + SUPABASE")
print("=" * 80)

# ============================================================================
# CARD 1: PROJETO PRINCIPAL
# ============================================================================
print("\n📦 1. Criando card principal do projeto...")

main_card_properties = {
    "Nome do projeto": {
        "title": [{"text": {"content": "🚀 Deploy ExpenseIQ - Render + Supabase"}}]
    },
    "Status": {"status": {"name": "Em Andamento"}},
    "Prioridade": {"select": {"name": "Alta"}},
    "Cliente": {"select": {"name": "Astracode"}},
    "Projeto": {"select": {"name": "Expense IQ"}}
}

main_card_content = [
    {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{"type": "text", "text": {"content": "🚀 Deploy ExpenseIQ - Render + Supabase"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": "Projeto completo de deploy do ExpenseIQ no Render com Supabase como banco PostgreSQL. Inclui compatibilidade híbrida, unificação de variáveis de ambiente e otimização de limites de upload."}}]
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "💰 Custo Total: $91/mês ($1,092/ano)"}}]
        }
    },
    {
        "object": "block",
        "type": "code",
        "code": {
            "language": "plain text",
            "rich_text": [{"type": "text", "text": {"content": "APLICAÇÕES (Render):\n- 8x Starter Services ($7)    = $56/mês\n- Frontend Static Site         = GRÁTIS\n\nBANCO DE DADOS:\n- Supabase Pro (PostgreSQL)    = $25/mês\n  - 8 GB storage\n  - 2 GB RAM\n  - 200 conexões\n  - Backups point-in-time\n\nCACHE:\n- Render Redis Starter         = $10/mês\n\nSTORAGE:\n- Render Persistent Disk 1GB   = GRÁTIS\n- Escala: $1/GB/mês quando necessário\n\nTOTAL: $91/mês\nECONOMIA vs Heroku: $60/mês ($720/ano)"}}]
            }
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "⏱️ Cronograma Total: 12-16 horas"}}]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": "Este projeto está dividido em 4 subitens principais que devem ser executados em sequência:"}}]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "1. Compatibilidade Híbrida Supabase/Postgres (2-3h)"}}]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "2. Separação de Migrations (2-3h)"}}]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "3. Unificação de Variáveis de Ambiente (1-2h)"}}]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "4. Redução de Limites de Upload (1h)"}}]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "5. Configuração Render + Deploy (4-6h)"}}]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "6. Testes Completos (2h)"}}]
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
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Sistema funciona com Supabase E Postgres local (híbrido)"}}],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Migrations rodadas separadamente (não automático)"}}],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Todas variáveis em configs/.env.global"}}],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Versão do sistema unificada"}}],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Persistent Disk configurado (arquivos não se perdem)"}}],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Limites de upload reduzidos (2MB fotos, 2.5MB recibos)"}}],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": "Deploy funcionando no Render"}}],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "📁 Arquivos Principais"}}]
        }
    },
    {
        "object": "block",
        "type": "code",
        "code": {
            "language": "plain text",
            "rich_text": [{"type": "text", "text": {"content": "configs/.env.global                           # Todas as variáveis unificadas\nVERSION                                       # Versão única do sistema\nrender.yaml                                   # Configuração Render\nMakefile                                      # Comandos atualizados\nexpenseiq-shared/database/database.py         # Híbrido Supabase/Postgres\nexpenseiq-shared/cache/cache_system.py        # REDIS_URL support\n*/entrypoint.sh (8 arquivos)                  # PORT dinâmico\nocr-service/app/validators/file_validator.py  # Limite 2.5MB\nuser-service/... (validação foto perfil)      # Limite 2MB"}}]
        }
    }
]

response = notion.session.post(
    f"{notion.base_url}/pages",
    json={
        "parent": {"database_id": notion.config.databases[DatabaseType.WORK]},
        "properties": main_card_properties,
        "children": main_card_content,
        "icon": {"type": "emoji", "emoji": "🚀"}
    },
    timeout=notion.config.timeout
)

if response.status_code == 200:
    main_page_id = response.json()['id']
    print(f"✅ Card principal criado: {main_page_id}")
else:
    print(f"❌ Erro: {response.status_code} - {response.text}")
    exit(1)

print(f"\n🔗 URL: https://www.notion.so/{main_page_id.replace('-', '')}")
print(f"\nPróximos: Criar 4 cards subitens e vincular ao principal")
print(f"ID Principal salvo: {main_page_id}")

# Salvar ID para próximos scripts
with open('/tmp/render_main_card_id.txt', 'w') as f:
    f.write(main_page_id)

print("\n✅ Card principal criado com sucesso!")

