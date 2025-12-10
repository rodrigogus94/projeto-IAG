import requests
import json
import logging
from typing import Dict, Any, Optional

# Configurar logger
logger = logging.getLogger(__name__)


class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = None):
        """
        Inicializa o serviço Ollama.

        Args:
            base_url: URL da API do Ollama (padrão: localhost:11434)
            timeout: Timeout para requisições em segundos (usa model_config se None)
                    Para geração de respostas, use um valor maior (60-120s)
        """
        # Usar timeout de model_config se não fornecido
        if timeout is None:
            try:
                from model_config import MODEL_RULES

                timeout = MODEL_RULES.get("timeout_seconds", 60)
            except ImportError:
                timeout = 60

        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.timeout = timeout

    def list_models(self) -> list:
        """
        Lista todos os modelos disponíveis no Ollama.

        Raises:
            ConnectionError: Se não conseguir conectar ao Ollama
            Exception: Para outros erros
        """
        try:
            logger.debug(f"Listando modelos do Ollama em {self.api_url}")
            response = requests.get(f"{self.api_url}/tags", timeout=self.timeout)
            response.raise_for_status()
            models = response.json().get("models", [])
            logger.info(f"Encontrados {len(models)} modelos")
            return models
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Erro de conexão ao Ollama: {str(e)}")
            raise ConnectionError(
                f"Ollama não está rodando ou não está acessível em {self.base_url}. "
                f"Verifique se o servidor está iniciado. Erro: {str(e)}"
            ) from e
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout ao conectar ao Ollama: {self.base_url}")
            raise Exception(
                f"Timeout ao conectar ao Ollama em {self.base_url}. "
                f"O servidor pode estar sobrecarregado ou inacessível."
            ) from e
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP ao listar modelos: {e.response.status_code}")
            raise Exception(
                f"Erro HTTP ao listar modelos: {e.response.status_code} - {str(e)}"
            ) from e
        except Exception as e:
            logger.error(f"Erro inesperado ao listar modelos: {str(e)}", exc_info=True)
            raise Exception(f"Erro ao listar modelos: {str(e)}") from e

    def generate_response(
        self,
        model: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        stream: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Gera uma resposta usando um modelo do Ollama.

        Args:
            model: Nome do modelo a ser usado
            prompt: Prompt do usuário
            system_prompt: Prompt do sistema (opcional)
            stream: Se True, retorna um gerador para streaming
            **kwargs: Parâmetros adicionais (temperature, top_p, etc.)

        Returns:
            Dicionário com a resposta ou gerador para streaming
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": kwargs,
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            if stream:
                logger.debug(f"Gerando resposta em streaming com modelo {model}")
                response = requests.post(
                    f"{self.api_url}/generate",
                    json=payload,
                    stream=True,
                    timeout=None,  # Sem timeout para streaming
                )
                response.raise_for_status()
                return self._handle_stream_response(response)
            else:
                logger.debug(
                    f"Gerando resposta com modelo {model} (timeout: {self.timeout}s)"
                )
                response = requests.post(
                    f"{self.api_url}/generate", json=payload, timeout=self.timeout
                )
                response.raise_for_status()
                result = response.json()
                logger.debug("Resposta gerada com sucesso")
                return result

        except requests.exceptions.ConnectionError as e:
            logger.error("Erro de conexão ao gerar resposta")
            raise Exception("Não foi possível conectar ao Ollama.") from e
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}", exc_info=True)
            raise Exception(f"Erro ao gerar resposta: {str(e)}") from e

    def _handle_stream_response(self, response):
        """Processa resposta em streaming."""
        logger.debug("Processando resposta em streaming")
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    yield data
                except json.JSONDecodeError as e:
                    logger.warning(f"Erro ao decodificar JSON do stream: {e}")
                    continue

    def chat(
        self, model: str, messages: list, stream: bool = False, **kwargs
    ) -> Dict[str, Any]:
        """
        Interface de chat com histórico de mensagens.

        Args:
            model: Nome do modelo
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            stream: Se True, streaming de resposta
            **kwargs: Parâmetros adicionais
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "options": kwargs,
        }

        try:
            # Timeout mais longo para chat (geração de respostas pode demorar)
            chat_timeout = self.timeout * 2 if not stream else None
            logger.debug(
                f"Iniciando chat com modelo {model}, streaming={stream}, timeout={chat_timeout}s"
            )
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                stream=stream,
                timeout=chat_timeout,  # Timeout dobrado para chat (geração pode demorar)
            )
            response.raise_for_status()

            if stream:
                logger.debug("Retornando resposta em streaming")
                return self._handle_stream_response(response)
            else:
                result = response.json()
                logger.debug("Resposta do chat recebida")
                return result

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Erro de conexão no chat: {str(e)}")
            raise ConnectionError(
                f"Não foi possível conectar ao Ollama em {self.base_url}. "
                f"Verifique se o servidor está rodando. Erro: {str(e)}"
            ) from e
        except requests.exceptions.Timeout as e:
            timeout_used = self.timeout * 2 if not stream else "ilimitado"
            logger.error(f"Timeout no chat após {timeout_used} segundos")
            raise Exception(
                f"Timeout ao comunicar com o Ollama. "
                f"A requisição demorou mais de {timeout_used} segundos. "
                f"Tente aumentar o timeout ou usar um modelo mais rápido."
            ) from e
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            try:
                error_json = e.response.json()
                error_detail = error_json.get("error", "")
            except:
                error_detail = e.response.text[:200]
            logger.error(
                f"Erro HTTP no chat: {e.response.status_code} - {error_detail}"
            )
            raise Exception(
                f"Erro HTTP no chat: {e.response.status_code} - {error_detail}"
            ) from e
        except Exception as e:
            logger.error(f"Erro inesperado no chat: {str(e)}", exc_info=True)
            raise Exception(f"Erro no chat: {str(e)}") from e
