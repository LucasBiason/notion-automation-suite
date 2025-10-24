# Contribuindo para Notion MCP Server

Obrigado por considerar contribuir! Este documento fornece diretrizes para contribuições.

## Code of Conduct

Este projeto adere a padrões profissionais de comportamento. Seja respeitoso e construtivo.

## Como Contribuir

### Reportar Bugs

1. Verifique se o bug já foi reportado em [Issues](https://github.com/LucasBiason/notion-mcp-server/issues)
2. Se não, crie uma nova issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs. observado
   - Versão do Python e do projeto
   - Logs relevantes

### Sugerir Features

1. Abra uma issue descrevendo:
   - O que você quer fazer
   - Por que isso é útil
   - Como deveria funcionar
2. Aguarde feedback antes de implementar

### Pull Requests

#### Antes de Começar

1. Fork o repositório
2. Clone seu fork
3. Crie uma branch: `git checkout -b feat/minha-feature`
4. Configure o ambiente de desenvolvimento

#### Desenvolvimento

1. **Instale dependências:**
   ```bash
   make install-dev
   ```

2. **Faça suas mudanças**
   - Siga o style guide (PEP 8)
   - Adicione type hints
   - Comente código complexo em inglês

3. **Execute testes:**
   ```bash
   make test
   ```

4. **Execute linter:**
   ```bash
   make lint
   ```

5. **Formate código:**
   ```bash
   make format
   ```

6. **Verifique tipos:**
   ```bash
   make type-check
   ```

#### Commit

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add support for Comments API
fix: correct timezone handling for Personal database
docs: update API documentation
test: add tests for StudyNotion.reschedule_classes()
refactor: simplify validation logic
chore: update dependencies
```

#### Pull Request

1. Push para seu fork
2. Abra PR no repositório principal
3. Preencha o template do PR
4. Aguarde review

### Code Review

Todos PRs passam por code review. Esperamos:

- ✅ Testes passando (CI verde)
- ✅ Coverage mantido (95%+)
- ✅ Documentação atualizada
- ✅ Commits bem descritos
- ✅ Code style consistente

## Style Guide

### Python

Seguimos **PEP 8** com algumas customizações:

```python
# Line length: 100 caracteres (não 79)
# Aspas: duplas para strings, simples para dict keys
# Imports: grouped (stdlib, third-party, local)

# ✅ BOM
from typing import Dict, List

def my_function(param: str) -> Dict[str, Any]:
    """
    Function docstring
    
    Args:
        param: Parameter description
    
    Returns:
        Return value description
    """
    result = {"key": "value"}
    return result

# ❌ RUIM
def myFunction(p):
    r = {'key':'value'}
    return r
```

### Nomenclatura

- **Funções e variáveis:** `lowercase_with_underscores`
- **Classes:** `PascalCase`
- **Constantes:** `UPPER_CASE`
- **Privadas:** `_leading_underscore`

### Docstrings

Use Google style:

```python
def my_function(param1: str, param2: int) -> str:
    """
    Brief description
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When something is wrong
    
    Examples:
        >>> my_function("test", 42)
        'result'
    """
    pass
```

## Testes

### Estrutura

```python
def test_feature_description():
    """Test that feature works correctly"""
    # Arrange
    service = NotionService(token="test")
    
    # Act
    result = service.some_method()
    
    # Assert
    assert result == expected
```

### Coverage

- Mínimo 95% de coverage
- Testar casos de sucesso E erro
- Testar edge cases
- Usar mocks para API externa

### Executar Testes

```bash
# Todos os testes
make test

# Com coverage
make test-cov

# Específico
pytest tests/test_notion_service.py -v

# Com logs
pytest -v -s
```

## Documentação

### Quando Documentar

- ✅ Toda função pública (docstring)
- ✅ Toda classe (docstring)
- ✅ Toda feature nova (docs/)
- ✅ Toda mudança de API (docs/API.md)

### Onde Documentar

- **Código:** Docstrings em inglês
- **API:** `docs/API.md`
- **Exemplos:** `docs/EXAMPLES.md`
- **Setup:** `docs/SETUP_CURSOR.md`
- **Arquitetura:** `docs/ARCHITECTURE.md`

## Versionamento

Usamos [Semantic Versioning](https://semver.org/):

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

Exemplo: `1.2.3`
- `1` = MAJOR
- `2` = MINOR
- `3` = PATCH

## Release Process

1. Update `version` in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit: `chore: bump version to X.Y.Z`
4. Tag: `git tag vX.Y.Z`
5. Push: `git push && git push --tags`
6. GitHub Actions build e publica automaticamente

## Perguntas?

- 📖 Leia a [documentação](docs/)
- 🐛 Abra uma [issue](https://github.com/LucasBiason/notion-mcp-server/issues)
- 💬 Inicie uma [discussion](https://github.com/LucasBiason/notion-mcp-server/discussions)

---

**Obrigado por contribuir!** 🎉

