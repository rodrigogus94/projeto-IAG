"""
Módulo para transcrição de áudio usando Whisper ou APIs alternativas
"""
import os
import tempfile
from typing import Optional


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
        if method == "whisper":
            return _transcribe_with_whisper(audio_file)
        elif method == "openai":
            return _transcribe_with_openai(audio_file)
        else:
            return None
    except Exception as e:
        print(f"Erro na transcrição: {str(e)}")
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
        
        # Carregar modelo Whisper (base é um bom equilíbrio)
        model = whisper.load_model("base")
        
        # Salvar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        try:
            # Transcrever
            result = model.transcribe(tmp_path, language="pt")
            return result["text"].strip()
        finally:
            # Limpar arquivo temporário
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except ImportError:
        raise ImportError(
            "Whisper não está instalado. Instale com: pip install openai-whisper"
        )
    except Exception as e:
        raise Exception(f"Erro ao transcrever com Whisper: {str(e)}")


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
            raise Exception("OPENAI_API_KEY não configurada no .env")
        
        client = OpenAI(api_key=api_key)
        
        # Salvar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        try:
            # Transcrever usando API
            with open(tmp_path, "rb") as audio:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    language="pt"
                )
            return transcript.text.strip()
        finally:
            # Limpar arquivo temporário
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except ImportError:
        raise ImportError(
            "OpenAI não está instalado. Instale com: pip install openai"
        )
    except Exception as e:
        raise Exception(f"Erro ao transcrever com OpenAI: {str(e)}")

