"""
Módulo para gerenciar persistência do histórico de conversas
"""

import json
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Configurar logger
logger = logging.getLogger(__name__)

# Diretório padrão para salvar históricos (relativo à raiz do projeto)
HISTORY_DIR = Path("data/chat_history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def save_history(messages: List[Dict[str, str]], session_id: Optional[str] = None) -> str:
    """
    Salva histórico de mensagens em arquivo JSON.
    
    Args:
        messages: Lista de mensagens no formato [{"role": "...", "content": "..."}]
        session_id: ID da sessão (gera automaticamente se None)
        
    Returns:
        Caminho do arquivo salvo
    """
    try:
        if not session_id:
            # Gerar ID baseado em timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = f"session_{timestamp}"
        
        filename = f"{session_id}.json"
        filepath = HISTORY_DIR / filename
        
        # Preparar dados para salvar
        history_data = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "message_count": len(messages),
            "messages": messages
        }
        
        # Salvar em arquivo
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Histórico salvo: {filepath} ({len(messages)} mensagens)")
        return str(filepath)
        
    except Exception as e:
        logger.error(f"Erro ao salvar histórico: {str(e)}", exc_info=True)
        raise


def load_history(session_id: str) -> Optional[List[Dict[str, str]]]:
    """
    Carrega histórico de mensagens de um arquivo.
    
    Args:
        session_id: ID da sessão ou nome do arquivo (sem extensão)
        
    Returns:
        Lista de mensagens ou None se não encontrado
    """
    try:
        # Adicionar extensão se não tiver
        if not session_id.endswith(".json"):
            session_id = f"{session_id}.json"
        
        filepath = HISTORY_DIR / session_id
        
        if not filepath.exists():
            logger.warning(f"Arquivo de histórico não encontrado: {filepath}")
            return None
        
        with open(filepath, "r", encoding="utf-8") as f:
            history_data = json.load(f)
        
        messages = history_data.get("messages", [])
        logger.info(f"Histórico carregado: {filepath} ({len(messages)} mensagens)")
        return messages
        
    except Exception as e:
        logger.error(f"Erro ao carregar histórico: {str(e)}", exc_info=True)
        return None


def list_history_sessions() -> List[Dict[str, Any]]:
    """
    Lista todas as sessões de histórico disponíveis.
    
    Returns:
        Lista de dicionários com informações das sessões
    """
    try:
        sessions = []
        
        if not HISTORY_DIR.exists():
            return sessions
        
        for filepath in HISTORY_DIR.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    history_data = json.load(f)
                
                sessions.append({
                    "session_id": history_data.get("session_id", filepath.stem),
                    "filename": filepath.name,
                    "created_at": history_data.get("created_at"),
                    "updated_at": history_data.get("updated_at"),
                    "message_count": history_data.get("message_count", 0),
                    "filepath": str(filepath)
                })
            except Exception as e:
                logger.warning(f"Erro ao ler arquivo {filepath}: {e}")
                continue
        
        # Ordenar por data de atualização (mais recente primeiro)
        sessions.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        
        logger.debug(f"Encontradas {len(sessions)} sessões de histórico")
        return sessions
        
    except Exception as e:
        logger.error(f"Erro ao listar sessões: {str(e)}", exc_info=True)
        return []


def delete_history(session_id: str) -> bool:
    """
    Deleta um arquivo de histórico.
    
    Args:
        session_id: ID da sessão ou nome do arquivo (sem extensão)
        
    Returns:
        True se deletado com sucesso, False caso contrário
    """
    try:
        # Adicionar extensão se não tiver
        if not session_id.endswith(".json"):
            session_id = f"{session_id}.json"
        
        filepath = HISTORY_DIR / session_id
        
        if not filepath.exists():
            logger.warning(f"Arquivo não encontrado para deletar: {filepath}")
            return False
        
        filepath.unlink()
        logger.info(f"Histórico deletado: {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao deletar histórico: {str(e)}", exc_info=True)
        return False


def auto_save_history(messages: List[Dict[str, str]], session_id: str = "current") -> None:
    """
    Salva histórico automaticamente (para uso em app.py).
    
    Args:
        messages: Lista de mensagens
        session_id: ID da sessão atual
    """
    try:
        if not messages:
            return
        
        # Salvar apenas se houver mensagens
        save_history(messages, session_id)
    except Exception as e:
        # Não falhar silenciosamente, mas logar o erro
        logger.warning(f"Erro no auto-save: {str(e)}")

