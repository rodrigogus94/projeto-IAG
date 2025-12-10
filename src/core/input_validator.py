"""
Módulo para validação de inputs do usuário antes de enviar ao modelo
"""

import logging
import re
from typing import Optional, Tuple, Dict, Any
from src.config.model_config import VALIDATION_RULES

# Configurar logger
logger = logging.getLogger(__name__)


def validate_user_input(
    user_input: str, 
    max_length: Optional[int] = None,
    min_length: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    """
    Valida input do usuário antes de enviar ao modelo.
    
    Args:
        user_input: Texto de entrada do usuário
        max_length: Comprimento máximo permitido (usa padrão se None)
        min_length: Comprimento mínimo permitido (usa padrão se None)
        
    Returns:
        Tupla (is_valid, error_message)
        - is_valid: True se válido, False caso contrário
        - error_message: Mensagem de erro se inválido, None se válido
    """
    if not user_input:
        return False, "Input não pode estar vazio"
    
    # Usar regras de validação do model_config
    rules = VALIDATION_RULES
    min_len = min_length or rules.get("min_message_length", 1)
    max_len = max_length or rules.get("max_message_length", 10000)
    
    # Validar comprimento
    input_len = len(user_input.strip())
    if input_len < min_len:
        logger.warning(f"Input muito curto: {input_len} caracteres (mínimo: {min_len})")
        return False, f"Mensagem muito curta. Mínimo: {min_len} caracteres"
    
    if input_len > max_len:
        logger.warning(f"Input muito longo: {input_len} caracteres (máximo: {max_len})")
        return False, f"Mensagem muito longa. Máximo: {max_len} caracteres"
    
    # Validar caracteres suspeitos (opcional - pode ser configurável)
    # Verificar se há apenas espaços
    if not user_input.strip():
        return False, "Input não pode conter apenas espaços"
    
    # Verificar padrões suspeitos (muitos caracteres repetidos)
    if _has_excessive_repetition(user_input):
        logger.warning("Input contém repetição excessiva de caracteres")
        return False, "Input contém muitos caracteres repetidos"
    
    logger.debug(f"Input validado com sucesso: {input_len} caracteres")
    return True, None


def _has_excessive_repetition(text: str, threshold: int = 50) -> bool:
    """
    Verifica se o texto tem repetição excessiva de caracteres.
    
    Args:
        text: Texto a verificar
        threshold: Número mínimo de caracteres repetidos consecutivos
        
    Returns:
        True se houver repetição excessiva
    """
    if len(text) < threshold:
        return False
    
    # Verificar padrões como "aaaa..." ou "1111..."
    pattern = r'(.)\1{' + str(threshold - 1) + r',}'
    return bool(re.search(pattern, text))


def validate_model_name(model_name: str) -> Tuple[bool, Optional[str]]:
    """
    Valida nome do modelo.
    
    Args:
        model_name: Nome do modelo
        
    Returns:
        Tupla (is_valid, error_message)
    """
    if not model_name or not model_name.strip():
        return False, "Nome do modelo não pode estar vazio"
    
    # Validar formato básico (pode conter letras, números, dois pontos, hífen, underscore)
    if not re.match(r'^[a-zA-Z0-9:_\-]+$', model_name):
        return False, "Nome do modelo contém caracteres inválidos"
    
    if len(model_name) > 100:
        return False, "Nome do modelo muito longo"
    
    return True, None


def sanitize_input(user_input: str) -> str:
    """
    Sanitiza input do usuário removendo caracteres problemáticos.
    
    Args:
        user_input: Texto de entrada
        
    Returns:
        Texto sanitizado
    """
    # Remover caracteres de controle (exceto quebras de linha e tabs)
    sanitized = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', user_input)
    
    # Normalizar espaços em branco múltiplos (mas manter quebras de linha)
    sanitized = re.sub(r'[ \t]+', ' ', sanitized)
    
    # Remover espaços no início e fim
    sanitized = sanitized.strip()
    
    return sanitized


def validate_messages(messages: list) -> Tuple[bool, Optional[str]]:
    """
    Valida lista de mensagens para o chat.
    
    Args:
        messages: Lista de mensagens no formato [{"role": "...", "content": "..."}]
        
    Returns:
        Tupla (is_valid, error_message)
    """
    if not messages:
        return False, "Lista de mensagens não pode estar vazia"
    
    valid_roles = {"system", "user", "assistant"}
    
    for i, msg in enumerate(messages):
        if not isinstance(msg, dict):
            return False, f"Mensagem {i} não é um dicionário"
        
        if "role" not in msg:
            return False, f"Mensagem {i} não tem campo 'role'"
        
        if "content" not in msg:
            return False, f"Mensagem {i} não tem campo 'content'"
        
        if msg["role"] not in valid_roles:
            return False, f"Role inválido na mensagem {i}: {msg['role']}"
        
        if not isinstance(msg["content"], str):
            return False, f"Content da mensagem {i} não é string"
        
        # Validar conteúdo da mensagem
        is_valid, error = validate_user_input(msg["content"])
        if not is_valid:
            return False, f"Erro na mensagem {i}: {error}"
    
    return True, None

