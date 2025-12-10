# llm_handler.py - Versão simplificada e corrigida
import os
from typing import Optional, List, Dict, Tuple
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class LLMHandler:
    # Modelos válidos da OpenAI
    VALID_MODELS = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo-preview",
        "gpt-4o",
        "gpt-4o-mini",
    ]

    def __init__(self, api_key: str = None):
        """Inicializa o handler do LLM de forma simplificada"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("⚠️  API Key não fornecida. Configure OPENAI_API_KEY no .env")

    def _validate_model(self, model: str) -> bool:
        """Valida se o modelo é suportado"""
        return model in self.VALID_MODELS

    def generate_response(
        self,
        messages: List[Dict[str, str]] = None,
        user_input: str = None,  # Mantido para compatibilidade
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Gera resposta usando a API da OpenAI diretamente.

        Args:
            messages: Lista completa de mensagens do histórico (preferencial)
            user_input: Mensagem única do usuário (compatibilidade retroativa)
            model: Modelo a ser usado
            temperature: Criatividade da resposta (0.0 a 2.0)
            max_tokens: Número máximo de tokens na resposta

        Returns:
            Resposta gerada pelo modelo
        """

        if not self.api_key:
            return "Erro: API Key não configurada. Configure na sidebar."

        # Validação do modelo
        if not self._validate_model(model):
            return f"Erro: Modelo '{model}' não é válido. Modelos disponíveis: {', '.join(self.VALID_MODELS)}"

        # Validação de temperatura
        if not 0.0 <= temperature <= 2.0:
            return "Erro: Temperature deve estar entre 0.0 e 2.0"

        # Prepara mensagens: usa histórico completo se disponível, senão cria nova
        if messages:
            # Adiciona mensagem do sistema se não existir
            if not messages or messages[0].get("role") != "system":
                system_message = {
                    "role": "system",
                    "content": "Você é um assistente útil e prestativo.",
                }
                formatted_messages = [system_message] + messages
            else:
                formatted_messages = messages
        elif user_input:
            # Modo compatibilidade: cria mensagens do zero
            formatted_messages = [
                {
                    "role": "system",
                    "content": "Você é um assistente útil e prestativo.",
                },
                {"role": "user", "content": user_input},
            ]
        else:
            return "Erro: Nenhuma mensagem fornecida."

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content

        except Exception as e:
            error_msg = str(e)
            # Não expõe a API key completa em erros
            if self.api_key and self.api_key in error_msg:
                error_msg = error_msg.replace(self.api_key, "sk-***")
            return f"Erro ao conectar com a API: {error_msg}"

    def is_configured(self) -> bool:
        """Verifica se o handler está configurado"""
        return bool(self.api_key)

    def validate_api_key(self) -> tuple[bool, str]:
        """Valida a API Key configurada"""
        if not self.api_key:
            return False, "API Key não configurada"
        if not self.api_key.startswith("sk-"):
            return False, "Formato inválido (deve começar com 'sk-')"
        if len(self.api_key) < 20:
            return False, "API Key muito curta"
        return True, "API Key válida"


# Função de fábrica
def create_llm_handler(api_key: str = None):
    return LLMHandler(api_key)
