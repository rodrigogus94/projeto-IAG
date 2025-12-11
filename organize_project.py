"""Script temporário para organizar o projeto em pastas"""

import shutil
import os
from pathlib import Path

# Obter o diretório do script
SCRIPT_DIR = Path(__file__).parent.absolute()
os.chdir(SCRIPT_DIR)

print(f"Diretório de trabalho: {os.getcwd()}")

# Mover arquivos
files_to_move = {
    "app.py": "src/app.py",
    "test_ollama_service.py": "tests/test_ollama_service.py",
    "test_llm_handler.py": "tests/test_llm_handler.py",
    "test_input_validator.py": "tests/test_input_validator.py",
    "test_history_manager.py": "tests/test_history_manager.py",
    "run_tests.py": "tests/run_tests.py",
    "diagnose_ollama.py": "scripts/diagnose_ollama.py",
}

docs_to_move = [
    "README_TECNICO.md",
    "INDICE_DOCUMENTACAO.md",
    "APRESENTACAO_PROJETO.md",
    "MELHORIAS_IMPLEMENTADAS.md",
    "README_TESTES.md",
    "CORRECAO_TIMEOUT.md",
    "INICIAR_OLLAMA.md",
]

# Mover arquivos Python
for src, dst in files_to_move.items():
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"✅ Copiado: {src} -> {dst}")
    else:
        print(f"⚠️ Arquivo não encontrado: {src}")

# Mover documentação (README.md fica na raiz)
for doc in docs_to_move:
    if os.path.exists(doc):
        os.makedirs("docs", exist_ok=True)
        shutil.copy2(doc, f"docs/{doc}")
        print(f"✅ Copiado: {doc} -> docs/{doc}")
    else:
        print(f"⚠️ Arquivo não encontrado: {doc}")

print("\n✅ Organização concluída!")
