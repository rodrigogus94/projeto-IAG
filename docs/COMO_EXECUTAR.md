# Como Executar o Projeto Após Organização

##  Estrutura do Projeto

O projeto foi organizado em pastas:

```
projeto-sdk-mk00/
├── src/                    # Código fonte
│   ├── app.py             # Aplicação principal
│   ├── core/              # Módulos principais
│   └── config/            # Configurações
├── tests/                  # Testes unitários
├── docs/                   # Documentação
├── scripts/                # Scripts utilitários
└── data/                   # Dados (logs, histórico)
```

##  Executar a Aplicação

### Opção 1: Streamlit (Recomendado)

No terminal, na raiz do projeto:

```bash
streamlit run src/app.py
```

### Opção 2: Python direto

```bash
python -m streamlit run src/app.py
```

##  Executar Testes

### Executar todos os testes:

```bash
cd tests
python run_tests.py
```

Ou da raiz do projeto:

```bash
python tests/run_tests.py
```

### Executar teste específico:

```bash
cd tests
python -m unittest test_ollama_service.py
```

##  Scripts Utilitários

### Diagnóstico do Ollama:

```bash
cd scripts
python diagnose_ollama.py
```

Ou da raiz:

```bash
python scripts/diagnose_ollama.py
```

##  Configuração

### 1. Instalar dependências:

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente (opcional):

Crie um arquivo `.env` na raiz do projeto:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=120
TRANSCRIPTION_METHOD=whisper
LOG_LEVEL=INFO
OPENAI_API_KEY=sk-sua-chave-aqui  # Opcional
```

### 3. Iniciar o Ollama:

```bash
ollama serve
```

##  Estrutura de Dados

Os dados são salvos em:

- **Logs**: `data/logs/app.log`
- **Histórico**: `data/chat_history/`

Essas pastas são criadas automaticamente quando necessário.

##  Solução de Problemas

### Erro de imports:

Se houver erros de import, certifique-se de:
1. Estar na raiz do projeto ao executar
2. Ter o Python path configurado corretamente
3. Ter todas as dependências instaladas

### Ollama não conecta:

Execute o diagnóstico:
```bash
python scripts/diagnose_ollama.py
```

### Erro de módulo não encontrado:

Verifique se está executando da raiz do projeto:
```bash
# Correto
streamlit run src/app.py

# Incorreto
cd src
streamlit run app.py
```

##  Notas Importantes

1. **Sempre execute da raiz do projeto** - Os caminhos relativos dependem disso
2. **O Ollama deve estar rodando** - Execute `ollama serve` antes de iniciar a aplicação
3. **Python 3.8+** - Certifique-se de ter Python 3.8 ou superior

##  Comandos Rápidos

```bash
# Executar aplicação
streamlit run src/app.py

# Executar testes
python tests/run_tests.py

# Diagnóstico
python scripts/diagnose_ollama.py

# Ver logs
cat data/logs/app.log  # Linux/Mac
type data\logs\app.log  # Windows
```

