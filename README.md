# Notion MCP Server

**MCP (Model Context Protocol) Server** completo para integração com Notion, com suporte a múltiplas bases de dados e regras customizadas.

## Visão Geral

Este projeto fornece um servidor MCP profissional que permite que agentes de IA (como Claude, GPT-4, etc.) interajam com o Notion de forma estruturada e consistente, respeitando regras específicas de cada base de dados.

### Arquitetura em Camadas

```
┌─────────────────────────────────────┐
│      AI Agent (Claude/GPT-4)        │
│        via MCP Protocol             │
└──────────────┬──────────────────────┘
               │
               │ MCP Tools
               ▼
┌─────────────────────────────────────┐
│       CustomNotion Layer            │
│  ┌─────────┬─────────┬──────────┐   │
│  │WorkNotion│StudyNotion│YoutuberNotion│PersonalNotion│   │
│  └─────────┴─────────┴──────────┘   │
└──────────────┬──────────────────────┘
               │
               │ Validates & Enforces Rules
               ▼
┌─────────────────────────────────────┐
│       NotionService Layer           │
│   Complete Notion API Wrapper       │
└──────────────┬──────────────────────┘
               │
               │ HTTP Requests
               ▼
┌─────────────────────────────────────┐
│          Notion API                 │
│    https://api.notion.com           │
└─────────────────────────────────────┘
```

## Recursos Principais

### NotionService (Camada Base)
- API completa do Notion encapsulada
- Métodos para todas as operações (pages, databases, blocks, users)
- Tratamento de erros robusto
- Rate limiting automático
- Retry logic configurável

### CustomNotion (Camada Especializada)
Quatro classes especializadas, cada uma com regras específicas:

#### WorkNotion
- Criação de projetos e tarefas de trabalho
- Gestão de cliente e projeto (Astracode, ExpenseIQ, etc)
- Subitens com hierarquia correta
- Status e prioridades específicas de trabalho

#### StudyNotion
- Criação de cursos, formações, fases, seções e aulas
- Hierarquia multi-nível (Curso > Fase > Seção > Aula)
- Horários de estudo respeitados (19:00-21:00, terça 19:30)
- Timezone GMT-3 automático
- Categorias e tags de aprendizado

#### YoutuberNotion
- Criação de séries e episódios
- Regras de gravação vs publicação
- Sinopse apenas no primeiro episódio
- Cronograma de gravações (21:00-23:50)
- Data de lançamento automática

#### PersonalNotion
- Tarefas pessoais e eventos
- Subtarefas com hierarquia
- Templates de eventos recorrentes
- Gestão de agenda pessoal

## Instalação

### Pré-requisitos
- Python 3.10+
- Docker (opcional)
- Token da API do Notion

### Via Docker (Recomendado)
```bash
docker pull ghcr.io/lucasbiason/notion-mcp-server:latest
docker run -e NOTION_TOKEN=seu_token ghcr.io/lucasbiason/notion-mcp-server
```

### Via Fonte
```bash
git clone https://github.com/LucasBiason/notion-mcp-server.git
cd notion-mcp-server
pip install -e .
```

## Configuração

### 1. Criar arquivo .env
```bash
cp .env.example .env
```

### 2. Preencher variáveis
```env
NOTION_TOKEN=secret_xxx
NOTION_WORK_DATABASE_ID=xxx
NOTION_STUDIES_DATABASE_ID=xxx
NOTION_PERSONAL_DATABASE_ID=xxx
NOTION_YOUTUBER_DATABASE_ID=xxx
```

### 3. Configurar no Cursor/Claude

#### Cursor Settings > MCP
```json
{
  "mcpServers": {
    "notion-custom": {
      "command": "docker",
      "args": ["run", "-i", "--rm", 
               "-e", "NOTION_TOKEN=${NOTION_TOKEN}",
               "-e", "NOTION_WORK_DATABASE_ID=${NOTION_WORK_DATABASE_ID}",
               "-e", "NOTION_STUDIES_DATABASE_ID=${NOTION_STUDIES_DATABASE_ID}",
               "-e", "NOTION_PERSONAL_DATABASE_ID=${NOTION_PERSONAL_DATABASE_ID}",
               "-e", "NOTION_YOUTUBER_DATABASE_ID=${NOTION_YOUTUBER_DATABASE_ID}",
               "ghcr.io/lucasbiason/notion-mcp-server:latest"]
    }
  }
}
```

## Uso via MCP

### Tools Disponíveis

#### NotionService Tools (API Completa)
- `notion_create_page` - Criar página
- `notion_update_page` - Atualizar página
- `notion_delete_page` - Deletar/arquivar página
- `notion_get_page` - Obter página
- `notion_query_database` - Consultar database
- `notion_append_blocks` - Adicionar blocos de conteúdo
- `notion_update_blocks` - Atualizar blocos
- `notion_delete_blocks` - Deletar blocos

#### WorkNotion Tools
- `work_create_project` - Criar projeto de trabalho
- `work_create_task` - Criar tarefa
- `work_create_subitem` - Criar subitem com hierarquia correta
- `work_update_status` - Atualizar status

#### StudyNotion Tools
- `study_create_course` - Criar curso completo
- `study_create_phase` - Criar fase do curso
- `study_create_section` - Criar seção
- `study_create_class` - Criar aula (com horários corretos)
- `study_reschedule` - Reorganizar cronograma

#### YoutuberNotion Tools
- `youtuber_create_series` - Criar série
- `youtuber_create_episode` - Criar episódio
- `youtuber_schedule_recordings` - Agendar gravações

#### PersonalNotion Tools
- `personal_create_task` - Criar tarefa pessoal
- `personal_create_subtask` - Criar subtarefa
- `personal_create_event` - Criar evento

## Exemplos

### Criar Projeto de Trabalho (AI Agent)
```
Prompt: "Crie um card de trabalho para implementar autenticação JWT no ExpenseIQ"

O MCP usa: work_create_project
Resultado: Card criado com:
- Cliente: Astracode
- Projeto: ExpenseIQ
- Status: Não iniciado
- Prioridade: Normal
- Ícone: 🚀 (na página, não no título)
```

### Criar Curso FIAP (AI Agent)
```
Prompt: "Crie a Fase 5 da FIAP com 3 seções: OpenAI, AWS e Projeto Final"

O MCP usa: study_create_phase + study_create_section
Resultado: 
- Fase 5 criada sem horário (apenas datas)
- 3 seções como subitens
- Timezone GMT-3
- Hierarquia correta (parent_item)
- Categorias: FIAP, IA
```

### Criar Série YouTube (AI Agent)
```
Prompt: "Crie série do Metal Gear Solid com 10 episódios, gravação 21h-23h50, publicação dia seguinte 12h"

O MCP usa: youtuber_create_series + youtuber_create_episode (loop)
Resultado:
- Série criada (período = primeira gravação → última gravação)
- 10 episódios como subitens
- Episódio 1 com sinopse da série completa
- Todos com data_lancamento
- Horários de gravação corretos
```

## Tecnologias

### Backend
- **Python 3.10+** - Linguagem principal
- **FastAPI** - Framework web para o MCP server
- **Pydantic v2** - Validação de dados
- **httpx** - Cliente HTTP assíncrono
- **structlog** - Logging estruturado

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração local
- **GitHub Actions** - CI/CD
- **GitHub Packages** - Publicação da imagem

### Desenvolvimento
- **pytest** - Testes unitários e integração
- **black** - Formatação de código
- **ruff** - Linting
- **mypy** - Type checking
- **pre-commit** - Hooks de qualidade

## Estrutura do Projeto

```
notion-mcp-server/
├── src/
│   └── notion_mcp/
│       ├── __init__.py
│       ├── server.py               # MCP Server principal
│       ├── services/
│       │   ├── __init__.py
│       │   └── notion_service.py   # API completa do Notion
│       ├── custom/
│       │   ├── __init__.py
│       │   ├── base.py             # CustomNotion base
│       │   ├── work_notion.py      # WorkNotion
│       │   ├── study_notion.py     # StudyNotion
│       │   ├── youtuber_notion.py  # YoutuberNotion
│       │   └── personal_notion.py  # PersonalNotion
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base_tools.py       # NotionService tools
│       │   ├── work_tools.py       # WorkNotion tools
│       │   ├── study_tools.py      # StudyNotion tools
│       │   ├── youtuber_tools.py   # YoutuberNotion tools
│       │   └── personal_tools.py   # PersonalNotion tools
│       └── utils/
│           ├── __init__.py
│           ├── validators.py       # Validações
│           ├── formatters.py       # Formatadores de data/timezone
│           └── constants.py        # Constantes (status, prioridades)
├── tests/
│   ├── test_notion_service.py
│   ├── test_work_notion.py
│   ├── test_study_notion.py
│   ├── test_youtuber_notion.py
│   └── test_personal_notion.py
├── docs/
│   ├── API.md                      # Documentação da API
│   ├── CUSTOMIZATION.md            # Como customizar
│   ├── EXAMPLES.md                 # Exemplos de uso
│   └── RULES.md                    # Regras de cada base
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── .editorconfig
└── README.md
```

## Desenvolvimento

### Comandos Úteis
```bash
# Instalar dependências
make install

# Executar testes
make test

# Executar linter
make lint

# Formatar código
make format

# Executar servidor local
make run

# Build Docker
make docker-build

# Executar via Docker
make docker-run
```

## Roadmap

### Fase 1: Core (2-3 semanas)
- [x] Estrutura do projeto
- [ ] NotionService completo (todas operações da API)
- [ ] CustomNotion base class
- [ ] Validadores e formatadores
- [ ] Testes unitários (95%+ cobertura)

### Fase 2: Classes Especializadas (2 semanas)
- [ ] WorkNotion (projetos e tarefas)
- [ ] StudyNotion (cursos e aulas)
- [ ] YoutuberNotion (séries e episódios)
- [ ] PersonalNotion (tarefas pessoais)
- [ ] Testes de integração

### Fase 3: MCP Server (1 semana)
- [ ] Implementação do protocolo MCP
- [ ] Tools para cada classe
- [ ] Resources (databases, templates)
- [ ] Prompts pré-configurados

### Fase 4: DevOps (1 semana)
- [ ] Dockerfile otimizado
- [ ] Docker Compose para desenvolvimento
- [ ] GitHub Actions (CI/CD)
- [ ] Publicação no GitHub Packages

### Fase 5: Documentação (1 semana)
- [ ] Documentação completa da API
- [ ] Guia de customização
- [ ] Exemplos práticos
- [ ] Tutorial de configuração no Cursor

## Diferencial do Projeto

### Por que Este MCP é Único?

1. **Regras de Negócio Embutidas**
   - Não é apenas um proxy para API do Notion
   - Conhece as regras específicas de cada base
   - Valida dados antes de criar
   - Garante consistência

2. **Multi-Base Support**
   - 4 bases diferentes com regras próprias
   - Hierarquias complexas gerenciadas automaticamente
   - Timezone e horários específicos por contexto

3. **Production Ready**
   - Testes completos
   - Docker first
   - Logging estruturado
   - Error handling robusto
   - Rate limiting
   - Retry logic

4. **Developer Experience**
   - Interface simples e intuitiva
   - Validações claras e úteis
   - Documentação completa
   - Exemplos práticos

## Casos de Uso

### Para Desenvolvedores
- Gerenciar projetos e tarefas via IA
- Criar estruturas complexas com um comando
- Sincronizar código com planejamento

### Para Estudantes
- Organizar cursos e cronogramas automaticamente
- Respeitar horários de estudo
- Criar revisões e flashcards

### Para Criadores de Conteúdo
- Agendar gravações e publicações
- Gerenciar séries e episódios
- Manter cronograma consistente

### Para Uso Pessoal
- Criar tarefas e eventos
- Templates de eventos recorrentes
- Gestão de agenda pessoal

## Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## Autor

**Lucas Biason**
- GitHub: [@LucasBiason](https://github.com/LucasBiason)
- LinkedIn: [lucasbiason](https://linkedin.com/in/lucasbiason)
- Email: lucas.biason@gmail.com

## Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes.

---

**Status**: 🚧 Em Desenvolvimento Ativo  
**Versão**: 0.1.0-alpha  
**Última Atualização**: 22/10/2025

