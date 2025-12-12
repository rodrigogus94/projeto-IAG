#  Como Executar o Projeto

##  Execução Rápida

### Executar a Aplicação Principal

**Na raiz do projeto**, execute:

```bash
streamlit run src/app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

---

##  Pré-requisitos

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o Ollama

Antes de executar a aplicação, inicie o servidor Ollama:

```bash
ollama serve
```

Ou no Windows, inicie pelo menu Iniciar.

### 3. Baixar um Modelo (se necessário)

```bash
ollama pull llama2
# ou
ollama pull mistral
```

---

##  Executar Testes

### Todos os testes:

```bash
python tests/run_tests.py
```

### Teste específico:

```bash
python -m unittest tests.test_ollama_service
```

---

##  Scripts Utilitários

### Diagnóstico do Ollama:

```bash
python scripts/diagnose_ollama.py
```

---

##  Configuração (Opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=120
TRANSCRIPTION_METHOD=whisper
LOG_LEVEL=INFO
OPENAI_API_KEY=sk-sua-chave-aqui
```

---

##  Estrutura de Pastas

```
projeto-sdk-mk00/
├── src/              # Código fonte
│   ├── app.py        # ← Execute: streamlit run src/app.py
│   ├── core/         # Módulos principais
│   └── config/       # Configurações
├── tests/            # Testes
├── docs/             # Documentação
├── scripts/          # Scripts
└── data/             # Dados (criado automaticamente)
    ├── logs/
    └── chat_history/
```

---

##  Importante

1. **Sempre execute da raiz do projeto** (não entre nas pastas)
2. **O Ollama deve estar rodando** antes de iniciar
3. **Python 3.8+** é necessário

---

##  Problemas Comuns

### Erro: "No module named 'src'"

**Solução:** O arquivo `src/app.py` já foi corrigido para adicionar automaticamente o diretório raiz ao Python path. Certifique-se de:

1. Executar da raiz do projeto: `streamlit run src/app.py`
2. Não executar de dentro da pasta `src/`
3. Verificar se o arquivo `src/__init__.py` existe

### Erro: "Ollama não está disponível"

Execute o diagnóstico:

```bash
python scripts/diagnose_ollama.py
```

### Erro: "Porta já em uso"

Feche outras instâncias do Streamlit ou use:

```bash
streamlit run src/app.py --server.port 8502
```

---

##  Verificação Rápida

```bash
# 1. Verificar Python
python --version  # Deve ser 3.8+

# 2. Verificar Ollama
ollama list  # Deve listar modelos

# 3. Executar aplicação
streamlit run src/app.py
```

---

##  Comandos Resumidos

| Ação            | Comando                             |
| --------------- | ----------------------------------- |
| Executar app    | `streamlit run src/app.py`          |
| Executar testes | `python tests/run_tests.py`         |
| Diagnóstico     | `python scripts/diagnose_ollama.py` |
| Ver logs        | `type data\logs\app.log` (Windows)  |

---

##  Solução do Erro "No module named 'src'"

O erro ocorria porque o Python não encontrava o pacote `src` quando executávamos `streamlit run src/app.py`.

**Correção aplicada:** O arquivo `src/app.py` foi atualizado para adicionar automaticamente o diretório raiz do projeto ao `sys.path` no início do arquivo. Isso permite que os imports `from src.core...` e `from src.config...` funcionem corretamente.

Se ainda encontrar o erro:

1. Certifique-se de estar na raiz do projeto
2. Verifique se o arquivo `src/__init__.py` existe
3. Execute: `python -c "import sys; print(sys.path)"` para verificar o path
