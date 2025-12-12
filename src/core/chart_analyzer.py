"""
Módulo para analisar requisições do usuário e gerar gráficos automaticamente
"""

import re
import logging
from typing import Optional, Dict, Any, List, Tuple
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
        "area": ["área", "area", "area chart", "área preenchida"],
        "violin": ["violino", "violin", "violin plot", "densidade"],
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
    
    # Mapeamento expandido de termos comuns para colunas
    term_mapping = {
        "quilometragem": "km_mes",
        "km": "km_mes",
        "quilometragem mensal": "km_mes",
        "quilometragem por mês": "km_mes",
        "velocidade": "velocidade_media",
        "velocidade média": "velocidade_media",
        "consumo": "consumo_combustivel",
        "combustível": "consumo_combustivel",
        "combustivel": "consumo_combustivel",
        "consumo de combustível": "consumo_combustivel",
        "consumo de combustivel": "consumo_combustivel",
        "custo": "custo_manutencao",
        "manutenção": "custo_manutencao",
        "manutencao": "custo_manutencao",
        "custo de manutenção": "custo_manutencao",
        "custo de manutencao": "custo_manutencao",
        "dias": "dias_operacionais",
        "operacionais": "dias_operacionais",
        "dias operacionais": "dias_operacionais",
    }

    user_input_lower = user_input.lower()
    found_columns = []

    # Primeiro, verificar mapeamentos de termos (ordem por tamanho para pegar termos mais específicos primeiro)
    sorted_mapping = sorted(term_mapping.items(), key=lambda x: len(x[0]), reverse=True)
    for term, col in sorted_mapping:
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


def detect_aggregation(user_input: str) -> Optional[str]:
    """
    Detecta qual tipo de agregação o usuário quer (soma, média, contagem, máximo, mínimo).
    
    Args:
        user_input: Texto da mensagem do usuário
        
    Returns:
        Tipo de agregação ('sum', 'mean', 'count', 'max', 'min') ou None
    """
    user_input_lower = user_input.lower()
    
    aggregation_keywords = {
        'sum': ['soma', 'total', 'somado', 'somar', 'soma de', 'total de'],
        'mean': ['média', 'media', 'médio', 'medio', 'média de', 'media de', 'médio de', 'medio de', 'average', 'avg'],
        'count': ['contar', 'quantidade', 'número', 'numero', 'qtd', 'qtde', 'count', 'quantos', 'quantas'],
        'max': ['máximo', 'maximo', 'maior', 'mais alto', 'peak', 'pico', 'max'],
        'min': ['mínimo', 'minimo', 'menor', 'mais baixo', 'min'],
    }
    
    # Verificar cada tipo de agregação
    for agg_type, keywords in aggregation_keywords.items():
        if any(keyword in user_input_lower for keyword in keywords):
            return agg_type
    
    return None


def validate_data_for_chart(df: pd.DataFrame, required_cols: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Valida se os dados são adequados para gerar um gráfico.
    
    Args:
        df: DataFrame do pandas
        required_cols: Lista de colunas necessárias
        
    Returns:
        Tupla (is_valid, error_message)
    """
    if df is None:
        return False, "DataFrame é None"
    
    if df.empty:
        return False, "DataFrame está vazio"
    
    # Verificar se todas as colunas necessárias existem
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return False, f"Colunas não encontradas: {', '.join(missing_cols)}"
    
    # Verificar se há dados suficientes
    if len(df) < 1:
        return False, "Não há dados suficientes para gerar o gráfico"
    
    # Verificar se há valores válidos nas colunas numéricas
    numeric_cols = [col for col in required_cols if col in df.select_dtypes(include=["int64", "float64"]).columns]
    for col in numeric_cols:
        if df[col].isna().all():
            return False, f"Coluna {col} contém apenas valores nulos"
        if (df[col] == 0).all() and col not in ['alertas', 'dias_operacionais']:  # Permitir zeros em algumas colunas
            logger.warning(f"Coluna {col} contém apenas zeros")
    
    return True, None


def clean_data_for_chart(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Limpa dados para preparar para visualização.
    
    Args:
        df: DataFrame do pandas
        columns: Lista de colunas a processar
        
    Returns:
        DataFrame limpo
    """
    df_clean = df.copy()
    
    # Remover linhas com valores nulos críticos
    for col in columns:
        if col in df_clean.columns:
            # Para colunas categóricas, remover apenas se todas forem nulas
            if df_clean[col].dtype == 'object':
                df_clean = df_clean[df_clean[col].notna()]
            # Para colunas numéricas, preencher com 0 ou remover dependendo do caso
            elif df_clean[col].dtype in ['int64', 'float64']:
                # Preencher nulos com 0 para colunas numéricas (ou média se preferir)
                df_clean[col] = df_clean[col].fillna(0)
    
    return df_clean


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
        # Validação inicial
        if df is None or df.empty:
            logger.warning("DataFrame vazio ou None, não é possível criar gráfico")
            return None
        from src.core.chart_generator import (
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
            
            # Validar dados
            is_valid, error_msg = validate_data_for_chart(df, [category_col])
            if not is_valid:
                logger.warning(f"Validação falhou para gráfico de pizza: {error_msg}")
                return None
            
            # Limpar dados
            df_clean = clean_data_for_chart(df, [category_col])
            
            # Agrupar e contar
            df_grouped = df_clean[category_col].value_counts().reset_index()
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
            
            # Detectar tipo de agregação
            aggregation = detect_aggregation(user_input)
            
            # Detectar coluna categórica (X) - melhor inferência
            x_col = None
            categorical_cols = [c for c in df.select_dtypes(include=["object"]).columns if c != "id_veiculo"]
            
            # Prioridade: colunas mencionadas > padrões comuns > primeira disponível
            for col in ["cidade", "marca", "status", "modelo"]:
                if col in user_input_lower or col in columns:
                    if col in df.columns:
                        x_col = col
                        break
            
            if not x_col:
                # Verificar outras colunas categóricas mencionadas
                for col in categorical_cols:
                    if col in user_input_lower or col in columns:
                        x_col = col
                        break
            
            if not x_col and categorical_cols:
                # Usar primeira coluna categórica disponível
                x_col = categorical_cols[0]
            
            # Detectar coluna numérica (Y) - melhor inferência
            y_col = None
            numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
            
            # Prioridade: colunas mencionadas > padrões comuns > primeira disponível
            numeric_priority = ["km_mes", "consumo_combustivel", "custo_manutencao", 
                              "velocidade_media", "alertas", "dias_operacionais"]
            
            for col in numeric_priority:
                if col in user_input_lower or col in columns:
                    if col in df.columns:
                        y_col = col
                        break
            
            if not y_col:
                # Verificar outras colunas numéricas mencionadas
                for col in numeric_cols:
                    if col in user_input_lower or col in columns:
                        y_col = col
                        break
            
            if not y_col and numeric_cols:
                # Usar primeira coluna numérica disponível
                y_col = numeric_cols[0]
            
            if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
                logger.warning(f"Colunas não encontradas: x={x_col}, y={y_col}. Colunas disponíveis: {list(df.columns)}")
                return None
            
            # Validar dados
            is_valid, error_msg = validate_data_for_chart(df, [x_col, y_col])
            if not is_valid:
                logger.warning(f"Validação falhou para gráfico de barras: {error_msg}")
                return None
            
            # Limpar dados
            df_clean = clean_data_for_chart(df, [x_col, y_col])
            
            # Agrupar dados com agregação apropriada
            if aggregation == "count" or "contar" in user_input_lower or "quantidade" in user_input_lower:
                # Contar ocorrências
                df_grouped = df_clean.groupby(x_col).size().reset_index(name="quantidade")
                y_col = "quantidade"
                title_suffix = "Quantidade"
            elif aggregation == "mean" or "média" in user_input_lower or "media" in user_input_lower:
                # Média
                df_grouped = df_clean.groupby(x_col)[y_col].mean().reset_index()
                title_suffix = f"Média de {y_col.replace('_', ' ').title()}"
            elif aggregation == "max" or "máximo" in user_input_lower or "maximo" in user_input_lower:
                # Máximo
                df_grouped = df_clean.groupby(x_col)[y_col].max().reset_index()
                title_suffix = f"Máximo de {y_col.replace('_', ' ').title()}"
            elif aggregation == "min" or "mínimo" in user_input_lower or "minimo" in user_input_lower:
                # Mínimo
                df_grouped = df_clean.groupby(x_col)[y_col].min().reset_index()
                title_suffix = f"Mínimo de {y_col.replace('_', ' ').title()}"
            else:
                # Padrão: somar valores numéricos por categoria
                df_grouped = df_clean.groupby(x_col)[y_col].sum().reset_index()
                title_suffix = f"Total de {y_col.replace('_', ' ').title()}"
            
            # Ordenar por valor (maior para menor) para melhor visualização
            df_grouped = df_grouped.sort_values(by=y_col, ascending=False)
            
            logger.info(f"Criando gráfico de barras: {x_col} x {y_col} ({len(df_grouped)} grupos, agregação: {aggregation or 'sum'})")
            
            return create_bar_chart(
                df_grouped,
                x=x_col,
                y=y_col,
                title=f"{title_suffix} por {x_col.title()}"
            )
        
        elif chart_type == "histogram":
            # Para histograma, usar coluna numérica
            columns = chart_request.get("columns", [])
            numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
            
            column = None
            for col in ["km_mes", "consumo_combustivel", "custo_manutencao", "velocidade_media"]:
                if col in user_input_lower or col in columns:
                    if col in df.columns:
                        column = col
                        break
            
            if not column and numeric_cols:
                column = numeric_cols[0]
            
            if not column or column not in df.columns:
                return None
            
            return create_histogram(
                df,
                column=column,
                title=f"Distribuição de {column.replace('_', ' ').title()}"
            )
        
        elif chart_type == "line" or chart_type == "linha":
            # Para gráfico de linha, detectar colunas
            columns = chart_request.get("columns", [])
            numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
            categorical_cols = [c for c in df.select_dtypes(include=["object"]).columns if c != "id_veiculo"]
            
            # Detectar eixo X (temporal ou categórico)
            x_col = None
            for col in ["ano", "cidade", "marca", "status"]:
                if col in user_input_lower or col in columns:
                    if col in df.columns:
                        x_col = col
                        break
            
            if not x_col and categorical_cols:
                x_col = categorical_cols[0]
            
            # Detectar eixo Y (numérico)
            y_col = None
            for col in ["km_mes", "consumo_combustivel", "custo_manutencao", "velocidade_media"]:
                if col in user_input_lower or col in columns:
                    if col in df.columns:
                        y_col = col
                        break
            
            if not y_col and numeric_cols:
                y_col = numeric_cols[0]
            
            if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
                return None
            
            # Agrupar se necessário
            if x_col in categorical_cols:
                aggregation = detect_aggregation(user_input)
                if aggregation == "mean":
                    df_grouped = df.groupby(x_col)[y_col].mean().reset_index()
                elif aggregation == "sum":
                    df_grouped = df.groupby(x_col)[y_col].sum().reset_index()
                else:
                    df_grouped = df.groupby(x_col)[y_col].mean().reset_index()
            else:
                df_grouped = df.sort_values(by=x_col)
            
            return create_line_chart(
                df_grouped,
                x=x_col,
                y=y_col,
                title=f"{y_col.replace('_', ' ').title()} por {x_col.replace('_', ' ').title()}"
            )
        
        elif chart_type == "scatter" or chart_type == "dispersao":
            # Para gráfico de dispersão, precisa de duas colunas numéricas
            columns = chart_request.get("columns", [])
            numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
            
            x_col = None
            y_col = None
            
            # Detectar colunas mencionadas
            for col in numeric_cols:
                if col in user_input_lower or col in columns:
                    if not x_col:
                        x_col = col
                    elif not y_col:
                        y_col = col
                        break
            
            if not x_col or not y_col:
                if len(numeric_cols) >= 2:
                    x_col = numeric_cols[0]
                    y_col = numeric_cols[1]
                else:
                    return None
            
            if x_col not in df.columns or y_col not in df.columns:
                return None
            
            return create_scatter_chart(
                df,
                x=x_col,
                y=y_col,
                title=f"{y_col.replace('_', ' ').title()} vs {x_col.replace('_', ' ').title()}"
            )
        
        elif chart_type == "box" or chart_type == "boxplot":
            # Para box plot, precisa de coluna numérica e opcionalmente categórica
            columns = chart_request.get("columns", [])
            numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
            categorical_cols = [c for c in df.select_dtypes(include=["object"]).columns if c != "id_veiculo"]
            
            y_col = None
            for col in numeric_cols:
                if col in user_input_lower or col in columns:
                    y_col = col
                    break
            
            if not y_col and numeric_cols:
                y_col = numeric_cols[0]
            
            x_col = None
            for col in ["marca", "status", "cidade"]:
                if col in user_input_lower or col in columns:
                    if col in df.columns:
                        x_col = col
                        break
            
            if not x_col and categorical_cols:
                x_col = categorical_cols[0]
            
            if not y_col or y_col not in df.columns:
                return None
            
            return create_box_plot(
                df,
                x=x_col,
                y=y_col,
                title=f"Distribuição de {y_col.replace('_', ' ').title()}" + (f" por {x_col.replace('_', ' ').title()}" if x_col else "")
            )
        
        elif chart_type == "area" or chart_type == "área":
            # Similar ao gráfico de linha, mas com área preenchida
            columns = chart_request.get("columns", [])
            numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
            categorical_cols = [c for c in df.select_dtypes(include=["object"]).columns if c != "id_veiculo"]
            
            x_col = None
            for col in ["ano", "cidade", "marca"]:
                if col in user_input_lower or col in columns:
                    if col in df.columns:
                        x_col = col
                        break
            
            if not x_col and categorical_cols:
                x_col = categorical_cols[0]
            
            y_col = None
            for col in numeric_cols:
                if col in user_input_lower or col in columns:
                    y_col = col
                    break
            
            if not y_col and numeric_cols:
                y_col = numeric_cols[0]
            
            if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
                return None
            
            # Agrupar se necessário
            if x_col in categorical_cols:
                aggregation = detect_aggregation(user_input)
                if aggregation == "mean":
                    df_grouped = df.groupby(x_col)[y_col].mean().reset_index()
                elif aggregation == "sum":
                    df_grouped = df.groupby(x_col)[y_col].sum().reset_index()
                else:
                    df_grouped = df.groupby(x_col)[y_col].sum().reset_index()
            else:
                df_grouped = df.sort_values(by=x_col)
            
            return create_area_chart(
                df_grouped,
                x=x_col,
                y=y_col,
                title=f"{y_col.replace('_', ' ').title()} por {x_col.replace('_', ' ').title()}"
            )
        
        elif chart_type == "violin" or chart_type == "violino":
            # Similar ao box plot, mas mostra distribuição de densidade
            columns = chart_request.get("columns", [])
            numeric_cols = list(df.select_dtypes(include=["int64", "float64"]).columns)
            categorical_cols = [c for c in df.select_dtypes(include=["object"]).columns if c != "id_veiculo"]
            
            y_col = None
            for col in numeric_cols:
                if col in user_input_lower or col in columns:
                    y_col = col
                    break
            
            if not y_col and numeric_cols:
                y_col = numeric_cols[0]
            
            x_col = None
            for col in ["marca", "status", "cidade"]:
                if col in user_input_lower or col in columns:
                    if col in df.columns:
                        x_col = col
                        break
            
            if not x_col and categorical_cols:
                x_col = categorical_cols[0]
            
            if not y_col or y_col not in df.columns:
                return None
            
            return create_violin_plot(
                df,
                x=x_col,
                y=y_col,
                title=f"Distribuição de Densidade de {y_col.replace('_', ' ').title()}" + (f" por {x_col.replace('_', ' ').title()}" if x_col else "")
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

