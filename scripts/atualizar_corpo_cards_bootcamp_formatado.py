#!/usr/bin/env python3
"""
Atualiza o corpo dos 4 cards do Bootcamp Pythonando no Notion:
- Formatação correta (headings, listas, bold, código, tabelas) via md_to_notion_blocks.
- Conteúdo integral nos cards (sem referências a arquivos).
- Preenche Bloco 3 e Bloco 4 com resumos e status.

Uso:
  cd notion-automation-suite
  BOOTCAMP_ROOT="/path/to/Pythonando Bootcamp" PYTHONPATH=src python3 scripts/atualizar_corpo_cards_bootcamp_formatado.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root / "src"))

from dotenv import load_dotenv

if (_root / "config" / ".env").exists():
    load_dotenv(_root / "config" / ".env", override=True)
else:
    load_dotenv(_root / ".env", override=True)
if os.environ.get("NOTION_ENV_FILE") and Path(os.environ["NOTION_ENV_FILE"]).exists():
    load_dotenv(Path(os.environ["NOTION_ENV_FILE"]), override=True)

from runtime.config import load_config
from services.notion_service import NotionService
from utils.md_to_notion_blocks import expand_tables_for_append, md_to_notion_blocks

# IDs dos cards criados por criar_blocos_bootcamp_subitens.py
PAGE_BLOCO_1 = "302962a7-693c-817f-b51b-f02d236ea63e"
PAGE_BLOCO_2 = "302962a7-693c-817c-a4a6-f7565d1c0442"
PAGE_BLOCO_3 = "302962a7-693c-8197-a750-d8011fecbf2b"
PAGE_BLOCO_4 = "302962a7-693c-81b4-87af-df1346e63bf9"
BOOTCAMP_PAGE_ID = "300962a7-693c-8140-8162-f651e3c5559d"

BATCH_SIZE = 100

# Resumo Bloco 3 — Funcionalidades com IA (Dia 2 manhã) — conteúdo integral no card
RESUMO_BLOCO_3 = """# Bloco 3 — Funcionalidades com IA (Dia 2 manhã)

Resumo do bloco: integração de IA no projeto Jury AI (chat, RAG, análise jurisprudencial, ver referências).

## Objetivos do bloco

- Revisar e praticar **Chat** com streaming e análise jurisprudencial.
- **RAG** e base de conhecimento (LanceDB, documentos, embeddings).
- Endpoint **Ver referências** e fluxo de respostas baseadas em contexto.
- Testes (pytest, E2E com Playwright) e validação das funcionalidades.

## Principais endpoints (Jury AI)

| Área | Endpoint / URL | Uso |
|------|----------------|-----|
| Chat | `POST /api/chat/` | Cria pergunta; stream e análise em views separadas |
| Análise jurisprudencial | `POST /api/chat/analise-jurisprudencia/` | Processar análise com classificação Médio/Crítico |
| Ver referências | `/ver-referencias/<pergunta_id>/` | Exibe fontes e trechos recuperados |
| Documentos (OCR) | `POST /api/documents/ocr/` | Upload e processamento de documentos |

## RAG e base de conhecimento

O agente **SecretariaAI** usa LanceDB e base `knowledge`; é necessário garantir que a base está populada (documentos/embedding) para respostas baseadas em conhecimento. O conceito de RAG foi praticado no Bloco 1 (LangChain + FAISS) e reutilizado no Jury AI.

## Status e observações

- Bloco 3 corresponde ao **Dia 2 manhã** do bootcamp (09:00–12:00).
- Conteúdo alinhado ao roteiro Notion (Construção da base + Funcionalidades com IA).
"""


async def _delete_all_children(service: NotionService, page_id: str) -> None:
    cursor = None
    while True:
        resp = await service.get_block_children(page_id, start_cursor=cursor, page_size=100)
        results = resp.get("results", [])
        for block in results:
            bid = block.get("id")
            if bid:
                await service.delete_block(bid)
        cursor = resp.get("next_cursor")
        if not cursor or not results:
            break


async def _append_blocks_batched(
    service: NotionService,
    page_id: str,
    flat: list[dict],
) -> None:
    for i in range(0, len(flat), BATCH_SIZE):
        await service.append_blocks(page_id, flat[i : i + BATCH_SIZE])


async def main() -> None:
    config = load_config()
    service = NotionService(token=config.token)

    bootcamp_root = os.environ.get("BOOTCAMP_ROOT")
    if bootcamp_root:
        bootcamp_root = Path(bootcamp_root)
    else:
        bootcamp_root = (
            _root.parent.parent
            / "Estudos"
            / "programming-lab"
            / "artificial-intelligence"
            / "projects"
            / "Pythonando Bootcamp"
        )
    if not bootcamp_root.exists():
        print(f"Pasta do Bootcamp nao encontrada: {bootcamp_root}. Defina BOOTCAMP_ROOT.")
        return

    # Bloco 1–4: resumos a partir dos arquivos no repositório do Bootcamp
    path_bloco1 = bootcamp_root / "Bloco 1" / "RESUMO_BLOCO1_CODIGO_DESENVOLVIDO.md"
    path_bloco2 = bootcamp_root / "Bloco 2" / "CONSTRUCAO_DA_BASE.md"
    path_bloco3 = bootcamp_root / "Bloco 3" / "RESUMO_BLOCO3.md"
    path_bloco4 = bootcamp_root / "Bloco 4" / "RESUMO_BLOCO4.md"
    path_bloco4_fallback = bootcamp_root / "Bloco 2" / "docs" / "GOOGLE_CALENDAR_BLOCO4.md"

    def _read(path: Path | None, fallback: str | None = None) -> str | None:
        if path and path.exists():
            return path.read_text(encoding="utf-8")
        return fallback

    for page_id, name, content in [
        (PAGE_BLOCO_1, "Bloco 1", _read(path_bloco1)),
        (PAGE_BLOCO_2, "Bloco 2", _read(path_bloco2)),
        (PAGE_BLOCO_3, "Bloco 3", _read(path_bloco3, RESUMO_BLOCO_3)),
        (PAGE_BLOCO_4, "Bloco 4", _read(path_bloco4) or _read(path_bloco4_fallback)),
    ]:
        if not content:
            print(f"  Sem conteudo para {name}; pulando corpo.")
            continue
        print(f"  Atualizando corpo: {name}...")
        await _delete_all_children(service, page_id)
        blocks = md_to_notion_blocks(content)
        flat, _ = expand_tables_for_append(blocks)
        await _append_blocks_batched(service, page_id, flat)
        print(f"  OK {name} ({len(flat)} blocos).")

    # Atualizar propriedades Bloco 3 e 4 (Status, Descrição) e Bootcamp (Descrição sem referências a arquivos)
    await service.update_page(
        page_id=PAGE_BLOCO_3,
        properties={
            "Status": service.build_status_property("Para Fazer"),
            "Descrição": service.build_rich_text_property(
                "Dia 2 manhã. Funcionalidades com IA: Chat, RAG, análise jurisprudencial, ver referências. Endpoints e base de conhecimento no corpo do card."
            ),
        },
    )
    await service.update_page(
        page_id=PAGE_BLOCO_4,
        properties={
            "Status": service.build_status_property("Para Fazer"),
            "Descrição": service.build_rich_text_property(
                "Dia 2 tarde. Google Calendar e Evolution API (WhatsApp) com SecretariaAI. Configuração, webhook, fluxo e segurança (prompt injection). Conteúdo completo no corpo do card."
            ),
        },
    )
    await service.update_page(
        page_id=BOOTCAMP_PAGE_ID,
        properties={
            "Descrição": service.build_rich_text_property(
                "Bootcamp 07 e 08/02. Subitens: Bloco 1 (RAG + FAISS), Bloco 2 (Construção da base Jury AI), Bloco 3 (Funcionalidades com IA), Bloco 4 (Google Calendar + WhatsApp). Todo o conteúdo dos blocos está no corpo de cada card."
            ),
        },
    )
    print("Propriedades (Status, Descrição) e card Bootcamp atualizados.")
    print("Concluído.")


if __name__ == "__main__":
    asyncio.run(main())
