# Roadmap — Notion MCP Server

## Foco atual

- ✅ Estrutura enxuta em `src/` com runtime, domínios, ferramentas e serviços.
- ✅ Suíte de testes reorganizada (`tests/custom`, `tests/services`, `tests/tools`).
- ✅ Documentação revisada para refletir o MCP standalone.
- ✅ Container e `make` targets prontos para desenvolvimento local.

## Próximas entregas

| Prioridade | Item | Detalhes |
|------------|------|----------|
| Alta | Melhorar mensagens de erro | Ajustar descrições das validações para orientar agentes de forma clara. |
| Alta | Exemplos adicionais | Expandir `docs/mcp/EXAMPLES.md` com cenários práticos para cada domínio. |
| Média | Observabilidade | Revisar formato dos logs e preparar hooks para métricas básicas (latência por tool). |
| Média | Configurabilidade | Permitir ajuste de estudos/horários via variáveis de ambiente sem editar código. |
| Baixa | Testes integrais com ambiente real | Planejar execução contra sandbox do Notion quando disponível. |

## Itens em avaliação

- Suporte a comentários e anexos (depende de demanda real).
- Exportação de relatórios agregados via MCP.
- Ferramentas para inspeção dos schemas das bases (listagem enriquecida).

## Cadência sugerida

- **Semanal:** rodar `make test` e revisar logs dos agentes que consumirem o MCP.
- **Mensal:** atualizar documentação e exemplos conforme novos fluxos forem incorporados.
- **Sob demanda:** publicar nova imagem Docker sempre que houver mudanças relevantes no protocolo ou nas regras de negócio.

> Última revisão: novembro/2025

