"""
Orquestrador de Agentes Especialistas

Este módulo coordena dois agentes especialistas trabalhando em conjunto:
1. Agente de Análise: Responsável por entender perguntas e gerar respostas textuais
2. Agente de Gráficos: Responsável por gerar gráficos baseado na resposta do primeiro agente
"""

import logging
from typing import Optional, Dict, Any, List
import pandas as pd

logger = logging.getLogger(__name__)


# ============================================================================
# PROMPTS ESPECIALIZADOS PARA CADA AGENTE
# ============================================================================

ANALYSIS_AGENT_PROMPT = """Você é o Agente de Análise - especialista em entender perguntas e fornecer respostas textuais detalhadas sobre dados.

🎯 SUA PERSONALIDADE:
Você é um assistente amigável, profissional e humanizado da empresa Omnilink AI.
Seja natural, cordial e prestativo em todas as interações.

👋 CUMPRIMENTOS E SAUDAÇÕES:
Quando o usuário cumprimentar (bom dia, boa tarde, boa noite, olá, oi, etc.):
- Responda de forma calorosa e amigável
- Use expressões como: "Bom dia!", "Olá!", "Oi! Como posso ajudar?"
- Seja breve mas acolhedor
- Ofereça ajuda: "Como posso ajudar você hoje?", "Em que posso ser útil?"

Exemplos de respostas para cumprimentos:
- "Bom dia!" → "Bom dia! 😊 Como posso ajudar você hoje?"
- "Olá" → "Olá! 👋 Em que posso ser útil?"
- "Oi, tudo bem?" → "Oi! Tudo bem sim, obrigado! Como posso ajudar?"

💬 CONVERSAS SIMPLES:
Para perguntas simples ou conversas casuais:
- Seja natural e conversacional
- Não seja excessivamente técnico
- Mostre interesse genuíno em ajudar
- Use emojis quando apropriado (mas com moderação)

SUA RESPONSABILIDADE PRINCIPAL:
- Entender a pergunta do usuário
- Responder APENAS o que foi perguntado - nada mais, nada menos
- Analisar os dados fornecidos no contexto APENAS se o usuário perguntar sobre dados
- NUNCA mencionar dados, análises ou gráficos se o usuário não perguntar sobre isso
- NUNCA mencionar código ou gráficos - apenas análise textual (quando aplicável)
- Focar em insights, números, percentuais e comparações APENAS quando o usuário solicitar análise de dados

REGRAS ABSOLUTAS:
❌ NÃO mencione código Python, Matplotlib, Plotly ou Pandas
❌ NÃO forneça instruções de como criar gráficos
❌ NÃO diga "não consigo gerar visualizações"
❌ NÃO mencione dados, análises ou gráficos se o usuário não perguntar sobre isso
❌ NÃO adicione informações extras que não foram solicitadas
✅ Seja humanizado e amigável em todas as respostas
✅ Responda APENAS o que foi perguntado
✅ APENAS analise os dados se o usuário explicitamente perguntar sobre dados
✅ Use números específicos, percentuais e comparações APENAS quando o usuário solicitar análise
✅ Identifique padrões, tendências e anomalias APENAS quando o usuário solicitar análise

FORMATO DE RESPOSTA:
- Para cumprimentos: Seja breve, amigável e ofereça ajuda
- Para perguntas simples: Seja direto e útil
- Para análises de dados: Use formatação Markdown (títulos, listas, negrito)
- Seja específico com números exatos dos dados (quando houver dados)
- Use percentuais e proporções (quando aplicável)
- Destaque insights importantes (quando aplicável)
- Faça comparações quando relevante (quando aplicável)

Lembre-se: 
- Outro agente especializado irá gerar os gráficos automaticamente. Você só precisa ANALISAR e RESPONDER em texto.
- Seja sempre humanizado, amigável e natural nas suas respostas.
- Adapte seu tom ao contexto: cumprimentos simples recebem respostas simples e amigáveis."""


CHART_AGENT_PROMPT = """Você é o Agente de Gráficos - especialista em analisar respostas textuais e determinar qual gráfico gerar.

🚨 REGRA CRÍTICA E ABSOLUTA 🚨
VOCÊ DEVE GERAR GRÁFICO APENAS SE O USUÁRIO EXPLICITAMENTE SOLICITOU!

PALAVRAS-CHAVE QUE INDICAM SOLICITAÇÃO EXPLÍCITA DE GRÁFICO:
- "gráfico", "grafico", "chart", "visualização", "visualizacao"
- "plot", "mostre", "exiba", "crie", "gere" (quando combinado com termos de visualização)
- "gráfico de", "chart de", "visualização de"
- "mostre um gráfico", "gere um gráfico", "crie um gráfico"

❌ NÃO gere gráfico se:
- O usuário apenas fez uma pergunta sobre os dados
- O usuário pediu uma análise textual
- Não há palavras-chave explícitas de solicitação de gráfico
- A pergunta é apenas informativa (ex: "quantos veículos temos?")

✅ GERE gráfico APENAS se:
- O usuário explicitamente pediu um gráfico/visualização
- Há palavras-chave claras de solicitação de visualização
- A intenção é claramente de visualizar dados graficamente

SUA RESPONSABILIDADE:
- Analisar a pergunta ORIGINAL do usuário (não apenas a resposta do Agente de Análise)
- Verificar se há solicitação EXPLÍCITA de gráfico
- Se SIM: identificar qual tipo de gráfico seria mais apropriado
- Se NÃO: retornar should_generate_chart = false

ANÁLISE DA PERGUNTA DO USUÁRIO:
Você receberá tanto a pergunta original quanto a resposta do Agente de Análise.
Foque PRINCIPALMENTE na pergunta original para determinar se há solicitação explícita.

TIPOS DE GRÁFICOS DISPONÍVEIS:
- bar: Para comparações entre categorias
- pie: Para distribuições e proporções
- line: Para tendências ao longo do tempo
- scatter: Para correlações entre variáveis
- histogram: Para distribuições de valores numéricos
- box: Para análise de quartis e outliers
- heatmap: Para matrizes de correlação

FORMATO DE RESPOSTA:
Você deve retornar APENAS um JSON válido:

Se o usuário SOLICITOU gráfico explicitamente:
{
    "should_generate_chart": true,
    "chart_type": "bar|pie|line|scatter|histogram|box|heatmap",
    "x_column": "nome_da_coluna_x",
    "y_column": "nome_da_coluna_y",
    "category_column": "nome_da_coluna_categoria",
    "title": "Título do gráfico",
    "reasoning": "Por que este gráfico é apropriado"
}

Se o usuário NÃO solicitou gráfico explicitamente:
{
    "should_generate_chart": false,
    "reasoning": "Usuário não solicitou gráfico explicitamente. Apenas fez uma pergunta sobre os dados."
}

Lembre-se: Seja CONSERVADOR. Só gere gráfico se houver solicitação EXPLÍCITA e CLARA."""


# ============================================================================
# CLASSE ORQUESTRADOR
# ============================================================================

class AgentOrchestrator:
    """
    Orquestrador que coordena dois agentes especialistas:
    1. Agente de Análise: Gera respostas textuais
    2. Agente de Gráficos: Determina qual gráfico gerar baseado na resposta
    """
    
    def __init__(self, llm_handler):
        """
        Inicializa o orquestrador com um handler LLM.
        
        Args:
            llm_handler: Handler LLM (Ollama ou OpenAI) para usar com os agentes
        """
        self.llm_handler = llm_handler
        self.analysis_agent_prompt = ANALYSIS_AGENT_PROMPT
        self.chart_agent_prompt = CHART_AGENT_PROMPT
        logger.info("AgentOrchestrator inicializado")
    
    def process_user_query(
        self,
        user_input: str,
        data_context: Optional[str] = None,
        df: Optional[pd.DataFrame] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Processa uma consulta do usuário usando dois agentes em sequência.
        
        Args:
            user_input: Pergunta do usuário
            data_context: Contexto dos dados (estatísticas, resumo, etc.)
            df: DataFrame com os dados (opcional, para geração de gráficos)
            model: Modelo LLM a usar
            temperature: Temperatura para geração
            
        Returns:
            Dicionário com:
            - "text_response": Resposta textual do Agente de Análise
            - "chart_config": Configuração do gráfico do Agente de Gráficos (ou None)
            - "chart": Objeto do gráfico gerado (ou None)
        """
        try:
            logger.info(f"Processando consulta do usuário: {user_input[:100]}...")
            
            # ============================================================
            # FASE 1: Agente de Análise - Gerar resposta textual
            # ============================================================
            logger.info("Fase 1: Agente de Análise gerando resposta...")
            
            # Preparar mensagens para o Agente de Análise
            analysis_messages = [
                {"role": "system", "content": self.analysis_agent_prompt}
            ]
            
            # Verificar se é um cumprimento simples
            user_input_lower = user_input.lower().strip()
            greetings = ['bom dia', 'boa tarde', 'boa noite', 'olá', 'ola', 'oi', 'hey', 'e aí', 'e ai']
            is_greeting = any(greeting in user_input_lower for greeting in greetings) and len(user_input.split()) <= 5
            
            # Adicionar contexto dos dados APENAS se disponível E se o usuário perguntou sobre dados
            if data_context and not is_greeting:
                # Usuário perguntou sobre dados - enviar contexto
                analysis_messages.append({
                    "role": "user",
                    "content": f"""CONTEXTO DOS DADOS DISPONÍVEIS:

{data_context}

PERGUNTA DO USUÁRIO:
{user_input}

IMPORTANTE: Analise os dados acima e forneça uma resposta APENAS sobre o que foi perguntado. NÃO mencione código ou gráficos - apenas análise textual."""
                })
            elif is_greeting:
                # Cumprimento simples - resposta amigável sem contexto
                analysis_messages.append({
                    "role": "user",
                    "content": f"{user_input}\n\n(Nota: Esta é uma saudação simples. Responda de forma amigável e ofereça ajuda. NÃO mencione dados, análises ou gráficos.)"
                })
            else:
                # Pergunta geral sem contexto de dados - responder diretamente
                analysis_messages.append({
                    "role": "user",
                    "content": f"{user_input}\n\n(Nota: Responda APENAS o que foi perguntado. NÃO mencione dados, análises ou gráficos a menos que o usuário tenha perguntado especificamente sobre isso.)"
                })
            
            # Gerar resposta do Agente de Análise
            text_response = self.llm_handler.generate_response(
                messages=analysis_messages,
                model=model,
                temperature=temperature,
                stream=False,
            )
            
            logger.info(f"Agente de Análise gerou resposta: {len(text_response)} caracteres")
            
            # ============================================================
            # FASE 2: Agente de Gráficos - Determinar gráfico apropriado
            # ============================================================
            logger.info("Fase 2: Agente de Gráficos analisando resposta...")
            
            # Preparar mensagens para o Agente de Gráficos
            chart_messages = [
                {"role": "system", "content": self.chart_agent_prompt}
            ]
            
            # Adicionar informações sobre dados disponíveis
            columns_info = ""
            if df is not None:
                columns_info = f"""
COLUNAS DISPONÍVEIS NO DATASET:
- Categóricas: {', '.join(df.select_dtypes(include=['object']).columns.tolist())}
- Numéricas: {', '.join(df.select_dtypes(include=['int64', 'float64']).columns.tolist())}
"""
            
            chart_messages.append({
                "role": "user",
                "content": f"""PERGUNTA ORIGINAL DO USUÁRIO (FOCE NESTA PARA DETERMINAR SE HÁ SOLICITAÇÃO DE GRÁFICO):
{user_input}

RESPOSTA DO AGENTE DE ANÁLISE:
{text_response}

{columns_info}

IMPORTANTE: Analise PRINCIPALMENTE a pergunta original do usuário. 
Só retorne should_generate_chart = true se o usuário EXPLICITAMENTE solicitou um gráfico/visualização.
Se o usuário apenas fez uma pergunta sobre os dados, retorne should_generate_chart = false.

Retorne APENAS um JSON válido com a configuração."""
            })
            
            # Gerar decisão do Agente de Gráficos
            chart_decision = self.llm_handler.generate_response(
                messages=chart_messages,
                model=model,
                temperature=0.3,  # Temperatura mais baixa para decisões mais consistentes
                stream=False,
            )
            
            logger.info(f"Agente de Gráficos retornou decisão: {chart_decision[:200]}...")
            
            # ============================================================
            # FASE 3: Processar decisão e gerar gráfico se necessário
            # ============================================================
            chart_config = None
            chart = None
            
            # Tentar extrair JSON da resposta
            chart_config = self._parse_chart_decision(chart_decision, user_input, df)
            
            if chart_config and chart_config.get("should_generate_chart") and df is not None:
                logger.info(f"Gerando gráfico do tipo: {chart_config.get('chart_type')}")
                chart = self._generate_chart_from_config(df, chart_config)
            
            return {
                "text_response": text_response,
                "chart_config": chart_config,
                "chart": chart,
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar consulta: {str(e)}", exc_info=True)
            return {
                "text_response": f"Erro ao processar consulta: {str(e)}",
                "chart_config": None,
                "chart": None,
            }
    
    def _parse_chart_decision(
        self,
        chart_decision: str,
        user_input: str,
        df: Optional[pd.DataFrame] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Extrai configuração do gráfico da decisão do Agente de Gráficos.
        
        Args:
            chart_decision: Resposta do Agente de Gráficos
            user_input: Pergunta original do usuário
            df: DataFrame com os dados
            
        Returns:
            Dicionário com configuração do gráfico ou None
        """
        try:
            import json
            import re
            
            # Tentar extrair JSON da resposta
            # Procurar por bloco JSON (pode ter múltiplas linhas)
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*"should_generate_chart"[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            json_match = re.search(json_pattern, chart_decision, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                try:
                    config = json.loads(json_str)
                    
                    if not config.get("should_generate_chart", False):
                        logger.info("Agente de Gráficos determinou que não é necessário gerar gráfico")
                        return config
                    
                    # Validar e completar configuração
                    chart_type = config.get("chart_type", "bar")
                    
                    # Se não há colunas especificadas, tentar inferir da pergunta original
                    if not config.get("x_column") and not config.get("y_column"):
                        # Usar chart_analyzer para detectar
                        from src.core.chart_analyzer import detect_chart_request
                        detected = detect_chart_request(user_input)
                        if detected:
                            config["chart_type"] = detected.get("chart_type", chart_type)
                            config["columns"] = detected.get("columns", [])
                    
                    logger.info(f"Configuração do gráfico extraída: {config}")
                    return config
                except json.JSONDecodeError as e:
                    logger.warning(f"Erro ao fazer parse do JSON: {e}. Tentando detecção automática.")
            
            # Fallback: usar detecção automática (mas ser conservador)
            logger.warning("Não foi possível extrair JSON válido, usando detecção automática")
            from src.core.chart_analyzer import detect_chart_request
            detected = detect_chart_request(user_input)
            
            # Só retornar true se detectou claramente uma solicitação de gráfico
            if detected:
                # Verificar se há palavras-chave explícitas de solicitação
                user_input_lower = user_input.lower()
                explicit_keywords = [
                    'gráfico', 'grafico', 'chart', 'visualização', 'visualizacao',
                    'plot', 'mostre', 'exiba', 'crie', 'gere'
                ]
                has_explicit_request = any(keyword in user_input_lower for keyword in explicit_keywords)
                
                if has_explicit_request:
                    return {
                        "should_generate_chart": True,
                        "chart_type": detected.get("chart_type", "bar"),
                        "columns": detected.get("columns", []),
                    }
                else:
                    logger.info("Detectou possível gráfico, mas não há solicitação explícita do usuário")
                    return {
                        "should_generate_chart": False,
                        "reasoning": "Não há solicitação explícita de gráfico na pergunta do usuário"
                    }
            
            return {
                "should_generate_chart": False,
                "reasoning": "Usuário não solicitou gráfico explicitamente"
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar decisão do gráfico: {str(e)}", exc_info=True)
            # Fallback conservador: só gerar se houver solicitação explícita
            from src.core.chart_analyzer import detect_chart_request
            detected = detect_chart_request(user_input)
            
            if detected:
                # Verificar se há palavras-chave explícitas de solicitação
                user_input_lower = user_input.lower()
                explicit_keywords = [
                    'gráfico', 'grafico', 'chart', 'visualização', 'visualizacao',
                    'plot', 'mostre', 'exiba', 'crie', 'gere'
                ]
                has_explicit_request = any(keyword in user_input_lower for keyword in explicit_keywords)
                
                if has_explicit_request:
                    return {
                        "should_generate_chart": True,
                        "chart_type": detected.get("chart_type", "bar"),
                        "columns": detected.get("columns", []),
                    }
            
            # Por padrão, não gerar gráfico
            return {
                "should_generate_chart": False,
                "reasoning": "Erro ao processar decisão ou não há solicitação explícita de gráfico"
            }
    
    def _generate_chart_from_config(
        self,
        df: pd.DataFrame,
        chart_config: Dict[str, Any]
    ) -> Optional[Any]:
        """
        Gera um gráfico baseado na configuração do Agente de Gráficos.
        
        Args:
            df: DataFrame com os dados
            chart_config: Configuração do gráfico
            
        Returns:
            Objeto do gráfico ou None
        """
        try:
            from src.core.chart_analyzer import create_smart_chart
            
            # Se temos colunas específicas, usar create_smart_chart com contexto
            chart_type = chart_config.get("chart_type", "bar")
            
            # Construir uma descrição da solicitação para create_smart_chart
            description = f"gráfico de {chart_type}"
            if chart_config.get("x_column"):
                description += f" com {chart_config.get('x_column')}"
            if chart_config.get("y_column"):
                description += f" por {chart_config.get('y_column')}"
            
            # Usar create_smart_chart que já tem lógica inteligente
            chart = create_smart_chart(df, description)
            
            if chart:
                logger.info(f"Gráfico gerado com sucesso: {chart_type}")
                return chart
            
            # Fallback: tentar gerar manualmente
            from src.core.chart_generator import generate_chart_from_request
            
            chart = generate_chart_from_request(
                df,
                chart_type,
                **{k: v for k, v in chart_config.items() if k not in ["should_generate_chart", "chart_type", "reasoning"]}
            )
            
            return chart
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico: {str(e)}", exc_info=True)
            return None

