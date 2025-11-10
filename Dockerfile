FROM python:3.11-slim

LABEL maintainer="Lucas Biason <lucas.biason@gmail.com>"
LABEL description="Notion Automation Suite - MCP + ferramentas unificadas"

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia metadados e código
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Instala dependências e pacote
RUN pip install --no-cache-dir pip>=24.0 && \
    pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 notionuser && \
    chown -R notionuser:notionuser /app

USER notionuser

# STDIO MCP server
ENTRYPOINT ["notion-mcp-server"]

