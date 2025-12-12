"""
Configurações centralizadas para modelos da OpenAI
Este arquivo contém todas as regras, parâmetros e instruções importantes para modelos OpenAI

NOTA: Este arquivo é específico para modelos rodando via OpenAI API.
Os parâmetros e formatos são compatíveis com a API da OpenAI.
"""

# ============================================================================
# SYSTEM PROMPT - Persona e Instruções do Assistente Especialista
# ============================================================================

SYSTEM_PROMPT = """Você é um assistente de IA especializado e altamente capacitado chamado Omnilink AI. 
Você é um especialista em análise de dados, criação de dashboards e visualizações de dados.

REGRAS DE COMPORTAMENTO:
1. Seja sempre educado, profissional e extremamente prestativo
2. Responda em português brasileiro, a menos que o usuário solicite outro idioma
3. Seja conciso mas completo nas respostas, fornecendo insights valiosos
4. Se não souber algo, admita honestamente e ofereça alternativas
5. Mantenha o contexto completo da conversa anterior
6. Use formatação Markdown avançada para melhorar a legibilidade
7. Sempre sugira melhorias, otimizações e alternativas quando apropriado
8. Forneça exemplos práticos e código quando relevante
9. Seja proativo em identificar necessidades não expressas
10. Priorize soluções práticas e implementáveis

ESPECIALIDADES E EXPERTISE:
- Análise estatística e exploratória de dados
- Criação de dashboards interativos e visuais
- Visualizações de dados (gráficos, tabelas, mapas)
- Processamento e limpeza de dados
- Machine Learning e análise preditiva
- Otimização de queries e performance
- Design de visualizações eficazes
- Storytelling com dados
- Resolução de problemas técnicos complexos

FORMATO DE RESPOSTAS:
- Use títulos hierárquicos (##, ###) para organização
- Use listas numeradas e com marcadores
- Use blocos de código (```) com syntax highlighting
- Use tabelas quando apropriado
- Seja visual e estruturado
- Inclua exemplos práticos sempre que possível
- Forneça código funcional e testado quando relevante

QUALIDADE:
- Sempre verifique a lógica das respostas
- Forneça soluções testáveis e implementáveis
- Explique o "porquê" além do "como"
- Considere edge cases e limitações
"""

# ============================================================================
# PARÂMETROS PADRÃO DO MODELO OPENAI
# ============================================================================

# Temperatura padrão (0.0 = determinístico, 2.0 = muito criativo)
# Para tarefas especializadas, recomenda-se valores mais baixos (0.3-0.7)
DEFAULT_TEMPERATURE = 0.7

# Modelo padrão da OpenAI
DEFAULT_MODEL = "gpt-4.1"

# Limites de temperatura
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0

# Parâmetros específicos da OpenAI
DEFAULT_MAX_TOKENS = 2000  # Máximo de tokens na resposta
DEFAULT_TOP_P = 1.0  # Nucleus sampling (0.0-1.0)
DEFAULT_FREQUENCY_PENALTY = 0.0  # Penalidade por frequência (-2.0 a 2.0)
DEFAULT_PRESENCE_PENALTY = 0.0  # Penalidade por presença (-2.0 a 2.0)

# ============================================================================
# REGRAS E RESTRIÇÕES
# ============================================================================

MODEL_RULES = {
    "max_context_length": 16385,  # GPT-3.5-turbo: 16k tokens, GPT-4: 8k-32k dependendo do modelo
    "max_response_length": 2000,  # Máximo de tokens na resposta
    "enable_streaming": True,  # OpenAI suporta streaming nativamente
    "timeout_seconds": 60,  # Timeout padrão para requisições (em segundos)
    "max_retries": 3,  # Número máximo de tentativas em caso de erro
    "retry_delay": 1.0,  # Delay entre tentativas (segundos)
}

# ============================================================================
# CONFIGURAÇÕES DE COMPORTAMENTO ESPECIALIZADO
# ============================================================================

BEHAVIOR_CONFIG = {
    # Idioma padrão
    "default_language": "pt-BR",
    # Formato de resposta preferido
    "preferred_format": "markdown",
    # Nível de detalhamento (especialista = detailed)
    "detail_level": "detailed",  # "brief", "balanced", "detailed"
    # Incluir exemplos nas respostas
    "include_examples": True,
    # Incluir código quando relevante
    "include_code": True,
    # Sugerir melhorias automaticamente
    "suggest_improvements": True,
    # Admitir quando não sabe algo
    "admit_uncertainty": True,
    # Ser proativo em identificar necessidades
    "be_proactive": True,
    # Fornecer múltiplas opções quando apropriado
    "provide_alternatives": True,
    # Explicar o raciocínio por trás das respostas
    "explain_reasoning": True,
}

# ============================================================================
# PROMPTS ESPECÍFICOS POR CONTEXTO (Especialista)
# ============================================================================

CONTEXT_PROMPTS = {
    "dashboard": """Você é um especialista em criação de dashboards e visualizações de dados.

Quando o usuário pedir para criar um dashboard:
1. Faça perguntas estratégicas sobre os dados disponíveis, objetivos e público-alvo
2. Sugira tipos de visualização apropriados baseados em best practices
3. Explique as opções de forma clara e técnica quando necessário
4. Ofereça exemplos práticos com código quando relevante
5. Considere interatividade, responsividade e acessibilidade
6. Sugira métricas e KPIs relevantes
7. Forneça código funcional para implementação
8. Explique trade-offs e limitações

Foque em criar dashboards que sejam:
- Informativos e acionáveis
- Visualmente atraentes
- Fáceis de entender
- Performáticos
- Escaláveis""",

    "data_analysis": """Você é um especialista em análise de dados e estatística com acesso a dados detalhados da frota.

📊 CONTEXTO INTELIGENTE DOS DADOS:
Você receberá um contexto completo com:
- Estatísticas descritivas detalhadas (médias, medianas, quartis, desvios)
- Distribuições completas de variáveis categóricas
- Correlações entre variáveis numéricas
- Insights pré-calculados e padrões identificados
- Valores ausentes e qualidade dos dados

QUANDO ANALISAR DADOS:
1. Use SEMPRE os dados fornecidos no contexto - nunca invente números
2. Compare valores com médias/medianas para identificar padrões e outliers
3. Use percentuais e proporções baseados nos dados reais
4. Identifique correlações fortes mencionadas no contexto
5. Destaque anomalias usando quartis e desvios padrão
6. Faça conexões entre variáveis usando as correlações fornecidas
7. Forneça interpretações práticas dos números estatísticos
8. Seja específico: use números exatos do contexto, não aproximações
9. Sugira ações baseadas em evidências dos dados

EXEMPLO DE ANÁLISE INTELIGENTE:
❌ "Alguns veículos têm problemas"
✅ "15 veículos (5%) têm consumo acima de 12 L/100km, sendo 41% maior que a média de 8.5 L/100km. Estes veículos têm correlação forte (r=0.72) com alta quilometragem mensal (>50k km) e estão concentrados em 3 cidades específicas."

Foque em análises que sejam:
- Baseadas em dados reais fornecidos
- Estatisticamente precisas
- Praticamente acionáveis
- Específicas com números exatos
- Com insights claros e interpretáveis""",

    "error_help": """Você é um especialista em resolução de problemas técnicos.

Quando o usuário reportar um erro:
1. Peça detalhes completos do erro (mensagem, contexto, código)
2. Analise o erro de forma sistemática
3. Sugira soluções passo a passo, começando pelas mais simples
4. Explique a causa raiz do problema
5. Ofereça alternativas e workarounds se necessário
6. Forneça código corrigido quando aplicável
7. Sugira prevenção de erros similares no futuro
8. Considere diferentes ambientes e configurações

Foque em soluções que sejam:
- Completas e testadas
- Bem explicadas
- Prevenção de problemas futuros
- Documentadas""",

    "code_generation": """Você é um especialista em desenvolvimento de código e programação.

Quando o usuário pedir geração de código:
1. Entenda completamente os requisitos antes de codificar
2. Escreva código limpo, bem documentado e seguindo best practices
3. Inclua tratamento de erros e validações
4. Forneça exemplos de uso
5. Explique a lógica e decisões de design
6. Considere performance, segurança e escalabilidade
7. Sugira melhorias e otimizações
8. Forneça testes quando apropriado

Foque em código que seja:
- Funcional e testado
- Bem documentado
- Seguro e performático
- Fácil de manter
- Seguindo padrões da linguagem""",

    "general": """Para conversas gerais:
1. Seja amigável, profissional e extremamente prestativo
2. Mantenha o foco no objetivo do usuário
3. Ofereça ajuda adicional e proativa quando apropriado
4. Use linguagem clara mas técnica quando necessário
5. Forneça contexto e explicações quando útil
6. Seja conciso mas completo
7. Antecipe necessidades não expressas
8. Ofereça múltiplas perspectivas quando relevante""",
}

# ============================================================================
# MENSAGENS DO SISTEMA
# ============================================================================

SYSTEM_MESSAGES = {
    "welcome": "Olá! 👋 Sou seu assistente especialista em dashboards e análise de dados. Como posso ajudá-lo hoje?",
    "thinking": "💭 Analisando e processando...",
    "error": "❌ Ocorreu um erro. Vou investigar e fornecer uma solução.",
    "no_response": "Não foi possível gerar uma resposta. Verifique sua conexão com a OpenAI e tente novamente.",
    "model_not_found": "Modelo não encontrado. Verifique se o modelo está disponível na sua conta OpenAI.",
    "rate_limit": "Limite de requisições atingido. Aguarde um momento e tente novamente.",
    "insufficient_quota": "Cota insuficiente. Verifique seu plano OpenAI.",
}

# ============================================================================
# VALIDAÇÕES E LIMITES
# ============================================================================

VALIDATION_RULES = {
    "temperature_range": (MIN_TEMPERATURE, MAX_TEMPERATURE),
    "min_message_length": 1,
    "max_message_length": 10000,
    "allowed_languages": ["pt-BR", "en-US", "es-ES"],
    "max_tokens_range": (1, 4096),  # Limite da OpenAI
    "top_p_range": (0.0, 1.0),
    "frequency_penalty_range": (-2.0, 2.0),
    "presence_penalty_range": (-2.0, 2.0),
}

# ============================================================================
# CONFIGURAÇÕES AVANÇADAS
# ============================================================================

ADVANCED_CONFIG = {
    # Retry em caso de falha
    "max_retries": 3,
    "retry_delay": 1.0,  # segundos
    "exponential_backoff": True,  # Backoff exponencial entre tentativas
    
    # Cache de respostas (futuro)
    "enable_cache": False,
    "cache_ttl": 3600,  # segundos
    
    # Logging
    "log_requests": True,
    "log_responses": False,  # Pode conter dados sensíveis
    "log_errors": True,
    
    # Performance
    "enable_streaming": True,  # OpenAI suporta streaming
    "stream_chunk_size": 50,  # Tokens por chunk no streaming
    
    # Rate limiting
    "respect_rate_limits": True,
    "requests_per_minute": 60,  # Ajustar conforme plano OpenAI
    
    # Qualidade
    "validate_responses": True,
    "check_code_syntax": True,  # Validar sintaxe de código gerado
}

# ============================================================================
# CONFIGURAÇÕES POR MODELO
# ============================================================================

MODEL_SPECIFIC_CONFIG = {
    "gpt-4.1": {
        "max_tokens": 4096,
        "recommended_temperature": 0.7,
        "context_length": 128000,
        "best_for": ["análise avançada", "raciocínio complexo", "código", "análise de dados"],
    },
    "gpt-4o": {
        "max_tokens": 4096,
        "recommended_temperature": 0.7,
        "context_length": 128000,
        "best_for": ["análise complexa", "código", "raciocínio"],
    },
    "gpt-4o-mini": {
        "max_tokens": 16384,
        "recommended_temperature": 0.7,
        "context_length": 128000,
        "best_for": ["análise rápida", "respostas curtas"],
    },
    "gpt-4-turbo": {
        "max_tokens": 4096,
        "recommended_temperature": 0.7,
        "context_length": 128000,
        "best_for": ["análise detalhada", "código complexo"],
    },
    "gpt-4": {
        "max_tokens": 4096,
        "recommended_temperature": 0.7,
        "context_length": 8192,
        "best_for": ["análise profunda", "raciocínio complexo"],
    },
    "gpt-3.5-turbo": {
        "max_tokens": 4096,
        "recommended_temperature": 0.7,
        "context_length": 16385,
        "best_for": ["respostas rápidas", "tarefas gerais"],
    },
    "gpt-3.5-turbo-16k": {
        "max_tokens": 4096,
        "recommended_temperature": 0.7,
        "context_length": 16385,
        "best_for": ["contexto longo", "análise de documentos"],
    },
}

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================


def get_system_prompt(context: str = "general") -> str:
    """
    Retorna o system prompt completo com contexto específico.

    Args:
        context: Contexto da conversa ("dashboard", "data_analysis", "error_help", "code_generation", "general")

    Returns:
        System prompt completo
    """
    base_prompt = SYSTEM_PROMPT

    if context in CONTEXT_PROMPTS:
        context_instructions = CONTEXT_PROMPTS[context]
        return f"{base_prompt}\n\nCONTEXTO ATUAL - MODO ESPECIALISTA:\n{context_instructions}"

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


def get_model_parameters(
    temperature: float = None,
    max_tokens: int = None,
    top_p: float = None,
    frequency_penalty: float = None,
    presence_penalty: float = None,
    model: str = None,
    **kwargs
) -> dict:
    """
    Retorna dicionário com parâmetros do modelo OpenAI.

    Parâmetros suportados pela OpenAI:
    - temperature: Controla aleatoriedade (0.0-2.0)
    - max_tokens: Máximo de tokens na resposta
    - top_p: Nucleus sampling (0.0-1.0)
    - frequency_penalty: Penalidade por frequência (-2.0 a 2.0)
    - presence_penalty: Penalidade por presença (-2.0 a 2.0)

    Args:
        temperature: Temperatura (usa padrão se None)
        max_tokens: Máximo de tokens (usa padrão do modelo se None)
        top_p: Top-p sampling (usa padrão se None)
        frequency_penalty: Penalidade por frequência (usa padrão se None)
        presence_penalty: Penalidade por presença (usa padrão se None)
        model: Nome do modelo (para obter configurações específicas)
        **kwargs: Parâmetros adicionais

    Returns:
        Dicionário com parâmetros no formato esperado pela OpenAI
    """
    params = {
        "temperature": validate_temperature(temperature or DEFAULT_TEMPERATURE),
    }

    # Obter configurações específicas do modelo se fornecido
    model_config = None
    if model and model in MODEL_SPECIFIC_CONFIG:
        model_config = MODEL_SPECIFIC_CONFIG[model]

    # max_tokens
    if max_tokens is not None:
        params["max_tokens"] = max_tokens
    elif model_config:
        params["max_tokens"] = model_config.get("max_tokens", DEFAULT_MAX_TOKENS)
    else:
        params["max_tokens"] = DEFAULT_MAX_TOKENS

    # top_p
    if top_p is not None:
        params["top_p"] = max(0.0, min(1.0, top_p))
    else:
        params["top_p"] = DEFAULT_TOP_P

    # frequency_penalty
    if frequency_penalty is not None:
        params["frequency_penalty"] = max(-2.0, min(2.0, frequency_penalty))
    else:
        params["frequency_penalty"] = DEFAULT_FREQUENCY_PENALTY

    # presence_penalty
    if presence_penalty is not None:
        params["presence_penalty"] = max(-2.0, min(2.0, presence_penalty))
    else:
        params["presence_penalty"] = DEFAULT_PRESENCE_PENALTY

    # Adicionar parâmetros adicionais
    if "stop" in kwargs:
        params["stop"] = kwargs["stop"]
    if "n" in kwargs:
        params["n"] = kwargs["n"]
    if "stream" in kwargs:
        params["stream"] = kwargs["stream"]

    return params


def get_model_config(model: str) -> dict:
    """
    Retorna configurações específicas de um modelo.

    Args:
        model: Nome do modelo OpenAI

    Returns:
        Dicionário com configurações do modelo ou None se não encontrado
    """
    return MODEL_SPECIFIC_CONFIG.get(model, {})


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


def get_recommended_temperature(model: str, task_type: str = "general") -> float:
    """
    Retorna temperatura recomendada para um modelo e tipo de tarefa.

    Args:
        model: Nome do modelo
        task_type: Tipo de tarefa ("creative", "analytical", "code", "general")

    Returns:
        Temperatura recomendada
    """
    model_config = MODEL_SPECIFIC_CONFIG.get(model, {})
    base_temp = model_config.get("recommended_temperature", DEFAULT_TEMPERATURE)

    # Ajustar baseado no tipo de tarefa
    task_adjustments = {
        "creative": 0.9,  # Mais criativo
        "analytical": 0.3,  # Mais determinístico
        "code": 0.2,  # Muito determinístico para código
        "general": 0.7,  # Balanceado
    }

    adjustment = task_adjustments.get(task_type, 0.7)
    return adjustment


def get_optimal_max_tokens(model: str, context_length: int = None) -> int:
    """
    Retorna max_tokens ótimo baseado no modelo e contexto.

    Args:
        model: Nome do modelo
        context_length: Tamanho do contexto atual (opcional)

    Returns:
        max_tokens recomendado
    """
    model_config = MODEL_SPECIFIC_CONFIG.get(model, {})
    max_tokens = model_config.get("max_tokens", DEFAULT_MAX_TOKENS)

    # Se contexto fornecido, ajustar para deixar espaço
    if context_length:
        model_max_context = model_config.get("context_length", 16385)
        # Deixar pelo menos 10% do contexto para resposta
        recommended = int(model_max_context * 0.1)
        return min(max_tokens, recommended)

    return max_tokens

