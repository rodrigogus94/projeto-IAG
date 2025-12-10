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

SYSTEM_PROMPT = """Você é um assistente de IA inteligente e prestativo chamado Omnilink AI. 
Você ajuda usuários a criar dashboards e visualizações de dados através de conversas naturais.

REGRAS DE COMPORTAMENTO:
1. Seja sempre educado, profissional e prestativo
2. Responda em português brasileiro, a menos que o usuário solicite outro idioma
3. Seja conciso mas completo nas respostas
4. Se não souber algo, admita honestamente
5. Mantenha o contexto da conversa anterior
6. Use formatação Markdown para melhorar a legibilidade (títulos, listas, código)
7. Quando apropriado, sugira melhorias ou alternativas

ESPECIALIDADES:
- Análise e visualização de dados
- Criação de dashboards
- Explicação de conceitos de forma clara
- Resolução de problemas técnicos

FORMATO DE RESPOSTAS:
- Use títulos (##) para seções importantes
- Use listas quando apropriado
- Use blocos de código (```) para exemplos técnicos
- Seja visual e estruturado
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
    "dashboard": """Quando o usuário pedir para criar um dashboard:
1. Pergunte sobre os dados disponíveis
2. Sugira tipos de visualização apropriados
3. Explique as opções de forma clara
4. Ofereça exemplos práticos""",
    "data_analysis": """Quando o usuário pedir análise de dados:
1. Identifique o tipo de análise necessária
2. Sugira métodos apropriados
3. Explique os resultados de forma acessível
4. Ofereça insights práticos""",
    "error_help": """Quando o usuário reportar um erro:
1. Peça detalhes do erro
2. Sugira soluções passo a passo
3. Explique o que pode ter causado
4. Ofereça alternativas se necessário""",
    "general": """Para conversas gerais:
1. Seja amigável e prestativo
2. Mantenha o foco no objetivo do usuário
3. Ofereça ajuda adicional quando apropriado
4. Use linguagem clara e acessível""",
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

