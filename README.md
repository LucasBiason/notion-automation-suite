# Notion Automation Suite

Suite unificada que concentra o servidor MCP, agentes autônomos, workflows e ferramentas de linha de comando para automatizar o ecossistema Notion do Lucas Biason.

## Componentes

- **`notion_mcp`** — Servidor MCP completo exposto via STDIO compatível com Cursor e outros agentes Model Context Protocol.
- **`notion_automation_suite`** — Pacote principal contendo CLI, agentes, adapters e código legado em processo de migração.
- **`config/private/`** — Área local (fora do Git) para scripts e anotações pessoais.
- **`docs/`** — Documentação técnica, incluindo arquitetura atual e alvo da migração.
- **`tests/`** — Suíte de testes (unitários + integração) portados do projeto MCP.

## Instalação (Ambiente Local)

```bash
poetry shell # ou python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

Configure as variáveis notional no arquivo `config/defaults/env.example`.

## Executando o Servidor MCP Localmente

```bash
notion-mcp-server
```

O comando expõe o servidor via STDIO para integração com o Cursor.

## CLI Consolidada

```bash
notion-suite info
```

Comandos específicos por domínio ficarão em `src/notion_automation_suite/cli_apps/` e serão carregados gradualmente.

## Próximos Passos

1. Migrar workflows legados para os módulos em `domains/` e `workflows/` (ver `docs/ARCHITECTURE_TARGET.md`).
2. Atualizar agentes para consumir a nova camada de serviços assíncrona.
3. Revisar documentação pública e publicar imagem Docker consolidada.
4. Desativar repositórios antigos após confirmar que o fluxo unificado está funcional.

---

> **Nota:** Scripts pessoais e anotações sensíveis foram movidos para `config/private/` e permanecem fora do versionamento para evitar exposição de dados.
