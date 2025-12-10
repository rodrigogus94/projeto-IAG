"""
Handler LLM que integra OllamaService com a interface esperada pelo app.py
"""
from typing import Optional, List, Dict, Any
from ollama_service import OllamaService


class OllamaLLMHandler:
    """Handler que adapta OllamaService para a interface do app.py"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Inicializa o handler com OllamaService.
        
        Args:
            base_url: URL base do servidor Ollama (padrão: localhost:11434)
        """
        self.ollama_service = OllamaService(base_url=base_url)
        self.base_url = base_url
        self.data_context = ""   # <- AQUI: espaço reservado para os dados

    def set_dataframe_context(self, df_text: str):
        """Define o conteúdo da base de dados que será usado pelo modelo."""
        self.data_context = df_text


        
    def generate_response(
        self, 
        messages: Optional[List[Dict[str, str]]] = None, 
        user_input: Optional[str] = None, 
        model: str = "llama2", 
        temperature: float = 0.7
    ) -> str:
        """
        Gera uma resposta usando o Ollama.
        
        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            user_input: Input direto do usuário (alternativa a messages)
            model: Nome do modelo Ollama a usar
            temperature: Temperatura para geração (0.0-2.0)
            
        Returns:
            String com a resposta gerada
        """
        try:
            # Se não há messages mas há user_input, criar messages
            if not messages and user_input:
                messages = [{"role": "user", "content": user_input}]
            
            # Se não há messages nem user_input, retornar erro
            if not messages:
                return "Erro: Nenhuma mensagem fornecida."
            
            # Converter temperatura para formato do Ollama (0-1)
            # Ollama usa temperature de 0 a 1, mas aceita valores maiores
            ollama_temperature = min(max(temperature, 0.0), 2.0)
            
            # Injetar os dados do dataframe como contexto do sistema (RAG textual)
            context_message = {
                "role": "system",
                "content": (
                    "Você é um assistente especializado em análise de dados para veículos rastreados.\n"
                    "Aqui está a base completa dos dados que você deve usar como referência em TODAS as respostas:\n\n"
                    f"{self.data_context}\n\n"
                    "Sempre que o usuário pedir gráficos, análises, métricas ou informações, "
                    "consulte exclusivamente esses dados."
                )
            }

            # ========== INJETAR O CONTEXTO DOS DADOS NO PROMPT ==========

            # Mensagem de sistema com os dados do CSV (RAG tabular)
            context_message = {
                "role": "system",
                "content": (
                    "Você é um assistente especializado em análise de dados de veículos rastreados.\n"
                    "Sempre utilize EXCLUSIVAMENTE a base de dados abaixo para responder às perguntas.\n\n"
                    f"{self.data_context}\n\n"
                    "Se o usuário pedir gráficos, análises estatísticas, comparações, listagens ou tendências, "
                    "baseie-se apenas nesses dados."
                )
            }

            # Inserir a mensagem de contexto ANTES das mensagens do usuário
            messages = [context_message] + messages


            # Chamar o modelo com contexto + mensagem do usuário
            response = self.ollama_service.chat(
                model=model,
                messages=messages,
                stream=False,
                temperature=ollama_temperature
            )

            
            # Extrair a resposta do formato do Ollama
            if isinstance(response, dict):
                message = response.get("message", {})
                content = message.get("content", "")
                return content if content else "Erro: Resposta vazia do modelo."
            else:
                return "Erro: Formato de resposta inesperado."
                
        except Exception as e:
            return f"Erro ao gerar resposta: {str(e)}"
    
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
        except Exception:
            return False
    
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


def create_llm_handler(base_url: Optional[str] = None) -> OllamaLLMHandler:
    """
    Factory function para criar um handler LLM.
    
    Args:
        base_url: URL base do servidor Ollama (opcional)
        
    Returns:
        Instância de OllamaLLMHandler
    """
    if base_url:
        return OllamaLLMHandler(base_url=base_url)
    else:
        return OllamaLLMHandler()

