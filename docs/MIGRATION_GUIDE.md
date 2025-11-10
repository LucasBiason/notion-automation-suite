# Guia de Migração para Notion Automation Suite

Este guia descreve como atualizar fluxos antigos para a nova estrutura unificada.

## 1. Variáveis de Ambiente

- Copie `config/defaults/env.example` para um arquivo `.env` local.
- Renomeie `NOTION_TOKEN` para `NOTION_API_TOKEN` onde for necessário.

## 2. Instalação

```bash
pip install -e .[dev]
```

## 3. Scripts Antigos

- Scripts pessoais foram movidos para `config/private/scripts/` e permanecem fora do versionamento.
- O código legado baseado em `requests` está em `notion_automation_suite.legacy`; utilize apenas como referência até que os novos workflows sejam criados.

## 4. Novo Fluxo com MCP

- Utilize `notion_mcp.custom.*` para aplicar regras específicas de cada base (Work, Studies, Personal, Youtuber).
- Exponha automações via CLI (`notion-suite`) ou via MCP (`notion-mcp-server`).

## 5. Agentes

1. Ajuste as importações para usar `notion_automation_suite.agent_core`.
2. Consuma serviços assíncronos via `notion_mcp.services.NotionService`.
3. Atualize o agendador/maestro para orquestrar workflows centralizados.

## 6. Testes

- Testes do MCP estão em `tests/mcp/`.
- Adicione novos testes por domínio conforme os workflows migrarem do legado.

## 7. Próximas Entregas

- Criar módulos em `notion_automation_suite.domains` e `workflows`.
- Publicar imagem Docker final em `ghcr.io/lucasbiason/notion-automation-suite`.
- Atualizar documentação pública e checklist final de conformidade.
