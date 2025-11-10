# 🤖 Regras Obrigatórias Para TODOS os Agentes

**Data:** 09/10/2025  
**Versão:** 1.0.0  
**Aplicável a:** TODOS os agentes que criarem código

---

## ⚠️ **REGRA CRÍTICA: SEMPRE COMMITAR CÓDIGO**

### **Quando um agente criar/modificar qualquer código Python:**

#### **1. Commitar IMEDIATAMENTE após criar:**
```bash
cd /home/lucas-biason/Projetos/Automações/notion-automations/notion-automation-scripts
git add .
git commit -m "feat(agent-X): [descrição do que foi criado]"
git push origin main
```

#### **2. Mensagem de commit deve seguir padrão:**
```
feat(agent-1): criar gerenciador de cards semanais
feat(agent-2): adicionar reorganizador de cronogramas
fix(agent-3): corrigir bug em finalizador semanal
docs(agent-1): atualizar documentação
```

#### **3. NUNCA deixar código apenas local**
- ❌ **ERRADO:** Criar código e não commitar
- ✅ **CERTO:** Criar código → Commitar → Push

---

## 📁 **REPOSITÓRIOS**

### **notion-automation-scripts**
**URL:** https://github.com/LucasBiason/notion-automation-scripts  
**Para:** Scripts de automação Notion (já existente)  
**Commitar:** Todo script novo ou modificado

### **notion-automation-agents**
**URL:** https://github.com/LucasBiason/notion-automation-agents  
**Para:** Agentes inteligentes (em desenvolvimento)  
**Commitar:** Todo código de agente criado

---

## 🔄 **WORKFLOW OBRIGATÓRIO**

### **Ao criar novo agente:**
1. Criar código do agente
2. Criar testes
3. **COMMITAR no repositório correto**
4. Atualizar README
5. **COMMITAR atualização do README**
6. Notificar usuário

### **Ao modificar agente existente:**
1. Modificar código
2. Atualizar testes
3. **COMMITAR modificações**
4. Notificar usuário das mudanças

---

## 📝 **CHECKLIST ANTES DE FINALIZAR**

Antes de dizer "concluído", o agente DEVE:
- [ ] Código criado/modificado
- [ ] Testes criados/atualizados
- [ ] **Git add executado**
- [ ] **Git commit executado**
- [ ] **Git push executado**
- [ ] **Notion atualizado** (subtarefa → Concluído)
- [ ] **Link do commit adicionado no Notion**
- [ ] README atualizado (se necessário)
- [ ] Usuário notificado

---

## 🚨 **NUNCA FAZER**

❌ Criar código e deixar apenas local  
❌ Esquecer de commitar  
❌ Commitar sem mensagem descritiva  
❌ Deixar código sem push  
❌ Não atualizar documentação

---

## ✅ **SEMPRE FAZER**

✅ Commitar imediatamente após criar código  
✅ Usar mensagens de commit descritivas  
✅ Fazer push para o GitHub  
✅ Atualizar documentação quando necessário  
✅ Notificar usuário que código foi commitado

---

## 📍 **LOCALIZAÇÃO DOS REPOSITÓRIOS**

### **Local:**
```
/home/lucas-biason/Projetos/Automações/notion-automations/
├── notion-automation-scripts/  (scripts já funcionais)
└── notion-automation-agents/    (agentes em desenvolvimento)
```

### **GitHub:**
```
https://github.com/LucasBiason/notion-automation-scripts
https://github.com/LucasBiason/notion-automation-agents
```

---

## 🎯 **EXEMPLO COMPLETO**

### **Cenário: Agente cria Agent 1**

```bash
# 1. Criar código
# ... código do agent_1_weekly_cards.py criado ...

# 2. Commitar IMEDIATAMENTE
cd /home/lucas-biason/Projetos/Automações/notion-automations/notion-automation-agents
git add agents/agent_1_weekly_cards.py
git commit -m "feat(agent-1): implementar gerenciador de cards semanais

- Criar cards semanais (Planejamento, Hamilton, Tratamento)
- Criar cards mensais (Revisão Financeira, NF, Fechamento)
- Validação de duplicação
- Timezone GMT-3
- Testes incluídos"

git push origin main

# 3. Notificar usuário
# "✅ Agent 1 implementado e commitado no GitHub!"
```

---

## 🔐 **CREDENCIAIS E SEGURANÇA**

### **NUNCA commitar:**
- ❌ `.env` com tokens
- ❌ Credenciais
- ❌ Senhas
- ❌ Tokens de API

### **SEMPRE commitar:**
- ✅ `.env.example` (template)
- ✅ Código Python
- ✅ README e documentação
- ✅ Requirements.txt
- ✅ Testes

---

## 📊 **VALIDAÇÃO**

### **Como saber se seguiu as regras:**
1. Código existe no GitHub? ✅
2. Commit tem mensagem descritiva? ✅
3. Push foi feito? ✅
4. README foi atualizado (se necessário)? ✅
5. Usuário foi notificado? ✅

**Se todas respostas são SIM:** ✅ **Regras seguidas!**  
**Se alguma é NÃO:** ❌ **Voltar e corrigir!**

---

## 💬 **MENSAGEM AO USUÁRIO**

### **Sempre que commitar, avisar:**
```
✅ [Nome do Agente] implementado!

📦 Commitado em: https://github.com/LucasBiason/[repo]
🔗 Commit: [hash]
📋 Notion atualizado: https://www.notion.so/Agentes-de-Automa-o-Notion-Cursor-287962a7693c8171982ff9b13993df67
📝 Arquivos criados:
  - agents/agent_X.py
  - tests/test_agent_X.py
  
Pronto para testar!
```

---

## 🎯 **RESPONSABILIDADE**

**CADA agente é responsável por:**
1. Seu próprio código
2. Commitar seu código
3. Manter GitHub atualizado
4. Notificar usuário

**NÃO depender de outro agente para commitar!**

---

**Esta regra é OBRIGATÓRIA e INEGOCIÁVEL!**

**Última Atualização:** 09/10/2025  
**Validade:** Permanente  
**Exceções:** Nenhuma

