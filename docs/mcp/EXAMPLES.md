# Exemplos Práticos

Exemplos completos de uso do Notion MCP Server.

## Exemplo 1: Criar Projeto de Trabalho Completo

### Via MCP (Cursor Composer)

```
Prompt: "Crie um projeto de trabalho chamado 'Implementar Sistema de Cache' 
para o ExpenseIQ da Astracode, com prioridade Alta e 3 subitens: 
1) Implementar Redis Client
2) Criar Cache Middleware  
3) Adicionar Testes"
```

### Via Python

```python
from notion_mcp import NotionService, WorkNotion
from datetime import datetime

# Initialize
service = NotionService(token="secret_xxx")
work = WorkNotion(service, database_id="xxx")

# Create project
project = await work.create_card(
    title="Implementar Sistema de Cache",
    cliente="Astracode",
    projeto="ExpenseIQ",
    prioridade="Alta",
    icon="🔧"
)

# Create subitems
subitems = [
    "Implementar Redis Client",
    "Criar Cache Middleware",
    "Adicionar Testes",
]

for subitem_title in subitems:
    await work.create_subitem(
        parent_id=project['id'],
        title=subitem_title,
        prioridade="Normal"
    )
```

---

## Exemplo 2: Criar Curso FIAP Completo

### Via MCP (Cursor Composer)

```
Prompt: "Crie o curso 'FIAP IA para Devs - Fase 5' começando em 15/01/2025 
até 31/03/2025, com 2 seções: OpenAI (40h) e AWS (40h). Cada seção tem 8 aulas 
de 2h30 cada, começando às 19:00 em dias úteis."
```

### Via Python

```python
from notion_mcp import NotionService, StudyNotion
from datetime import datetime, timedelta

# Initialize
service = NotionService(token="secret_xxx")
study = StudyNotion(service, database_id="xxx")

# Create course (without time)
course = await study.create_card(
    title="FIAP IA para Devs - Fase 5",
    categorias=["FIAP", "Inteligência Artificial", "Pós-Graduação"],
    periodo={"start": "2025-01-15", "end": "2025-03-31"},
    tempo_total="80:00:00",
    descricao="Última fase da pós-graduação FIAP focada em IA avançada",
    icon="🎓"
)

# Create sections
sections = [
    {"title": "OpenAI e LLMs", "start": "2025-01-15", "end": "2025-02-15"},
    {"title": "AWS e ML na Nuvem", "start": "2025-02-16", "end": "2025-03-31"},
]

for section_data in sections:
    section = await study.create_section(
        parent_id=course['id'],
        title=section_data['title'],
        periodo={"start": section_data['start'], "end": section_data['end']},
        tempo_total="40:00:00",
        icon="📑"
    )
    
    # Create 8 classes of 2h30 each
    current_date = datetime.fromisoformat(section_data['start'] + "T19:00:00")
    
    for i in range(1, 9):
        # Skip weekends
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)
        
        await study.create_class(
            parent_id=section['id'],
            title=f"Aula {i:02d}",
            start_time=current_date,
            duration_minutes=150,  # 2h30
            icon="🎯"
        )
        
        # Next class: next business day
        current_date += timedelta(days=1)
```

---

## Exemplo 3: Criar Série de YouTube

### Via MCP (Cursor Composer)

```
Prompt: "Crie a série 'Metal Gear Solid' com 15 episódios. 
Gravações de 27/10 a 15/11, sempre 21h-23h50. 
Publicações sempre no dia seguinte às 12h."
```

### Via Python

```python
from notion_mcp import NotionService, YoutuberNotion
from datetime import datetime, timedelta

# Initialize
service = NotionService(token="secret_xxx")
youtuber = YoutuberNotion(service, database_id="xxx")

# Create series
series = await youtuber.create_card(
    title="Metal Gear Solid",
    periodo={
        "start": "2025-10-27T21:00:00-03:00",  # First recording
        "end": "2025-11-15T23:50:00-03:00"      # Last recording
    },
    descricao="Série completa do jogo Metal Gear Solid",
    icon="🎮"
)

# Create episodes
start_date = datetime(2025, 10, 27, 21, 0)

for i in range(1, 16):  # 15 episodes
    recording = start_date + timedelta(days=i-1)
    
    # Skip weekends
    while recording.weekday() >= 5:
        recording += timedelta(days=1)
    
    publication = recording + timedelta(hours=15)  # Next day 12:00
    
    # Episode 1 has series synopsis
    resumo = None
    if i == 1:
        resumo = (
            "Bem-vindos à nossa jornada através de Metal Gear Solid! "
            "Nesta série, vamos explorar um dos maiores clássicos do PlayStation, "
            "seguindo Solid Snake em sua missão para impedir o Metal Gear."
        )
    
    await youtuber.create_episode(
        parent_id=series['id'],
        episode_number=i,
        title=f"Episódio {i:02d}",
        recording_date=recording,
        publication_date=publication,
        resumo_episodio=resumo,
        icon="📺"
    )
```

---

## Exemplo 4: Reorganizar Cronograma de Estudos

### Via MCP (Cursor Composer)

```
Prompt: "Reorganize todas as aulas da seção 'OpenAI' para começar 
no dia 27/10/2025 às 19:00, respeitando fins de semana"
```

### Via Python

```python
from notion_mcp import NotionService, StudyNotion
from datetime import datetime

# Initialize
service = NotionService(token="secret_xxx")
study = StudyNotion(service, database_id="xxx")

# Reschedule all classes from a section
new_start = datetime(2025, 10, 27, 19, 0)

updated_classes = await study.reschedule_classes(
    parent_id=section_id,
    new_start_date=new_start,
    respect_weekends=True
)

print(f"✅ {len(updated_classes)} aulas reagendadas")
```

---

## Exemplo 5: Criar Tarefa Pessoal com Subtarefas

### Via MCP (Cursor Composer)

```
Prompt: "Crie uma tarefa pessoal 'Renovar CNH' com 3 subtarefas:
1) Agendar exame médico
2) Fazer exame
3) Ir ao Detran"
```

### Via Python

```python
from notion_mcp import NotionService, PersonalNotion

# Initialize
service = NotionService(token="secret_xxx")
personal = PersonalNotion(service, database_id="xxx")

# Create main task
task = await personal.create_card(
    title="Renovar CNH",
    atividade="Pessoal",
    icon="🚗"
)

# Create subtasks
subtasks = [
    "Agendar exame médico",
    "Fazer exame",
    "Ir ao Detran",
]

for subtask_title in subtasks:
    await personal.create_subitem(
        parent_id=task['id'],
        title=subtask_title,
        icon="✅"
    )
```

---

## Exemplo 6: Atualizar Status de Múltiplos Cards

### Via Python

```python
# Update multiple cards to "Concluído"
card_ids = ["xxx", "yyy", "zzz"]

for card_id in card_ids:
    await work.update_card(
        page_id=card_id,
        status="Concluído"
    )
    
    print(f"✅ Card {card_id} marcado como concluído")
```

---

## Exemplo 7: Buscar e Atualizar Cards

### Via Python

```python
# Find all "Em Andamento" work cards
results = await work.query_cards(
    filter_conditions={
        "property": "Status",
        "status": {"equals": "Em Andamento"}
    }
)

print(f"Encontrados {len(results)} cards em andamento")

# Archive old cards
for card in results:
    # Check if older than 30 days
    created = card.get("created_time")
    # ... logic ...
    
    await work.archive_card(card['id'])
```

---

## Exemplo 8: Criar Consulta Médica (Template)

### Via Python

```python
from datetime import datetime

# Helper method for medical appointments
appointment = await personal.create_medical_appointment(
    doctor="Silva",
    specialty="Cardiologia",
    date=datetime(2025, 10, 25, 15, 0),
    duration_minutes=60
)

# This automatically:
# - Creates title: "Consulta Médica - Dr. Silva"
# - Sets atividade: "Consulta Médica"
# - Sets icon: 🏥
# - Calculates end time (15:00 + 60min = 16:00)
```

---

## Exemplo 9: Workflow Completo - Sprint de Trabalho

```python
# 1. Create sprint card
sprint = await work.create_card(
    title="Sprint 42 - ExpenseIQ",
    cliente="Astracode",
    projeto="ExpenseIQ",
    prioridade="Alta",
    periodo={
        "start": "2025-10-28T09:00:00-03:00",
        "end": "2025-11-08T18:00:00-03:00"
    },
    tempo_total="80:00:00",
    icon="🚀"
)

# 2. Create tasks
tasks = [
    {"title": "Implementar Cache Redis", "prioridade": "Alta"},
    {"title": "Refatorar User Service", "prioridade": "Normal"},
    {"title": "Adicionar Logs Estruturados", "prioridade": "Baixa"},
]

for task_data in tasks:
    await work.create_subitem(
        parent_id=sprint['id'],
        title=task_data['title'],
        prioridade=task_data['prioridade']
    )

print(f"✅ Sprint criada com {len(tasks)} tarefas")
```

---

## Exemplo 10: Workflow Completo - Curso com Revisões

```python
from datetime import datetime, timedelta

# Create course
course = await study.create_card(
    title="Rocketseat - IA na Prática",
    categorias=["Rocketseat", "IA", "Python"],
    periodo={"start": "2025-11-01", "end": "2025-12-31"},
    icon="🚀"
)

# Create module
module = await study.create_section(
    parent_id=course['id'],
    title="Módulo 1: Fundamentos",
    periodo={"start": "2025-11-01", "end": "2025-11-15"},
    icon="📖"
)

# Create classes with reviews between them
current_date = datetime(2025, 11, 1, 19, 0)

for i in range(1, 6):
    # Create class
    await study.create_class(
        parent_id=module['id'],
        title=f"Aula {i}",
        start_time=current_date,
        duration_minutes=120  # 2h
    )
    
    # Add 15 min review on next day
    next_day = current_date + timedelta(days=1)
    await study.create_class(
        parent_id=module['id'],
        title=f"Revisão Aula {i}",
        start_time=next_day,
        duration_minutes=15,
        icon="🔄"
    )
    
    # Next class: day after review
    current_date = next_day + timedelta(days=1)
```

---

## Mais Exemplos

Ver também:
- [API.md](API.md) - Referência completa da API
- [RULES.md](RULES.md) - Regras de cada database
- `/tests/` - Testes unitários com exemplos reais

