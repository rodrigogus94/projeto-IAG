"""
Testes unitários para input_validator
"""

import unittest
from input_validator import (
    validate_user_input,
    validate_model_name,
    validate_messages,
    sanitize_input,
    _has_excessive_repetition
)


class TestInputValidator(unittest.TestCase):
    """Testes para validação de inputs"""
    
    def test_validate_user_input_empty(self):
        """Testa validação de input vazio"""
        is_valid, error = validate_user_input("")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_user_input_too_short(self):
        """Testa input muito curto"""
        is_valid, error = validate_user_input("a", min_length=5)
        self.assertFalse(is_valid)
        self.assertIn("curto", error.lower())
    
    def test_validate_user_input_too_long(self):
        """Testa input muito longo"""
        long_text = "a" * 10001
        is_valid, error = validate_user_input(long_text, max_length=10000)
        self.assertFalse(is_valid)
        self.assertIn("longo", error.lower())
    
    def test_validate_user_input_valid(self):
        """Testa input válido"""
        is_valid, error = validate_user_input("Esta é uma mensagem válida")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_user_input_only_spaces(self):
        """Testa input com apenas espaços"""
        is_valid, error = validate_user_input("   ")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_model_name_empty(self):
        """Testa nome de modelo vazio"""
        is_valid, error = validate_model_name("")
        self.assertFalse(is_valid)
    
    def test_validate_model_name_valid(self):
        """Testa nome de modelo válido"""
        is_valid, error = validate_model_name("llama2:latest")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_model_name_invalid_chars(self):
        """Testa nome de modelo com caracteres inválidos"""
        is_valid, error = validate_model_name("model@name#")
        self.assertFalse(is_valid)
    
    def test_validate_messages_empty(self):
        """Testa lista de mensagens vazia"""
        is_valid, error = validate_messages([])
        self.assertFalse(is_valid)
    
    def test_validate_messages_valid(self):
        """Testa lista de mensagens válida"""
        messages = [
            {"role": "user", "content": "Olá"},
            {"role": "assistant", "content": "Oi!"}
        ]
        is_valid, error = validate_messages(messages)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_messages_missing_role(self):
        """Testa mensagem sem campo role"""
        messages = [{"content": "Mensagem sem role"}]
        is_valid, error = validate_messages(messages)
        self.assertFalse(is_valid)
        self.assertIn("role", error.lower())
    
    def test_sanitize_input(self):
        """Testa sanitização de input"""
        dirty_input = "  Texto   com   espaços   extras  "
        sanitized = sanitize_input(dirty_input)
        self.assertEqual(sanitized, "Texto com espaços extras")
    
    def test_has_excessive_repetition(self):
        """Testa detecção de repetição excessiva"""
        # Texto com muitas repetições
        repetitive = "a" * 100
        self.assertTrue(_has_excessive_repetition(repetitive, threshold=50))
        
        # Texto normal
        normal = "Esta é uma mensagem normal"
        self.assertFalse(_has_excessive_repetition(normal, threshold=50))


if __name__ == '__main__':
    unittest.main()

