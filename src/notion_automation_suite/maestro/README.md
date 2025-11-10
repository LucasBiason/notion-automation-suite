# 🎭 Maestro - Orquestrador Multiagente

**Versão:** 1.0.0  
**Data:** 01/11/2025  
**Status:** ✅ MVP Pronto

---

## 🎯 **O QUE É O MAESTRO?**

O Maestro é o **orquestrador central** do sistema multiagente. Ele:

- 🧠 **Entende** requisições do usuário
- 🎯 **Decide** quais agentes acionar
- ⚡ **Delega** tarefas (paralelo quando possível)
- 📊 **Consolida** resultados
- 💾 **Mantém** knowledge base compartilhada

---

## 🚀 **INSTALAÇÃO**

```bash
cd /home/lucas-biason/Projetos/Automações/notion-automations/maestro
pip install -r requirements.txt
```

---

## 💻 **USO**

### **Via Python:**

```python
import asyncio
from maestro import Maestro

async def main():
    maestro = Maestro()
    
    # Processar requisição
    result = await maestro.handle_request("Prepare minha semana")
    print(result)

asyncio.run(main())
```

### **Via CLI:**

```bash
python orchestrator.py
```

### **Exemplos de Requisições:**

```python
# Preparar semana
await maestro.handle_request("Prepare minha semana")

# Verificar atrasos
await maestro.handle_request("Verificar tarefas atrasadas")

# Gerar relatório
await maestro.handle_request("Gerar relatório semanal")

# Criar revisão
await maestro.handle_request("Criar revisão da Aula 10", {"aula": "Aula 10"})

# Reorganizar cronograma
await maestro.handle_request("Reorganizar cronograma da FIAP")
```

---

## 🏗️ **ARQUITETURA**

```
┌─────────────────────────────────────────┐
│          MAESTRO (Orquestrador)         │
│  - understand_intent()                  │
│  - decide_agents()                      │
│  - delegate_tasks()                     │
│  - consolidate_results()                │
└───────────────┬─────────────────────────┘
                │
    ┌───────────┴───────────┐
    │                       │
┌───▼────────┐    ┌────────▼──────┐
│  Agentes   │    │   Knowledge   │
│  (8 total) │◄───┤     Base      │
└────────────┘    └───────────────┘
```

---

## 📋 **INTENÇÕES SUPORTADAS**

| Intenção | Palavras-chave | Agentes Acionados |
|----------|----------------|-------------------|
| `PREPARE_WEEK` | prepare, preparar, semana | WeeklyCards, Monitor, Reports |
| `CREATE_REVIEW` | criar, revisão, resumo | CoachEstudos, NotionManager |
| `CHECK_DELAYS` | verificar, atraso | Monitor |
| `GENERATE_REPORT` | gerar, relatório | Reports |
| `REORGANIZE_SCHEDULE` | reorganizar, cronograma | StudyCoach, NotionManager |
| `PLAN_YOUTUBE` | planejar, youtube | YouTubeOrganizer |
| `UPDATE_GAMING` | atualizar, gaming, xp | GamingScripts |

---

## 💾 **KNOWLEDGE BASE**

A Knowledge Base compartilhada armazena:

```json
{
  "system": {
    "current_date": "2025-11-01",
    "timezone": "GMT-3",
    "user": {
      "name": "Lucas Biason",
      "level_xp": 360,
      "duolingo_streak": 56
    }
  },
  "bases": {
    "personal": { "pending_tasks": 0, "late_tasks": 0 },
    "studies": { "current_phase": "FIAP Fase 3" },
    "youtube": { "active_series": 6 },
    "work": { "status": "maintenance" }
  },
  "agents": {},
  "recent_actions": [],
  "pending_decisions": []
}
```

**Localização:** `/tmp/multiagent_state.json`

---

## 🔄 **FLUXO DE EXECUÇÃO**

### **Exemplo: "Prepare minha semana"**

```
1. Maestro recebe: "Prepare minha semana"
         ↓
2. Identifica intent: PREPARE_WEEK
         ↓
3. Decide agentes:
   - WeeklyCards: create_weekly_cards (high priority)
   - Monitor: check_delays (high priority)
   - Reports: generate_weekly_report (medium priority)
         ↓
4. Executa em paralelo (quando possível):
   - WeeklyCards: Cria 3 cards ✅
   - Monitor: Verifica atrasos ✅
   - Reports: Gera relatório ✅
         ↓
5. Consolida resultados:
   "✅ Operação Concluída
    
    Resumo: 3 agentes executados com sucesso
    
    Detalhes:
    ✅ weekly_cards: 3 cards criados
    ✅ monitor: 0 atrasos encontrados
    ✅ reports: Relatório semanal gerado"
```

---

## 🛠️ **PRÓXIMOS PASSOS**

### **TODO (MVP):**
- [ ] Integrar com agentes Python reais
- [ ] Implementar execução de scripts
- [ ] Adicionar logs estruturados
- [ ] Criar testes unitários

### **TODO (Futuro):**
- [ ] Usar LLM para classificação de intent (mais inteligente)
- [ ] Dashboard em tempo real
- [ ] Alertas proativos
- [ ] Métricas de performance

---

## 📝 **EXEMPLOS DE USO**

### **Preparar Semana:**

```python
result = await maestro.handle_request("Prepare minha semana")
```

**Output:**
```
✅ Operação Concluída

Resumo: 3 agentes executados com sucesso

Detalhes:
✅ weekly_cards: 3 cards criados (Planejamento, Tratamento, Pagamento)
✅ monitor: Verificação completa - 2 atrasos detectados
✅ reports: Relatório semanal gerado

⚠️ Ações Recomendadas:
- Reorganizar Aula 10 (2 dias de atraso)
- Editar Ep 05 (lançamento em 6 horas)
```

### **Verificar Atrasos:**

```python
result = await maestro.handle_request("Verificar tarefas atrasadas")
```

**Output:**
```
✅ Operação Concluída

Resumo: 1 agente executado com sucesso

Detalhes:
✅ monitor: Verificação completa

📊 Status:
- Personal: 0 atrasos
- Studies: 1 atraso (Aula 10 - 2 dias)
- YouTube: 1 atraso (Ep 05 - edição pendente)
- Work: 0 atrasos
```

---

## 🎯 **INTEGRAÇÃO COM CURSOR**

Para usar com Cursor 2.0:

```bash
# 1. Adicionar ao PATH
export PYTHONPATH="/home/lucas-biason/Projetos/Automações/notion-automations:$PYTHONPATH"

# 2. Chamar do Cursor
from maestro import Maestro
maestro = Maestro()
await maestro.handle_request("sua requisição aqui")
```

---

## 📊 **STATUS DO DESENVOLVIMENTO**

| Componente | Status | Completude |
|------------|--------|------------|
| Orquestrador | ✅ MVP | 70% |
| Knowledge Base | ✅ Funcional | 80% |
| Intent Classification | ✅ Keywords | 60% |
| Agent Delegation | ⏳ Simulado | 40% |
| Result Consolidation | ✅ Funcional | 75% |
| Logs & Monitoring | ⏳ Básico | 30% |
| Tests | ⏳ Pendente | 0% |

---

## 🤝 **CONTRIBUINDO**

Este é um projeto pessoal, mas sugestões são bem-vindas!

---

## 📞 **CONTATO**

**Autor:** Lucas Biason  
**Data:** 01/11/2025  
**Versão:** 1.0.0 (MVP)

---

**🎉 MAESTRO PRONTO PARA ORQUESTRAR!** 🎭






