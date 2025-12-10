import requests
import json
from typing import Dict, Any, Optional

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Inicializa o serviço Ollama.
        
        Args:
            base_url: URL da API do Ollama (padrão: localhost:11434)
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        
    def list_models(self) -> list:
        """Lista todos os modelos disponíveis no Ollama."""
        try:
            response = requests.get(f"{self.api_url}/tags")
            response.raise_for_status()
            return response.json().get("models", [])
        except requests.exceptions.ConnectionError:
            raise Exception("Ollama não está rodando. Por favor, inicie o servidor Ollama.")
        except Exception as e:
            raise Exception(f"Erro ao listar modelos: {str(e)}")
    
    def generate_response(self, 
                         model: str, 
                         prompt: str, 
                         system_prompt: Optional[str] = None,
                         stream: bool = False,
                         **kwargs) -> Dict[str, Any]:
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
            "options": kwargs
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            if stream:
                response = requests.post(
                    f"{self.api_url}/generate",
                    json=payload,
                    stream=True
                )
                response.raise_for_status()
                return self._handle_stream_response(response)
            else:
                response = requests.post(
                    f"{self.api_url}/generate",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
                
        except requests.exceptions.ConnectionError:
            raise Exception("Não foi possível conectar ao Ollama.")
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta: {str(e)}")
    
    def _handle_stream_response(self, response):
        """Processa resposta em streaming."""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    yield data
                except json.JSONDecodeError:
                    continue
    
    def chat(self, 
             model: str, 
             messages: list, 
             stream: bool = False,
             **kwargs) -> Dict[str, Any]:
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
            "options": kwargs
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._handle_stream_response(response)
            else:
                return response.json()
                
        except Exception as e:
            raise Exception(f"Erro no chat: {str(e)}")