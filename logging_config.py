"""
Configuração centralizada de logging para a aplicação
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Diretório para logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Arquivo de log
LOG_FILE = LOG_DIR / "app.log"

# Formato de log
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    level: str = "INFO",
    log_to_file: bool = True,
    log_to_console: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """
    Configura logging para a aplicação.
    
    Args:
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Se True, salva logs em arquivo
        log_to_console: Se True, exibe logs no console
        max_bytes: Tamanho máximo do arquivo de log antes de rotacionar
        backup_count: Número de arquivos de backup a manter
    """
    # Converter string para nível de log
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configurar formato
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    # Obter logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remover handlers existentes
    root_logger.handlers.clear()
    
    # Handler para console
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # Handler para arquivo (com rotação)
    if log_to_file:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    logging.info("Logging configurado com sucesso")


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger com o nome especificado.
    
    Args:
        name: Nome do logger (geralmente __name__)
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)

