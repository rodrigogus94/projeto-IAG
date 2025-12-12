"""
Configurações centralizadas para o modelo de linguagem - OLLAMA
Este arquivo contém todas as regras, parâmetros e instruções importantes para o modelo Ollama

NOTA: Este arquivo é específico para modelos rodando via Ollama.
Os parâmetros e formatos são compatíveis com a API do Ollama.
Para usar com outros provedores (OpenAI, Anthropic, etc.), ajuste os parâmetros conforme necessário.
"""

# ============================================================================
# SYSTEM PROMPT - Persona e Instruções do Assistente
# ============================================================================

SYSTEM_PROMPT = """Você é Omnilink AI - assistente de análise de frotas em um SISTEMA WEB QUE JÁ GERA GRÁFICOS AUTOMATICAMENTE.

🚨 ATENÇÃO - REGRAS ABSOLUTAS E INEGOCIÁVEIS 🚨

JAMAIS, EM HIPÓTESE ALGUMA:
❌ Diga "não consigo gerar visualizações"
❌ Diga "não posso criar gráficos diretamente"
❌ Forneça código Python, Matplotlib, Plotly, Pandas
❌ Mencione bibliotecas de programação
❌ Dê instruções de "como fazer" com código
❌ Sugira usar Excel, ferramentas externas
❌ Use blocos de código (```)

O SISTEMA JÁ FAZ ISSO AUTOMATICAMENTE. SEU PAPEL É APENAS ANALISAR.

QUANDO PEDIREM GRÁFICOS:
✅ Analise os dados imediatamente
✅ Apresente números e insights em texto
✅ Confie que o sistema gerará o gráfico sozinho
✅ Diga algo como: "Analisando os dados da frota: [insights]"

📊 INTELIGÊNCIA EM ANÁLISE DE DADOS:

Você receberá um contexto completo e detalhado dos dados disponíveis, incluindo:
- Estatísticas descritivas (médias, medianas, desvios padrão)
- Distribuições de valores categóricos
- Correlações entre variáveis
- Insights pré-calculados
- Padrões e anomalias identificadas

COMO ANALISAR OS DADOS INTELIGENTEMENTE:
1. Use SEMPRE os dados fornecidos no contexto - não invente números
2. Compare valores com médias e medianas para identificar outliers
3. Use percentuais e proporções para facilitar compreensão
4. Identifique padrões e tendências nos dados
5. Faça conexões entre diferentes variáveis (ex: consumo vs quilometragem)
6. Destaque anomalias e valores atípicos quando relevantes
7. Forneça insights acionáveis baseados nos dados reais
8. Seja específico: use números exatos, não aproximações vagas

DADOS DISPONÍVEIS (já carregados):
- Base: dados_veiculos_300.csv com 300 registros
- Colunas: id_veiculo, marca, modelo, ano, status, cidade, km_mes, velocidade_media, alertas, consumo_combustivel, dias_operacionais, custo_manutencao
- Você receberá estatísticas detalhadas no contexto de cada mensagem

EXEMPLO DE RESPOSTA CORRETA:

Usuário: "gere um gráfico de pizza dos veículos por status"

✅ CORRETO:
"📊 **Análise da Frota por Status**

Distribuição dos 300 veículos:
- **Ativos**: 217 veículos (72.3%) - Maior parte operacional
- **Inativos**: 61 veículos (20.3%) - Fora de operação
- **Em manutenção**: 22 veículos (7.3%) - Em reparo

A frota tem boa taxa de disponibilidade, com menos de 8% em manutenção."

❌ ERRADO:
"Não consigo gerar gráficos. Use este código Python..."

LEMBRE-SE: O gráfico já aparece automaticamente na tela. Você só precisa COMENTAR os dados.
"""
# ============================================================================
# PARÂMETROS PADRÃO DO MODELO
# ============================================================================

# Temperatura padrão (0.0 = determinístico, 2.0 = muito criativo)
DEFAULT_TEMPERATURE = 0.7

# Modelo padrão (será substituído pelo primeiro disponível se não existir)
DEFAULT_MODEL = "llama2:latest"

# Limites de temperatura
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0

# Outros parâmetros do Ollama (opcionais)
# Documentação: https://github.com/ollama/ollama/blob/main/docs/modelfile.md#parameter
DEFAULT_TOP_P = 0.9  # Nucleus sampling (0.0-1.0) - controla diversidade
DEFAULT_TOP_K = 40  # Top-k sampling - número de tokens mais prováveis a considerar
DEFAULT_NUM_PREDICT = -1  # -1 = sem limite, ou número máximo de tokens a gerar
DEFAULT_REPEAT_PENALTY = 1.1  # Penalidade por repetição (1.0 = sem penalidade)
DEFAULT_SEED = -1  # Seed para reprodutibilidade (-1 = aleatório)

# ============================================================================
# REGRAS E RESTRIÇÕES
# ============================================================================

MODEL_RULES = {
    "max_context_length": 4096,  # Máximo de tokens no contexto (ajustar conforme modelo)
    "max_response_length": 2048,  # Máximo de tokens na resposta
    "enable_streaming": False,  # Streaming de respostas (será implementado)
    "timeout_seconds": 120,  # Timeout padrão para requisições (em segundos)
    # Pode ser sobrescrito por OLLAMA_TIMEOUT no .env
    # Para chat, o timeout é automaticamente dobrado (240s)
}

# ============================================================================
# CONFIGURAÇÕES DE COMPORTAMENTO
# ============================================================================

BEHAVIOR_CONFIG = {
    # Idioma padrão
    "default_language": "pt-BR",
    # Formato de resposta preferido
    "preferred_format": "markdown",
    # Nível de detalhamento
    "detail_level": "balanced",  # "brief", "balanced", "detailed"
    # Incluir exemplos nas respostas
    "include_examples": True,
    # Sugerir melhorias automaticamente
    "suggest_improvements": True,
    # Admitir quando não sabe algo
    "admit_uncertainty": True,
}

# ============================================================================
# PROMPTS ESPECÍFICOS POR CONTEXTO
# ============================================================================

CONTEXT_PROMPTS = {
    "fleet_data": """📊 ANÁLISE INTELIGENTE DE DADOS DA FROTA:

Você receberá um contexto completo com:
- Estatísticas detalhadas de todas as variáveis numéricas
- Distribuições completas de variáveis categóricas
- Correlações entre variáveis
- Insights pré-calculados e padrões identificados

REGRAS DE ANÁLISE INTELIGENTE:
1. Use SEMPRE os dados fornecidos no contexto - nunca invente números
2. Compare valores individuais com médias/medianas para identificar padrões
3. Use percentuais e proporções para facilitar compreensão
4. Identifique outliers e valores atípicos quando relevantes
5. Faça conexões entre variáveis (ex: "veículos com maior km_mes tendem a ter maior consumo")
6. Destaque tendências e padrões nos dados
7. Forneça insights acionáveis baseados em evidências dos dados
8. Seja específico: use números exatos do contexto fornecido
9. Se não tiver a informação exata, diga claramente e sugira como obter

EXEMPLO DE ANÁLISE INTELIGENTE:
❌ "Alguns veículos têm alto consumo"
✅ "15 veículos (5%) têm consumo acima de 12 L/100km, sendo 3x maior que a média de 8.5 L/100km. Estes veículos estão principalmente em São Paulo e têm mais de 50.000 km/mês."

❌ "A maioria dos veículos está ativa"
✅ "217 veículos (72.3%) estão ativos, 22 (7.3%) em manutenção e 61 (20.3%) inativos. A taxa de disponibilidade de 72.3% está abaixo do ideal de 85%+ para frotas eficientes."
""",
    
    "dashboard": """📈 CRIAÇÃO INTELIGENTE DE DASHBOARDS:

Quando o usuário pedir visualizações:
1. Analise o contexto completo dos dados fornecido
2. Identifique as métricas mais relevantes baseado nos dados reais
3. Sugira gráficos apropriados baseado nas distribuições observadas:
   - Barras: para comparações entre categorias
   - Pizza: para proporções e distribuições percentuais
   - Linha: para tendências temporais (se houver dados de tempo)
   - Scatter: para relações entre variáveis numéricas
4. Destaque KPIs críticos identificados nos dados:
   - Consumo médio e veículos com consumo anormal
   - Custos totais e por categoria
   - Alertas críticos e veículos problemáticos
   - Taxa de disponibilidade da frota
5. Use os dados reais para sugerir filtros úteis (cidade, marca, status)
6. Identifique padrões nos dados que merecem destaque visual

Lembre-se: O sistema gera o gráfico automaticamente. Você só precisa analisar e comentar os dados.""",

    "data_analysis": """🔍 ANÁLISE ESTATÍSTICA INTELIGENTE:

Quando analisando dados:
1. Use todas as estatísticas fornecidas no contexto (média, mediana, desvio padrão)
2. Calcule proporções e percentuais baseados nos dados reais
3. Identifique correlações fortes mencionadas no contexto
4. Compare grupos usando as distribuições fornecidas
5. Identifique outliers usando quartis e desvios padrão
6. Forneça interpretações práticas dos números
7. Sugira ações baseadas nos insights encontrados
8. Seja preciso: use os números exatos do contexto, não aproximações
""",

}

# ============================================================================
# MENSAGENS DO SISTEMA
# ============================================================================

SYSTEM_MESSAGES = {
    "welcome": "Olá! 👋 Sou seu assistente de dashboards. Peça visualizações de dados e eu gero para você em tempo real!",
    "thinking": "💭 Pensando...",
    "error": "❌ Ocorreu um erro. Por favor, tente novamente.",
    "no_response": "Não foi possível gerar uma resposta. Verifique sua conexão com o Ollama.",
    "model_not_found": "Modelo não encontrado. Verifique se o modelo está instalado no Ollama.",
}

# ============================================================================
# VALIDAÇÕES E LIMITES
# ============================================================================

VALIDATION_RULES = {
    "temperature_range": (MIN_TEMPERATURE, MAX_TEMPERATURE),
    "min_message_length": 1,
    "max_message_length": 10000,
    "allowed_languages": ["pt-BR", "en-US", "es-ES"],
}

# ============================================================================
# CONFIGURAÇÕES AVANÇADAS
# ============================================================================

ADVANCED_CONFIG = {
    # Retry em caso de falha
    "max_retries": 3,
    "retry_delay": 1.0,  # segundos
    # Cache de respostas (futuro)
    "enable_cache": False,
    "cache_ttl": 3600,  # segundos
    # Logging
    "log_requests": True,
    "log_responses": False,  # Pode conter dados sensíveis
    # Performance
    "enable_streaming": False,  # Será implementado
    "stream_chunk_size": 50,  # Tokens por chunk no streaming
}

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================


def get_system_prompt(context: str = "general") -> str:
    """
    Retorna o system prompt completo com contexto específico.

    Args:
        context: Contexto da conversa ("dashboard", "data_analysis", "error_help", "general")

    Returns:
        System prompt completo
    """
    base_prompt = SYSTEM_PROMPT

    if context in CONTEXT_PROMPTS:
        context_instructions = CONTEXT_PROMPTS[context]
        return f"{base_prompt}\n\nCONTEXTO ATUAL:\n{context_instructions}"

    return base_prompt


def validate_temperature(temperature: float) -> float:
    """
    Valida e ajusta a temperatura para o range permitido.

    Args:
        temperature: Temperatura a validar

    Returns:
        Temperatura validada
    """
    min_temp, max_temp = VALIDATION_RULES["temperature_range"]
    return max(min_temp, min(max_temp, temperature))


def get_model_parameters(temperature: float = None, **kwargs) -> dict:
    """
    Retorna dicionário com parâmetros do modelo Ollama.

    Parâmetros suportados pelo Ollama:
    - temperature: Controla aleatoriedade (0.0-2.0)
    - top_p: Nucleus sampling (0.0-1.0)
    - top_k: Top-k sampling (número inteiro)
    - num_predict: Máximo de tokens a gerar (-1 = ilimitado)
    - repeat_penalty: Penalidade por repetição (1.0+)
    - seed: Seed para reprodutibilidade (-1 = aleatório)

    Args:
        temperature: Temperatura (usa padrão se None)
        **kwargs: Parâmetros adicionais do Ollama

    Returns:
        Dicionário com parâmetros no formato esperado pelo Ollama
    """
    params = {
        "temperature": validate_temperature(temperature or DEFAULT_TEMPERATURE),
    }

    # Adicionar parâmetros opcionais se fornecidos
    if "top_p" in kwargs:
        params["top_p"] = kwargs["top_p"]
    elif "use_defaults" not in kwargs or kwargs.get("use_defaults"):
        params["top_p"] = DEFAULT_TOP_P

    if "top_k" in kwargs:
        params["top_k"] = kwargs["top_k"]
    elif "use_defaults" not in kwargs or kwargs.get("use_defaults"):
        params["top_k"] = DEFAULT_TOP_K

    if "num_predict" in kwargs:
        params["num_predict"] = kwargs["num_predict"]
    elif "use_defaults" not in kwargs or kwargs.get("use_defaults"):
        params["num_predict"] = DEFAULT_NUM_PREDICT

    if "repeat_penalty" in kwargs:
        params["repeat_penalty"] = kwargs["repeat_penalty"]

    if "seed" in kwargs:
        params["seed"] = kwargs["seed"]

    return params


def get_behavior_settings() -> dict:
    """
    Retorna configurações de comportamento do modelo.

    Returns:
        Dicionário com configurações
    """
    return BEHAVIOR_CONFIG.copy()


def get_validation_rules() -> dict:
    """
    Retorna regras de validação.

    Returns:
        Dicionário com regras
    """
    return VALIDATION_RULES.copy()

