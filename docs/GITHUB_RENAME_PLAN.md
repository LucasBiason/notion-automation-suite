# Plano para renomear o repositório no GitHub

1. **Preparar repositório local**
   ```bash
   git init
   git remote add origin git@github.com:LucasBiason/notion-automation-suite.git
   git add .
   git commit -m "chore: bootstrap suite unificada"
   ```

2. **Consolidar históricos (opcional)**
   - Usar `git subtree add` ou `git filter-repo` para trazer histórico dos projetos antigos caso necessário.

3. **Publicar**
   ```bash
   git push -u origin main
   ```

4. **Arquivar repositórios legados**
   - Definir como read-only ou mover para uma organização/pasta de histórico.
   - Atualizar README dos repositórios antigos apontando para a suite.

5. **Atualizar integrações**
   - Ajustar tokens/variáveis nas pipelines (GitHub Actions, Render, Cursor) para apontar para o novo repositório.
   - Atualizar install scripts (`install.sh`, Docker) com o novo nome de imagem/publicação.

6. **Comunicar**
   - Registrar mudança na documentação interna.
   - Atualizar referências no Cursor (`mcpServers`) com o novo nome de imagem Docker (`ghcr.io/lucasbiason/notion-automation-suite`).

Este plano assume que a publicação será feita no repositório `LucasBiason/notion-automation-suite` substituindo os projetos anteriores.
