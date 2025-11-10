# Notion MCP Server — Visão Geral

Este documento apresenta o resumo do projeto e aponta para as seções detalhadas da documentação.

## Sumário

- [Contexto](#contexto)
- [Abordagem](#abordagem)
- [Arquitetura resumida](#arquitetura-resumida)
- [Stack e métricas](#stack-e-métricas)
- [Referências adicionais](#referências-adicionais)

## Contexto

Agentes MCP genéricos não enxergam as regras particulares das bases do Notion utilizadas no dia a dia. Isso levava a cartões com campos incorretos, status inválidos, horários inconsistentes e repetição de scripts. O objetivo deste projeto é encapsular essas regras em um servidor MCP pequeno, determinístico e testado.

## Abordagem

- **Regras por domínio:** cada base (trabalho, estudos, pessoal, conteúdo) tem uma classe dedicada com campos, hierarquias e padrões aceitos.
- **Validação antecipada:** entradas são verificadas antes de chamar a API, reduzindo erros e economizando requisições.
- **Interface enxuta:** operações de alto nível (`create_card`, `create_subitem`, `query_schedule`, etc.) traduzem automaticamente para o payload esperado pelo Notion.
- **Integração direta:** o servidor expõe tools MCP via stdio, prontas para o Cursor ou outros orquestradores compatíveis.

## Arquitetura resumida

```
Agente MCP → runtime/stdio_server.py → runtime/notion_server.py
                       │                    └── custom/* (regras)
                       └── services/notion_service.py
                                └── utils/* (constantes, validações, formatadores)
```

### Camadas

1. **Runtime** (`server.py`, `runtime/*`): carrega ambiente, configura logging e executa o loop stdio.
2. **Serviço HTTP** (`services/notion_service.py`): wrapper assíncrono sobre a API REST do Notion (httpx + tenacity).
3. **Domínios** (`custom/*`): regras por base com validações e defaults reutilizáveis.
4. **Ferramentas MCP** (`tools/*`): metadados e roteamento das tools.
5. **Utilitários** (`utils/*`): constantes, validadores e formatadores parametrizáveis.

### Exemplo rápido

```python
from custom.work_notion import WorkNotion
from services.notion_service import NotionService

service = NotionService(token="NOTION_API_TOKEN")
work = WorkNotion(service, database_id="WORK_DATABASE_ID")

await work.create_card(title="Planejamento da Sprint")
```

No Cursor, basta chamar a tool `work_create_project`; o MCP valida entradas e envia o payload correto ao Notion.

## Stack e métricas

- **Tecnologias:** Python 3.10+, `httpx`, `tenacity`, `structlog`, `pytest`, `ruff`, `mypy`.
- **Qualidade:** testes unitários e de integração (`make test`) cobrindo domínios, serviço HTTP e tools.
- **Observabilidade:** logs JSON com `structlog`; métricas podem ser adicionadas conforme necessidade.

## Referências adicionais

| Documento | Assunto |
|-----------|---------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Detalhamento da arquitetura e fluxo interno |
| [API.md](API.md) | Referência das classes, métodos e tools disponíveis |
| [SETUP_CURSOR.md](SETUP_CURSOR.md) | Passo a passo para integrar o MCP ao Cursor |
| [EXAMPLES.md](EXAMPLES.md) | Exemplos de uso em Python e prompts |
| [ROADMAP.md](ROADMAP.md) | Próximas entregas e itens em avaliação |

Consulte esses arquivos conforme a etapa do desenvolvimento ou da integração que você estiver trabalhando.

