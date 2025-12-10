"""
Script para executar todos os testes unitários
"""

import unittest
import sys
from pathlib import Path

def run_all_tests():
    """Executa todos os testes unitários"""
    
    # Adicionar diretório raiz do projeto ao path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Descobrir e executar todos os testes
    loader = unittest.TestLoader()
    suite = loader.discover(str(Path(__file__).parent), pattern='test_*.py')
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de saída baseado no resultado
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)

