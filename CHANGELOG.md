# Changelog

## [0.1.0] - 2025-11-10

### Added
- Servidor MCP enxuto focado em regras de negócio para quatro bases (trabalho, estudos, pessoal e conteúdo).
- Nova organização modular em `src/` com pacotes `custom`, `services`, `runtime`, `tools`, `utils` e `exceptions`.
- Suíte de testes reorganizada (`tests/custom`, `tests/services`, `tests/tools`) cobrindo domínios e camada HTTP.
- Documentação revisada em `docs/mcp/` (visão geral, arquitetura, API, exemplos, setup no Cursor e roadmap).
- Configuração Docker/Docker Compose atualizada para execução via `docker compose run --rm -i -T notion-suite`.
- Logging estruturado direcionado para `logs/mcp.log` (configurável via `LOG_FILE_PATH`).

### Removed
- Código legado e agentes do pacote `notion_automation_suite/` (automatizações agora ficam no repositório `cursor-multiagent-system`).
- Documentação antiga de migração e agentes.

### Changed
- `README.md` atualizado com instruções completas de instalação, execução e integração com Cursor.
- `.gitignore` agora ignora `config/.env` e diretório `logs/`.
- `pyproject.toml` ajustado para empacotar apenas o módulo MCP flatten (`src/notion_mcp.py` + pacotes associados).
