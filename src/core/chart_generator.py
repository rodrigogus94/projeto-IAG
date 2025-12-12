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

        # Validar dados antes de criar gráfico
        if df.empty:
            logger.warning("DataFrame vazio, não é possível criar gráfico")
            return None
        
        # Limitar número de categorias se muito grande (para melhor visualização)
        if orientation == "v" and len(df) > 20:
            df = df.head(20)
            logger.info(f"Limitando gráfico a 20 categorias para melhor visualização")

        fig = px.bar(
            df,
            x=x,
            y=y,
            color=color,
            orientation=orientation,
            title=title or f"{y} por {x}",
            text=y,  # Mostrar valores nas barras
        )

        # Melhorar formatação
        fig.update_traces(
            texttemplate='%{text:.2s}',
            textposition='outside',
            hovertemplate=f'<b>%{{x}}</b><br>{y}: %{{y}}<extra></extra>'
        )
        
        fig.update_layout(
            height=500,
            showlegend=True if color else False,
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title(),
            hovermode='closest',
        )
        
        # Rotacionar labels do eixo X se necessário
        if orientation == "v" and len(df) > 5:
            fig.update_xaxes(tickangle=-45)

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

        # Validar dados
        if df.empty:
            logger.warning("DataFrame vazio, não é possível criar gráfico")
            return None
        
        # Filtrar valores zero ou negativos se necessário
        df = df[df[values] > 0].copy()
        
        if df.empty:
            logger.warning("Nenhum valor positivo encontrado para o gráfico")
            return None
        
        # Limitar número de categorias se muito grande (agrupar menores em "Outros")
        if len(df) > 10:
            df_sorted = df.sort_values(by=values, ascending=False)
            top_9 = df_sorted.head(9)
            others_sum = df_sorted.tail(len(df_sorted) - 9)[values].sum()
            
            if others_sum > 0:
                others_row = pd.DataFrame({names: ['Outros'], values: [others_sum]})
                df = pd.concat([top_9, others_row], ignore_index=True)
            else:
                df = top_9
            
            logger.info(f"Agrupando categorias menores em 'Outros' para melhor visualização")

        # Criar o gráfico
        fig = px.pie(
            df,
            values=values,
            names=names,
            title=title or f"Distribuição de {names.replace('_', ' ').title()}",
            hole=0.3,  # Donut chart - mais moderno
        )

        # Configurar layout melhorado
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>',
            marker=dict(line=dict(color='#FFFFFF', width=2))  # Borda branca para separar fatias
        )

        fig.update_layout(
            height=500,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
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
            aspect="auto",
            text_auto=True,  # Mostrar valores na matriz
        )

        fig.update_layout(
            height=600,
            xaxis_title="",
            yaxis_title="",
        )
        
        # Melhorar hover
        fig.update_traces(
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlação: %{z:.2f}<extra></extra>'
        )
        
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar heatmap: {str(e)}", exc_info=True)
        return None


def create_area_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = None,
    color: Optional[str] = None,
) -> Optional[Any]:
    """
    Cria um gráfico de área.

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

        fig = px.area(
            df,
            x=x,
            y=y,
            color=color,
            title=title or f"{y.replace('_', ' ').title()} ao longo de {x.replace('_', ' ').title()}",
        )

        fig.update_layout(
            height=500,
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title(),
            hovermode='x unified',
        )
        
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar gráfico de área: {str(e)}", exc_info=True)
        return None


def create_violin_plot(
    df: pd.DataFrame,
    x: Optional[str],
    y: str,
    title: str = None,
) -> Optional[Any]:
    """
    Cria um gráfico de violino (distribuição de densidade).

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

        fig = px.violin(
            df,
            x=x,
            y=y,
            title=title or f"Distribuição de {y.replace('_', ' ').title()}",
            box=True,  # Mostrar box plot dentro do violino
        )

        fig.update_layout(
            height=500,
            xaxis_title=x.replace('_', ' ').title() if x else "",
            yaxis_title=y.replace('_', ' ').title(),
        )
        
        return fig

    except Exception as e:
        logger.error(f"Erro ao criar gráfico de violino: {str(e)}", exc_info=True)
        return None


def display_chart(chart: Any, key: str = None) -> None:
    """
    Exibe um gráfico no Streamlit com atualização forçada.

    Args:
        chart: Objeto do gráfico (Plotly)
        key: Chave única para forçar atualização (opcional)
    """
    try:
        if chart is not None and PLOTLY_AVAILABLE:
            # Usar key única para forçar atualização do Streamlit
            import hashlib
            import time
            
            if key is None:
                # Gerar key baseada no timestamp e conteúdo do gráfico
                chart_str = str(chart.to_dict() if hasattr(chart, 'to_dict') else str(chart))
                key = hashlib.md5(f"{chart_str}{time.time()}".encode()).hexdigest()[:12]
            
            # Atualizar layout para garantir renderização
            if hasattr(chart, 'update_layout'):
                chart.update_layout(
                    autosize=True,
                    height=500,
                )
            
            # Renderizar com use_container_width para melhor responsividade
            # Usar height=None para permitir que o gráfico se ajuste automaticamente
            try:
                st.plotly_chart(
                    chart, 
                    use_container_width=True,
                    key=f"chart_{key}"
                )
            except Exception as plotly_error:
                # Fallback se houver erro com key
                logger.warning(f"Erro ao renderizar com key, tentando sem key: {plotly_error}")
                st.plotly_chart(
                    chart, 
                    use_container_width=True
                )
            logger.debug(f"Gráfico exibido com sucesso (key: {key})")
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
        chart_type: Tipo de gráfico ("bar", "line", "scatter", "pie", "histogram", "box", "heatmap", "area", "violin")
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
        elif chart_type == "area" or chart_type == "área" or chart_type == "area":
            return create_area_chart(df, **kwargs)
        elif chart_type == "violin" or chart_type == "violino":
            return create_violin_plot(df, **kwargs)
        else:
            logger.warning(f"Tipo de gráfico desconhecido: {chart_type}")
            return None

    except Exception as e:
        logger.error(f"Erro ao gerar gráfico: {str(e)}", exc_info=True)
        return None

