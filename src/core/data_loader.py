"""
Módulo para carregar e processar dados de arquivos CSV
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

# Configurar logger
logger = logging.getLogger(__name__)

# Caminho padrão para dados
DEFAULT_DATA_DIR = Path(__file__).parent.parent.parent / "dados"


def load_csv_data(filepath: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Carrega dados de um arquivo CSV.

    Args:
        filepath: Caminho para o arquivo CSV. Se None, tenta carregar dados_veiculos_300.csv

    Returns:
        DataFrame do pandas ou None se houver erro
    """
    try:
        if filepath is None:
            # Tentar carregar o arquivo padrão
            filepath = DEFAULT_DATA_DIR / "dados_veiculos_300.csv"
        else:
            filepath = Path(filepath)

        if not filepath.exists():
            logger.error(f"Arquivo não encontrado: {filepath}")
            return None

        logger.info(f"Carregando dados de: {filepath}")
        df = pd.read_csv(filepath, encoding="utf-8")

        logger.info(f"Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
        return df

    except Exception as e:
        logger.error(f"Erro ao carregar dados: {str(e)}", exc_info=True)
        return None


def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Retorna informações sobre o DataFrame.

    Args:
        df: DataFrame do pandas

    Returns:
        Dicionário com informações do dataset
    """
    if df is None or df.empty:
        return {}

    info = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_columns": list(df.select_dtypes(include=["int64", "float64"]).columns),
        "categorical_columns": list(df.select_dtypes(include=["object"]).columns),
    }

    # Estatísticas básicas para colunas numéricas
    if info["numeric_columns"]:
        info["numeric_stats"] = df[info["numeric_columns"]].describe().to_dict()

    # Valores únicos para colunas categóricas
    if info["categorical_columns"]:
        info["categorical_counts"] = {
            col: df[col].value_counts().to_dict()
            for col in info["categorical_columns"]
        }

    return info


def filter_data(
    df: pd.DataFrame, filters: Dict[str, Any]
) -> pd.DataFrame:
    """
    Filtra dados baseado em critérios.

    Args:
        df: DataFrame do pandas
        filters: Dicionário com filtros {coluna: valor}

    Returns:
        DataFrame filtrado
    """
    try:
        filtered_df = df.copy()

        for column, value in filters.items():
            if column in filtered_df.columns:
                if isinstance(value, list):
                    filtered_df = filtered_df[filtered_df[column].isin(value)]
                else:
                    filtered_df = filtered_df[filtered_df[column] == value]

        logger.info(f"Dados filtrados: {len(filtered_df)} linhas")
        return filtered_df

    except Exception as e:
        logger.error(f"Erro ao filtrar dados: {str(e)}", exc_info=True)
        return df


def get_data_summary(df: pd.DataFrame) -> str:
    """
    Retorna um resumo textual dos dados.

    Args:
        df: DataFrame do pandas

    Returns:
        String com resumo dos dados
    """
    if df is None or df.empty:
        return "Nenhum dado disponível."

    info = get_data_info(df)
    summary = f"""
## Resumo dos Dados

- **Total de registros**: {info.get('total_rows', 0)}
- **Total de colunas**: {info.get('total_columns', 0)}

### Colunas Disponíveis:
{', '.join(info.get('columns', []))}

### Colunas Numéricas:
{', '.join(info.get('numeric_columns', []))}

### Colunas Categóricas:
{', '.join(info.get('categorical_columns', []))}
"""

    return summary


def get_available_datasets() -> List[Dict[str, str]]:
    """
    Lista arquivos CSV disponíveis no diretório de dados.

    Returns:
        Lista de dicionários com informações dos datasets
    """
    datasets = []

    try:
        if DEFAULT_DATA_DIR.exists():
            csv_files = list(DEFAULT_DATA_DIR.glob("*.csv"))
            for csv_file in csv_files:
                try:
                    df = pd.read_csv(csv_file, nrows=1)  # Ler apenas primeira linha para verificar
                    datasets.append({
                        "name": csv_file.stem,
                        "path": str(csv_file),
                        "columns": list(df.columns),
                    })
                except Exception as e:
                    logger.warning(f"Erro ao ler {csv_file}: {e}")

    except Exception as e:
        logger.error(f"Erro ao listar datasets: {str(e)}")

    return datasets


def get_intelligent_data_context(df: pd.DataFrame) -> str:
    """
    Gera um contexto rico e inteligente dos dados para melhorar a compreensão do modelo.
    Inclui estatísticas detalhadas, distribuições, correlações e insights pré-calculados.

    Args:
        df: DataFrame do pandas

    Returns:
        String com contexto detalhado e inteligente dos dados
    """
    if df is None or df.empty:
        return "Nenhum dado disponível."

    try:
        context_parts = []
        
        # Informações básicas
        context_parts.append(f"📊 BASE DE DADOS: {len(df)} registros | {len(df.columns)} colunas")
        context_parts.append(f"Colunas: {', '.join(df.columns.tolist())}")
        
        # Separar colunas por tipo
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        context_parts.append(f"\n📈 COLUNAS NUMÉRICAS ({len(numeric_cols)}): {', '.join(numeric_cols)}")
        context_parts.append(f"📋 COLUNAS CATEGÓRICAS ({len(categorical_cols)}): {', '.join(categorical_cols)}")
        
        # Estatísticas detalhadas para colunas numéricas
        if numeric_cols:
            context_parts.append("\n📊 ESTATÍSTICAS NUMÉRICAS:")
            for col in numeric_cols:
                stats = df[col].describe()
                context_parts.append(
                    f"  • {col}: "
                    f"Média={stats['mean']:.2f}, "
                    f"Mediana={stats['50%']:.2f}, "
                    f"Min={stats['min']:.2f}, "
                    f"Max={stats['max']:.2f}, "
                    f"Desvio={stats['std']:.2f}"
                )
        
        # Distribuições para colunas categóricas
        if categorical_cols:
            context_parts.append("\n📋 DISTRIBUIÇÕES CATEGÓRICAS:")
            for col in categorical_cols:
                value_counts = df[col].value_counts()
                total = len(df)
                top_values = value_counts.head(5)
                context_parts.append(f"  • {col}:")
                for val, count in top_values.items():
                    pct = (count / total) * 100
                    context_parts.append(f"    - {val}: {count} ({pct:.1f}%)")
                if len(value_counts) > 5:
                    context_parts.append(f"    ... e mais {len(value_counts) - 5} valores únicos")
        
        # Correlações entre variáveis numéricas (se houver pelo menos 2)
        if len(numeric_cols) >= 2:
            try:
                corr_matrix = df[numeric_cols].corr()
                # Encontrar correlações fortes (>0.5 ou <-0.5)
                strong_corrs = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_val = corr_matrix.iloc[i, j]
                        if abs(corr_val) > 0.5:
                            strong_corrs.append(
                                (corr_matrix.columns[i], corr_matrix.columns[j], corr_val)
                            )
                
                if strong_corrs:
                    context_parts.append("\n🔗 CORRELAÇÕES FORTES (>0.5):")
                    for col1, col2, corr in strong_corrs[:5]:  # Top 5 correlações
                        context_parts.append(f"  • {col1} ↔ {col2}: {corr:.2f}")
            except Exception as e:
                logger.debug(f"Erro ao calcular correlações: {e}")
        
        # Insights pré-calculados específicos para dados de veículos
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            total = len(df)
            context_parts.append("\n💡 INSIGHTS DE STATUS:")
            for status, count in status_counts.items():
                pct = (count / total) * 100
                context_parts.append(f"  • {status.capitalize()}: {count} veículos ({pct:.1f}%)")
            if 'ativo' in status_counts:
                disponibilidade = (status_counts.get('ativo', 0) / total) * 100
                context_parts.append(f"  • Taxa de disponibilidade: {disponibilidade:.1f}%")
        
        if 'cidade' in df.columns:
            city_counts = df['cidade'].value_counts()
            context_parts.append("\n🌍 DISTRIBUIÇÃO POR CIDADE:")
            for city, count in city_counts.head(5).items():
                pct = (count / len(df)) * 100
                context_parts.append(f"  • {city}: {count} veículos ({pct:.1f}%)")
        
        if 'km_mes' in df.columns:
            km_stats = df['km_mes'].describe()
            context_parts.append("\n🚗 QUILOMETRAGEM MENSAL:")
            context_parts.append(f"  • Média: {km_stats['mean']:.0f} km/mês")
            context_parts.append(f"  • Mediana: {km_stats['50%']:.0f} km/mês")
            context_parts.append(f"  • Total: {df['km_mes'].sum():,.0f} km/mês")
        
        if 'consumo_combustivel' in df.columns:
            consumo_stats = df['consumo_combustivel'].describe()
            context_parts.append("\n⛽ CONSUMO DE COMBUSTÍVEL:")
            context_parts.append(f"  • Média: {consumo_stats['mean']:.2f} L/100km")
            context_parts.append(f"  • Melhor: {consumo_stats['min']:.2f} L/100km")
            context_parts.append(f"  • Pior: {consumo_stats['max']:.2f} L/100km")
        
        if 'custo_manutencao' in df.columns:
            custo_stats = df['custo_manutencao'].describe()
            total_custo = df['custo_manutencao'].sum()
            context_parts.append("\n💰 CUSTOS DE MANUTENÇÃO:")
            context_parts.append(f"  • Média: R$ {custo_stats['mean']:,.2f}")
            context_parts.append(f"  • Total: R$ {total_custo:,.2f}")
        
        if 'alertas' in df.columns:
            alertas_stats = df['alertas'].describe()
            total_alertas = df['alertas'].sum()
            veiculos_com_alertas = (df['alertas'] > 0).sum()
            context_parts.append("\n⚠️ ALERTAS:")
            context_parts.append(f"  • Total de alertas: {total_alertas}")
            context_parts.append(f"  • Veículos com alertas: {veiculos_com_alertas} ({veiculos_com_alertas/len(df)*100:.1f}%)")
            context_parts.append(f"  • Média por veículo: {alertas_stats['mean']:.2f}")
        
        # Valores ausentes
        missing = df.isnull().sum()
        if missing.sum() > 0:
            context_parts.append("\n⚠️ VALORES AUSENTES:")
            for col, count in missing[missing > 0].items():
                pct = (count / len(df)) * 100
                context_parts.append(f"  • {col}: {count} ({pct:.1f}%)")
        else:
            context_parts.append("\n✅ DADOS COMPLETOS: Nenhum valor ausente")
        
        # Sugestões de análises possíveis
        context_parts.append("\n💡 ANÁLISES SUGERIDAS:")
        if 'status' in df.columns and 'cidade' in df.columns:
            context_parts.append("  • Distribuição de status por cidade")
        if 'km_mes' in df.columns and 'consumo_combustivel' in df.columns:
            context_parts.append("  • Relação entre quilometragem e consumo")
        if 'custo_manutencao' in df.columns and 'status' in df.columns:
            context_parts.append("  • Custos de manutenção por status")
        if 'alertas' in df.columns:
            context_parts.append("  • Veículos com mais alertas e suas características")
        if 'marca' in df.columns:
            context_parts.append("  • Comparação de marcas (consumo, custos, alertas)")
        
        return "\n".join(context_parts)
        
    except Exception as e:
        logger.error(f"Erro ao gerar contexto inteligente: {str(e)}", exc_info=True)
        # Fallback para resumo básico
        return get_data_summary(df)

