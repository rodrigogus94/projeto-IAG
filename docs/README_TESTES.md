# Testes Unitários

Este projeto inclui testes unitários para garantir a qualidade e funcionamento correto dos módulos principais.

## Estrutura de Testes

```
projeto-sdk-mk00/
├── test_ollama_service.py      # Testes para OllamaService
├── test_llm_handler.py          # Testes para OllamaLLMHandler
├── test_input_validator.py      # Testes para validação de inputs
├── test_history_manager.py      # Testes para gerenciamento de histórico
└── README_TESTES.md             # Este arquivo
```

## Como Executar os Testes

### Opção 1: Usando unittest (padrão do Python)

Execute cada arquivo de teste individualmente:

```bash
python test_ollama_service.py
python test_llm_handler.py
python test_input_validator.py
python test_history_manager.py
```

### Opção 2: Executar todos os testes de uma vez

```bash
python -m unittest discover -s . -p "test_*.py"
```

### Opção 3: Usando pytest (recomendado, se instalado)

```bash
# Instalar pytest (opcional)
pip install pytest pytest-cov

# Executar todos os testes
pytest test_*.py

# Executar com cobertura
pytest test_*.py --cov=. --cov-report=html
```

## Cobertura de Testes

Os testes cobrem:

-  **OllamaService**: Listagem de modelos, geração de respostas, chat
-  **OllamaLLMHandler**: Configuração, geração de respostas, status de conexão
-  **Input Validator**: Validação de inputs do usuário, nomes de modelos, mensagens
-  **History Manager**: Salvamento, carregamento, listagem e deleção de históricos

## Adicionando Novos Testes

Para adicionar novos testes:

1. Crie um arquivo `test_<modulo>.py`
2. Importe `unittest` e o módulo a ser testado
3. Crie uma classe que herda de `unittest.TestCase`
4. Adicione métodos que começam com `test_`

Exemplo:

```python
import unittest
from meu_modulo import MinhaClasse

class TestMinhaClasse(unittest.TestCase):
    def test_metodo_exemplo(self):
        obj = MinhaClasse()
        resultado = obj.metodo_exemplo()
        self.assertEqual(resultado, esperado)
```

## Notas

- Os testes usam mocks para simular chamadas à API do Ollama
- Arquivos temporários são criados e limpos automaticamente
- Os testes não requerem que o Ollama esteja rodando

