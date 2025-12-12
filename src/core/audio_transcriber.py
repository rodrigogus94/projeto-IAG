"""
Módulo para transcrição de áudio usando Whisper ou APIs alternativas
"""
import os
import tempfile
import logging
import warnings
from typing import Optional
from contextlib import contextmanager

# Suprimir aviso do Whisper sobre FP16 não suportado em CPU (é apenas informativo)
# O Whisper automaticamente usa FP32 em CPU, então este aviso não é necessário
warnings.filterwarnings("ignore", message=".*FP16 is not supported on CPU.*", category=UserWarning)

# Configurar logger
logger = logging.getLogger(__name__)


@contextmanager
def _temp_audio_file(audio_file, suffix=".wav"):
    """
    Context manager para criar e limpar arquivo temporário de áudio.
    Garante limpeza mesmo em caso de erro.
    Versão otimizada para Windows.
    
    Args:
        audio_file: Arquivo de áudio (BytesIO ou similar do Streamlit)
        suffix: Sufixo do arquivo temporário
        
    Yields:
        Caminho absoluto do arquivo temporário
    """
    tmp_path = None
    tmp_file_handle = None
    try:
        # Streamlit audio_input retorna um objeto BytesIO
        # Resetar posição do arquivo se possível
        if hasattr(audio_file, 'seek'):
            audio_file.seek(0)
        
        # Ler conteúdo do arquivo
        # Streamlit retorna BytesIO diretamente
        if hasattr(audio_file, 'read'):
            audio_content = audio_file.read()
        else:
            audio_content = audio_file
        
        # Garantir que é bytes
        if isinstance(audio_content, bytes):
            content_to_write = audio_content
        elif isinstance(audio_content, str):
            # Se for string, tentar codificar
            content_to_write = audio_content.encode('utf-8')
        else:
            # Tentar converter para bytes
            try:
                content_to_write = bytes(audio_content)
            except Exception:
                logger.error(f"Tipo de conteúdo de áudio não suportado: {type(audio_content)}")
                raise ValueError(f"Não foi possível processar o arquivo de áudio. Tipo: {type(audio_content)}")
        
        if len(content_to_write) == 0:
            raise ValueError("Arquivo de áudio está vazio")
        
        # Abordagem alternativa mais robusta para Windows
        # Usar NamedTemporaryFile com delete=False para evitar problemas de acesso
        import uuid
        
        # Criar nome único para o arquivo
        unique_id = str(uuid.uuid4())
        temp_dir = tempfile.gettempdir()
        
        # Garantir que o diretório temporário existe
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
        
        # Criar caminho completo com nome único
        tmp_path = os.path.join(temp_dir, f"whisper_audio_{unique_id}{suffix}")
        
        # Normalizar caminho para Windows (resolve problemas com barras)
        tmp_path = os.path.normpath(os.path.abspath(tmp_path))
        
        # Escrever conteúdo no arquivo de forma atômica
        try:
            # Usar modo 'xb' (exclusive binary) para evitar conflitos
            # Se falhar, tentar modo 'wb' normal
            try:
                with open(tmp_path, 'xb') as tmp_file:
                    tmp_file.write(content_to_write)
            except FileExistsError:
                # Se o arquivo já existe (muito improvável), tentar novamente com novo UUID
                unique_id = str(uuid.uuid4())
                tmp_path = os.path.join(temp_dir, f"whisper_audio_{unique_id}{suffix}")
                tmp_path = os.path.normpath(os.path.abspath(tmp_path))
                with open(tmp_path, 'xb') as tmp_file:
                    tmp_file.write(content_to_write)
            
            # Fechar o arquivo explicitamente antes de verificar
            # No Windows, arquivos abertos podem não ser acessíveis por outros processos
            
            # Verificar se o arquivo foi criado corretamente
            if not os.path.exists(tmp_path):
                raise Exception(f"Arquivo temporário não foi criado: {tmp_path}")
            
            # Aguardar um pouco para garantir que o arquivo está totalmente escrito (Windows)
            import time
            time.sleep(0.1)
            
            file_size = os.path.getsize(tmp_path)
            if file_size == 0:
                raise Exception(f"Arquivo temporário está vazio: {tmp_path}")
            
            if file_size != len(content_to_write):
                logger.warning(f"Tamanho do arquivo ({file_size}) diferente do esperado ({len(content_to_write)})")
            
            logger.debug(f"Arquivo temporário criado: {tmp_path} ({file_size} bytes)")
            
            # Verificar novamente antes de yield (importante no Windows)
            if not os.path.isfile(tmp_path):
                raise Exception(f"Caminho não é um arquivo válido: {tmp_path}")
            
            yield tmp_path
            
        except Exception as e:
            # Se houver erro, limpar o arquivo antes de re-raise
            if tmp_path and os.path.exists(tmp_path):
                try:
                    # Tentar fechar o arquivo se ainda estiver aberto
                    if tmp_file_handle and not tmp_file_handle.closed:
                        tmp_file_handle.close()
                    # Aguardar um pouco antes de deletar (Windows)
                    import time
                    time.sleep(0.1)
                    os.unlink(tmp_path)
                except Exception as cleanup_error:
                    logger.warning(f"Erro ao limpar arquivo temporário durante erro: {cleanup_error}")
            raise
    finally:
        # Sempre limpar o arquivo temporário
        if tmp_path and os.path.exists(tmp_path):
            try:
                # Aguardar um pouco antes de deletar (Windows pode ter o arquivo ainda em uso)
                import time
                time.sleep(0.1)
                os.unlink(tmp_path)
                logger.debug(f"Arquivo temporário removido: {tmp_path}")
            except PermissionError as pe:
                # No Windows, às vezes o arquivo ainda está em uso
                logger.warning(f"Arquivo ainda em uso, tentando novamente: {tmp_path}")
                try:
                    time.sleep(0.5)
                    os.unlink(tmp_path)
                except Exception as e2:
                    logger.warning(f"Não foi possível remover arquivo temporário {tmp_path}: {e2}")
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
        
        # Validar arquivo de áudio
        if audio_file is None:
            logger.error("Arquivo de áudio é None")
            raise ValueError("Arquivo de áudio não fornecido")
        
        # Verificar se o arquivo tem conteúdo
        if hasattr(audio_file, 'seek'):
            audio_file.seek(0)
            current_pos = audio_file.tell()
            audio_file.seek(0, 2)  # Ir para o final
            file_size = audio_file.tell()
            audio_file.seek(current_pos)  # Voltar para a posição original
            
            if file_size == 0:
                logger.error("Arquivo de áudio está vazio")
                raise ValueError("Arquivo de áudio está vazio")
            
            logger.debug(f"Tamanho do arquivo de áudio: {file_size} bytes")
        
        if method == "whisper":
            result = _transcribe_with_whisper(audio_file)
            if result:
                logger.info(f"Transcrição bem-sucedida: {len(result)} caracteres")
            else:
                logger.warning("Transcrição retornou None")
            return result
        elif method == "openai":
            result = _transcribe_with_openai(audio_file)
            if result:
                logger.info(f"Transcrição bem-sucedida: {len(result)} caracteres")
            else:
                logger.warning("Transcrição retornou None")
            return result
        else:
            logger.warning(f"Método de transcrição inválido: {method}")
            raise ValueError(f"Método de transcrição inválido: {method}. Use 'whisper' ou 'openai'")
    except ValueError as e:
        # Erros de validação - re-raise para que a UI possa mostrar mensagem específica
        logger.error(f"Erro de validação na transcrição: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Erro na transcrição: {str(e)}", exc_info=True)
        raise Exception(f"Erro ao transcrever áudio: {str(e)}") from e


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
        # Usar cache para não recarregar a cada vez
        model = None
        model_name = "base"
        try:
            model = whisper.load_model("base")
            logger.debug("Modelo Whisper 'base' carregado com sucesso")
        except Exception as e:
            logger.warning(f"Erro ao carregar modelo base: {e}, tentando tiny")
            try:
                model = whisper.load_model("tiny")  # Modelo menor como fallback
                model_name = "tiny"
                logger.debug("Modelo Whisper 'tiny' carregado com sucesso")
            except Exception as e2:
                logger.error(f"Erro ao carregar modelo tiny: {e2}")
                raise Exception(f"Não foi possível carregar modelo Whisper. Erro base: {e}, Erro tiny: {e2}")
        
        if model is None:
            raise Exception("Modelo Whisper não foi carregado")
        
        # Usar context manager para garantir limpeza
        with _temp_audio_file(audio_file, suffix=".wav") as tmp_path:
            logger.debug(f"Transcrevendo arquivo: {tmp_path} com modelo {model_name}")
            
            # Verificar se o arquivo existe e tem conteúdo (já verificado no context manager, mas verificar novamente)
            # No Windows, às vezes é necessário aguardar um pouco para o arquivo estar totalmente disponível
            import time
            max_retries = 5
            retry_delay = 0.2
            
            for attempt in range(max_retries):
                if os.path.exists(tmp_path) and os.path.isfile(tmp_path):
                    try:
                        file_size = os.path.getsize(tmp_path)
                        if file_size > 0:
                            break
                    except (OSError, PermissionError):
                        if attempt < max_retries - 1:
                            logger.debug(f"Tentativa {attempt + 1}: Arquivo ainda não acessível, aguardando...")
                            time.sleep(retry_delay)
                            continue
                        else:
                            raise Exception(f"Arquivo temporário não está acessível após {max_retries} tentativas: {tmp_path}")
                else:
                    if attempt < max_retries - 1:
                        logger.debug(f"Tentativa {attempt + 1}: Arquivo não existe ainda, aguardando...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise Exception(f"Arquivo temporário não existe: {tmp_path}")
            else:
                raise Exception(f"Arquivo temporário não está disponível: {tmp_path}")
            
            file_size = os.path.getsize(tmp_path)
            if file_size == 0:
                raise Exception(f"Arquivo de áudio está vazio: {tmp_path}")
            
            logger.debug(f"Tamanho do arquivo: {file_size} bytes, caminho absoluto: {os.path.abspath(tmp_path)}")
            
            # Transcrever - garantir que o caminho seja absoluto e normalizado
            try:
                # Normalizar o caminho para evitar problemas com caracteres especiais
                normalized_path = os.path.normpath(os.path.abspath(tmp_path))
                
                # Verificar novamente se o arquivo existe após normalização
                if not os.path.exists(normalized_path):
                    raise Exception(f"Arquivo não encontrado após normalização: {normalized_path} (original: {tmp_path})")
                
                # Verificar se o arquivo pode ser lido
                try:
                    with open(normalized_path, 'rb') as test_file:
                        test_file.read(1)  # Tentar ler pelo menos 1 byte
                except (IOError, PermissionError) as read_error:
                    raise Exception(f"Não foi possível ler o arquivo: {read_error}")
                
                logger.debug(f"Transcrevendo com caminho normalizado: {normalized_path}")
                
                # Tentar transcrever com retry em caso de erro de arquivo
                try:
                    result = model.transcribe(normalized_path, language="pt")
                except FileNotFoundError:
                    # Se ainda assim não encontrar, tentar com caminho original
                    logger.warning(f"Arquivo não encontrado com caminho normalizado, tentando original: {tmp_path}")
                    if os.path.exists(tmp_path):
                        result = model.transcribe(tmp_path, language="pt")
                    else:
                        raise Exception(f"Arquivo não encontrado: {normalized_path}")
                
                text = result.get("text", "").strip()
                
                if not text:
                    logger.warning("Transcrição retornou texto vazio - pode ser silêncio ou áudio sem fala")
                    raise Exception("Não foi possível transcrever o áudio. O arquivo pode conter apenas silêncio ou não ter fala audível.")
                
                logger.info(f"Transcrição concluída: {len(text)} caracteres")
                return text
            except FileNotFoundError as fnf_error:
                logger.error(f"Arquivo não encontrado durante transcrição: {str(fnf_error)}", exc_info=True)
                raise Exception(f"Arquivo de áudio não encontrado: {str(fnf_error)}") from fnf_error
            except Exception as transcribe_error:
                logger.error(f"Erro durante transcrição: {str(transcribe_error)}", exc_info=True)
                raise Exception(f"Erro durante transcrição: {str(transcribe_error)}") from transcribe_error
                
    except ImportError as e:
        logger.error("Whisper não está instalado", exc_info=True)
        raise ImportError(
            "Whisper não está instalado. Instale com: pip install openai-whisper"
        ) from e
    except Exception as e:
        logger.error(f"Erro ao transcrever com Whisper: {str(e)}", exc_info=True)
        # Re-raise com mensagem mais clara
        error_msg = str(e)
        if "Erro ao transcrever com Whisper" not in error_msg:
            raise Exception(f"Erro ao transcrever com Whisper: {error_msg}") from e
        raise


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
            
            # Verificar se o arquivo existe e é acessível antes de enviar
            import time
            max_retries = 5
            retry_delay = 0.2
            
            for attempt in range(max_retries):
                if os.path.exists(tmp_path) and os.path.isfile(tmp_path):
                    try:
                        file_size = os.path.getsize(tmp_path)
                        if file_size > 0:
                            break
                    except (OSError, PermissionError):
                        if attempt < max_retries - 1:
                            logger.debug(f"Tentativa {attempt + 1}: Arquivo ainda não acessível, aguardando...")
                            time.sleep(retry_delay)
                            continue
                        else:
                            raise Exception(f"Arquivo temporário não está acessível após {max_retries} tentativas: {tmp_path}")
                else:
                    if attempt < max_retries - 1:
                        logger.debug(f"Tentativa {attempt + 1}: Arquivo não existe ainda, aguardando...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise Exception(f"Arquivo temporário não existe: {tmp_path}")
            
            # Normalizar caminho para Windows
            normalized_path = os.path.normpath(os.path.abspath(tmp_path))
            
            # Transcrever usando API
            try:
                with open(normalized_path, "rb") as audio:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio,
                        language="pt"
                    )
            except FileNotFoundError:
                # Tentar com caminho original se normalizado falhar
                logger.warning(f"Arquivo não encontrado com caminho normalizado, tentando original: {tmp_path}")
                if os.path.exists(tmp_path):
                    with open(tmp_path, "rb") as audio:
                        transcript = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio,
                            language="pt"
                        )
                else:
                    raise Exception(f"Arquivo não encontrado: {normalized_path}")
            
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

