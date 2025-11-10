# Exemplos Práticos

A seguir alguns exemplos enxutos de como interagir com o MCP utilizando Python ou via tools no Cursor. Ajuste os valores conforme suas bases.

## Trabalho — Criar Projeto e Subitens

### Via Python

```python
from notion_mcp import NotionService, WorkNotion

service = NotionService(token="NOTION_API_TOKEN")
work = WorkNotion(service, database_id="WORK_DATABASE_ID")

project = await work.create_card(
    title="Planejamento de Sprint",
    prioridade="Alta",
    icon="🚀",
)

for title in ("Mapear requisitos", "Implementar stories", "Realizar retrospectiva"):
    await work.create_subitem(parent_id=project["id"], title=title)
```

### Via Cursor (prompt sugerido)

```
Use a tool work_create_project para criar um projeto chamado "Planejamento de Sprint" com prioridade alta e adicione três subitens genéricos para acompanhamento.
```

## Estudos — Criar Aula com Validação de Horário

```python
from datetime import datetime
from notion_mcp import NotionService, StudyNotion

service = NotionService(token="NOTION_API_TOKEN")
study = StudyNotion(service, database_id="STUDIES_DATABASE_ID")

await study.create_class(
    parent_id="SECTION_PAGE_ID",
    title="Sessão de estudo",
    start_time=datetime(2025, 1, 13, 19, 0),
    duration_minutes=90,
)
```

> Os horários válidos são definidos em `utils/constants.py`. Ajuste ali caso a rotina mude.

## Pessoal — Usar Template Genérico

```python
from notion_mcp import NotionService, PersonalNotion

service = NotionService(token="NOTION_API_TOKEN")
personal = PersonalNotion(service, database_id="PERSONAL_DATABASE_ID")

task = await personal.use_template(
    template_name="weekly_planning",
    reference_date=datetime(2025, 1, 6),
)
```

## Conteúdo — Reagendar Episódio

```python
from datetime import datetime, timedelta
from notion_mcp import NotionService, YoutuberNotion

service = NotionService(token="NOTION_API_TOKEN")
youtube = YoutuberNotion(service, database_id="CONTENT_DATABASE_ID")

await youtube.reschedule_episode(
    episode_id="EP_PAGE_ID",
    new_recording_date=datetime.now() + timedelta(days=2),
)
```

## Dicas gerais

- Sempre forneça `database_id` via variável de ambiente (`NOTION_*_DATABASE_ID`).
- Utilize `make test` após alterações para garantir que novas regras continuam passando na suíte.
- Ao criar prompts para o Cursor, descreva a intenção de forma objetiva; o MCP cuida das regras de negocio antes de chamar o Notion.

