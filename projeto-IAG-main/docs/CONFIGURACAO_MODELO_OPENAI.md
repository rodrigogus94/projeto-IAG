# 🎯 Configuração de Modelo Especialista OpenAI

## 📋 Visão Geral

O arquivo `openai_model_config.py` contém todas as configurações para criar um modelo especialista usando a API da OpenAI. Este arquivo permite personalizar o comportamento, prompts e parâmetros do modelo para diferentes contextos.

## 🎓 O que é um Modelo Especialista?

Um modelo especialista é configurado com:
- **System prompts detalhados** com regras específicas
- **Contextos especializados** para diferentes tipos de tarefas
- **Parâmetros otimizados** para cada modelo OpenAI
- **Comportamento proativo** e insights valiosos

## 📁 Estrutura do Arquivo

### 1. System Prompt Base
Define a persona e regras gerais do assistente especialista.

### 2. Parâmetros Padrão
- Temperatura, max_tokens, top_p, etc.
- Configurações específicas por modelo

### 3. Contextos Especializados
- `dashboard`: Especialista em dashboards
- `data_analysis`: Especialista em análise de dados
- `error_help`: Especialista em resolução de problemas
- `code_generation`: Especialista em código
- `general`: Conversas gerais

### 4. Configurações de Comportamento
- Nível de detalhamento
- Inclusão de exemplos
- Proatividade
- Explicação de raciocínio

## 🔧 Como Personalizar

### Personalizar System Prompt

Edite `SYSTEM_PROMPT` em `openai_model_config.py`:

```python
SYSTEM_PROMPT = """Você é um assistente especializado em [SUA ÁREA].
[SUAS REGRAS ESPECÍFICAS]
[SUAS ESPECIALIDADES]
"""
```

### Adicionar Novo Contexto

Adicione em `CONTEXT_PROMPTS`:

```python
CONTEXT_PROMPTS = {
    "seu_contexto": """Instruções específicas para este contexto:
1. Regra 1
2. Regra 2
3. Regra 3
""",
}
```

### Ajustar Parâmetros por Modelo

Edite `MODEL_SPECIFIC_CONFIG`:

```python
MODEL_SPECIFIC_CONFIG = {
    "gpt-4o": {
        "max_tokens": 4096,
        "recommended_temperature": 0.7,
        "context_length": 128000,
        "best_for": ["sua tarefa específica"],
    },
}
```

### Modificar Comportamento

Edite `BEHAVIOR_CONFIG`:

```python
BEHAVIOR_CONFIG = {
    "detail_level": "detailed",  # "brief", "balanced", "detailed"
    "include_examples": True,
    "be_proactive": True,
    # ... outras configurações
}
```

## 🎯 Contextos Disponíveis

### 1. Dashboard (`dashboard`)
**Especialista em criação de dashboards**

- Faz perguntas estratégicas sobre dados
- Sugere visualizações baseadas em best practices
- Fornece código funcional
- Considera interatividade e acessibilidade

**Uso**: Quando o usuário pedir dashboards ou visualizações

### 2. Análise de Dados (`data_analysis`)
**Especialista em análise estatística**

- Identifica tipo de análise necessária
- Sugere métodos estatísticos apropriados
- Explica resultados de forma técnica mas acessível
- Fornece código para análise

**Uso**: Quando o usuário pedir análise de dados

### 3. Resolução de Erros (`error_help`)
**Especialista em troubleshooting**

- Analisa erros sistematicamente
- Sugere soluções passo a passo
- Explica causa raiz
- Previne problemas futuros

**Uso**: Quando o usuário reportar erros

### 4. Geração de Código (`code_generation`)
**Especialista em programação**

- Escreve código limpo e documentado
- Inclui tratamento de erros
- Considera performance e segurança
- Fornece testes quando apropriado

**Uso**: Quando o usuário pedir código

### 5. Geral (`general`)
**Conversas gerais especializadas**

- Amigável e profissional
- Proativo
- Fornece contexto e explicações
- Antecipa necessidades

**Uso**: Para conversas gerais

## ⚙️ Parâmetros Importantes

### Temperature
- **0.0-0.3**: Determinístico (ideal para código, análise)
- **0.4-0.7**: Balanceado (padrão, ideal para maioria das tarefas)
- **0.8-2.0**: Criativo (ideal para escrita criativa)

### Max Tokens
- **500-1000**: Respostas curtas
- **1000-2000**: Respostas médias (padrão)
- **2000-4000**: Respostas longas e detalhadas

### Top P
- **0.1-0.5**: Mais focado
- **0.5-0.9**: Balanceado (padrão: 1.0)
- **0.9-1.0**: Mais diverso

## 📊 Configurações por Modelo

### GPT-4o
- **Contexto**: 128k tokens
- **Melhor para**: Análise complexa, código, raciocínio
- **Temperatura recomendada**: 0.7

### GPT-4o-mini
- **Contexto**: 128k tokens
- **Melhor para**: Análise rápida, respostas curtas
- **Temperatura recomendada**: 0.7

### GPT-3.5-turbo
- **Contexto**: 16k tokens
- **Melhor para**: Respostas rápidas, tarefas gerais
- **Temperatura recomendada**: 0.7

## 🔄 Como Usar no Código

### Usar Configuração Especializada

```python
from src.config.openai_model_config import (
    get_system_prompt,
    get_model_parameters,
    get_recommended_temperature,
)

# Obter prompt para contexto específico
system_prompt = get_system_prompt(context="dashboard")

# Obter parâmetros otimizados
params = get_model_parameters(
    temperature=0.7,
    model="gpt-4o",
    max_tokens=2000
)

# Obter temperatura recomendada
temp = get_recommended_temperature("gpt-4o", task_type="analytical")
```

## 🎨 Exemplos de Personalização

### Exemplo 1: Especialista em Marketing

```python
SYSTEM_PROMPT = """Você é um especialista em marketing digital e análise de campanhas.
Você ajuda a criar estratégias, analisar métricas e otimizar campanhas.
[regras específicas de marketing]
"""
```

### Exemplo 2: Especialista em Finanças

```python
SYSTEM_PROMPT = """Você é um analista financeiro especializado.
Você ajuda com análise de investimentos, relatórios financeiros e planejamento.
[regras específicas de finanças]
"""
```

### Exemplo 3: Especialista em Saúde

```python
SYSTEM_PROMPT = """Você é um assistente especializado em saúde e bem-estar.
Você fornece informações educacionais e sugestões baseadas em evidências.
[regras específicas de saúde]
"""
```

## 📝 Boas Práticas

1. **Seja Específico**: Defina claramente a especialidade
2. **Forneça Contexto**: Inclua exemplos e casos de uso
3. **Defina Regras**: Estabeleça limites e diretrizes claras
4. **Teste e Ajuste**: Experimente diferentes configurações
5. **Documente**: Mantenha notas sobre o que funciona melhor

## 🔍 Validação

O arquivo inclui validações automáticas:
- Range de temperatura (0.0-2.0)
- Range de max_tokens (1-4096)
- Range de top_p (0.0-1.0)
- Range de penalties (-2.0 a 2.0)

## 🚀 Próximos Passos

1. **Personalize o System Prompt** para sua área
2. **Adicione contextos específicos** se necessário
3. **Ajuste parâmetros** baseado em testes
4. **Monitore resultados** e refine

## 📚 Referências

- [Documentação OpenAI](https://platform.openai.com/docs)
- [Guia de Prompts](https://platform.openai.com/docs/guides/prompt-engineering)
- [Parâmetros da API](https://platform.openai.com/docs/api-reference/chat/create)

---

**Criado para o Projeto IAG - Chat Assistente com IA**

