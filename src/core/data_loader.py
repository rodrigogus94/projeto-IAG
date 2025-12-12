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

