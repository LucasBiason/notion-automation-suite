# 🤖 Especificação Completa dos Agentes

**Versão:** 1.0.0  
**Data:** 09/10/2025

---

## 📋 **VISÃO GERAL**

Este documento detalha a especificação completa de cada agente, incluindo funcionalidades, triggers, integrações e considerações especiais baseadas no feedback do usuário.

---

## 🤖 **AGENTE 1: GERENCIADOR DE CARDS SEMANAIS**

### **Objetivo**
Automatizar completamente a criação de cards recorrentes semanais e mensais, eliminando o trabalho manual.

### **Funcionalidades**

#### **Cards Semanais**
1. **Planejamento Semanal** (toda segunda-feira):
   - Data: Segunda-feira da semana
   - Horário: 07:00 (início do dia)
   - Status: Não iniciado
   - Atividade: Gestão
   - Descrição: "Revisão semanal e planejamento da semana"

2. **Pagamento Hamilton (Médico)** (toda segunda-feira):
   - Data: Segunda-feira da semana
   - Status: Não iniciado
   - Atividade: Finanças
   - Descrição: "Realizar transferência bancária e envio do comprovante"
   - Notas: Dados bancários salvos no template

3. **Tratamento Médico** (toda terça-feira):
   - Data: Terça-feira da semana
   - Horário: 16:00-18:00
   - Status: Não iniciado
   - Atividade: Saúde
   - Descrição: "Sessão de tratamento sempre às terças das 16:00 às 18:00"

#### **Cards Mensais**
1. **Revisão Financeira** (dia 15):
   - Data: Dia 15 do mês
   - Horário: Flexível (manhã sugerido)
   - Status: Não iniciado
   - Atividade: Finanças
   - Descrição: "Revisão quinzenal das finanças"

2. **Emissão de Nota Fiscal** (dia 25):
   - Data: Dia 25 do mês
   - Status: Não iniciado
   - Atividade: Finanças
   - Descrição: "Emitir nota fiscal mensal"

3. **Revisão Financeira - Fechamento** (dia 30):
   - Data: Dia 30 do mês
   - Status: Não iniciado
   - Atividade: Finanças
   - Descrição: "Fechamento mensal das finanças"

### **Triggers**
- **Domingo 23:00**: Criar cards da próxima semana
- **Dia 1 do mês 00:00**: Criar cards mensais
- **Sob demanda**: Quando usuário pedir

### **Validações**
- ✅ Verificar se card já existe antes de criar
- ✅ Sempre usar GMT-3
- ✅ Buscar templates salvos no Notion
- ✅ Adaptar datas ao mês corrente

### **Templates no Notion**
- Buscar em base de templates (usuário confirmou que existem)
- Adaptar propriedades automaticamente
- Manter descrições e notas padrão

---

## 📚 **AGENTE 2: COACH DE ESTUDOS**

### **Objetivo**
Atuar como professor particular e reorganizador inteligente de cronogramas de estudo.

### **Funcionalidades**

#### **Parte 1: Reorganizador de Cronogramas**

**Quando executar:**
- Detectar aula marcada como "Pulada" ou "Adiada"
- Novo curso adicionado
- Usuário solicita reajuste
- Diariamente às 07:00 (verificação preventiva)

**Lógica de Reorganização:**
1. Identificar cards afetados (tudo após o pulo)
2. Recalcular datas respeitando:
   - **Horários**: 19:00-21:00 (seg, qua, qui, sex)
   - **Terça**: 19:30-21:00 (horário reduzido)
   - **Limite**: 21:00 SEMPRE (nunca passar)
   - **Overflow**: Se aula passa das 21:00, mover para próximo dia
   - **Finais de semana**: Pular automaticamente
   - **Revisões**: 15min entre aulas, 30min entre módulos

3. Atualizar TODOS os cards subsequentes
4. Manter timezone GMT-3
5. Notificar usuário das mudanças

**Exemplo de Cenário:**
```
Situação: Usuário pula semana inteira (canal YouTube)
Ação: 
- Identificar 5 aulas agendadas
- Mover TODAS as aulas para semana seguinte
- Recalcular períodos de revisão
- Ajustar data final do curso
- Notificar: "FIAP Fase 4 agora termina em 23/10 ao invés de 16/10"
```

#### **Parte 2: Professor Particular (IA)**

**Contextos Necessários:**
- `@01-Estudos/` - Base de conhecimento de estudos
- `@ia-ml-knowledge-base/` - Projetos de IA
- `@Apostilas e Materiais de Cursos/` - Material didático
- `@Cronograma Estudos/` - Planejamentos
- `@CONTEXTO_PROJETO.md` - Contexto geral

**Funcionalidades:**

1. **Geração de Resumos de Aulas:**
   - Input: Transcrição da aula + Apostila PDF
   - Prompt: Buscar na Galeria de Prompts do Notion
   - Output: Card resumo detalhado com:
     - Conceitos principais
     - Exemplos práticos
     - Pontos importantes
     - Relação com outros conteúdos
     - Próximos passos

2. **Criação de Exercícios Práticos:**
   - Baseado no conteúdo da aula
   - Níveis: Básico, Intermediário, Avançado
   - Formato: Código executável
   - Inclui gabarito e explicações

3. **Acompanhamento de Progresso:**
   - Verifica cards de aulas concluídos
   - Identifica lacunas no aprendizado
   - Sugere revisões quando necessário
   - Alerta sobre conceitos não dominados

4. **Coach Pessoal:**
   - Responde dúvidas sobre conteúdo
   - Explica conceitos complexos
   - Sugere materiais complementares
   - Motiva e acompanha evolução

**Workflow Automático:**
1. Usuário marca aula como "Concluída"
2. Agent detecta e cria card "Revisão - [Nome da Aula]"
3. Agent busca transcrição + apostila
4. Agent usa prompt da galeria para gerar resumo
5. Agent cria card com resumo detalhado
6. Agent cria exercícios práticos
7. Agent agenda próxima aula respeitando cronograma

### **Integração com Galeria de Prompts**
- Buscar prompts na base de dados específica do Notion
- Usar prompt adequado para cada tipo de conteúdo:
  - Resumo de aula
  - Exercícios práticos
  - Análise de código
  - Revisão de conceitos

### **Prevenção de Esquecimentos** (Preocupação do usuário)
- ✅ Verificar se revisão foi criada
- ✅ Alertar se passou 24h sem revisar
- ✅ Lembrar de atualizar prompts se mudarem
- ✅ Validar que resumo foi gerado
- ✅ Confirmar exercícios criados

---

## ✅ **AGENTE 3: FINALIZADOR SEMANAL**

### **Objetivo**
Manter as bases limpas marcando cards antigos como concluídos ou cancelados.

### **Funcionalidades**

#### **Execução Semanal (Segunda 07:00)**
1. Buscar todos os cards da semana anterior (seg-sex)
2. Filtrar apenas: "Não iniciado" ou "Em andamento"
3. Para cada card:
   - Perguntar ao usuário: "Concluir ou Cancelar?"
   - Ou: Auto-marcar como "Concluído" (configurável)
4. Atualizar status
5. Gerar relatório de cards finalizados

#### **Execução Diária (23:00)**
1. Buscar cards de HOJE não concluídos
2. Notificar usuário:
   - "Você tem X cards pendentes hoje"
   - Listar os cards
   - Perguntar se quer mover para amanhã

### **Validações**
- Não marcar cards de trabalho críticos automaticamente
- Não tocar em cards de cursos em andamento
- Sempre pedir confirmação para cards importantes

---

## 🎬 **AGENTE 4: ORGANIZADOR YOUTUBE**

### **Objetivo**
Garantir que episódios sejam gravados, editados e publicados no prazo.

### **Funcionalidades**

#### **Criação Automática de Cards de Produção**

**48h antes da Data de Lançamento:**
1. **Card de Gravação:**
   - Título: "Gravar - [Nome do Episódio]"
   - Período: Calculado para caber no horário 21:00-00:00
   - Data: 2 dias antes do lançamento
   - Status: Para Gravar
   - Relação: Link para o episódio principal

2. **Card de Edição:**
   - Título: "Editar - [Nome do Episódio]"
   - Período: Após gravação (21:30-23:30)
   - Status: Para Editar

3. **Card de Upload:**
   - Título: "Upload - [Nome do Episódio]"
   - Período: 2h antes do lançamento
   - Status: Para Publicar

#### **Monitoramento de Produção**
- Verifica se episódio foi gravado 24h antes do lançamento
- Alerta se gravação não foi feita
- Reorganiza cronograma se houver atraso
- Move data de lançamento se necessário

#### **Diferenciação de Datas** (Importante!)
- **Data de Lançamento**: Quando episódio fica público (informativo)
- **Período**: Quando GRAVAR o episódio (ação real)
- Agent trabalha com ambas, mas foca no Período

### **Regras de Horário YouTube**
- Gravação: 21:00-23:30 (seg-sex)
- Edição: Mesma sessão ou próximo dia
- Upload: 2h antes do lançamento
- Timezone: Sempre GMT-3

---

## 📊 **AGENTE 6: GERADOR DE RELATÓRIOS**

### **Objetivo**
Fornecer visão clara e atualizada de tudo o que está acontecendo.

### **Funcionalidades**

#### **Relatório Semanal (Segunda 07:00)**
```markdown
# 📊 Relatório Semanal - [Data]

## ✅ Concluído na Semana Passada
- [X] Card 1
- [X] Card 2
...

## 📚 Cursos em Andamento
- FIAP Fase 4: 45% concluído
- Rocketseat IA: Iniciando em Nov

## 📅 Próximos Compromissos (Esta Semana)
- Segunda 07:00: Planejamento Semanal
- Terça 16:00: Tratamento Médico
- Quarta 19:00: Aula FIAP
...

## 🎬 YouTube
- 3 episódios para gravar
- 2 episódios em edição
- 1 episódio para lançar hoje

## ⚠️ Alertas
- FIAP Fase 4 termina em 9 dias
- 2 cards atrasados
```

#### **Relatório Mensal (Dia 1 00:00)**
```markdown
# 📊 Relatório Mensal - [Mês/Ano]

## 📊 Estatísticas
- Horas estudadas: 72h
- Cards concluídos: 45
- Episódios publicados: 12
- Cursos completados: 1

## 📚 Progresso de Cursos
- FIAP Fase 4: 100% ✅
- Rocketseat: 30% 🔄

## 🎯 Metas Atingidas
- ✅ Finalizar FIAP Fase 4
- ✅ Gravar 12 episódios
- ❌ Curso Rocketseat (movido para próximo mês)

## 📈 Evolução
- Mês anterior: 60h estudadas
- Este mês: 72h (+20%)
```

#### **Relatório Sob Demanda**
Quando usuário pedir: "Como estamos hoje?" ou "Qual minha agenda?"
- Status atual de tudo
- Próximas 24h detalhadas
- Cards pendentes urgentes
- Conflitos de horário

---

## 🚨 **AGENTE 7-8-9: MONITOR INTEGRADO**

### **Objetivo**
Combinar monitoramento de prazos, otimização de cronograma e integração entre bases em um único agente inteligente.

### **Funcionalidades Combinadas**

#### **1. Monitor de Prazos**

**Verificações Contínuas:**
- Cursos com prazo próximo (< 7 dias)
- Cards vencidos não concluídos
- Conflitos de horário (duas coisas ao mesmo tempo)
- Tech Challenges próximos

**Alertas Proativos:**
```
⚠️ ALERTA: A Fase 4 da FIAP termina em 5 dias
   - 8 aulas restantes
   - 16 horas de conteúdo
   - Você tem 10 horas disponíveis
   - SUGESTÃO: Adiar 2 aulas para semana seguinte
```

#### **2. Otimizador de Cronograma**

**Análise de Carga:**
- Calcular horas de trabalho + estudo + YouTube por semana
- Detectar sobrecarga (> 40h total)
- Sugerir redistribuição

**Exemplo de Otimização:**
```
🎯 ANÁLISE DA SEMANA 14-18/10:
   - Trabalho: 40h
   - Estudo: 10h (5 aulas)
   - YouTube: 6h (2 episódios)
   - TOTAL: 56h (SOBRECARGA!)

💡 SUGESTÃO:
   - Mover 1 episódio para semana seguinte
   - Adiar 1 aula de revisão
   - Novo total: 48h (melhor!)
```

#### **3. Integrador de Bases**

**Verificações de Conflito:**
- Curso não pode conflitar com trabalho (08:00-17:00)
- YouTube não pode conflitar com estudo (19:00-21:00)
- Tarefa pessoal não pode conflitar com tratamento médico
- Gravação YouTube precisa de 2h livres (21:00-23:00)

**Exemplo de Integração:**
```
🔗 VERIFICANDO INTEGRAÇÃO:
   - Card: "Aula FIAP" agendada para 15/10 14:00
   - CONFLITO: Horário de trabalho (08:00-17:00)
   - CORREÇÃO: Mover para 15/10 19:00
   - VALIDADO: ✅ Sem conflitos
```

### **Sistema de Alertas** (Resposta à pergunta 9)

**Dentro do Cursor:**
- Notificações no próprio Cursor
- Messages na sidebar
- Toast notifications

**Fora do Cursor:**
- Atualmente: Apenas quando abrir o Cursor
- **Futuro (Fase 2)**:
  - Integração com Telegram/Discord
  - Email para alertas críticos
  - Push notifications (se configurar)

**Por enquanto:**
- Alertas ficam salvos em log
- Quando abrir Cursor, vê resumo de alertas pendentes
- Relatório semanal por email (opcional)

---

## 🔧 **CONSIDERAÇÕES TÉCNICAS**

### **Timezone (Resposta à pergunta 7)**
- ✅ Todos os cards existentes JÁ CORRIGIDOS para GMT-3 (317 cards)
- ✅ Todos os agentes SEMPRE usam GMT-3
- ✅ Validação forçada: qualquer card novo = GMT-3
- ✅ Verificação diária: se algum card vier em UTC, corrigir

### **Backup (Resposta à pergunta 12)**
- ❌ NÃO implementar Agente 10 (Backup)
- Motivo: Notion versão paga já tem backup nativo
- Alternativa: Se necessário, criar exports semanais simples

### **Agentes Unificados (Respostas às perguntas 9, 10, 11)**
- Agent 7, 8, 9 = **UM ÚNICO AGENTE** com 3 funcionalidades
- Motivo: Trabalham juntos, compartilham lógica
- Benefício: Mais eficiente e menos complexo

---

## 📝 **ESPECIFICAÇÕES PARA COACH DE ESTUDOS (IA)**

### **Contexto Required**
```python
CONTEXTS = {
    'estudos_base': '/home/lucas-biason/Projetos/Contextos de IA/01-Estudos/',
    'ia_ml_kb': '/home/lucas-biason/Projetos/Estudos/ia-ml-knowledge-base/',
    'apostilas': '/home/lucas-biason/Projetos/Estudos/Apostilas e Materiais de Cursos/',
    'cronogramas': '/home/lucas-biason/Projetos/Arquivos e Rascunhos/Cronograma Estudos/',
    'contexto_projeto': '/home/lucas-biason/Projetos/Arquivos e Rascunhos/CONTEXTO_PROJETO.md'
}
```

### **Prompt de Sistema (Base)**
```
Você é um Coach de Estudos especializado em IA e Machine Learning.

Seu papel:
1. Gerar resumos detalhados de aulas
2. Criar exercícios práticos personalizados
3. Acompanhar progresso do aluno
4. Explicar conceitos complexos de forma didática
5. Motivar e manter engajamento

Contexto do Aluno:
- Pós-graduação FIAP em IA
- Desenvolvedor Senior Python
- Foco: RAG, Fine Tuning, Agentes, React
- Horários limitados: 19:00-21:00 (seg-sex), 19:30-21:00 (ter)

Sempre:
- Respeitar horários de estudo
- Gerar conteúdo acionável
- Explicar o "porquê" dos conceitos
- Conectar com projetos práticos
- Manter motivação alta
```

### **Prompts da Galeria (Notion)**
O agent deve buscar prompts específicos para:
- `resumo_aula_tecnica`
- `exercicios_praticos_ia`
- `revisao_conceitos_complexos`
- `analise_codigo_estudante`

---

## 🎯 **IMPLEMENTAÇÃO PRIORITIES**

### **Fase 1 - Essencial (Esta Semana)**
1. ✅ Agent 1: Gerenciador de Cards Semanais
2. ✅ Agent 3: Finalizador Semanal
3. ✅ Core: Notion Client + Timezone Utils

### **Fase 2 - Inteligência (Próxima Semana)**
4. ✅ Agent 2: Coach de Estudos (IA)
5. ✅ Agent 6: Gerador de Relatórios
6. ✅ Integração OpenAI + Prompts

### **Fase 3 - Monitoramento (Semana 3)**
7. ✅ Agent 4: Organizador YouTube
8. ✅ Agent 7-8-9: Monitor Integrado
9. ✅ Sistema de alertas

### **Fase 4 - Polimento (Semana 4)**
10. ✅ Testes completos
11. ✅ Documentação final
12. ✅ Deploy e automação

---

## 🔒 **SEGURANÇA E PRIVACIDADE**

### **Dados Sensíveis**
- Tokens nunca no código
- Sempre em `.env`
- `.env` no `.gitignore`
- Repositório PRIVADO

### **Validações**
- Verificar propriedades antes de criar cards
- Validar datas e horários
- Prevenir duplicação
- Log de todas as ações

---

**Última Atualização:** 09/10/2025  
**Próxima Revisão:** 16/10/2025  
**Status:** 📋 ESPECIFICAÇÃO COMPLETA

