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
    
    IMPORTANTE: Só detecta se houver solicitação EXPLÍCITA de gráfico/visualização.

    Args:
        user_input: Texto da mensagem do usuário

    Returns:
        Dicionário com informações do gráfico ou None
    """
    user_input_lower = user_input.lower()

    # Palavras-chave EXPLÍCITAS para detectar solicitação de gráfico
    # Removidas palavras genéricas como "análise", "estatística" que não indicam gráfico
    explicit_chart_keywords = [
        "gráfico", "grafico", "chart", "visualização", "visualizacao",
        "plot", "gráfico de", "chart de", "visualização de",
        "mostre um gráfico", "exiba um gráfico", "crie um gráfico", "gere um gráfico",
        "mostre gráfico", "exiba gráfico", "crie gráfico", "gere gráfico",
        "mostre chart", "exiba chart", "crie chart", "gere chart",
        "mostre visualização", "exiba visualização", "crie visualização", "gere visualização",
        "dashboard"  # Dashboard geralmente implica visualização
    ]
    
    # Palavras que indicam ação de visualização quando combinadas
    action_keywords = ["mostre", "exiba", "crie", "gere", "faça", "construa"]
    visualization_keywords = ["gráfico", "grafico", "chart", "visualização", "visualizacao", "plot"]

    # Verificar se contém palavras-chave explícitas
    has_explicit_keyword = any(keyword in user_input_lower for keyword in explicit_chart_keywords)
    
    # Verificar combinação de ação + visualização (ex: "mostre um gráfico")
    has_action_visualization = False
    for action in action_keywords:
        for viz in visualization_keywords:
            if action in user_input_lower and viz in user_input_lower:
                has_action_visualization = True
                break
        if has_action_visualization:
            break

    # Só retornar se houver solicitação EXPLÍCITA
    if not (has_explicit_keyword or has_action_visualization):
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
    
    # Mapeamento de termos comuns para colunas
    term_mapping = {
        "quilometragem": "km_mes",
        "km": "km_mes",
        "quilometragem mensal": "km_mes",
        "velocidade": "velocidade_media",
        "consumo": "consumo_combustivel",
        "combustível": "consumo_combustivel",
        "combustivel": "consumo_combustivel",
        "custo": "custo_manutencao",
        "manutenção": "custo_manutencao",
        "manutencao": "custo_manutencao",
        "dias": "dias_operacionais",
        "operacionais": "dias_operacionais",
    }

    user_input_lower = user_input.lower()
    found_columns = []

    # Primeiro, verificar mapeamentos de termos
    for term, col in term_mapping.items():
        if term in user_input_lower and col not in found_columns:
            found_columns.append(col)

    # Depois, buscar colunas diretamente
    for col in known_columns:
        if col in found_columns:
            continue
            
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
        from src.core.chart_generator import (
            create_bar_chart, 
            create_pie_chart, 
            create_histogram,
            create_line_chart,
            create_scatter_chart,
            create_box_plot,
            create_heatmap
        )

        # Detectar solicitação de gráfico
        chart_request = detect_chart_request(user_input)
        if not chart_request:
            return None

        chart_type = chart_request.get("chart_type", "bar")
        user_input_lower = user_input.lower()
        
        # Processar dados baseado no tipo de gráfico solicitado
        if chart_type == "pie" or "pizza" in user_input_lower or "distribuição" in user_input_lower:
            # Para gráfico de pizza, agrupar por categoria e contar
            columns = chart_request.get("columns", [])
            if columns:
                category_col = columns[0]
            elif "status" in user_input_lower:
                category_col = "status"
            elif "cidade" in user_input_lower:
                category_col = "cidade"
            elif "marca" in user_input_lower:
                category_col = "marca"
            else:
                # Usar primeira coluna categórica (excluindo id_veiculo)
                categorical_cols = [c for c in df.select_dtypes(include=["object"]).columns if c != "id_veiculo"]
                if categorical_cols:
                    category_col = categorical_cols[0]
                else:
                    return None
            
            if category_col not in df.columns:
                return None
            
            # Agrupar e contar
            df_grouped = df[category_col].value_counts().reset_index()
            df_grouped.columns = [category_col, "count"]
            
            logger.info(f"Criando gráfico de pizza: {category_col} ({len(df_grouped)} categorias)")
            
            return create_pie_chart(
                df_grouped,
                values="count",
                names=category_col,
                title=f"Distribuição de Veículos por {category_col.title()}"
            )
        
        elif chart_type == "bar" or chart_type == "barras":
            # Para gráfico de barras, detectar colunas
            columns = chart_request.get("columns", [])
            user_input_lower = user_input.lower()
            
            # Detectar coluna categórica (X)
            if "cidade" in user_input_lower or "cidade" in columns:
                x_col = "cidade"
            elif "marca" in user_input_lower or "marca" in columns:
                x_col = "marca"
            elif "status" in user_input_lower or "status" in columns:
                x_col = "status"
            elif "modelo" in user_input_lower or "modelo" in columns:
                x_col = "modelo"
            else:
                # Usar colunas categóricas disponíveis (excluindo id_veiculo)
                categorical_cols = [c for c in df.select_dtypes(include=["object"]).columns if c != "id_veiculo"]
                x_col = categorical_cols[0] if categorical_cols else None
            
            # Detectar coluna numérica (Y)
            if "km_mes" in user_input_lower or "km_mes" in columns or "quilometragem" in user_input_lower or "km" in user_input_lower:
                y_col = "km_mes"
            elif "consumo" in user_input_lower or "consumo_combustivel" in columns:
                y_col = "consumo_combustivel"
            elif "custo" in user_input_lower or "custo_manutencao" in columns:
                y_col = "custo_manutencao"
            elif "velocidade" in user_input_lower or "velocidade_media" in columns:
                y_col = "velocidade_media"
            elif "alertas" in user_input_lower or "alertas" in columns:
                y_col = "alertas"
            elif "dias" in user_input_lower or "dias_operacionais" in columns:
                y_col = "dias_operacionais"
            else:
                # Usar primeira coluna numérica disponível
                numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
                y_col = numeric_cols[0] if numeric_cols else None
            
            if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
                logger.warning(f"Colunas não encontradas: x={x_col}, y={y_col}. Colunas disponíveis: {list(df.columns)}")
                return None
            
            # SEMPRE agrupar dados para gráficos de barras
            # Agrupar por categoria e agregar valores numéricos
            if "contar" in user_input_lower or "quantidade" in user_input_lower or "total de" in user_input_lower:
                # Contar ocorrências
                df_grouped = df.groupby(x_col).size().reset_index(name=y_col)
            else:
                # Somar valores numéricos por categoria
                df_grouped = df.groupby(x_col)[y_col].sum().reset_index()
            
            logger.info(f"Criando gráfico de barras: {x_col} x {y_col} ({len(df_grouped)} grupos)")
            
            return create_bar_chart(
                df_grouped,
                x=x_col,
                y=y_col,
                title=f"{y_col.replace('_', ' ').title()} por {x_col.title()}"
            )
        
        elif chart_type == "histogram":
            # Para histograma, usar coluna numérica
            columns = chart_request.get("columns", [])
            if "km_mes" in user_input_lower or "km_mes" in columns:
                column = "km_mes"
            elif "consumo" in user_input_lower:
                column = "consumo_combustivel"
            else:
                numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
                column = numeric_cols[0] if numeric_cols else None
            
            if not column or column not in df.columns:
                return None
            
            return create_histogram(
                df,
                column=column,
                title=f"Distribuição de {column.replace('_', ' ').title()}"
            )
        
        # Outros tipos de gráfico
        chart_config = suggest_chart_for_data(df, user_input)
        if chart_config:
            from src.core.chart_generator import generate_chart_from_request
            return generate_chart_from_request(df, chart_config.get("chart_type", "bar"), **chart_config)
        
        return None

    except Exception as e:
        logger.error(f"Erro ao criar gráfico inteligente: {str(e)}", exc_info=True)
        return None

