"""
Testes unitários para OllamaService
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import requests

# Adicionar diretório raiz ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.ollama_service import OllamaService


class TestOllamaService(unittest.TestCase):
    """Testes para a classe OllamaService"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.service = OllamaService(base_url="http://localhost:11434", timeout=5)
    
    @patch('ollama_service.requests.get')
    def test_list_models_success(self, mock_get):
        """Testa listagem de modelos com sucesso"""
        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = {
            "models": [
                {"name": "llama2:latest", "size": 1000000},
                {"name": "mistral:latest", "size": 2000000}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Executar
        models = self.service.list_models()
        
        # Verificar
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0]["name"], "llama2:latest")
        mock_get.assert_called_once()
    
    @patch('ollama_service.requests.get')
    def test_list_models_connection_error(self, mock_get):
        """Testa erro de conexão ao listar modelos"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        # Executar e verificar exceção
        with self.assertRaises(ConnectionError):
            self.service.list_models()
    
    @patch('ollama_service.requests.post')
    def test_generate_response_success(self, mock_post):
        """Testa geração de resposta com sucesso"""
        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "Esta é uma resposta de teste"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Executar
        result = self.service.generate_response(
            model="llama2:latest",
            prompt="Teste",
            stream=False
        )
        
        # Verificar
        self.assertIn("response", result)
        mock_post.assert_called_once()
    
    @patch('ollama_service.requests.post')
    def test_chat_success(self, mock_post):
        """Testa chat com sucesso"""
        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {
                "role": "assistant",
                "content": "Resposta do assistente"
            }
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Executar
        messages = [{"role": "user", "content": "Olá"}]
        result = self.service.chat(
            model="llama2:latest",
            messages=messages,
            stream=False
        )
        
        # Verificar
        self.assertIn("message", result)
        mock_post.assert_called_once()


if __name__ == '__main__':
    unittest.main()

