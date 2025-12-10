"""
Testes unitários para OllamaLLMHandler
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Adicionar diretório raiz ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.llm_handler import OllamaLLMHandler, create_llm_handler


class TestOllamaLLMHandler(unittest.TestCase):
    """Testes para a classe OllamaLLMHandler"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        with patch('llm_handler.OllamaService'):
            self.handler = OllamaLLMHandler(base_url="http://localhost:11434")
            self.handler.ollama_service = Mock()
    
    def test_is_configured_true(self):
        """Testa verificação de configuração quando Ollama está disponível"""
        self.handler.ollama_service.list_models.return_value = [
            {"name": "llama2:latest"}
        ]
        
        result = self.handler.is_configured()
        self.assertTrue(result)
    
    def test_is_configured_false(self):
        """Testa verificação de configuração quando Ollama não está disponível"""
        self.handler.ollama_service.list_models.side_effect = ConnectionError()
        
        result = self.handler.is_configured()
        self.assertFalse(result)
    
    @patch('llm_handler.get_system_prompt')
    @patch('llm_handler.get_model_parameters')
    @patch('llm_handler.validate_user_input')
    def test_generate_response_success(self, mock_validate, mock_params, mock_prompt):
        """Testa geração de resposta com sucesso"""
        # Configurar mocks
        mock_validate.return_value = (True, None)
        mock_prompt.return_value = "System prompt"
        mock_params.return_value = {"temperature": 0.7}
        
        self.handler.ollama_service.chat.return_value = {
            "message": {
                "role": "assistant",
                "content": "Resposta do modelo"
            }
        }
        
        # Executar
        result = self.handler.generate_response(
            user_input="Teste",
            model="llama2:latest"
        )
        
        # Verificar
        self.assertEqual(result, "Resposta do modelo")
        self.handler.ollama_service.chat.assert_called_once()
    
    def test_list_available_models(self):
        """Testa listagem de modelos disponíveis"""
        self.handler.ollama_service.list_models.return_value = [
            {"name": "llama2:latest"},
            {"name": "mistral:latest"}
        ]
        
        models = self.handler.list_available_models()
        
        self.assertEqual(len(models), 2)
        self.assertIn("llama2:latest", models)
        self.assertIn("mistral:latest", models)
    
    def test_get_connection_status_connected(self):
        """Testa status de conexão quando conectado"""
        self.handler.ollama_service.list_models.return_value = [
            {"name": "llama2:latest"}
        ]
        
        status = self.handler.get_connection_status()
        
        self.assertTrue(status["connected"])
        self.assertEqual(status["model_count"], 1)
    
    def test_get_connection_status_disconnected(self):
        """Testa status de conexão quando desconectado"""
        self.handler.ollama_service.list_models.side_effect = ConnectionError("Erro")
        
        status = self.handler.get_connection_status()
        
        self.assertFalse(status["connected"])
        self.assertIn("não está rodando", status["message"])


class TestCreateLLMHandler(unittest.TestCase):
    """Testes para a função create_llm_handler"""
    
    @patch('llm_handler.OllamaLLMHandler')
    def test_create_with_url(self, mock_handler_class):
        """Testa criação de handler com URL"""
        mock_handler = Mock()
        mock_handler_class.return_value = mock_handler
        
        result = create_llm_handler("http://test:11434")
        
        mock_handler_class.assert_called_once_with(base_url="http://test:11434")
        self.assertEqual(result, mock_handler)
    
    @patch('llm_handler.OllamaLLMHandler')
    def test_create_without_url(self, mock_handler_class):
        """Testa criação de handler sem URL"""
        mock_handler = Mock()
        mock_handler_class.return_value = mock_handler
        
        result = create_llm_handler()
        
        mock_handler_class.assert_called_once_with(base_url="http://localhost:11434")
        self.assertEqual(result, mock_handler)


if __name__ == '__main__':
    unittest.main()

