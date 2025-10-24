# Changelog

All notable changes to Notion MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- NotionService - Complete Notion API wrapper
- CustomNotion base class
- WorkNotion implementation
- StudyNotion implementation
- YoutuberNotion implementation
- PersonalNotion implementation
- Validators and formatters
- Docker support
- Documentation (API, Examples, Setup, Architecture)
- GitHub Actions CI/CD
- Unit tests structure
- Makefile with development commands

### Features
- Create pages with business rules validation
- Update pages with type safety
- Query databases with filters
- Archive pages
- Multi-database support (Work, Studies, Personal, Youtuber)
- Timezone handling (GMT-3 automatic)
- Study hours validation (19:00-21:00, Tuesday 19:30)
- YouTube recording schedule (21:00-23:50)
- Hierarchical relationships (parent-subitem)

## [0.1.0-alpha] - 2025-10-22

### Added
- Initial alpha release
- Core functionality implemented
- Basic documentation

### Known Issues
- MCP protocol stdio implementation pending
- Some tests pending
- Performance optimization needed

---

## Como Usar Este Changelog

### Para Desenvolvedores
- Veja [Unreleased] para features em desenvolvimento
- Veja versões publicadas para histórico

### Para Usuários
- Veja versões publicadas para mudanças que afetam uso
- Breaking changes sempre destacados

### Para Contribuidores
- Adicione suas mudanças em [Unreleased]
- Categorize: Added, Changed, Deprecated, Removed, Fixed, Security
- Seja específico e claro

---

**Formato:**
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature 1
- New feature 2

### Changed
- Changed behavior of X

### Fixed
- Bug in Y
```

