"""
Testes unitários para history_manager
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
from history_manager import (
    save_history,
    load_history,
    list_history_sessions,
    delete_history,
    HISTORY_DIR
)


class TestHistoryManager(unittest.TestCase):
    """Testes para gerenciamento de histórico"""
    
    def setUp(self):
        """Configuração inicial - criar diretório temporário"""
        # Usar diretório temporário para testes
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_dir = HISTORY_DIR
        
        # Patch do HISTORY_DIR
        import history_manager
        history_manager.HISTORY_DIR = self.test_dir
        history_manager.HISTORY_DIR.mkdir(exist_ok=True)
    
    def tearDown(self):
        """Limpeza após cada teste"""
        # Remover diretório temporário
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        
        # Restaurar diretório original
        import history_manager
        history_manager.HISTORY_DIR = self.original_dir
    
    def test_save_history(self):
        """Testa salvamento de histórico"""
        messages = [
            {"role": "user", "content": "Olá"},
            {"role": "assistant", "content": "Oi!"}
        ]
        
        filepath = save_history(messages, "test_session")
        
        # Verificar se arquivo foi criado
        self.assertTrue(Path(filepath).exists())
        
        # Verificar conteúdo
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.assertEqual(data["session_id"], "test_session")
        self.assertEqual(len(data["messages"]), 2)
    
    def test_load_history(self):
        """Testa carregamento de histórico"""
        # Criar arquivo de teste
        messages = [
            {"role": "user", "content": "Teste"}
        ]
        save_history(messages, "test_load")
        
        # Carregar
        loaded = load_history("test_load")
        
        self.assertIsNotNone(loaded)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["content"], "Teste")
    
    def test_load_history_not_found(self):
        """Testa carregamento de histórico inexistente"""
        loaded = load_history("nonexistent")
        self.assertIsNone(loaded)
    
    def test_list_history_sessions(self):
        """Testa listagem de sessões"""
        # Criar múltiplas sessões
        save_history([{"role": "user", "content": "1"}], "session1")
        save_history([{"role": "user", "content": "2"}], "session2")
        
        sessions = list_history_sessions()
        
        self.assertEqual(len(sessions), 2)
        self.assertTrue(any(s["session_id"] == "session1" for s in sessions))
        self.assertTrue(any(s["session_id"] == "session2" for s in sessions))
    
    def test_delete_history(self):
        """Testa deleção de histórico"""
        # Criar e deletar
        messages = [{"role": "user", "content": "Teste"}]
        filepath = save_history(messages, "test_delete")
        
        self.assertTrue(Path(filepath).exists())
        
        deleted = delete_history("test_delete")
        self.assertTrue(deleted)
        self.assertFalse(Path(filepath).exists())
    
    def test_delete_history_not_found(self):
        """Testa deleção de histórico inexistente"""
        deleted = delete_history("nonexistent")
        self.assertFalse(deleted)


if __name__ == '__main__':
    unittest.main()

