# 📝 Notion Automation Scripts

**Versão:** 5.0  
**Data:** 10/10/2025  
**Repositório:** https://github.com/LucasBiason/notion-automation-scripts

---

## 🎯 Visão Geral

Motor centralizado para automação de criação de cards no Notion.

### Arquitetura:
- **Motor:** `core/notion_engine.py` - Recebe JSONs e cria cards
- **Scripts:** `scripts/` - Apenas chamam o motor com dados
- **MCP:** Leitura/busca de cards via MCP do Notion

---

## 📂 Estrutura

```
notion-automation-scripts/
├── core/
│   ├── __init__.py
│   ├── notion_engine.py          # Motor principal
│   ├── notion_manager.py          # Legado (manter)
│   ├── work_cards.py              # Specs Work
│   ├── personal_cards.py          # Specs Personal
│   ├── studies_cards.py           # Specs Studies
│   └── youtuber_cards.py          # Specs Youtuber
│
├── scripts/
│   ├── Personal/
│   │   ├── create_agentes_automation.py
│   │   ├── create_mylocalplace_phases.py
│   │   ├── create_personal_cards.py
│   │   └── criar_todos_subitens_personal.py
│   │
│   ├── Studies/
│   │   ├── create_fiap_phase4_cards.py
│   │   ├── create_rocketseat_cards.py
│   │   ├── create_studies_cards.py
│   │   ├── fix_rocketseat_complete_structure.py
│   │   ├── fix_rocketseat_final.py
│   │   └── fix_rocketseat_with_review.py
│   │
│   ├── Work/
│   │   ├── create_mylocalplace_cards.py
│   │   ├── create_render_deployment_complete.py
│   │   ├── create_supabase_implementation_card.py
│   │   └── create_work_cards.py
│   │
│   └── Youtuber/
│       ├── create_youtuber_cards.py
│       ├── fix_trails_dates.py
│       ├── get_daily_todos_v2.py
│       ├── reorganize_series_schedule_v2.py
│       └── reorganize_series_schedule.py
│
├── README.md
├── requirements.txt
├── env.example
└── .gitignore
```

---

## 🚀 Uso do Motor

```python
from core.notion_engine import NotionEngine

engine = NotionEngine(token)

# Criar subitens
result = engine.create_subitems_only('PERSONAL', parent_id, [
    {'title': 'Task 1', 'emoji': '✅', 'atividade': 'Desenvolvimento'}
])

# Resultado: {'created': 1, 'failed': 0, 'ids': ['...']}
```

---

## 🔑 Bases Configuradas

| Base | ID | Campo Título | Campo Relação |
|------|-----|--------------|---------------|
| WORK | 1f9962a7-693c-80a3-b947-c471a975acb0 | Nome do projeto | Sprint |
| PERSONAL | 1fa962a7-693c-8032-8996-dd9cd2607dbf | Nome da tarefa | Subtarefa |
| STUDIES | 1fa962a7-693c-80de-b90b-eaa513dcf9d1 | Project name | Parent item |
| YOUTUBER | 1fa962a7-693c-80ce-9f1d-ff86223d6bda | Nome | Série Principal |

---

## 📦 Instalação

```bash
pip install -r requirements.txt
cp env.example .env
# Editar .env com seu token
```

---

## ⚠️ Problema Conhecido

**Terminal Cursor travado** - Outputs não aparecem mas comandos executam.

**Solução:**
- Reiniciar Cursor
- OU usar terminal externo
- OU executar: `reset` no terminal

**Documentação:** `PROBLEMA_TERMINAL.md`

---

**Mantido por:** Lucas Biason  
**Última Atualização:** 10/10/2025
