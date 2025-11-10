#!/usr/bin/env python3
"""
Script para migrar relatórios markdown para cards do Notion
"""

import os
import re
from pathlib import Path

# Mapeamento de arquivos para IDs dos cards
CARD_MAPPING = {
    'relatorio_dashboard_service_final.md': '279962a7-693c-81f6-a537-e12b2b7e7ea9',
    'relatorio_ocr_service_final.md': '279962a7-693c-8109-aada-d46736fdf04a',
    'relatorio_documents_service.md': '279962a7-693c-812b-8dd8-fa1d5fde1e9c',
    'relatorio_company_service.md': '279962a7-693c-81c3-b4db-e1dec8178414',
    'relatorio_user_service.md': '279962a7-693c-814c-bb1f-ffb2f655ddb1',
    'relatorio_verificacao_curl_commands.md': '279962a7-693c-8127-9d47-ed1ddfe9d285',
    'relatorio_teste_campo_number.md': '279962a7-693c-8127-9d47-ed1ddfe9d285',
    'relatorio_final_testes_expenseiq_consolidado.md': '279962a7-693c-8118-aa97-ec9a677c0f01',
    'relatorio_final_testes_expenseiq_completo.md': '279962a7-693c-8118-aa97-ec9a677c0f01'
}

def read_markdown_file(file_path):
    """Lê arquivo markdown e retorna conteúdo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")
        return None

def parse_markdown_to_notion_blocks(content):
    """Converte markdown para blocos do Notion"""
    blocks = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Títulos
        if line.startswith('# '):
            blocks.append({
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{'type': 'text', 'text': {'content': f"📋 {line[2:]}"}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{'type': 'text', 'text': {'content': f"🔹 {line[3:]}"}}]
                }
            })
        elif line.startswith('### '):
            blocks.append({
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{'type': 'text', 'text': {'content': f"• {line[4:]}"}}]
                }
            })
        # Listas
        elif line.startswith('- '):
            blocks.append({
                'type': 'bulleted_list_item',
                'bulleted_list_item': {
                    'rich_text': [{'type': 'text', 'text': {'content': line[2:]}}]
                }
            })
        # Texto normal
        else:
            # Adiciona emojis baseado no conteúdo
            emoji = ""
            if 'passaram' in line.lower() or 'passou' in line.lower():
                emoji = "✅ "
            elif 'falharam' in line.lower() or 'falhou' in line.lower():
                emoji = "❌ "
            elif 'erro' in line.lower():
                emoji = "⚠️ "
            elif 'cobertura' in line.lower():
                emoji = "📈 "
            elif 'problema' in line.lower():
                emoji = "🔧 "
            elif 'conclusão' in line.lower():
                emoji = "📝 "
            elif 'data' in line.lower():
                emoji = "🕒 "
            
            blocks.append({
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{'type': 'text', 'text': {'content': f"{emoji}{line}"}}]
                }
            })
    
    return blocks

def main():
    """Função principal"""
    base_dir = Path(__file__).parent
    
    for filename, card_id in CARD_MAPPING.items():
        file_path = base_dir / filename
        if file_path.exists():
            print(f"Processando {filename}...")
            content = read_markdown_file(file_path)
            if content:
                blocks = parse_markdown_to_notion_blocks(content)
                print(f"  - {len(blocks)} blocos gerados para card {card_id}")
                # Aqui você adicionaria a lógica para enviar para o Notion
                # Por enquanto, apenas mostra o que seria enviado
                print(f"  - Primeiro bloco: {blocks[0] if blocks else 'Nenhum'}")
            else:
                print(f"  - Erro ao ler arquivo")
        else:
            print(f"Arquivo não encontrado: {filename}")

if __name__ == "__main__":
    main()
