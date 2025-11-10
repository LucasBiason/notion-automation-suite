# Arquitetura do Notion MCP Server

## Visão geral

O servidor MCP é composto por quatro blocos principais:

```
Agente MCP  →  runtime/stdio_server.py  →  runtime/notion_server.py
                                     │           └── custom/* (regras por domínio)
                                     └── services/notion_service.py
                                             └── utils/* (constantes, validações, formatadores)
```

### 1. Runtime (`server.py`, `runtime/*`)

- Inicializa variáveis de ambiente com `runtime/config.py` (via `.env`).
- Configura logging estruturado (`structlog`).
- Expõe o loop stdio (`runtime/stdio_server.py`) para receber JSON-RPC MCP.
- Roteia chamadas para o servidor principal (`runtime/notion_server.py`).

### 2. Serviço HTTP (`services/notion_service.py`)

- Wrapper assíncrono sobre a REST API do Notion.
- Usa `httpx` + `tenacity` para requisições resilientes (timeout, retry exponencial, tratamento de 429).
- Constrói propriedades (`build_title_property`, `build_relation_property`, etc.).
- Oferece operações: páginas (create/update/get/archive), databases (query/get), blocks, users e search.

### 3. Regras de domínio (`custom/*`)

- `custom/base.py`: classe base `CustomNotion` com validações e helpers comuns.
- Implementações específicas:
  - `work_notion.py`
  - `study_notion.py`
  - `personal_notion.py`
  - `youtuber_notion.py`
- Cada classe conhece os campos da base correspondente, valida inputs, aplica defaults e chama o serviço HTTP preparado.
- As regras internas (status válidos, relacionamento pai/filho, limites de agenda) são parametrizadas via `utils/constants.py` e podem ser ajustadas sem expor dados pessoais.

### 4. Tools MCP (`tools/*`)

- Definem o catálogo de tools (`get_tools`) e o handler (`handle_tool_call`).
- Conversão de entradas MCP → chamadas nos domínios.
- Retorno padronizado para o agente (texto JSON serializado).

### Utilitários (`utils/*`)

- `constants.py`: enums, nomes de campos, status permitidos por base, horas de estudo configuráveis.
- `validators.py`: valida títulos, status, períodos, hierarquias e faz sanity-check dos argumentos.
- `formatters.py`: normaliza datas para o timezone desejado e calcula janelas de estudo sem revelar cronogramas pessoais.

### Exceptions (`exceptions/notion_service.py`)

- `NotionAPIError` e `NotionRateLimitError` são usados pelo serviço HTTP e propagados para o runtime.

## Fluxo de uma chamada

1. Agente envia `tools/call` com `name` e `arguments`.
2. `runtime/stdio_server.py` lê a linha, converte JSON e roteia.
3. `runtime/notion_server.py` valida se a tool existe, recupera handler e executa.
4. O domínio (`custom/*`) aplica validações e monta payload.
5. `services/notion_service.py` envia requisição ao Notion, trata eventuais retentativas, retorna JSON.
6. O runtime devolve a resposta MCP com `result.content` contendo o JSON serializado.

## Tratamento de erros

- **Validações**: ocorrem na camada de domínio/utilitários antes de chamar a API; retornos com mensagens claras.
- **Erros HTTP**: mapeados para `NotionAPIError` com detalhes do status e mensagem.
- **Rate limit**: lança `NotionRateLimitError` com cabeçalho `Retry-After`; o agente pode fazer backoff ou reexecutar.

## Testes

Estrutura atual:

```
tests/
├── custom/      # testes por domínio (work, study, personal, youtuber)
├── services/    # unit e integração do NotionService
├── tools/       # roteamento e conversão de tools
└── conftest.py  # fixtures compartilhadas
```

A suíte usa `pytest` com `asyncio` e mocks de `httpx`. A cobertura é executada via `make test` (configurada em `pyproject.toml`).

## Deployment

- Executável direto (`notion-mcp-server`) via entrypoint definido no `pyproject.toml`.
- Dockerfile disponível na raiz para containerização.
- O runtime depende apenas de variáveis de ambiente (`NOTION_API_TOKEN` e IDs das bases).

## Extensão

Para adicionar uma nova base:

1. Criar arquivo em `custom/` herdando de `CustomNotion`.
2. Adicionar regras específicas (campos, status, validações).
3. Registrar tools correspondentes em `tools/`.
4. Atualizar `runtime/notion_server.py` para registrar a nova classe.
5. Acrescentar testes em `tests/custom/` e, se necessário, ferramentas em `tests/tools/`.

Para novas tools em bases existentes basta expandir a classe de domínio e ajustar o arquivo em `tools/` pertinente.

## Observabilidade

- Logs estruturados com `structlog`, emitidos no stdout (JSON).
- Mensagens utilizam campos neutros (sem dados sensíveis) e incluem contexto da operação.
- Métricas podem ser adicionadas via wrapper ao serviço HTTP, caso necessário.

---

> Consulte `docs/mcp/API.md` para detalhes de cada tool e parâmetros aceitos.

