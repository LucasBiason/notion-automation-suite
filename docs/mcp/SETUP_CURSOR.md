# Configuração no Cursor

Guia rápido para conectar o Notion MCP Server ao Cursor usando o protocolo stdio.

## Pré-requisitos

- Docker instalado **ou** ambiente Python local configurado.
- Token da integração do Notion (`NOTION_API_TOKEN`).
- IDs das databases que o MCP irá manipular (`NOTION_WORK_DATABASE_ID`, `NOTION_STUDIES_DATABASE_ID`, etc.).
- Databases compartilhadas com a integração do Notion.

## 1. Criar integração e coletar IDs

1. Acesse <https://www.notion.so/my-integrations> e crie uma integração.
2. Copie o *Internal Integration Token* (`secret_xxx`).
3. Abra cada database no Notion, copie a URL e extraia o identificador de 32 caracteres.
4. Compartilhe as databases com a integração (menu `Connections` > `Add connections`).

## 2. Configurar servidor MCP no Cursor

1. Abra **Cursor Settings** → procure por **MCP** → clique em **Add New MCP Server**.
2. Informe um nome (ex.: `notion-mcp`).
3. Defina o tipo `stdio`.
4. Preencha o comando. Exemplos abaixo.

### Opção A — Docker

```bash
docker run -i --rm \
  -e NOTION_API_TOKEN=secret_xxx \
  -e NOTION_WORK_DATABASE_ID=... \
  -e NOTION_STUDIES_DATABASE_ID=... \
  -e NOTION_PERSONAL_DATABASE_ID=... \
  -e NOTION_YOUTUBER_DATABASE_ID=... \
  ghcr.io/lucasbiason/notion-mcp-server:latest
```

### Opção B — Ambiente local

```json
{
  "command": "/caminho/para/venv/bin/python",
  "args": ["-m", "server"],
  "env": {
    "NOTION_API_TOKEN": "secret_xxx",
    "NOTION_WORK_DATABASE_ID": "...",
    "NOTION_STUDIES_DATABASE_ID": "..."
  }
}
```

> O módulo `server` está na raiz de `src/` e inicia o loop stdio.

## 3. Validar instalação

- Após salvar, clique em **Refresh** na tela do MCP no Cursor.
- Aguarde alguns segundos e verifique se os grupos de tools aparecem (work, studies, personal, content, base).
- Execute um prompt simples no Composer, por exemplo: “crie um projeto de trabalho genérico para planejamento da sprint”.
- O Cursor deve selecionar a tool `work_create_project` e retornar o payload/result.

## 4. Troubleshooting rápido

| Sintoma | Ações |
|--------|-------|
| Sem tools listadas | Verifique se o container/processo está ativo (`docker ps` ou logs). Clique em **Refresh** novamente. |
| Erro de conexão | Confirme token e IDs, além do compartilhamento das databases com a integração. |
| ValidationError | Revise a mensagem: geralmente indica título com emoji, status inválido ou datas fora do padrão suportado pelas regras. |

## 5. Dicas

- Mantenha os IDs sensíveis em `.env` e carregue-os automaticamente (`runtime/config.py` suporta `NOTION_ENV_FILE`).
- Ajuste prompts para descrever intenção; o MCP cuida dos detalhes dos campos.
- Consulte `docs/mcp/API.md` para a lista completa de tools e argumentos.
- Rode `make test` após adicionar novas regras para garantir que o agente continue consistente.

