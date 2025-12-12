"""
Serviço para comunicação com a API da OpenAI
"""

import logging
from typing import Dict, Any, Optional, List, Generator
from openai import OpenAI

# Configurar logger
logger = logging.getLogger(__name__)


class OpenAIService:
    """Serviço para comunicação com a API da OpenAI"""

    # Modelos disponíveis da OpenAI
    AVAILABLE_MODELS = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
    ]

    def __init__(self, api_key: Optional[str] = None, timeout: int = None):
        """
        Inicializa o serviço OpenAI.

        Args:
            api_key: Chave da API OpenAI (usa OPENAI_API_KEY do .env se None)
            timeout: Timeout para requisições em segundos (usa model_config se None)
        """
        import os
        from dotenv import load_dotenv

        load_dotenv()

        # Usar timeout de model_config se não fornecido
        if timeout is None:
            try:
                from src.config.model_config import MODEL_RULES
                timeout = MODEL_RULES.get("timeout_seconds", 60)
            except ImportError:
                timeout = 60

        # Obter API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY não encontrada. Configure no .env ou passe como parâmetro."
            )
        
        # Validar se não é um placeholder
        if "sua-chave" in self.api_key.lower() or "sk-sua" in self.api_key.lower() or len(self.api_key) < 30:
            raise ValueError(
                "❌ **Chave de API inválida (placeholder detectado)**\n\n"
                "A chave configurada parece ser um exemplo/placeholder.\n\n"
                "**Como corrigir:**\n\n"
                "1. **Obtenha uma chave válida:**\n"
                "   - Acesse: https://platform.openai.com/account/api-keys\n"
                "   - Faça login na sua conta OpenAI\n"
                "   - Clique em \"Create new secret key\"\n"
                "   - Copie a chave (ela começa com `sk-` e tem mais de 40 caracteres)\n\n"
                "2. **Configure no arquivo `.env`:**\n"
                "   - Abra o arquivo `.env` na raiz do projeto\n"
                "   - Encontre a linha: `OPENAI_API_KEY=sk-sua-chave-api-aqui`\n"
                "   - Substitua `sk-sua-chave-api-aqui` pela sua chave real\n"
                "   - Salve o arquivo\n\n"
                "3. **Reinicie o Streamlit:**\n"
                "   - Pare o Streamlit (Ctrl+C)\n"
                "   - Execute novamente: `streamlit run src/app.py`"
            )

        self.client = OpenAI(api_key=self.api_key, timeout=timeout)
        self.timeout = timeout

    def list_models(self) -> List[Dict[str, Any]]:
        """
        Lista todos os modelos disponíveis da OpenAI.

        Returns:
            Lista de dicionários com informações dos modelos
        """
        try:
            logger.debug("Listando modelos da OpenAI")
            # Retornar lista de modelos disponíveis
            models = []
            for model_name in self.AVAILABLE_MODELS:
                models.append(
                    {
                        "name": model_name,
                        "id": model_name,
                        "available": True,
                    }
                )
            logger.info(f"Encontrados {len(models)} modelos da OpenAI")
            return models
        except Exception as e:
            logger.error(f"Erro ao listar modelos: {str(e)}", exc_info=True)
            raise Exception(f"Erro ao listar modelos da OpenAI: {str(e)}") from e

    def chat(
        self, model: str, messages: List[Dict[str, str]], stream: bool = False, **kwargs
    ) -> Dict[str, Any]:
        """
        Interface de chat com histórico de mensagens.

        Args:
            model: Nome do modelo (ex: "gpt-4o", "gpt-3.5-turbo")
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            stream: Se True, streaming de resposta
            **kwargs: Parâmetros adicionais (temperature, max_tokens, etc.)

        Returns:
            Dicionário com a resposta ou gerador para streaming
        """
        try:
            # Preparar parâmetros
            params = {
                "model": model,
                "messages": messages,
                "stream": stream,
            }

            # Adicionar parâmetros opcionais
            if "temperature" in kwargs:
                params["temperature"] = kwargs["temperature"]
            if "max_tokens" in kwargs:
                params["max_tokens"] = kwargs["max_tokens"]
            if "top_p" in kwargs:
                params["top_p"] = kwargs["top_p"]

            logger.debug(
                f"Iniciando chat com modelo {model}, streaming={stream}"
            )

            if stream:
                # Streaming
                response = self.client.chat.completions.create(**params)
                return self._handle_stream_response(response)
            else:
                # Resposta completa
                response = self.client.chat.completions.create(**params)
                result = {
                    "message": {
                        "role": response.choices[0].message.role,
                        "content": response.choices[0].message.content,
                    },
                    "model": response.model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    } if response.usage else None,
                }
                logger.debug("Resposta do chat recebida")
                return result

        except Exception as e:
            logger.error(f"Erro no chat: {str(e)}", exc_info=True)
            raise Exception(f"Erro ao comunicar com OpenAI: {str(e)}") from e

    def _handle_stream_response(
        self, response: Generator
    ) -> Generator[Dict[str, Any], None, None]:
        """Processa resposta em streaming da OpenAI."""
        logger.debug("Processando resposta em streaming")
        try:
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield {
                        "message": {
                            "role": "assistant",
                            "content": chunk.choices[0].delta.content,
                        },
                        "done": False,
                    }
            # Último chunk
            yield {"done": True}
        except Exception as e:
            logger.error(f"Erro no streaming: {str(e)}", exc_info=True)
            raise

    def is_configured(self) -> bool:
        """
        Verifica se o serviço está configurado e a API key é válida.

        Returns:
            True se configurado, False caso contrário
        """
        try:
            # Tentar listar modelos para verificar se a API key é válida
            self.list_models()
            return True
        except Exception:
            return False

