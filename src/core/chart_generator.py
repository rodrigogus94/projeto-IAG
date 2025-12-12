"""
Módulo para gerar gráficos e visualizações de dados
"""

import pandas as pd
import logging
from typing import Optional, Dict, Any, List
import streamlit as st

# Configurar logger
logger = logging.getLogger(__name__)

# Tentar importar bibliotecas de visualização
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger.warning("Plotly não disponível. Gráficos interativos não funcionarão.")

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.warning("Matplotlib/Seaborn não disponível. Alguns gráficos podem não funcionar.")


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = None,
    color: Optional[str] = None,
    orientation: str = "v",
) -> Optional[Any]:
    """
    Cria um gráfico de barras.

    Args:
        df: DataFrame do pandas
        x: Coluna para eixo X
        y: Coluna para eixo Y
        title: Título do gráfico
        color: Coluna para colorir (opcional)
        orientation: "v" (vertical) ou "h" (horizontal)

    Returns:
        Objeto do gráfico ou None
    """
    try:
        if not PLOTLY_AVAILABLE:
            logger.error("Plotly não está disponível")
            return None

        if x not in df.columns or y not in df.columns:
            logger.error(f"Colunas {x} ou {y} não encontradas no DataFrame")
            return None

        fig = px.bar(
            df,
            x=x,
            y=y,
            color=color,
            orientation=orientation,
            title=title or f"{y} por {x}",
        )

        fig.update_layout(
            height=500,
            showlegend=True if color else False,
        )

        return fig

    except Exception as e:
        logger.error(f"Erro ao criar gráfico de barras: {str(e)}", exc_info=True)
        return None


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = None,
    color: Optional[str] = None,
) -> Optional[Any]:
    """
    Cria um gráfico de linha.

    Args:
        df: DataFrame do pandas
        x: Coluna para eixo X
        y: Coluna para eixo Y
        title: Título do gráfico
        color: Coluna para colorir (opcional)

    Returns:
        Objeto do gráfico ou None
    """
    try:
        if not PLOTLY_AVAILABLE:
            return None

        if x not in df.columns or y not in df.columns:
            logger.error(f"Colunas {x} ou {y} não encontradas")
            return None

        fig = px.line(
            df,
            x=x,
            y=y,
            color=color,
            title=title or f"{y} ao longo de {x}",
        )

        fig.update_layout(height=500)
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar gráfico de linha: {str(e)}", exc_info=True)
        return None


def create_scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = None,
    color: Optional[str] = None,
    size: Optional[str] = None,
) -> Optional[Any]:
    """
    Cria um gráfico de dispersão.

    Args:
        df: DataFrame do pandas
        x: Coluna para eixo X
        y: Coluna para eixo Y
        title: Título do gráfico
        color: Coluna para colorir (opcional)
        size: Coluna para tamanho dos pontos (opcional)

    Returns:
        Objeto do gráfico ou None
    """
    try:
        if not PLOTLY_AVAILABLE:
            return None

        if x not in df.columns or y not in df.columns:
            logger.error(f"Colunas {x} ou {y} não encontradas")
            return None

        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=color,
            size=size,
            title=title or f"{y} vs {x}",
        )

        fig.update_layout(height=500)
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar gráfico de dispersão: {str(e)}", exc_info=True)
        return None


def create_pie_chart(
    df: pd.DataFrame,
    values: str,
    names: str,
    title: str = None,
) -> Optional[Any]:
    """
    Cria um gráfico de pizza.

    Args:
        df: DataFrame do pandas
        values: Coluna com valores
        names: Coluna com nomes/categorias
        title: Título do gráfico

    Returns:
        Objeto do gráfico ou None
    """
    try:
        if not PLOTLY_AVAILABLE:
            logger.error("Plotly não disponível")
            return None

        # Verificar se as colunas existem
        if values not in df.columns:
            logger.error(f"Coluna {values} não encontrada no DataFrame")
            logger.error(f"Colunas disponíveis: {df.columns.tolist()}")
            return None
            
        if names not in df.columns:
            logger.error(f"Coluna {names} não encontrada no DataFrame")
            logger.error(f"Colunas disponíveis: {df.columns.tolist()}")
            return None

        # Criar o gráfico
        fig = px.pie(
            df,
            values=values,
            names=names,
            title=title or f"Distribuição de {names}",
            hole=0.3,  # Donut chart - mais moderno
        )

        # Configurar layout
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>'
        )

        fig.update_layout(
            height=500,
            showlegend=True,
        )

        return fig

    except Exception as e:
        logger.error(f"Erro ao criar gráfico de pizza: {str(e)}", exc_info=True)
        return None
def create_histogram(
    df: pd.DataFrame,
    column: str,
    title: str = None,
    bins: int = 30,
) -> Optional[Any]:
    """
    Cria um histograma.

    Args:
        df: DataFrame do pandas
        column: Coluna para histograma
        title: Título do gráfico
        bins: Número de bins

    Returns:
        Objeto do gráfico ou None
    """
    try:
        if not PLOTLY_AVAILABLE:
            return None

        if column not in df.columns:
            logger.error(f"Coluna {column} não encontrada")
            return None

        fig = px.histogram(
            df,
            x=column,
            nbins=bins,
            title=title or f"Distribuição de {column}",
        )

        fig.update_layout(height=500)
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar histograma: {str(e)}", exc_info=True)
        return None


def create_box_plot(
    df: pd.DataFrame,
    x: Optional[str],
    y: str,
    title: str = None,
) -> Optional[Any]:
    """
    Cria um box plot.

    Args:
        df: DataFrame do pandas
        x: Coluna categórica (opcional)
        y: Coluna numérica
        title: Título do gráfico

    Returns:
        Objeto do gráfico ou None
    """
    try:
        if not PLOTLY_AVAILABLE:
            return None

        if y not in df.columns:
            logger.error(f"Coluna {y} não encontrada")
            return None

        fig = px.box(
            df,
            x=x,
            y=y,
            title=title or f"Box Plot de {y}",
        )

        fig.update_layout(height=500)
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar box plot: {str(e)}", exc_info=True)
        return None


def create_heatmap(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    title: str = None,
) -> Optional[Any]:
    """
    Cria um mapa de calor de correlação.

    Args:
        df: DataFrame do pandas
        columns: Lista de colunas (usa todas numéricas se None)
        title: Título do gráfico

    Returns:
        Objeto do gráfico ou None
    """
    try:
        if not PLOTLY_AVAILABLE:
            return None

        # Selecionar apenas colunas numéricas
        numeric_df = df.select_dtypes(include=["int64", "float64"])
        
        if columns:
            numeric_df = numeric_df[[col for col in columns if col in numeric_df.columns]]

        if numeric_df.empty:
            logger.error("Nenhuma coluna numérica encontrada")
            return None

        # Calcular correlação
        corr_matrix = numeric_df.corr()

        fig = px.imshow(
            corr_matrix,
            labels=dict(x="Variável", y="Variável", color="Correlação"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale="RdBu",
            title=title or "Matriz de Correlação",
        )

        fig.update_layout(height=600)
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar heatmap: {str(e)}", exc_info=True)
        return None


def display_chart(chart: Any) -> None:
    """
    Exibe um gráfico no Streamlit.

    Args:
        chart: Objeto do gráfico (Plotly)
    """
    try:
        if chart is not None and PLOTLY_AVAILABLE:
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.warning("Gráfico não disponível ou biblioteca não instalada")
    except Exception as e:
        logger.error(f"Erro ao exibir gráfico: {str(e)}", exc_info=True)
        st.error(f"Erro ao exibir gráfico: {str(e)}")


def generate_chart_from_request(
    df: pd.DataFrame,
    chart_type: str,
    **kwargs
) -> Optional[Any]:
    """
    Gera um gráfico baseado em uma requisição.

    Args:
        df: DataFrame do pandas
        chart_type: Tipo de gráfico ("bar", "line", "scatter", "pie", "histogram", "box", "heatmap")
        **kwargs: Parâmetros específicos do gráfico

    Returns:
        Objeto do gráfico ou None
    """
    chart_type = chart_type.lower()

    try:
        if chart_type == "bar" or chart_type == "barras":
            return create_bar_chart(df, **kwargs)
        elif chart_type == "line" or chart_type == "linha":
            return create_line_chart(df, **kwargs)
        elif chart_type == "scatter" or chart_type == "dispersao":
            return create_scatter_chart(df, **kwargs)
        elif chart_type == "pie" or chart_type == "pizza":
            return create_pie_chart(df, **kwargs)
        elif chart_type == "histogram" or chart_type == "histograma":
            return create_histogram(df, **kwargs)
        elif chart_type == "box" or chart_type == "boxplot":
            return create_box_plot(df, **kwargs)
        elif chart_type == "heatmap" or chart_type == "mapa_calor":
            return create_heatmap(df, **kwargs)
        else:
            logger.warning(f"Tipo de gráfico desconhecido: {chart_type}")
            return None

    except Exception as e:
        logger.error(f"Erro ao gerar gráfico: {str(e)}", exc_info=True)
        return None

