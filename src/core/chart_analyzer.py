"""
Módulo para analisar requisições do usuário e gerar gráficos automaticamente
"""

import re
import logging
from typing import Optional, Dict, Any, List
import pandas as pd

logger = logging.getLogger(__name__)


def detect_chart_request(user_input: str) -> Optional[Dict[str, Any]]:
    """
    Detecta se o usuário está pedindo um gráfico e extrai informações.

    Args:
        user_input: Texto da mensagem do usuário

    Returns:
        Dicionário com informações do gráfico ou None
    """
    user_input_lower = user_input.lower()

    # Palavras-chave para detectar solicitação de gráfico
    chart_keywords = [
        "gráfico", "grafico", "chart", "visualização", "visualizacao",
        "plot", "gráfico de", "mostre", "exiba", "crie", "gere",
        "dashboard", "análise", "analise", "estatística", "estatistica"
    ]

    # Verificar se contém palavras-chave
    has_chart_keyword = any(keyword in user_input_lower for keyword in chart_keywords)

    if not has_chart_keyword:
        return None

    # Detectar tipo de gráfico
    chart_type = None
    chart_type_keywords = {
        "bar": ["barra", "barras", "bar chart", "coluna", "colunas"],
        "line": ["linha", "linhas", "line chart", "tendência", "tendencia"],
        "pie": ["pizza", "pie chart", "torta", "distribuição", "distribuicao"],
        "scatter": ["dispersão", "dispersao", "scatter", "correlação", "correlacao"],
        "histogram": ["histograma", "histogram", "distribuição", "distribuicao"],
        "box": ["box", "boxplot", "quartis", "quartiles"],
        "heatmap": ["heatmap", "mapa de calor", "correlação", "correlacao"],
    }

    for chart, keywords in chart_type_keywords.items():
        if any(keyword in user_input_lower for keyword in keywords):
            chart_type = chart
            break

    # Se não detectou tipo específico, usar bar como padrão
    if chart_type is None:
        chart_type = "bar"

    # Extrair colunas mencionadas
    columns = extract_columns(user_input)

    return {
        "chart_type": chart_type,
        "columns": columns,
        "user_input": user_input,
    }


def extract_columns(user_input: str) -> List[str]:
    """
    Extrai nomes de colunas mencionadas no texto.

    Args:
        user_input: Texto da mensagem

    Returns:
        Lista de nomes de colunas encontradas
    """
    # Colunas conhecidas do dataset de veículos
    known_columns = [
        "marca", "modelo", "ano", "status", "cidade",
        "km_mes", "velocidade_media", "alertas",
        "consumo_combustivel", "dias_operacionais", "custo_manutencao"
    ]

    user_input_lower = user_input.lower()
    found_columns = []

    for col in known_columns:
        # Buscar variações do nome da coluna
        patterns = [
            col,
            col.replace("_", " "),
            col.replace("_", ""),
        ]

        for pattern in patterns:
            if pattern in user_input_lower:
                found_columns.append(col)
                break

    return found_columns


def suggest_chart_for_data(df: pd.DataFrame, user_input: str) -> Optional[Dict[str, Any]]:
    """
    Sugere um gráfico apropriado baseado nos dados e na solicitação.

    Args:
        df: DataFrame do pandas
        user_input: Texto da mensagem do usuário

    Returns:
        Dicionário com sugestão de gráfico ou None
    """
    if df is None or df.empty:
        return None

    user_input_lower = user_input.lower()

    # Analisar dados disponíveis
    numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
    categorical_cols = list(df.select_dtypes(include=["object"]).columns)

    # Detectar intenção
    if "por" in user_input_lower or "por cidade" in user_input_lower or "por marca" in user_input_lower:
        # Gráfico de barras agrupado
        if "cidade" in categorical_cols:
            return {
                "chart_type": "bar",
                "x": "cidade",
                "y": numeric_cols[0] if numeric_cols else None,
            }
        elif "marca" in categorical_cols:
            return {
                "chart_type": "bar",
                "x": "marca",
                "y": numeric_cols[0] if numeric_cols else None,
            }

    if "distribuição" in user_input_lower or "distribuicao" in user_input_lower:
        # Histograma ou pizza
        if numeric_cols:
            return {
                "chart_type": "histogram",
                "column": numeric_cols[0],
            }
        elif categorical_cols:
            return {
                "chart_type": "pie",
                "names": categorical_cols[0],
                "values": "count",
            }

    if "correlação" in user_input_lower or "correlacao" in user_input_lower:
        # Heatmap de correlação
        return {
            "chart_type": "heatmap",
        }

    # Padrão: gráfico de barras simples
    if categorical_cols and numeric_cols:
        return {
            "chart_type": "bar",
            "x": categorical_cols[0],
            "y": numeric_cols[0],
        }

    return None


def generate_chart_code(
    df: pd.DataFrame,
    chart_config: Dict[str, Any]
) -> str:
    """
    Gera código Python para criar o gráfico.

    Args:
        df: DataFrame do pandas
        chart_config: Configuração do gráfico

    Returns:
        String com código Python
    """
    chart_type = chart_config.get("chart_type", "bar")

    if chart_type == "bar":
        x = chart_config.get("x", "cidade")
        y = chart_config.get("y", "km_mes")
        return f"""
import plotly.express as px
fig = px.bar(df, x='{x}', y='{y}', title='{y} por {x}')
fig.show()
"""

    elif chart_type == "pie":
        names = chart_config.get("names", "status")
        values = chart_config.get("values", "count")
        return f"""
import plotly.express as px
fig = px.pie(df, names='{names}', title='Distribuição por {names}')
fig.show()
"""

    elif chart_type == "histogram":
        column = chart_config.get("column", "km_mes")
        return f"""
import plotly.express as px
fig = px.histogram(df, x='{column}', title='Distribuição de {column}')
fig.show()
"""

    return ""


def create_smart_chart(
    df: pd.DataFrame,
    user_input: str
) -> Optional[Any]:
    """
    Cria um gráfico inteligente baseado na solicitação do usuário.

    Args:
        df: DataFrame do pandas
        user_input: Texto da mensagem do usuário

    Returns:
        Objeto do gráfico ou None
    """
    try:
        from src.core.chart_generator import generate_chart_from_request

        # Detectar solicitação de gráfico
        chart_request = detect_chart_request(user_input)
        if not chart_request:
            return None

        # Sugerir configuração
        chart_config = suggest_chart_for_data(df, user_input)
        if not chart_config:
            return None

        # Gerar gráfico
        chart = generate_chart_from_request(df, **chart_config)
        return chart

    except Exception as e:
        logger.error(f"Erro ao criar gráfico inteligente: {str(e)}", exc_info=True)
        return None

