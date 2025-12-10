"""
Módulo para transcrição de áudio usando Whisper ou APIs alternativas
"""
import os
import tempfile
import logging
from typing import Optional
from contextlib import contextmanager

# Configurar logger
logger = logging.getLogger(__name__)


@contextmanager
def _temp_audio_file(audio_file, suffix=".wav"):
    """
    Context manager para criar e limpar arquivo temporário de áudio.
    Garante limpeza mesmo em caso de erro.
    
    Args:
        audio_file: Arquivo de áudio (BytesIO ou similar)
        suffix: Sufixo do arquivo temporário
        
    Yields:
        Caminho do arquivo temporário
    """
    tmp_path = None
    try:
        # Resetar posição do arquivo se possível
        if hasattr(audio_file, 'seek'):
            audio_file.seek(0)
        
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        logger.debug(f"Arquivo temporário criado: {tmp_path}")
        yield tmp_path
    finally:
        # Sempre limpar o arquivo temporário
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
                logger.debug(f"Arquivo temporário removido: {tmp_path}")
            except Exception as e:
                logger.warning(f"Erro ao remover arquivo temporário {tmp_path}: {e}")


def transcribe_audio(audio_file, method: str = "whisper") -> Optional[str]:
    """
    Transcreve um arquivo de áudio para texto.
    
    Args:
        audio_file: Arquivo de áudio (BytesIO ou similar)
        method: Método de transcrição ("whisper" ou "openai")
        
    Returns:
        Texto transcrito ou None em caso de erro
    """
    try:
        logger.info(f"Iniciando transcrição com método: {method}")
        if method == "whisper":
            return _transcribe_with_whisper(audio_file)
        elif method == "openai":
            return _transcribe_with_openai(audio_file)
        else:
            logger.warning(f"Método de transcrição inválido: {method}")
            return None
    except Exception as e:
        logger.error(f"Erro na transcrição: {str(e)}", exc_info=True)
        return None


def _transcribe_with_whisper(audio_file) -> Optional[str]:
    """
    Transcreve usando Whisper local (openai-whisper).
    
    Args:
        audio_file: Arquivo de áudio
        
    Returns:
        Texto transcrito
    """
    try:
        import whisper
        
        logger.debug("Carregando modelo Whisper (base)")
        # Carregar modelo Whisper (base é um bom equilíbrio)
        model = whisper.load_model("base")
        
        # Usar context manager para garantir limpeza
        with _temp_audio_file(audio_file, suffix=".wav") as tmp_path:
            logger.debug(f"Transcrevendo arquivo: {tmp_path}")
            # Transcrever
            result = model.transcribe(tmp_path, language="pt")
            text = result["text"].strip()
            logger.info(f"Transcrição concluída: {len(text)} caracteres")
            return text
                
    except ImportError as e:
        logger.error("Whisper não está instalado", exc_info=True)
        raise ImportError(
            "Whisper não está instalado. Instale com: pip install openai-whisper"
        ) from e
    except Exception as e:
        logger.error(f"Erro ao transcrever com Whisper: {str(e)}", exc_info=True)
        raise Exception(f"Erro ao transcrever com Whisper: {str(e)}") from e


def _transcribe_with_openai(audio_file) -> Optional[str]:
    """
    Transcreve usando OpenAI Whisper API.
    
    Args:
        audio_file: Arquivo de áudio
        
    Returns:
        Texto transcrito
    """
    try:
        from openai import OpenAI
        import os
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY não configurada")
            raise Exception("OPENAI_API_KEY não configurada no .env")
        
        logger.debug("Inicializando cliente OpenAI")
        client = OpenAI(api_key=api_key)
        
        # Usar context manager para garantir limpeza
        with _temp_audio_file(audio_file, suffix=".wav") as tmp_path:
            logger.debug(f"Enviando arquivo para API OpenAI: {tmp_path}")
            # Transcrever usando API
            with open(tmp_path, "rb") as audio:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    language="pt"
                )
            text = transcript.text.strip()
            logger.info(f"Transcrição concluída: {len(text)} caracteres")
            return text
                
    except ImportError as e:
        logger.error("OpenAI não está instalado", exc_info=True)
        raise ImportError(
            "OpenAI não está instalado. Instale com: pip install openai"
        ) from e
    except Exception as e:
        logger.error(f"Erro ao transcrever com OpenAI: {str(e)}", exc_info=True)
        raise Exception(f"Erro ao transcrever com OpenAI: {str(e)}") from e

