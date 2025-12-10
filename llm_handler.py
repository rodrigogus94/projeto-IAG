"""
Handler LLM que integra OllamaService com a interface esperada pelo app.py
"""

import logging
from typing import Optional, List, Dict, Any, Generator
from ollama_service import OllamaService
from model_config import (
    get_system_prompt,
    get_model_parameters,
    validate_temperature,
    DEFAULT_TEMPERATURE,
    DEFAULT_MODEL,
    SYSTEM_MESSAGES,
    VALIDATION_RULES,
)
from input_validator import (
    validate_user_input,
    validate_model_name,
    validate_messages,
    sanitize_input,
)

# Configurar logger
logger = logging.getLogger(__name__)


class OllamaLLMHandler:
    """Handler que adapta OllamaService para a interface do app.py"""

    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = None):
        """
        Inicializa o handler com OllamaService.

        Args:
            base_url: URL base do servidor Ollama (padrão: localhost:11434)
            timeout: Timeout para requisições em segundos (usa model_config se None)
        """
        # Usar timeout de model_config se não fornecido
        if timeout is None:
            try:
                from model_config import MODEL_RULES
                timeout = MODEL_RULES.get("timeout_seconds", 60)
            except ImportError:
                timeout = 60
        
        self.ollama_service = OllamaService(base_url=base_url, timeout=timeout)
        self.base_url = base_url
        self.timeout = timeout

    def generate_response(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        user_input: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        context: str = "general",
        stream: bool = False,
        **kwargs,
    ) -> str:
        """
        Gera uma resposta usando o Ollama.

        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            user_input: Input direto do usuário (alternativa a messages)
            model: Nome do modelo Ollama a usar (usa padrão se None)
            temperature: Temperatura para geração (usa padrão se None)
            context: Contexto da conversa para system prompt ("dashboard", "data_analysis", etc.)
            stream: Se True, retorna um gerador para streaming
            **kwargs: Parâmetros adicionais do modelo

        Returns:
            String com a resposta gerada ou gerador se stream=True
        """
        try:
            logger.info(f"Gerando resposta (stream={stream}, context={context})")
            
            # Usar valores padrão se não fornecidos
            model = model or DEFAULT_MODEL
            
            # Validar nome do modelo
            is_valid, error = validate_model_name(model)
            if not is_valid:
                logger.error(f"Nome do modelo inválido: {error}")
                return SYSTEM_MESSAGES.get("error", f"Erro: {error}")
            
            temperature = (
                temperature if temperature is not None else DEFAULT_TEMPERATURE
            )

            # Validar temperatura
            temperature = validate_temperature(temperature)

            # Se não há messages mas há user_input, criar messages
            if not messages and user_input:
                # Sanitizar e validar input do usuário
                user_input = sanitize_input(user_input)
                is_valid, error = validate_user_input(user_input)
                if not is_valid:
                    logger.warning(f"Input do usuário inválido: {error}")
                    return f"Erro de validação: {error}"
                messages = [{"role": "user", "content": user_input}]

            # Se não há messages nem user_input, retornar erro
            if not messages:
                logger.error("Nenhuma mensagem fornecida")
                return SYSTEM_MESSAGES.get("error", "Erro: Nenhuma mensagem fornecida.")
            
            # Validar mensagens
            is_valid, error = validate_messages(messages)
            if not is_valid:
                logger.error(f"Mensagens inválidas: {error}")
                return SYSTEM_MESSAGES.get("error", f"Erro: {error}")

            # Preparar mensagens com system prompt
            # Verificar se já existe system prompt nas mensagens
            has_system = any(msg.get("role") == "system" for msg in messages)

            if not has_system:
                # Adicionar system prompt no início
                system_prompt = get_system_prompt(context)
                messages_with_system = [
                    {"role": "system", "content": system_prompt}
                ] + messages
            else:
                messages_with_system = messages

            # Obter parâmetros do modelo
            model_params = get_model_parameters(temperature=temperature, **kwargs)

            # Chamar o método chat do OllamaService
            response = self.ollama_service.chat(
                model=model, messages=messages_with_system, stream=stream, **model_params
            )

            # Se streaming, retornar gerador
            if stream:
                logger.debug("Retornando resposta em streaming")
                return self._handle_stream_response(response)

            # Extrair a resposta do formato do Ollama
            if isinstance(response, dict):
                message = response.get("message", {})
                content = message.get("content", "")
                if content:
                    logger.info(f"Resposta gerada: {len(content)} caracteres")
                    return content
                else:
                    logger.warning("Resposta vazia do modelo")
                    return SYSTEM_MESSAGES.get(
                        "no_response", "Erro: Resposta vazia do modelo."
                    )
            else:
                logger.error(f"Formato de resposta inesperado: {type(response)}")
                return SYSTEM_MESSAGES.get(
                    "error", "Erro: Formato de resposta inesperado."
                )

        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}", exc_info=True)
            error_msg = SYSTEM_MESSAGES.get("error", "Erro ao gerar resposta")
            return f"{error_msg}: {str(e)}"
    
    def _handle_stream_response(self, response_generator: Generator) -> Generator[str, None, None]:
        """
        Processa resposta em streaming do Ollama.
        
        Args:
            response_generator: Gerador do OllamaService
            
        Yields:
            Chunks de texto da resposta
        """
        logger.debug("Processando resposta em streaming")
        full_response = ""
        
        try:
            for chunk in response_generator:
                if isinstance(chunk, dict):
                    # Extrair conteúdo do chunk
                    message = chunk.get("message", {})
                    content = message.get("content", "")
                    
                    if content:
                        full_response += content
                        yield content
                    
                    # Verificar se é o último chunk
                    if chunk.get("done", False):
                        logger.debug(f"Streaming concluído: {len(full_response)} caracteres")
                        break
        except Exception as e:
            logger.error(f"Erro no streaming: {str(e)}", exc_info=True)
            raise

    def is_configured(self) -> bool:
        """
        Verifica se o handler está configurado e o Ollama está disponível.

        Returns:
            True se o Ollama está acessível, False caso contrário
        """
        try:
            # Tentar listar modelos para verificar se o Ollama está rodando
            self.ollama_service.list_models()
            return True
        except ConnectionError:
            # ConnectionError indica que o Ollama não está rodando
            return False
        except Exception:
            # Outros erros também indicam problema de configuração
            return False

    def get_connection_status(self) -> dict:
        """
        Retorna status detalhado da conexão com o Ollama.

        Returns:
            Dicionário com status, mensagem e detalhes
        """
        try:
            models = self.ollama_service.list_models()
            model_count = len(models)
            return {
                "connected": True,
                "message": "✅ Conectado ao Ollama",
                "url": self.base_url,
                "model_count": model_count,
                "models": [
                    m.get("name", "") for m in models[:5]
                ],  # Primeiros 5 modelos
            }
        except ConnectionError as e:
            return {
                "connected": False,
                "message": "❌ Ollama não está rodando",
                "url": self.base_url,
                "error": str(e),
                "suggestion": "Inicie o Ollama com: ollama serve",
            }
        except Exception as e:
            return {
                "connected": False,
                "message": "❌ Erro ao conectar",
                "url": self.base_url,
                "error": str(e),
                "suggestion": "Verifique se o Ollama está rodando e a URL está correta",
            }

    def list_available_models(self) -> List[str]:
        """
        Lista os modelos disponíveis no Ollama.

        Returns:
            Lista de nomes de modelos disponíveis
        """
        try:
            models = self.ollama_service.list_models()
            return [model.get("name", "") for model in models if model.get("name")]
        except Exception as e:
            return []


def create_llm_handler(base_url: Optional[str] = None, timeout: Optional[int] = None) -> OllamaLLMHandler:
    """
    Factory function para criar um handler LLM.

    Args:
        base_url: URL base do servidor Ollama (opcional)
        timeout: Timeout para requisições em segundos (opcional, usa padrão se None)

    Returns:
        Instância de OllamaLLMHandler
    """
    if base_url and timeout is not None:
        return OllamaLLMHandler(base_url=base_url, timeout=timeout)
    elif base_url:
        return OllamaLLMHandler(base_url=base_url)
    elif timeout is not None:
        return OllamaLLMHandler(timeout=timeout)
    else:
        return OllamaLLMHandler()
