# Arquitetura Atual Consolidada

Este documento registra o estado pós-migração inicial dos projetos `notion-automations`, `notion-automation-scripts`, `notion-mcp-server` e `notion-automation-suite` dentro de um único repositório.

## Distribuição de Módulos

- `src/notion_mcp/` — Servidor MCP completo migrado do projeto `notion-mcp-server`, incluindo serviços, ferramentas e regras de cartões por domínio (Work, Studies, Personal, Youtuber).
- `src/notion_automation_suite/` — Pacote raiz da suite. No momento abriga:
  - `cli.py` — CLI unificada (Typer) para comandos gerais.
  - `cli_apps/` — Scripts operacionais separados por domínio migrados da antiga pasta `cli/`.
  - `legacy/` — Implementações históricas baseadas em `requests` que ainda precisam ser adaptadas para a nova API assíncrona.
  - `agents/` e `agent_core/` — Código dos agentes automáticos.
  - `adapters/` e `utils/` — Camadas auxiliares para integrações externas.
- `config/private/` — Armazena scripts pessoais (ex.: rotinas semanais, dashboards de gamificação). Diretório ignorado pelo Git.
- `docs/` — Documentos de arquitetura e guias de configuração.

## Fontes Migradas

| Origem | Local Atual | Observações |
|--------|-------------|-------------|
| `notion-mcp-server` | `src/notion_mcp/` | Mantida estrutura original para compatibilidade de imports. |
| `notion-automation-agents` | `src/notion_automation_suite/agents/`, `agent_core/`, `utils/` | Necessário revisar dependências e adaptar para uso do novo serviço MCP. |
| `notion-automation-scripts` | `src/notion_automation_suite/legacy/scripts/` e `config/private/scripts/` | Código principal legado disponível; scripts pessoais movidos para área privada. |

## Próximos Passos Técnicos

1. Substituir dependências antigas (`requests`) por `notion_mcp.services.NotionService` nas camadas legacy.
2. Expor comandos CLI padronizados que reutilizam as regras de negócio do MCP.
3. Refatorar agentes para operar sobre a camada de domínio compartilhada.
4. Consolidar testes automatizados em `tests/` cobrindo fluxos centrais e garantindo compatibilidade com MCP.
5. Atualizar documentação pública (README, guias de instalação) com o fluxo unificado.

Este arquivo deve ser mantido até a finalização da migração, quando será substituído por um documento de arquitetura definitiva.
