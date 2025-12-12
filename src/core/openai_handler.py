"""
Handler OpenAI que integra OpenAIService com a interface esperada pelo app.py
"""

import logging
from typing import Optional, List, Dict, Any, Generator
from src.core.openai_service import OpenAIService
from src.config.openai_model_config import (
    get_system_prompt,
    validate_temperature,
    DEFAULT_TEMPERATURE,
    DEFAULT_MODEL,
    SYSTEM_MESSAGES,
    VALIDATION_RULES,
    get_model_parameters,
    get_recommended_temperature,
    get_optimal_max_tokens,
)
from src.core.input_validator import (
    validate_user_input,
    validate_messages,
    sanitize_input,
)

# Configurar logger
logger = logging.getLogger(__name__)


class OpenAILLMHandler:
    """Handler que adapta OpenAIService para a interface do app.py"""

    def __init__(self, api_key: Optional[str] = None, timeout: Optional[int] = None):
        """
        Inicializa o handler com OpenAIService.

        Args:
            api_key: Chave da API OpenAI (usa OPENAI_API_KEY do .env se None)
            timeout: Timeout para requisições em segundos (usa model_config se None)
        """
        # Usar timeout de model_config se não fornecido
        if timeout is None:
            try:
                from src.config.model_config import MODEL_RULES
                timeout = MODEL_RULES.get("timeout_seconds", 60)
            except ImportError:
                timeout = 60

        self.openai_service = OpenAIService(api_key=api_key, timeout=timeout)
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
        Gera uma resposta usando a OpenAI.

        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            user_input: Input direto do usuário (alternativa a messages)
            model: Nome do modelo OpenAI a usar (usa padrão se None)
            temperature: Temperatura para geração (usa padrão se None)
            context: Contexto da conversa para system prompt
            stream: Se True, retorna um gerador para streaming
            **kwargs: Parâmetros adicionais do modelo

        Returns:
            String com a resposta gerada ou gerador se stream=True
        """
        try:
            logger.info(f"Gerando resposta (stream={stream}, context={context})")

            # Usar modelo padrão se não fornecido
            if model is None:
                model = DEFAULT_MODEL  # Modelo padrão da OpenAI (gpt-4.1)

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

            # Preparar parâmetros usando configuração especializada
            model_params = get_model_parameters(
                temperature=temperature,
                model=model,
                **kwargs
            )

            # Chamar o método chat do OpenAIService
            response = self.openai_service.chat(
                model=model, messages=messages_with_system, stream=stream, **model_params
            )

            # Se streaming, retornar gerador
            if stream:
                logger.debug("Retornando resposta em streaming")
                return self._handle_stream_response(response)

            # Extrair a resposta do formato da OpenAI
            if isinstance(response, dict):
                # Tentar extrair conteúdo de diferentes formas
                message = response.get("message", {})
                content = ""
                
                if isinstance(message, dict):
                    content = message.get("content", "")
                elif isinstance(message, str):
                    content = message
                
                # Fallback: tentar extrair diretamente do response
                if not content:
                    content = response.get("content", "")
                
                if content and len(str(content).strip()) > 0:
                    logger.info(f"Resposta gerada: {len(content)} caracteres")
                    return str(content)
                else:
                    logger.warning(f"Resposta vazia do modelo. Response structure: {list(response.keys())}")
                    return SYSTEM_MESSAGES.get(
                        "no_response", "Erro: Resposta vazia do modelo."
                    )
            else:
                logger.error(f"Formato de resposta inesperado: {type(response)} - {response}")
                return SYSTEM_MESSAGES.get(
                    "error", "Erro: Formato de resposta inesperado."
                )

        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}", exc_info=True)
            error_str = str(e)
            
            # Detectar erros específicos de API key
            if "401" in error_str or "invalid_api_key" in error_str or "Incorrect API key" in error_str:
                return """❌ **Chave de API inválida**

A chave de API configurada no arquivo `.env` não é válida.

**Como corrigir:**

1. **Obtenha uma chave válida:**
   - Acesse: https://platform.openai.com/account/api-keys
   - Faça login na sua conta OpenAI
   - Clique em "Create new secret key"
   - Copie a chave (ela começa com `sk-`)

2. **Configure no arquivo `.env`:**
   - Abra o arquivo `.env` na raiz do projeto
   - Encontre a linha: `OPENAI_API_KEY=sk-sua-chave-api-aqui`
   - Substitua `sk-sua-chave-api-aqui` pela sua chave real
   - Salve o arquivo

3. **Reinicie o Streamlit:**
   - Pare o Streamlit (Ctrl+C)
   - Execute novamente: `streamlit run src/app.py`

**Nota:** Certifique-se de que sua conta OpenAI tem créditos disponíveis."""
            
            # Detectar outros erros comuns
            if "rate_limit" in error_str.lower():
                return SYSTEM_MESSAGES.get("rate_limit", "Limite de requisições atingido. Aguarde um momento e tente novamente.")
            
            if "insufficient_quota" in error_str.lower() or "quota" in error_str.lower():
                return SYSTEM_MESSAGES.get("insufficient_quota", "Cota insuficiente. Verifique seu plano OpenAI.")
            
            # Erro genérico
            error_msg = SYSTEM_MESSAGES.get("error", "Erro ao gerar resposta")
            return f"{error_msg}: {error_str}"

    def _handle_stream_response(
        self, response_generator: Generator
    ) -> Generator[str, None, None]:
        """
        Processa resposta em streaming da OpenAI.

        Args:
            response_generator: Gerador do OpenAIService

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
        Verifica se o handler está configurado e a OpenAI está disponível.

        Returns:
            True se a OpenAI está acessível, False caso contrário
        """
        try:
            return self.openai_service.is_configured()
        except Exception:
            return False

    def get_connection_status(self) -> dict:
        """
        Retorna status detalhado da conexão com a OpenAI.

        Returns:
            Dicionário com status, mensagem e detalhes
        """
        try:
            models = self.openai_service.list_models()
            model_count = len(models)
            return {
                "connected": True,
                "message": "✅ Conectado à OpenAI",
                "provider": "OpenAI",
                "model_count": model_count,
                "models": [m.get("name", "") for m in models[:5]],  # Primeiros 5 modelos
            }
        except ValueError as e:
            return {
                "connected": False,
                "message": "❌ OPENAI_API_KEY não configurada",
                "provider": "OpenAI",
                "error": str(e),
                "suggestion": "Configure OPENAI_API_KEY no arquivo .env",
            }
        except Exception as e:
            return {
                "connected": False,
                "message": "❌ Erro ao conectar à OpenAI",
                "provider": "OpenAI",
                "error": str(e),
                "suggestion": "Verifique sua API key e conexão com a internet",
            }

    def list_available_models(self) -> List[str]:
        """
        Lista os modelos disponíveis da OpenAI.

        Returns:
            Lista de nomes de modelos disponíveis
        """
        try:
            models = self.openai_service.list_models()
            return [model.get("name", "") for model in models if model.get("name")]
        except Exception as e:
            logger.error(f"Erro ao listar modelos: {str(e)}")
            return []


def create_openai_handler(
    api_key: Optional[str] = None, timeout: Optional[int] = None
) -> OpenAILLMHandler:
    """
    Factory function para criar um handler OpenAI.

    Args:
        api_key: Chave da API OpenAI (opcional)
        timeout: Timeout para requisições em segundos (opcional)

    Returns:
        Instância de OpenAILLMHandler
    """
    if api_key and timeout is not None:
        return OpenAILLMHandler(api_key=api_key, timeout=timeout)
    elif api_key:
        return OpenAILLMHandler(api_key=api_key)
    elif timeout is not None:
        return OpenAILLMHandler(timeout=timeout)
    else:
        return OpenAILLMHandler()

