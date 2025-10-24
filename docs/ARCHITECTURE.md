# Arquitetura do Notion MCP Server

## Visão Geral

O Notion MCP Server é construído em camadas, cada uma com responsabilidades específicas:

```
┌─────────────────────────────────────────────────┐
│              AI Agent                           │
│         (Claude, GPT-4, etc)                    │
└──────────────────┬──────────────────────────────┘
                   │ MCP Protocol (stdio)
                   │
┌──────────────────▼──────────────────────────────┐
│         MCP Server (server.py)                  │
│  - Tool routing                                 │
│  - Request/response handling                    │
│  - MCP protocol implementation                  │
└──────────────────┬──────────────────────────────┘
                   │
       ┌───────────┴────────────┐
       │                        │
       ▼                        ▼
┌──────────────┐     ┌─────────────────────┐
│ NotionService│     │ CustomNotion Layer  │
│  (Base API)  │◄────│ - WorkNotion        │
│              │     │ - StudyNotion       │
│              │     │ - YoutuberNotion    │
│              │     │ - PersonalNotion    │
└──────┬───────┘     └──────────┬──────────┘
       │                        │
       │                        ▼
       │             ┌─────────────────────┐
       │             │ Utils                │
       │             │ - Validators        │
       │             │ - Formatters        │
       │             │ - Constants         │
       │             └─────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────┐
│           Notion REST API                       │
│     https://api.notion.com/v1                   │
└─────────────────────────────────────────────────┘
```

## Camadas

### 1. MCP Server Layer

**Arquivo:** `src/notion_mcp/server.py`

**Responsabilidades:**
- Implementar protocolo MCP (stdio)
- Rotear chamadas de tools
- Gerenciar ciclo de vida do servidor
- Converter requests/responses MCP ↔ Python

**Características:**
- Suporta múltiplas databases simultaneamente
- Valida tools antes de executar
- Logging estruturado de todas operações
- Error handling com respostas MCP-compliant

### 2. NotionService Layer

**Arquivo:** `src/notion_mcp/services/notion_service.py`

**Responsabilidades:**
- Wrapper completo da API do Notion
- HTTP requests com retry logic
- Rate limiting automático
- Property builders (helpers)

**Operações Suportadas:**
- Pages: create, read, update, archive
- Databases: query, read schema
- Blocks: append, update, delete, read
- Users: list, read
- Search: pages and databases

**Características:**
- Async/await para performance
- Retry automático em erros transitórios
- Structured logging
- Type hints completos

### 3. CustomNotion Layer

**Arquivos:**
- `src/notion_mcp/custom/base.py` - Base class abstrata
- `src/notion_mcp/custom/work_notion.py` - Work implementation
- `src/notion_mcp/custom/study_notion.py` - Studies implementation
- `src/notion_mcp/custom/youtuber_notion.py` - Youtuber implementation
- `src/notion_mcp/custom/personal_notion.py` - Personal implementation

**Responsabilidades:**
- Aplicar regras de negócio específicas
- Validar dados antes de criar
- Usar campos corretos para cada database
- Fornecer métodos de alto nível

**Características:**
- Herança de `CustomNotion` base
- Validação automática via `_validate_and_prepare()`
- Defaults inteligentes
- Type safety

### 4. Utils Layer

**Arquivos:**
- `src/notion_mcp/utils/constants.py` - Constantes e enums
- `src/notion_mcp/utils/formatters.py` - Formatadores de data/timezone
- `src/notion_mcp/utils/validators.py` - Validações

**Responsabilidades:**
- Fornecer constantes (statuses, priorities, etc)
- Formatar datas para GMT-3
- Validar dados de entrada
- Calcular horários de estudo

## Fluxo de Execução

### Criar Card de Trabalho

```
1. AI Agent (Cursor) envia:
   {
     "method": "tools/call",
     "params": {
       "name": "work_create_project",
       "arguments": {"title": "My Project"}
     }
   }

2. MCP Server recebe e roteia para:
   server.handle_tool_call("work_create_project", {...})

3. WorkNotion valida e prepara:
   - validate_title("My Project")  ✅
   - Adiciona defaults (cliente, status, prioridade)
   - Formata icon {"type": "emoji", "emoji": "🚀"}

4. NotionService constrói payload:
   {
     "parent": {"database_id": "xxx"},
     "icon": {"type": "emoji", "emoji": "🚀"},
     "properties": {
       "Project name": {"title": [...]},
       "Cliente": {"select": {"name": "Astracode"}},
       "Status": {"status": {"name": "Não iniciado"}},
       ...
     }
   }

5. NotionService envia HTTP POST:
   POST https://api.notion.com/v1/pages
   Headers: Authorization, Notion-Version
   Body: payload

6. Notion API responde:
   {
     "object": "page",
     "id": "created_page_id",
     ...
   }

7. MCP Server retorna ao Agent:
   {
     "jsonrpc": "2.0",
     "result": {"content": [...]}
   }
```

## Validações

### Ordem de Validação

1. **Input Validation** (Utils Layer)
   - Title não vazio
   - Title sem emojis
   - Status válido para database
   - Timezone GMT-3 em datas

2. **Business Rules** (CustomNotion Layer)
   - Cliente padrão "Astracode" para Work
   - Horários 19:00-21:00 para Studies
   - Episode 1 com synopsis para Youtuber
   - Campo "Data" (não "Período") para Personal

3. **API Validation** (NotionService Layer)
   - Database ID exists
   - Properties schema valid
   - Relation targets exist

### Tratamento de Erros

```
ValidationError (antes de chamar API)
    ↓
Logged e retornado ao Agent
    ↓
Agent pode corrigir e tentar novamente

NotionAPIError (depois de chamar API)
    ↓
Retry automático (3x) se transitório
    ↓
Se persistir, logged e retornado ao Agent
```

## Performance

### Async/Await

Todas operações são assíncronas:
- Múltiplas pages podem ser criadas em paralelo
- Não bloqueia o event loop
- Escalável para alta carga

### Caching

Não há cache por design:
- Garante dados sempre atualizados
- Evita state inconsistente
- Notion API é rápida o suficiente

### Rate Limiting

- Notion API: 3 requests/second
- Implementado via tenacity
- Retry com backoff exponencial
- Evita 429 errors

## Segurança

### Token Management

- Token nunca é logged
- Passado apenas via environment variables
- Validado na inicialização
- Não é exposto em responses

### Input Validation

- Todos inputs são validados
- Type checking via Pydantic
- SQL injection não é possível (API REST)
- XSS prevention via Notion API

## Extensibilidade

### Adicionar Nova Database

1. Criar nova classe em `src/notion_mcp/custom/`
2. Herdar de `CustomNotion`
3. Implementar `create_card()` e `create_subitem()`
4. Adicionar em `server.py`
5. Adicionar tools correspondentes

### Adicionar Nova Tool

1. Definir em `server.get_tools()`
2. Implementar em `server.handle_tool_call()`
3. Adicionar testes em `tests/`
4. Documentar em `docs/API.md`

## Deployment

### Docker

Imagem otimizada:
- Base: `python:3.11-slim`
- Multi-stage build (se necessário)
- Non-root user
- Health check incluído
- Tamanho: ~200MB

### Kubernetes (futuro)

- Deployment com replicas
- Service para load balancing
- ConfigMap para configuração
- Secret para tokens
- Ingress para acesso externo

## Monitoring

### Logs Estruturados

Todos logs em JSON:
```json
{
  "timestamp": "2025-10-22T19:00:00Z",
  "level": "info",
  "event": "creating_work_card",
  "title": "My Project",
  "cliente": "Astracode"
}
```

### Métricas (futuro)

- Requests por segundo
- Latência por operation
- Error rate
- Tool usage statistics

## Testes

### Estrutura

```
tests/
├── test_notion_service.py  # NotionService tests
├── test_work_notion.py     # WorkNotion tests
├── test_study_notion.py    # StudyNotion tests
├── test_youtuber_notion.py # YoutuberNotion tests
├── test_personal_notion.py # PersonalNotion tests
├── test_validators.py      # Validation tests
├── test_formatters.py      # Formatter tests
└── conftest.py            # Shared fixtures
```

### Coverage Goal

- **Target:** 95%+ coverage
- **Current:** TBD
- **Strategy:** Unit tests + integration tests

### Test Pyramid

```
       ┌─────────┐
       │   E2E   │ (5%)  - Full workflow tests
       ├─────────┤
       │Integration│ (25%) - Component interaction
       ├─────────┤
       │   Unit    │ (70%) - Individual functions
       └──────────┘
```

## Decisões de Design

### Por que FastAPI?

- Suporte nativo a async/await
- Type validation via Pydantic
- Auto-documentation com OpenAPI
- Modern Python framework
- Fácil deploy

### Por que Não Usar Notion SDK Oficial?

- SDK não cobre 100% da API
- Queremos controle total
- Custom error handling
- Custom retry logic
- Menor dependência externa

### Por que Camadas?

- Separação de responsabilidades
- Fácil manutenção
- Testabilidade
- Extensibilidade
- Reutilização de código

### Por que Validações?

- Garantir dados consistentes
- Evitar cards mal formados
- Feedback imediato ao Agent
- Economizar API calls
- Manter padrão de qualidade

---

**Próximo:** Ver [API.md](API.md) para referência completa

