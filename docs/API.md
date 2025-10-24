# API Documentation

Complete API reference for Notion MCP Server.

## Table of Contents

1. [NotionService](#notionservice) - Low-level Notion API
2. [WorkNotion](#worknotion) - Work projects and tasks
3. [StudyNotion](#studynotion) - Courses and classes
4. [YoutuberNotion](#youtubernotion) - Series and episodes
5. [PersonalNotion](#personalnotion) - Personal tasks

---

## NotionService

Low-level wrapper for Notion API.

### create_page()

Create a page in any database.

```python
page = await service.create_page(
    database_id="xxx",
    properties={
        "Project name": {"title": [{"text": {"content": "My Page"}}]},
        "Status": {"status": {"name": "Não iniciado"}},
    },
    icon={"type": "emoji", "emoji": "🎓"}
)
```

### update_page()

Update page properties.

```python
updated = await service.update_page(
    page_id="xxx",
    properties={
        "Status": {"status": {"name": "Concluído"}}
    }
)
```

### query_database()

Query database with filters.

```python
results = await service.query_database(
    database_id="xxx",
    filter_conditions={
        "property": "Status",
        "status": {"equals": "Concluído"}
    }
)
```

---

## WorkNotion

Work projects and tasks with business rules.

### create_card()

Create work project.

```python
work = WorkNotion(service, database_id)

project = await work.create_card(
    title="Implementar Autenticação JWT",
    cliente="Astracode",  # Default
    projeto="ExpenseIQ",
    prioridade="Alta",
    icon="🔐"
)
```

**Default Values:**
- cliente: `"Astracode"`
- status: `"Não iniciado"`
- prioridade: `"Normal"`
- icon: `"🚀"`

### create_subitem()

Create subitem linked to project.

```python
subitem = await work.create_subitem(
    parent_id=project['id'],
    title="Implementar Login Endpoint",
    prioridade="Alta"
)
```

**Default Values:**
- status: `"Não iniciado"`
- prioridade: `"Normal"`
- icon: `"📋"`

---

## StudyNotion

Courses, phases, sections, and classes.

### create_card() - Course

Create course (no time, only dates).

```python
study = StudyNotion(service, database_id)

course = await study.create_card(
    title="FIAP IA para Devs - Fase 5",
    categorias=["FIAP", "Inteligência Artificial"],
    periodo={"start": "2025-01-15", "end": "2025-03-31"},
    tempo_total="80:00:00",
    icon="🎓"
)
```

### create_class() - Class

Create class with study hours.

**Rules:**
- Default: 19:00-21:00
- Tuesday: 19:30-21:00
- If exceeds 21:00 → overflow to next day

```python
from datetime import datetime

start = datetime(2025, 10, 22, 19, 0)  # 19:00

class_card = await study.create_class(
    parent_id=section_id,
    title="Aula 1: Introdução",
    start_time=start,
    duration_minutes=120  # 2 hours
)
```

**Automatic Calculations:**
- End time: `calculate_class_end_time()`
- Overflow handling: If would end after 21:00
- Timezone: Always GMT-3

### reschedule_classes()

Reschedule all classes from a section/course.

```python
from datetime import datetime

new_start = datetime(2025, 10, 27, 19, 0)

updated = await study.reschedule_classes(
    parent_id=section_id,
    new_start_date=new_start,
    respect_weekends=True  # Skip Sat/Sun
)
```

---

## YoutuberNotion

YouTube series and episodes.

### create_card() - Series

Create series (recording period).

```python
youtuber = YoutuberNotion(service, database_id)

series = await youtuber.create_card(
    title="The Legend of Heroes - Trails Series",
    periodo={
        "start": "2025-10-27T21:00:00-03:00",  # First recording
        "end": "2025-11-30T23:50:00-03:00"      # Last recording
    },
    icon="🎮"
)
```

**Note:** Series does NOT have `data_lancamento` field.

### create_episode()

Create episode with publication date.

```python
from datetime import datetime

episode = await youtuber.create_episode(
    parent_id=series['id'],
    episode_number=1,
    title="Episódio 01",
    recording_date=datetime(2025, 10, 27, 21, 0),    # 21:00
    publication_date=datetime(2025, 10, 28, 12, 0),  # Next day 12:00
    resumo_episodio="Série completa sobre The Legend of Heroes..."  # REQUIRED for ep 1
)
```

**Rules:**
- Episode 1: MUST have `resumo_episodio` (series synopsis)
- Other episodes: Optional (episode-specific description)
- Recording: Usually 21:00-23:50
- Publication: Usually next day at 12:00

---

## PersonalNotion

Personal tasks and events.

### create_card()

Create personal task/event.

```python
personal = PersonalNotion(service, database_id)

task = await personal.create_card(
    title="Consulta Médica - Dr. Silva",
    atividade="Consulta Médica",
    data={
        "start": "2025-10-25T15:00:00-03:00",
        "end": "2025-10-25T16:00:00-03:00"
    },
    icon="🏥"
)
```

**Note:** Personal database uses `"Data"` field (not `"Período"`).

### create_subitem()

Create subtask.

```python
subtask = await personal.create_subitem(
    parent_id=task['id'],
    title="Pegar exames",
    icon="✅"
)
```

### create_medical_appointment()

Helper for medical appointments.

```python
appointment = await personal.create_medical_appointment(
    doctor="Silva",
    specialty="Cardiologia",
    date=datetime(2025, 10, 25, 15, 0),
    duration_minutes=60
)
```

---

## Common Patterns

### Creating Hierarchy

#### Work
```python
# Project
project = await work.create_card(title="My Project")

# Subtask
task = await work.create_subitem(
    parent_id=project['id'],
    title="My Task"
)
```

#### Studies
```python
# Course
course = await study.create_card(title="My Course", periodo={"start": "2025-01-01"})

# Phase
phase = await study.create_phase(
    parent_id=course['id'],
    title="Phase 1",
    periodo={"start": "2025-01-01", "end": "2025-01-31"}
)

# Section
section = await study.create_section(
    parent_id=phase['id'],
    title="Section 1",
    periodo={"start": "2025-01-01", "end": "2025-01-15"}
)

# Class (with time!)
from datetime import datetime
class_card = await study.create_class(
    parent_id=section['id'],
    title="Aula 1",
    start_time=datetime(2025, 1, 2, 19, 0),  # 19:00
    duration_minutes=120
)
```

### Updating Status

```python
# Any database
await work.update_card(page_id, status="Concluído")
await study.update_card(page_id, status="Concluido")  # Note: without accent
await youtuber.update_card(page_id, status="Publicado")
await personal.update_card(page_id, status="Concluído")
```

### Archiving Cards

```python
await work.archive_card(page_id)
```

---

## Error Handling

### ValidationError

Raised when card data is invalid.

```python
from notion_mcp.utils import ValidationError

try:
    await work.create_card(title="🚀 My Project")  # Emoji in title
except ValidationError as e:
    print(f"Validation error: {e}")
    # "Title contains emojis. Please use 'icon' property instead."
```

### NotionAPIError

Raised on Notion API errors.

```python
from notion_mcp.services.notion_service import NotionAPIError

try:
    await service.get_page("invalid_id")
except NotionAPIError as e:
    print(f"API error: {e}")
```

---

## Best Practices

### 1. Always Use Icons Correctly

```python
# ❌ WRONG
await work.create_card(title="🚀 My Project")

# ✅ CORRECT
await work.create_card(title="My Project", icon="🚀")
```

### 2. Use Correct Timezones

```python
from datetime import datetime
from notion_mcp.utils import format_date_gmt3

# Create datetime in GMT-3
dt = datetime(2025, 10, 22, 19, 0)
formatted = format_date_gmt3(dt)  # '2025-10-22T19:00:00-03:00'
```

### 3. Respect Study Hours

```python
# ✅ CORRECT - Respects 19:00-21:00
await study.create_class(
    parent_id=section_id,
    title="Aula 1",
    start_time=datetime(2025, 10, 22, 19, 0),
    duration_minutes=120  # Ends at 21:00
)

# ⚠️ OVERFLOW - Would end at 22:00, overflows to next day
await study.create_class(
    parent_id=section_id,
    title="Aula Long",
    start_time=datetime(2025, 10, 22, 19, 0),
    duration_minutes=180  # 3 hours - will overflow
)
```

### 4. Use Correct Relation Fields

```python
# Work and Studies
await work.create_subitem(parent_id=xxx, ...)  # Uses "Item Principal"

# Personal
await personal.create_subitem(parent_id=xxx, ...)  # Uses "Tarefa Principal"
```

---

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete usage examples.

## Rules

See [RULES.md](RULES.md) for detailed business rules per database type.

