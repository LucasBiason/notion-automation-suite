# Arquitetura Objetivo da Notion Automation Suite

Este plano descreve a estrutura final desejada após a consolidação dos projetos legados.

## Pacotes Python

```
src/
├─ notion_automation_suite/
│  ├─ __init__.py
│  ├─ cli.py                  # Entrada Typer com comandos padronizados
│  ├─ cli_apps/               # Subcomandos por domínio (work, studies, etc.)
│  ├─ adapters/               # Integrações externas (Notion, Google, Render)
│  ├─ agents/                 # Agentes autônomos (rotinas automáticas)
│  ├─ agent_core/             # Núcleo compartilhado dos agentes (clientes, orquestração)
│  ├─ domains/
│  │   ├─ work.py             # Regras de domínio reutilizando CustomNotion
│  │   ├─ studies.py
│  │   ├─ personal.py
│  │   └─ youtuber.py
│  ├─ services/
│  │   ├─ notion_async.py     # Fachada sobre notion_mcp.services.NotionService
│  │   └─ scheduler.py        # Utilitários de agendamento/pipelines
│  ├─ workflows/
│  │   ├─ generators.py       # Automação de criação de cards com regras compostas
│  │   └─ reports.py          # Rotinas de relatórios/monitoramento
│  └─ legacy/
│      └─ ...                 # Código histórico preservado até refatoração completa
├─ notion_mcp/                # Servidor MCP pronto para uso (sem mudanças estruturais)
└─ notion_suite_cli/          # (Opcional) wrappers específicos se necessário
```

## Diretórios de Projeto

- `config/`
  - `defaults/env.example` — variáveis padrão para desenvolvimento.
  - `private/` — dados locais, scripts pessoais, credenciais (fora do Git).
- `docs/` — documentação pública e guias de migração.
- `tests/`
  - `unit/` — testes unitários (mocks).
  - `integration/` — testes com sandbox Notion (futuros).
  - `end_to_end/` — validações executadas via Cursor/CLI.
- `tools/` (futuro) — scripts utilitários que podem ser distribuídos com o pacote.

## Fluxo de Trabalho

1. **Camada de Serviços**: `notion_mcp` oferece acesso baixo nível. `notion_automation_suite.services.notion_async` expõe wrappers de alto nível para o restante do código.
2. **Domínios**: regras de negócio expressas em módulos funcionais, reaproveitando constantes/validações do MCP.
3. **Workflows**: combinam múltiplos domínios para automatizações complexas (ex.: criação de sprint + aulas associadas).
4. **CLI & Agentes**: reutilizam os workflows e domínios, sem depender de scripts soltos.
5. **MCP Server**: distribuído junto, permitindo que agentes externos (ex.: Cursor) executem as mesmas regras.

## Metodologia de Migração

1. **Adaptação por Domínio**: migrar scripts de cada base (Work, Studies, etc.) para `domains/` e `workflows/`, eliminando dependências legado.
2. **Refino dos Agentes**: apontar orquestradores para os novos workflows.
3. **Remoção do Legacy**: após cobertura de testes, remover o código em `legacy/` e scripts privados duplicados.
4. **Publicação**: disponibilizar pacote via PyPI interno ou `.whl` local, com Docker consolidado.

Este documento deve ser revisado à medida que os módulos forem migrados para a estrutura alvo.
