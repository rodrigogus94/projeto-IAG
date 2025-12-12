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

SUA RESPONSABILIDADE PRINCIPAL:
1. PRIMEIRO: Verificar na pergunta ORIGINAL do usuário se há solicitação EXPLÍCITA de gráfico
2. SEGUNDO: Se SIM, analisar a RESPOSTA DO AGENTE DE ANÁLISE para extrair:
   - Quais colunas/dados foram mencionados na resposta
   - Quais métricas ou valores foram destacados
   - Qual tipo de análise foi feita (comparação, distribuição, tendência, etc.)
3. TERCEIRO: Usar essas informações da resposta para determinar:
   - Qual tipo de gráfico é mais apropriado
   - Quais colunas usar (x_column, y_column, category_column)
   - Qual título seria mais descritivo

🎯 ANÁLISE INTELIGENTE DA RESPOSTA DO AGENTE DE ANÁLISE:
A resposta do Agente de Análise contém informações valiosas sobre os dados analisados:
- Se a resposta menciona "por cidade", "por marca", "por status" → use essas colunas categóricas
- Se a resposta menciona "quilometragem", "km", "consumo", "custo" → use essas colunas numéricas
- Se a resposta fala de "distribuição", "proporção" → considere gráfico de pizza ou histograma
- Se a resposta fala de "comparação", "maior", "menor" → considere gráfico de barras
- Se a resposta fala de "tendência", "ao longo do tempo" → considere gráfico de linha
- Se a resposta menciona "média", "total", "soma" → use essas agregações

EXEMPLO DE ANÁLISE:
Pergunta: "Mostre um gráfico de consumo por cidade"
Resposta do Agente: "A análise mostra que São Paulo tem o maior consumo médio (12.5 L/100km), seguido por Rio de Janeiro (11.8 L/100km)..."
→ Você deve gerar: gráfico de barras com x_column="cidade" e y_column="consumo_combustivel" (com agregação média)

TIPOS DE GRÁFICOS DISPONÍVEIS:
- bar: Para comparações entre categorias (ex: consumo por cidade, custo por marca)
- pie: Para distribuições e proporções (ex: distribuição de status, veículos por cidade)
- line: Para tendências ao longo do tempo (ex: consumo ao longo dos anos)
- scatter: Para correlações entre variáveis (ex: km_mes vs consumo)
- histogram: Para distribuições de valores numéricos (ex: distribuição de velocidade)
- box: Para análise de quartis e outliers (ex: consumo por marca)
- heatmap: Para matrizes de correlação (ex: correlação entre todas variáveis numéricas)
- area: Para tendências com área preenchida (similar a line, mas com área)
- violin: Para distribuição de densidade (similar a box, mas mostra densidade)

MAPEAMENTO DE TERMOS PARA COLUNAS:
- "quilometragem", "km", "quilometragem mensal" → km_mes
- "velocidade", "velocidade média" → velocidade_media
- "consumo", "combustível", "combustivel" → consumo_combustivel
- "custo", "manutenção", "manutencao" → custo_manutencao
- "dias", "operacionais" → dias_operacionais
- "alertas" → alertas

FORMATO DE RESPOSTA:
Você deve retornar APENAS um JSON válido:

Se o usuário SOLICITOU gráfico explicitamente:
{
    "should_generate_chart": true,
    "chart_type": "bar|pie|line|scatter|histogram|box|heatmap|area|violin",
    "x_column": "nome_da_coluna_x",
    "y_column": "nome_da_coluna_y",
    "category_column": "nome_da_coluna_categoria",
    "title": "Título descritivo do gráfico baseado na resposta do agente",
    "reasoning": "Explicação de como você usou a resposta do agente de análise para determinar este gráfico"
}

Se o usuário NÃO solicitou gráfico explicitamente:
{
    "should_generate_chart": false,
    "reasoning": "Usuário não solicitou gráfico explicitamente. Apenas fez uma pergunta sobre os dados."
}

⚠️ IMPORTANTE:
- Use a RESPOSTA DO AGENTE DE ANÁLISE para extrair informações sobre colunas e métricas
- O título do gráfico deve refletir o que foi analisado na resposta
- Se a resposta menciona agregações (média, total, soma), considere isso ao escolher o gráfico
- Seja preciso: use exatamente os nomes das colunas disponíveis no dataset"""


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
                "content": f"""PERGUNTA ORIGINAL DO USUÁRIO (USE PARA VERIFICAR SE HÁ SOLICITAÇÃO EXPLÍCITA DE GRÁFICO):
{user_input}

RESPOSTA DO AGENTE DE ANÁLISE (USE ESTA PARA EXTRAIR INFORMAÇÕES SOBRE COLUNAS E DADOS):
{text_response}

{columns_info}

INSTRUÇÕES CRÍTICAS:
1. PRIMEIRO: Verifique na pergunta original se o usuário EXPLICITAMENTE solicitou um gráfico/visualização.
   - Se NÃO houver solicitação explícita → retorne should_generate_chart = false
   - Se HOUVER solicitação explícita → continue para o passo 2

2. SEGUNDO: Analise a RESPOSTA DO AGENTE DE ANÁLISE para extrair:
   - Quais colunas foram mencionadas? (cidade, marca, status, km_mes, consumo_combustivel, etc.)
   - Quais métricas foram destacadas? (média, total, soma, quantidade, etc.)
   - Que tipo de análise foi feita? (comparação, distribuição, tendência, etc.)
   
3. TERCEIRO: Use essas informações da resposta para determinar:
   - chart_type: tipo de gráfico mais apropriado baseado na análise
   - x_column: coluna categórica mencionada na resposta (ex: cidade, marca, status)
   - y_column: coluna numérica mencionada na resposta (ex: km_mes, consumo_combustivel, custo_manutencao)
   - title: título descritivo que reflita o que foi analisado na resposta

EXEMPLO:
Se a resposta menciona "consumo médio por cidade" e lista valores por cidade:
→ chart_type: "bar"
→ x_column: "cidade"
→ y_column: "consumo_combustivel"
→ title: "Consumo Médio de Combustível por Cidade"

Se a resposta menciona "distribuição de veículos por status":
→ chart_type: "pie"
→ category_column: "status"
→ title: "Distribuição de Veículos por Status"

Retorne APENAS um JSON válido com a configuração. NÃO adicione texto antes ou depois do JSON."""
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
            
            # Tentar extrair JSON da resposta - múltiplas estratégias
            config = None
            
            # Estratégia 1: Procurar por bloco JSON completo
            json_patterns = [
                r'\{[^{}]*"should_generate_chart"[^{}]*\}',  # JSON simples
                r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*"should_generate_chart"[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # JSON aninhado
                r'```json\s*(\{.*?\})\s*```',  # JSON em bloco de código
                r'```\s*(\{.*?\})\s*```',  # JSON em bloco genérico
            ]
            
            for pattern in json_patterns:
                json_match = re.search(pattern, chart_decision, re.DOTALL | re.IGNORECASE)
                if json_match:
                    json_str = json_match.group(1) if json_match.lastindex else json_match.group(0)
                    try:
                        config = json.loads(json_str)
                        logger.info(f"JSON extraído com sucesso usando padrão: {pattern[:50]}...")
                        break
                    except json.JSONDecodeError:
                        continue
            
            # Estratégia 2: Tentar encontrar JSON começando com {
            if not config:
                start_idx = chart_decision.find('{')
                end_idx = chart_decision.rfind('}')
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    json_str = chart_decision[start_idx:end_idx+1]
                    try:
                        config = json.loads(json_str)
                        logger.info("JSON extraído encontrando primeiro { e último }")
                    except json.JSONDecodeError:
                        pass
            
            if config:
                if not config.get("should_generate_chart", False):
                    logger.info("Agente de Gráficos determinou que não é necessário gerar gráfico")
                    return config
                
                # Validar e completar configuração
                chart_type = config.get("chart_type", "bar")
                
                # Validar colunas se DataFrame disponível
                if df is not None:
                    x_col = config.get("x_column")
                    y_col = config.get("y_column")
                    cat_col = config.get("category_column")
                    
                    # Verificar se as colunas existem no DataFrame
                    available_cols = list(df.columns)
                    
                    if x_col and x_col not in available_cols:
                        logger.warning(f"Coluna x_column '{x_col}' não encontrada. Tentando encontrar similar...")
                        # Tentar encontrar coluna similar (case-insensitive)
                        x_col_lower = x_col.lower()
                        for col in available_cols:
                            if col.lower() == x_col_lower or x_col_lower in col.lower():
                                config["x_column"] = col
                                logger.info(f"Coluna x_column corrigida: '{x_col}' -> '{col}'")
                                break
                        else:
                            config["x_column"] = None
                    
                    if y_col and y_col not in available_cols:
                        logger.warning(f"Coluna y_column '{y_col}' não encontrada. Tentando encontrar similar...")
                        y_col_lower = y_col.lower()
                        for col in available_cols:
                            if col.lower() == y_col_lower or y_col_lower in col.lower():
                                config["y_column"] = col
                                logger.info(f"Coluna y_column corrigida: '{y_col}' -> '{col}'")
                                break
                        else:
                            config["y_column"] = None
                    
                    if cat_col and cat_col not in available_cols:
                        logger.warning(f"Coluna category_column '{cat_col}' não encontrada. Tentando encontrar similar...")
                        cat_col_lower = cat_col.lower()
                        for col in available_cols:
                            if col.lower() == cat_col_lower or cat_col_lower in col.lower():
                                config["category_column"] = col
                                logger.info(f"Coluna category_column corrigida: '{cat_col}' -> '{col}'")
                                break
                        else:
                            config["category_column"] = None
                
                # Se não há colunas especificadas, tentar inferir da pergunta original
                if not config.get("x_column") and not config.get("y_column") and not config.get("category_column"):
                    logger.info("Nenhuma coluna especificada, tentando inferir da pergunta original...")
                    from src.core.chart_analyzer import detect_chart_request
                    detected = detect_chart_request(user_input)
                    if detected:
                        config["chart_type"] = detected.get("chart_type", chart_type)
                        config["columns"] = detected.get("columns", [])
                
                logger.info(f"Configuração do gráfico extraída e validada: {config}")
                return config
            
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
        Usa as informações extraídas da resposta do agente de análise.
        
        Args:
            df: DataFrame com os dados
            chart_config: Configuração do gráfico
            
        Returns:
            Objeto do gráfico ou None
        """
        try:
            from src.core.chart_generator import (
                generate_chart_from_request,
                create_bar_chart,
                create_pie_chart,
                create_histogram,
                create_line_chart,
                create_scatter_chart,
                create_box_plot,
                create_heatmap,
                create_area_chart,
                create_violin_plot
            )
            
            chart_type = chart_config.get("chart_type", "bar")
            x_column = chart_config.get("x_column")
            y_column = chart_config.get("y_column")
            category_column = chart_config.get("category_column")
            title = chart_config.get("title")
            
            logger.info(f"Gerando gráfico: tipo={chart_type}, x={x_column}, y={y_column}, category={category_column}")
            
            # Validar que as colunas existem no DataFrame
            if x_column and x_column not in df.columns:
                logger.warning(f"Coluna x_column '{x_column}' não encontrada. Colunas disponíveis: {list(df.columns)}")
                # Tentar encontrar coluna similar
                x_column = None
            
            if y_column and y_column not in df.columns:
                logger.warning(f"Coluna y_column '{y_column}' não encontrada. Colunas disponíveis: {list(df.columns)}")
                # Tentar encontrar coluna similar
                y_column = None
            
            if category_column and category_column not in df.columns:
                logger.warning(f"Coluna category_column '{category_column}' não encontrada. Colunas disponíveis: {list(df.columns)}")
                category_column = None
            
            # Gerar gráfico baseado no tipo e colunas especificadas
            if chart_type == "bar" or chart_type == "barras":
                if x_column and y_column:
                    # Agrupar dados se necessário
                    if x_column in df.select_dtypes(include=['object']).columns:
                        # Agrupar por categoria e agregar
                        df_grouped = df.groupby(x_column)[y_column].sum().reset_index()
                        return create_bar_chart(
                            df_grouped,
                            x=x_column,
                            y=y_column,
                            title=title or f"{y_column.replace('_', ' ').title()} por {x_column.replace('_', ' ').title()}"
                        )
                    else:
                        return create_bar_chart(
                            df,
                            x=x_column,
                            y=y_column,
                            title=title or f"{y_column.replace('_', ' ').title()} por {x_column.replace('_', ' ').title()}"
                        )
            
            elif chart_type == "pie" or chart_type == "pizza":
                if category_column:
                    # Agrupar e contar
                    df_grouped = df[category_column].value_counts().reset_index()
                    df_grouped.columns = [category_column, "count"]
                    return create_pie_chart(
                        df_grouped,
                        values="count",
                        names=category_column,
                        title=title or f"Distribuição por {category_column.replace('_', ' ').title()}"
                    )
            
            elif chart_type == "histogram" or chart_type == "histograma":
                if y_column:
                    return create_histogram(
                        df,
                        column=y_column,
                        title=title or f"Distribuição de {y_column.replace('_', ' ').title()}"
                    )
            
            elif chart_type == "line" or chart_type == "linha":
                if x_column and y_column:
                    return create_line_chart(
                        df,
                        x=x_column,
                        y=y_column,
                        title=title or f"{y_column.replace('_', ' ').title()} por {x_column.replace('_', ' ').title()}"
                    )
            
            elif chart_type == "scatter" or chart_type == "dispersao":
                if x_column and y_column:
                    return create_scatter_chart(
                        df,
                        x=x_column,
                        y=y_column,
                        title=title or f"{y_column.replace('_', ' ').title()} vs {x_column.replace('_', ' ').title()}"
                    )
            
            elif chart_type == "box" or chart_type == "boxplot":
                if y_column:
                    return create_box_plot(
                        df,
                        x=x_column,
                        y=y_column,
                        title=title or f"Distribuição de {y_column.replace('_', ' ').title()}"
                    )
            
            elif chart_type == "heatmap" or chart_type == "mapa_calor":
                return create_heatmap(
                    df,
                    title=title or "Matriz de Correlação"
                )
            
            elif chart_type == "area":
                if x_column and y_column:
                    return create_area_chart(
                        df,
                        x=x_column,
                        y=y_column,
                        title=title or f"{y_column.replace('_', ' ').title()} por {x_column.replace('_', ' ').title()}"
                    )
            
            elif chart_type == "violin" or chart_type == "violino":
                if y_column:
                    return create_violin_plot(
                        df,
                        x=x_column,
                        y=y_column,
                        title=title or f"Distribuição de Densidade de {y_column.replace('_', ' ').title()}"
                    )
            
            # Fallback: usar generate_chart_from_request
            logger.info("Usando fallback: generate_chart_from_request")
            chart = generate_chart_from_request(
                df,
                chart_type,
                **{k: v for k, v in chart_config.items() 
                   if k not in ["should_generate_chart", "chart_type", "reasoning"] and v is not None}
            )
            
            return chart
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico: {str(e)}", exc_info=True)
            return None

