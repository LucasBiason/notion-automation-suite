#!/usr/bin/env python3
"""
Criar TODAS as aulas da Formação Udemy IA/ML como sub-itens das sessões
Marcar como Concluído (checkbox preenchido) ou Para Fazer (checkbox vazio)
"""

import requests
from datetime import datetime
import pytz

# Configuração
NOTION_TOKEN = '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'
NOTION_VERSION = '2022-06-28'
ESTUDOS_DB = '1fa962a7-693c-80de-b90b-eaa513dcf9d1'

# Timezone
gmt3 = pytz.timezone('America/Sao_Paulo')

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_VERSION
}

def query_database(database_id, filter_data=None):
    """Query Notion database."""
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    payload = {'filter': filter_data} if filter_data else {}
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"❌ Erro ao consultar database: {response.status_code} - {response.text}")
        return []

def create_page(database_id, properties, parent_id=None, icon=None):
    """Cria uma página no Notion."""
    url = 'https://api.notion.com/v1/pages'
    
    payload = {
        'parent': {'database_id': database_id},
        'properties': properties
    }
    
    if parent_id:
        payload['properties']['Parent item'] = {"relation": [{"id": parent_id}]}
    
    if icon:
        payload['icon'] = icon
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Erro ao criar página: {response.status_code} - {response.text}")
        return None

def find_session_by_title(title):
    """Encontra uma sessão pelo título."""
    filter_data = {
        "property": "Project name",
        "title": {
            "contains": title
        }
    }
    results = query_database(ESTUDOS_DB, filter_data)
    return results[0]['id'] if results else None

# Estrutura COMPLETA do curso baseada nas imagens
SESSOES = {
    "Seção 1: Introdução": [
        {"title": "Instruções", "duration": "2m", "completed": True},
        {"title": "Apresentação e Conteúdo do Curso", "duration": "5m", "completed": True},
        {"title": "Orientações Gerais", "duration": "3m", "completed": True},
        {"title": "Material para Download", "duration": "1m", "completed": True},
        {"title": "Ambiente Python para o Curso", "duration": "5m", "completed": True},
        {"title": "Tutorial de Google Colab", "duration": "14m", "completed": True},
        {"title": "Dica Extra para Google Colab", "duration": "5m", "completed": True},
    ],
    "Seção 2: Fundamentos de Machine Learning": [
        {"title": "8. Introdução", "duration": "9m", "completed": True},
        {"title": "9. Aplicações", "duration": "7m", "completed": True},
        {"title": "10. Definições Gerais", "duration": "6m", "completed": True},
        {"title": "11. Conceitos Fundamentais", "duration": "10m", "completed": True},
        {"title": "12. Introdução a Classificação", "duration": "21m", "completed": True},
        {"title": "13. Avaliação de Performance e Matriz de Confusão", "duration": "21m", "completed": True},
        {"title": "14. Avaliação de Performance para Regressão", "duration": "12m", "completed": True},
        {"title": "15. Codificação de Categorias", "duration": "7m", "completed": True},
        {"title": "16. Dimensionamento de Características", "duration": "9m", "completed": True},
        {"title": "17. Fundamentos de Agrupamentos", "duration": "8m", "completed": True},
        {"title": "18. Regras de Associação", "duration": "12m", "completed": True},
        {"title": "Teste 1: Fundamentos de Machine Learning", "duration": None, "completed": True},
        {"title": "Role play 1: Fundamentos de Machine Learning", "duration": None, "completed": True},
    ],
    "Seção 3: Estudo de Algoritmos de Machine Learning": [
        {"title": "19. Introdução a Correlação e Regressão Linear", "duration": "20m", "completed": True},
        {"title": "20. Condições para Regressão Linear", "duration": "7m", "completed": True},
        {"title": "21. Cálculos na Regressão Linear", "duration": "4m", "completed": True},
        {"title": "22. Lab: Regressão Linear em Python", "duration": "14m", "completed": True},
        {"title": "23. Lab: Regressão Linear com StatsModels", "duration": "18m", "completed": True},
        {"title": "24. Lab: Regressão Linear com StatsModels (Continuação)", "duration": "19m", "completed": True},
        {"title": "25. Naive Bayes", "duration": "16m", "completed": True},
        {"title": "26. Lab: Naive Bayes", "duration": "14m", "completed": True},
        {"title": "27. Lab: Naive Bayes (Continuação)", "duration": "17m", "completed": True},
        {"title": "28. Árvores de Decisão", "duration": "8m", "completed": True},
        {"title": "29. Opcional: Cálculos para Induzir uma Árvore de Decisão", "duration": "19m", "completed": True},
        {"title": "30. Lab: Implementando Árvores de Decisão", "duration": "12m", "completed": True},
        {"title": "31. Aprendizado Baseado em Grupos com Random Forest", "duration": "5m", "completed": True},
        {"title": "32. Lab: Random Forest", "duration": "11m", "completed": True},
        {"title": "33. Aprendizado Baseado em Instância", "duration": "7m", "completed": True},
        {"title": "34. KNN: Vizinho mais Próximo", "duration": "3m", "completed": True},
        {"title": "35. Lab: Implementando KNN", "duration": "17m", "completed": True},
        {"title": "36. KMeans", "duration": "10m", "completed": True},
        {"title": "37. Lab: Implementando Clusters Diversos", "duration": "18m", "completed": True},
        {"title": "38. Lab: Implementando Clusters Diversos (Continuação)", "duration": "20m", "completed": True},
        {"title": "39. Regras de Associação com Apriori", "duration": "6m", "completed": True},
        {"title": "40. Lab: Implementado Apriori", "duration": "10m", "completed": True},
    ],
    "Seção 4: Tópicos Avançados em Machine Learning": [
        {"title": "41. Engenharia e Seleção de Atributos", "duration": "10m", "completed": True},
        {"title": "42. Lab: Engenharia de Atributos", "duration": "17m", "completed": True},
        {"title": "43. Lab: Engenharia de Atributos (Continuação)", "duration": "25m", "completed": True},
        {"title": "44. PCA: Principal Component Analysis", "duration": "4m", "completed": True},
        {"title": "45. Lab: PCA", "duration": "14m", "completed": True},
        {"title": "46. Seleção de Atributos", "duration": "3m", "completed": True},
        {"title": "47. Lab: Seleção de Atributos", "duration": "16m", "completed": True},
        {"title": "48. Avaliando a Viabilidade de um Modelo", "duration": "11m", "completed": True},
        {"title": "49. Avaliando e Comparando a Performance de Modelos", "duration": "12m", "completed": True},
        {"title": "50. Custo de Modelos", "duration": "10m", "completed": True},
        {"title": "51. Técnicas Avançadas para Clusters", "duration": "10m", "completed": True},
        {"title": "52. Lab: Técnicas Avançadas para Clusters", "duration": "14m", "completed": True},
        {"title": "53. Lab: Técnicas Avançadas para Clusters (Continuação)", "duration": "8m", "completed": True},
        {"title": "54. Lab: Escolhendo o Melhor Agrupador", "duration": "16m", "completed": True},
        {"title": "55. Lab: Escolhendo o Melhor Agrupador (Continuação)", "duration": "7m", "completed": True},
        {"title": "56. Classificação Multi Label", "duration": "13m", "completed": True},
        {"title": "57. Métricas para Avaliação Multi Label", "duration": "4m", "completed": True},
        {"title": "58. Lab: Classificação Multi Label", "duration": "15m", "completed": True},
        {"title": "59. Dados Desbalanceados", "duration": "4m", "completed": True},
        {"title": "60. Lab: Dados Desbalanceados", "duration": "11m", "completed": True},
        {"title": "61. AutoML e Tunning de Modelos", "duration": "17m", "completed": True},
        {"title": "62. AutoML e Tunning de Modelos (Continuação)", "duration": "13m", "completed": True},
        {"title": "63. Lab: AutoML e Tunning", "duration": "24m", "completed": True},
        {"title": "64. Lab: AutoML e Tunning com H2O", "duration": "16m", "completed": True},
    ],
    "Seção 5: Redes Neurais, Deep Learning e Computer Vision": [
        {"title": "65. Introdução a Redes Neurais Artificiais", "duration": "4m", "completed": False},
        {"title": "66. Conhecendo o Perceptron", "duration": "7m", "completed": False},
        {"title": "67. Classificação com Perceptron", "duration": "14m", "completed": False},
        {"title": "68. Classificação com Perceptron (Continuação)", "duration": "12m", "completed": False},
        {"title": "69. Apresentação de Redes Neurais", "duration": "8m", "completed": False},
        {"title": "70. Deep Learning", "duration": "2m", "completed": False},
        {"title": "71. Compreendendo Hiper Parâmetros", "duration": "13m", "completed": False},
        {"title": "72. Lab: Implementando RNA", "duration": "14m", "completed": False},
        {"title": "73. Lab: RNA com Keras", "duration": "19m", "completed": False},
        {"title": "74. Lab: RNA com Keras (Continuação)", "duration": "9m", "completed": False},
        {"title": "75. Visão Computacional com CNN - Convolution", "duration": "14m", "completed": False},
        {"title": "76. Visão Computacional com CNN - Pooling", "duration": "6m", "completed": False},
        {"title": "77. Visão Computacional com CNN - Flattening", "duration": "2m", "completed": False},
        {"title": "78. Visão Computacional com CNN - Full Connected", "duration": "7m", "completed": False},
        {"title": "79. Dados Cifar10", "duration": "1m", "completed": False},
        {"title": "80. Lab: Convolution Neural Network (CNN)", "duration": "12m", "completed": False},
        {"title": "81. Lab: Convolution Neural Network (CNN) (Continuação)", "duration": "18m", "completed": False},
        {"title": "82. Lab: Convolution Neural Network (CNN) (Continuação II)", "duration": "6m", "completed": False},
        {"title": "83. Redes Neurais Recorrentes e LSTM (Long Short Term Memory)", "duration": "6m", "completed": False},
        {"title": "84. Conjunto de Dados Stock do Google", "duration": "4m", "completed": False},
        {"title": "85. Lab: Pré-processamento para LSTM", "duration": "15m", "completed": False},
        {"title": "86. Lab: Treinamento de LSTM", "duration": "11m", "completed": False},
        {"title": "87. Lab: Previsão e Comparação de Resultados de LSTM", "duration": "14m", "completed": False},
        {"title": "88. Introdução aos Autoencoders", "duration": "4m", "completed": False},
        {"title": "89. Sobre o Lab de Autoencoders", "duration": "2m", "completed": False},
        {"title": "90. Lab: Preprando o Autoencoder", "duration": "17m", "completed": False},
        {"title": "91. Lab: Criando o Modelo do Autoencoder", "duration": "11m", "completed": False},
        {"title": "92. Lab: Removendo o Ruído da Imagem", "duration": "10m", "completed": False},
        {"title": "93. Detecção de Objetos", "duration": "3m", "completed": False},
        {"title": "94. Lab: Detecção de Objetos com OpenCV", "duration": "19m", "completed": False},
        {"title": "95. Lab: Detecção de Objetos com OpenCV (Continuação)", "duration": "21m", "completed": False},
        {"title": "Role play 2: Redes Neurais, Deep Learning e Computer Vision", "duration": None, "completed": True},
    ],
    "Seção 6: Machine Learning Explicável": [
        {"title": "96. O que é Machine Learning Explicável (XAI)", "duration": "5m", "completed": True},
        {"title": "97. Por que um Modelo Precisa ser Explicado?", "duration": "6m", "completed": True},
        {"title": "98. Conceitos Fundamentais", "duration": "8m", "completed": True},
        {"title": "99. Exemplos de Modelos White-box e Black-box", "duration": "5m", "completed": True},
        {"title": "100. Lab: Preparando os Dados", "duration": "11m", "completed": True},
        {"title": "101. Lab: Lime e Eli5", "duration": "14m", "completed": True},
        {"title": "102. Lab: Shap e Interpret", "duration": "17m", "completed": True},
        {"title": "Role play 3: Machine Learning Explicável", "duration": None, "completed": True},
    ],
    "Seção 7: Processamento de Linguagem Natural (Natura Language Processing - NLP)": [
        {"title": "103. Introdução", "duration": "3m", "completed": False},
        {"title": "104. Aplicações", "duration": "5m", "completed": False},
        {"title": "105. Conceitos", "duration": "12m", "completed": False},
        {"title": "106. Lab: NLP na Prática", "duration": "12m", "completed": False},
        {"title": "107. Lab: NLP na Prática (Continuação)", "duration": "15m", "completed": False},
        {"title": "108. Lab: NLP na Prática (Continuação II)", "duration": "9m", "completed": False},
        {"title": "109. Word Embedding e Transformers", "duration": "10m", "completed": False},
        {"title": "110. Lab: Classificação com Keras", "duration": "19m", "completed": False},
        {"title": "111. Lab: Classificação com Keras (Continuação)", "duration": "18m", "completed": False},
        {"title": "Role play 4: Processamento de Linguagem Natural", "duration": None, "completed": True},
    ],
    "Seção 8: LLMs e Inteligência Artificial Generativa": [
        {"title": "112. LLMs: Grandes Modelos de Linguagem", "duration": "9m", "completed": True},
        {"title": "113. Hugging Face", "duration": "4m", "completed": True},
        {"title": "114. Lab: Geração de Texto com Modelos GPT", "duration": "7m", "completed": True},
        {"title": "115. Lab: Preenchimento de Máscara", "duration": "7m", "completed": True},
        {"title": "116. Lab: Resumo de Texto", "duration": "4m", "completed": True},
        {"title": "117. Modelos GPT com OpenAI", "duration": "7m", "completed": True},
        {"title": "118. Lab: GPT com Python", "duration": "15m", "completed": True},
        {"title": "119. Lab: Google Gemini", "duration": "7m", "completed": True},
        {"title": "120. Lab: DeepSeek", "duration": "15m", "completed": True},
        {"title": "121. DALL-E: Apresentação", "duration": "4m", "completed": True},
        {"title": "122. Lab: DALL-E", "duration": "15m", "completed": True},
        {"title": "123. Lab: Stable Diffusion", "duration": "14m", "completed": True},
        {"title": "124. Lab: Stable Diffusion (Continuação)", "duration": "10m", "completed": True},
        {"title": "125. Whisper: Apresentação", "duration": "3m", "completed": True},
        {"title": "126. Lab: Whisper", "duration": "7m", "completed": True},
    ],
    "Seção 9: Agentes de IA, RAGs e Langchain": [
        {"title": "127. Apresentação de Agentes de IA", "duration": "4m", "completed": True},
        {"title": "128. Tipos de Agentes de IA", "duration": "6m", "completed": True},
        {"title": "129. RAGs: Retrieval Augmented Generation", "duration": "4m", "completed": True},
        {"title": "130. Outros Conceitos de Agentes", "duration": "4m", "completed": True},
        {"title": "131. Lab: Agente com Pesquisa na Web", "duration": "18m", "completed": True},
        {"title": "132. Agente Especializado com RAG e Langchain", "duration": "2m", "completed": True},
        {"title": "133. Lab: Agente Especializado com RAG e Langchain", "duration": "18m", "completed": True},
        {"title": "134. Lab: Agente Especializado com RAG e Langchain (Continuação)", "duration": "15m", "completed": True},
        {"title": "Role play 5: Agentes de IA, RAGs e Langchain", "duration": None, "completed": True},
    ],
    "Seção 10: Detecção de Anomalias": [
        {"title": "135. Introdução a Detecção de Anomalias", "duration": "5m", "completed": False},
        {"title": "136. Técnicas Estatísticas", "duration": "5m", "completed": False},
        {"title": "137. Lab: Z-Score", "duration": "4m", "completed": False},
        {"title": "138. Lab: IQR", "duration": "6m", "completed": False},
        {"title": "139. Técnicas de Machine Learning", "duration": "3m", "completed": False},
        {"title": "140. Lab: Local Outlier Factor (LOF)", "duration": "8m", "completed": False},
        {"title": "141. Lab: Isolation Forest", "duration": "4m", "completed": False},
        {"title": "142. Técnicas de Deep Learning", "duration": "2m", "completed": False},
        {"title": "143. Lab: Autoencoders", "duration": "18m", "completed": False},
        {"title": "144. LSTM para Anomalias", "duration": "4m", "completed": False},
        {"title": "145. Lab: Treinando Modelo LSTM", "duration": "17m", "completed": False},
        {"title": "146. Lab: Buscando Anomalias com LSTM", "duration": "20m", "completed": True},  # Única concluída
        {"title": "147. Lab: Previsão de Avaliação com LSTM", "duration": "8m", "completed": False},
        {"title": "148. Técnicas de Séries Temporais", "duration": "4m", "completed": False},
        {"title": "149. Lab: Médias Móveis", "duration": "9m", "completed": False},
        {"title": "150. Lab: Exponential Smoothing", "duration": "9m", "completed": False},
        {"title": "151. Lab: Seasonal and Trend Decomposition (STD)", "duration": "15m", "completed": False},
        {"title": "152. Lab: Arima", "duration": "13m", "completed": False},
    ],
    "Seção 11: Algoritmos Genéticos": [
        {"title": "153. Introdução", "duration": "1m", "completed": True},
        {"title": "154. Evolução Biológica", "duration": "14m", "completed": True},
        {"title": "155. Introdução aos Algoritmos Genéticos", "duration": "9m", "completed": True},
        {"title": "156. Como Algoritmos Genéticos Funcionam", "duration": "7m", "completed": True},
        {"title": "157. Como Algoritmos Genéticos Funcionam (Continuação)", "duration": "7m", "completed": True},
        {"title": "158. Como Algoritmos Genéticos Funcionam (Continuação II)", "duration": "10m", "completed": True},
        {"title": "159. Demonstração de Exemplo", "duration": "8m", "completed": True},
        {"title": "160. Exemplo com Valor Real", "duration": "9m", "completed": True},
        {"title": "161. Lab: Criando Função Fitness", "duration": "9m", "completed": True},
        {"title": "162. Lab: Implementando Algoritmos Genéticos para Valor Real", "duration": "11m", "completed": True},
        {"title": "163. Exemplo de Problema Binário", "duration": "3m", "completed": True},
        {"title": "164. Lab: Implementando Problema Binário", "duration": "14m", "completed": True},
        {"title": "Teste 2: Algoritmos Genéticos", "duration": None, "completed": True},
    ],
    "Seção 12: Algoritmos de Busca e Otimização": [
        {"title": "165. Introdução a Busca e Otimização", "duration": "11m", "completed": False},
        {"title": "166. Introdução a Busca e Otimização (Continuação)", "duration": "12m", "completed": False},
        {"title": "167. Hill Climbing", "duration": "5m", "completed": False},
        {"title": "168. Força Bruta com BFS e DFS", "duration": "7m", "completed": False},
        {"title": "169. Caminhos", "duration": "10m", "completed": False},
        {"title": "170. Tabu Search e Simulated Annealing", "duration": "4m", "completed": False},
        {"title": "171. Problema de Simulated Annealing", "duration": "2m", "completed": False},
        {"title": "172. Lab: Implementando Simulated Annealing", "duration": "10m", "completed": False},
        {"title": "Teste 3: Busca e Otimização", "duration": None, "completed": False},
    ],
    "Seção 13: Lógica Difusa": [
        {"title": "173. Introdução a Lógica Difusa", "duration": "10m", "completed": False},
        {"title": "174. Introdução a Lógica Difusa (Continuação)", "duration": "11m", "completed": False},
        {"title": "175. Problema Prático", "duration": "7m", "completed": False},
        {"title": "176. Lab: Criando Modelo", "duration": "20m", "completed": False},
        {"title": "177. Lab: Criando Regras e Inferindo", "duration": "12m", "completed": False},
        {"title": "Teste 4: Lógica Difusa", "duration": None, "completed": False},
    ],
    "Seção 14: Projeto Final": [
        {"title": "178. Desafio Final", "duration": "7m", "completed": False},
    ],
    "Seção 15: Opcional I: Fundamentos de Python": [
        {"title": "179. Variáveis e Objetos", "duration": "13m", "completed": True},
        {"title": "180. Estruturas de Decisão", "duration": "17m", "completed": True},
        {"title": "181. Estruturas de Repetição", "duration": "7m", "completed": True},
        {"title": "182. Introdução ao Python", "duration": "4m", "completed": True},
        {"title": "183. Listas", "duration": "3m", "completed": True},
        {"title": "184. Dicionários, Sets e Tuplas", "duration": "4m", "completed": True},
        {"title": "185. Numpy", "duration": "3m", "completed": True},
        {"title": "186. Pandas", "duration": "2m", "completed": True},
        {"title": "187. Módulos e Pacotes", "duration": "6m", "completed": True},
        {"title": "188. Funções", "duration": "5m", "completed": True},
        {"title": "189. Funções Padrão", "duration": "3m", "completed": True},
        {"title": "190. Referências Adicionais", "duration": "2m", "completed": True},
    ],
    "Seção 16: Opcional II: Lab: Fundamentos de Python": [
        {"title": "191. Variáveis e Objetos", "duration": "9m", "completed": True},
        {"title": "192. Estruturas de Decisão", "duration": "6m", "completed": True},
        {"title": "193. Estruturas de Repetição", "duration": "8m", "completed": True},
        {"title": "194. Listas", "duration": "9m", "completed": True},
        {"title": "195. Dicionários, Sets e Tuplas", "duration": "12m", "completed": True},
        {"title": "196. Numpy", "duration": "28m", "completed": True},
        {"title": "197. Pandas", "duration": "21m", "completed": True},
        {"title": "198. Módulos e Pacotes", "duration": "6m", "completed": True},
        {"title": "199. Funções", "duration": "5m", "completed": True},
        {"title": "200. Funções Padrão", "duration": "4m", "completed": True},
        {"title": "201. Faça Você Mesmo!", "duration": "3m", "completed": True},
    ],
    "Seção 17: Aula Bônus": [
        {"title": "202. Aula Bônus", "duration": "1m", "completed": True},
    ],
}

def main():
    print("🚀 Criando TODAS as aulas da Formação Udemy IA/ML...\n")
    
    total_criadas = 0
    total_concluidas = 0
    total_para_fazer = 0
    
    for sessao_titulo, aulas in SESSOES.items():
        print(f"\n📚 Buscando sessão: {sessao_titulo}")
        
        # Buscar a sessão - tentar busca parcial
        session_id = find_session_by_title(sessao_titulo.split(":")[0])  # Busca apenas "Seção X"
        
        if not session_id:
            print(f"   ⚠️  Sessão não encontrada: {sessao_titulo}")
            continue
        
        print(f"   ✅ Sessão encontrada! Criando {len(aulas)} aulas...")
        
        # Criar cada aula como sub-item
        for idx, aula_data in enumerate(aulas, 1):
            aula_titulo = aula_data["title"]
            duracao = aula_data.get("duration")
            completed = aula_data["completed"]
            
            status = "Concluido" if completed else "Para Fazer"
            
            aula_props = {
                "Project name": {"title": [{"text": {"content": aula_titulo}}]},
                "Status": {"status": {"name": status}},
                "Prioridade": {"select": {"name": "Média"}},
                "Categorias": {"multi_select": [{"name": "IA"}, {"name": "Formação"}]},
            }
            
            if duracao:
                aula_props["Tempo Total"] = {"rich_text": [{"text": {"content": duracao}}]}
            
            aula = create_page(ESTUDOS_DB, aula_props, parent_id=session_id, icon={"type": "emoji", "emoji": "📝"})
            
            if aula:
                print(f"      ✅ {idx}/{len(aulas)}: {aula_titulo} - {status}")
                total_criadas += 1
                if completed:
                    total_concluidas += 1
                else:
                    total_para_fazer += 1
            else:
                print(f"      ❌ {idx}/{len(aulas)}: {aula_titulo}")
    
    print(f"\n\n{'='*60}")
    print(f"✅ CONCLUÍDO!")
    print(f"📊 Total de aulas criadas: {total_criadas}")
    print(f"✅ Concluídas: {total_concluidas}")
    print(f"📝 Para Fazer: {total_para_fazer}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()

