# Configuração no Cursor

Guia completo para configurar o Notion MCP Server no Cursor.

## Pré-requisitos

- Docker instalado
- Token da API do Notion
- IDs das suas databases do Notion

## Passo 1: Obter Token do Notion

1. Acesse: https://www.notion.so/my-integrations
2. Clique em "New integration"
3. Dê um nome (ex: "Notion MCP Server")
4. Selecione o workspace
5. Clique em "Submit"
6. Copie o "Internal Integration Token" (começa com `secret_`)

## Passo 2: Obter IDs das Databases

Para cada database que você quer usar:

1. Abra a database no Notion
2. Copie a URL:
   ```
   https://www.notion.so/{workspace}/{database_id}?v={view_id}
   ```
3. O `database_id` é a parte de 32 caracteres

**Exemplo:**
```
URL: https://www.notion.so/myworkspace/1fa962a7693c80deb90beaa513dcf9d1?v=xxx
Database ID: 1fa962a7693c80deb90beaa513dcf9d1
```

## Passo 3: Compartilhar Databases com a Integração

Para CADA database:

1. Abra a database no Notion
2. Clique nos `...` (três pontos) no canto superior direito
3. Clique em "Connections" ou "Add connections"
4. Selecione sua integração ("Notion MCP Server")
5. Clique em "Confirm"

**Sem este passo, a integração não terá acesso às databases!**

## Passo 4: Configurar no Cursor

### 4.1 Abrir Settings do Cursor

1. Abra o Cursor
2. Vá em: `Cursor Settings` (Ctrl+,)
3. Procure por: `MCP` no campo de busca
4. Ou navegue: `Features > MCP`
5. Clique em: `+ Add New MCP Server`

### 4.2 Preencher Configuração

#### Name:
```
Notion Custom
```

#### Type:
```
stdio
```

#### Command:
```bash
docker run -i --rm \
  -e NOTION_TOKEN=secret_xxx \
  -e NOTION_WORK_DATABASE_ID=xxx \
  -e NOTION_STUDIES_DATABASE_ID=xxx \
  -e NOTION_PERSONAL_DATABASE_ID=xxx \
  -e NOTION_YOUTUBER_DATABASE_ID=xxx \
  ghcr.io/lucasbiason/notion-mcp-server:latest
```

**Substitua:**
- `secret_xxx` pelo seu token
- Os IDs das databases

### 4.3 Exemplo Completo

```json
{
  "mcpServers": {
    "notion-custom": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "NOTION_TOKEN=secret_xxxYOURTOKENxxx",
        "-e",
        "NOTION_WORK_DATABASE_ID=162b0f651a9c80658a98d5afec50ddea",
        "-e",
        "NOTION_STUDIES_DATABASE_ID=1fa962a7693c80deb90beaa513dcf9d1",
        "-e",
        "NOTION_PERSONAL_DATABASE_ID=240962a7693c80808baaf8cd07e52b9a",
        "-e",
        "NOTION_YOUTUBER_DATABASE_ID=25a962a7693c80f3a3f5d2f4a00d9e4c",
        "ghcr.io/lucasbiason/notion-mcp-server:latest"
      ]
    }
  }
}
```

### 4.4 Salvar e Testar

1. Clique em "Save" ou "Add Server"
2. Clique em "Refresh" (ícone de atualizar)
3. Aguarde alguns segundos
4. Verifique se aparecem Tools, Prompts e Resources

## Passo 5: Verificar Instalação

### 5.1 Tools Disponíveis

Você deve ver tools como:

**NotionService (Base):**
- `notion_create_page`
- `notion_update_page`
- `notion_get_page`
- `notion_query_database`

**WorkNotion:**
- `work_create_project`
- `work_create_subitem`

**StudyNotion:**
- `study_create_course`
- `study_create_class`

**YoutuberNotion:**
- `youtuber_create_series`
- `youtuber_create_episode`

**PersonalNotion:**
- `personal_create_task`
- `personal_create_subtask`

### 5.2 Testar no Composer

Abra o Composer e teste:

```
"Crie um card de trabalho para implementar testes no ExpenseIQ"
```

O Cursor deve usar a tool `work_create_project` automaticamente!

## Troubleshooting

### Problema: "No tools, prompts or resources"

**Soluções:**
1. Clique em "Refresh" novamente
2. Aguarde 15-20 segundos
3. Verifique se o Docker está rodando (`docker ps`)
4. Veja os logs: `MCP Settings > View Logs`
5. Reinicie o Cursor

### Problema: "Connection error"

**Verifique:**
1. Docker está rodando?
2. Token está correto?
3. Database IDs estão corretos?
4. Databases foram compartilhadas com a integração?

### Problema: "Validation error"

**Isso é esperado!** O MCP está validando suas regras.

Exemplos:
```
❌ "Emoji in title" → Use icon property
❌ "Invalid status" → Use correct status for database type
❌ "Invalid timezone" → Use GMT-3 (-03:00)
```

### Ver Logs do Docker

```bash
docker logs -f notion-mcp-server
```

## Uso Avançado

### Configuração Local (Sem Docker)

Se preferir rodar localmente:

```bash
cd /path/to/notion-mcp-server
python -m venv venv
source venv/bin/activate
pip install -e .
```

**Cursor Settings:**
```json
{
  "mcpServers": {
    "notion-custom": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "notion_mcp.server"],
      "env": {
        "NOTION_TOKEN": "secret_xxx",
        "NOTION_WORK_DATABASE_ID": "xxx",
        ...
      }
    }
  }
}
```

### Múltiplas Configurações

Você pode ter múltiplas configurações:

```json
{
  "mcpServers": {
    "notion-work": {
      "command": "docker",
      "args": [...],
      "env": {
        "NOTION_WORK_DATABASE_ID": "xxx"
      }
    },
    "notion-studies": {
      "command": "docker",
      "args": [...],
      "env": {
        "NOTION_STUDIES_DATABASE_ID": "xxx"
      }
    }
  }
}
```

## Próximos Passos

1. ✅ MCP configurado
2. ✅ Tools disponíveis
3. 📖 Leia [API.md](API.md) para referência completa
4. 📖 Leia [EXAMPLES.md](EXAMPLES.md) para exemplos práticos
5. 🚀 Use no Composer!

---

**Dica:** Sempre use prompts naturais no Composer. O MCP escolhe a tool correta automaticamente!

Exemplos:
- "Crie um projeto de trabalho para implementar login"
- "Crie a Fase 5 da FIAP com 3 seções"
- "Agende gravação do episódio 1 de Metal Gear Solid"
- "Crie uma consulta médica para amanhã às 15h"

