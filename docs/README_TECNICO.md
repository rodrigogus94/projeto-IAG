# Documentação Técnica - Projeto Chat Assistente com IA

##  Índice

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Fluxo de Dados](#fluxo-de-dados)
4. [Módulos e Componentes](#módulos-e-componentes)
5. [Conexões e Dependências](#conexões-e-dependências)
6. [Fluxo de Execução](#fluxo-de-execução)
7. [Configuração e Inicialização](#configuração-e-inicialização)
8. [Tecnologias Utilizadas](#tecnologias-utilizadas)
9. [Diagrama de Arquitetura](#diagrama-de-arquitetura)

---

##  Visão Geral do Projeto

### Objetivo

Desenvolver uma aplicação web interativa de chat com IA que permite aos usuários conversar com modelos de linguagem locais através do Ollama, com suporte para entrada por texto e voz, persistência de histórico e validação de dados.

### Funcionalidades Principais

- **Chat Interativo**: Interface web para conversação com modelos de IA
- **Múltiplos Modelos**: Suporte para diferentes modelos do Ollama
- **Entrada por Voz**: Transcrição de áudio para texto
- **Persistência**: Salvamento automático de conversas
- **Validação**: Validação e sanitização de inputs
- **Logging**: Sistema completo de logs estruturados
- **Testes**: Suite de testes unitários

---

##  Arquitetura do Sistema

### Padrão Arquitetural

O projeto segue uma **arquitetura em camadas (Layered Architecture)** com separação clara de responsabilidades:

```
┌─────────────────────────────────────────┐
│         CAMADA DE APRESENTAÇÃO          │
│           (app.py - Streamlit)          │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│        CAMADA DE APLICAÇÃO              │
│    (llm_handler.py, input_validator.py) │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│        CAMADA DE SERVIÇOS               │
│  (ollama_service.py, audio_transcriber.py)│
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      CAMADA DE CONFIGURAÇÃO             │
│      (model_config.py, logging_config.py)│
└─────────────────────────────────────────┘
```

### Princípios de Design

1. **Separação de Responsabilidades**: Cada módulo tem uma função específica
2. **Baixo Acoplamento**: Módulos se comunicam através de interfaces bem definidas
3. **Alta Coesão**: Funcionalidades relacionadas estão agrupadas
4. **Configuração Centralizada**: Parâmetros em `model_config.py`
5. **Tratamento de Erros**: Logging e validação em todas as camadas

---

##  Fluxo de Dados

### Fluxo Principal: Envio de Mensagem

```
┌─────────────┐
│   Usuário   │
│  (Streamlit)│
└──────┬──────┘
       │ 1. Digita mensagem
       ▼
┌──────────────────┐
│   app.py         │
│  - Valida input  │
│  - Sanitiza      │
└──────┬───────────┘
       │ 2. Input validado
       ▼
┌──────────────────┐
│ input_validator  │
│  - Validação     │
│  - Sanitização   │
└──────┬───────────┘
       │ 3. Input limpo
       ▼
┌──────────────────┐
│  llm_handler     │
│  - Prepara       │
│  - Adiciona      │
│    system prompt │
└──────┬───────────┘
       │ 4. Mensagens formatadas
       ▼
┌──────────────────┐
│ ollama_service   │
│  - HTTP Request  │
│  - API Ollama    │
└──────┬───────────┘
       │ 5. Resposta JSON
       ▼
┌──────────────────┐
│  llm_handler     │
│  - Extrai texto  │
│  - Formata       │
└──────┬───────────┘
       │ 6. Resposta formatada
       ▼
┌──────────────────┐
│   app.py         │
│  - Exibe UI      │
│  - Salva histórico│
└──────┬───────────┘
       │ 7. Atualiza interface
       ▼
┌─────────────┐
│   Usuário   │
│  (Streamlit)│
└─────────────┘
```

### Fluxo de Transcrição de Áudio

```
┌─────────────┐
│   Usuário   │
│  (Grava áudio)│
└──────┬──────┘
       │ 1. Arquivo de áudio
       ▼
┌──────────────────┐
│   app.py         │
│  - Recebe áudio  │
└──────┬───────────┘
       │ 2. Arquivo temporário
       ▼
┌──────────────────┐
│ audio_transcriber│
│  - Escolhe método│
│  - Transcreve    │
└──────┬───────────┘
       │ 3. Texto transcrito
       ▼
┌──────────────────┐
│   app.py         │
│  - Usa como input│
└──────┬───────────┘
       │ 4. Segue fluxo principal
       ▼
    [Fluxo Principal]
```

---

##  Módulos e Componentes

### 1. `app.py` - Camada de Apresentação

**Responsabilidade**: Interface do usuário e gerenciamento de estado

**Funcionalidades**:
- Interface Streamlit (sidebar + área principal)
- Gerenciamento de sessão (session_state)
- Renderização de mensagens
- Controles de configuração
- Integração com todos os módulos

**Dependências**:
- `llm_handler` → Geração de respostas
- `audio_transcriber` → Transcrição de áudio
- `input_validator` → Validação de inputs
- `history_manager` → Persistência
- `styles.py` → Estilos CSS
- `logging_config` → Logging

**Conexões**:
```
app.py
├──→ llm_handler.create_llm_handler()
├──→ audio_transcriber.transcribe_audio()
├──→ input_validator.validate_user_input()
├──→ input_validator.sanitize_input()
├──→ history_manager.auto_save_history()
└──→ logging_config.setup_logging()
```

---

### 2. `llm_handler.py` - Camada de Aplicação

**Responsabilidade**: Adaptação entre UI e serviços de LLM

**Classe Principal**: `OllamaLLMHandler`

**Métodos Principais**:
- `generate_response()`: Gera resposta do modelo
- `is_configured()`: Verifica conexão
- `get_connection_status()`: Status detalhado
- `list_available_models()`: Lista modelos

**Dependências**:
- `ollama_service` → Comunicação com Ollama
- `model_config` → Configurações e prompts
- `input_validator` → Validação

**Conexões**:
```
llm_handler.py
├──→ ollama_service.OllamaService
├──→ model_config.get_system_prompt()
├──→ model_config.get_model_parameters()
├──→ model_config.validate_temperature()
├──→ input_validator.validate_user_input()
├──→ input_validator.validate_model_name()
└──→ input_validator.validate_messages()
```

**Fluxo Interno**:
1. Recebe mensagens do `app.py`
2. Valida inputs
3. Adiciona system prompt
4. Prepara parâmetros do modelo
5. Chama `ollama_service.chat()`
6. Processa resposta
7. Retorna texto formatado

---

### 3. `ollama_service.py` - Camada de Serviços

**Responsabilidade**: Comunicação HTTP com API do Ollama

**Classe Principal**: `OllamaService`

**Métodos Principais**:
- `list_models()`: Lista modelos disponíveis
- `chat()`: Interface de chat com histórico
- `generate_response()`: Geração direta (legado)
- `_handle_stream_response()`: Processa streaming

**Dependências**:
- `requests` → HTTP client
- `logging` → Logging estruturado
- `model_config` → Timeout padrão

**Endpoints Ollama Utilizados**:
- `GET /api/tags` → Listar modelos
- `POST /api/chat` → Chat com histórico
- `POST /api/generate` → Geração direta

**Conexões**:
```
ollama_service.py
├──→ requests.get() → Listar modelos
├──→ requests.post() → Chat/Geração
├──→ model_config.MODEL_RULES → Timeout
└──→ logging → Logs de operações
```

---

### 4. `audio_transcriber.py` - Camada de Serviços

**Responsabilidade**: Transcrição de áudio para texto

**Funções Principais**:
- `transcribe_audio()`: Função principal
- `_transcribe_with_whisper()`: Whisper local
- `_transcribe_with_openai()`: OpenAI API
- `_temp_audio_file()`: Context manager para arquivos

**Dependências**:
- `whisper` (opcional) → Whisper local
- `openai` (opcional) → OpenAI API
- `tempfile` → Arquivos temporários
- `logging` → Logging

**Conexões**:
```
audio_transcriber.py
├──→ whisper.load_model() → Modelo Whisper
├──→ openai.OpenAI() → Cliente OpenAI
├──→ tempfile.NamedTemporaryFile() → Arquivos temp
└──→ logging → Logs de transcrição
```

**Fluxo de Transcrição**:
1. Recebe arquivo de áudio
2. Cria arquivo temporário (context manager)
3. Escolhe método (Whisper/OpenAI)
4. Transcreve áudio
5. Limpa arquivo temporário (garantido)
6. Retorna texto

---

### 5. `input_validator.py` - Camada de Aplicação

**Responsabilidade**: Validação e sanitização de inputs

**Funções Principais**:
- `validate_user_input()`: Valida mensagens
- `validate_model_name()`: Valida nomes de modelos
- `validate_messages()`: Valida lista de mensagens
- `sanitize_input()`: Remove caracteres problemáticos
- `_has_excessive_repetition()`: Detecta spam

**Dependências**:
- `model_config.VALIDATION_RULES` → Regras de validação
- `re` → Expressões regulares
- `logging` → Logging

**Conexões**:
```
input_validator.py
├──→ model_config.VALIDATION_RULES → Limites
├──→ re.match() → Validação de padrões
└──→ logging → Logs de validação
```

**Validações Implementadas**:
- Comprimento mínimo/máximo
- Caracteres válidos
- Repetição excessiva
- Estrutura de mensagens
- Formato de nomes de modelos

---

### 6. `history_manager.py` - Camada de Persistência

**Responsabilidade**: Gerenciamento de histórico de conversas

**Funções Principais**:
- `save_history()`: Salva histórico em JSON
- `load_history()`: Carrega histórico
- `list_history_sessions()`: Lista sessões
- `delete_history()`: Deleta histórico
- `auto_save_history()`: Auto-salvamento

**Dependências**:
- `json` → Serialização
- `pathlib` → Manipulação de caminhos
- `datetime` → Timestamps
- `logging` → Logging

**Estrutura de Arquivo JSON**:
```json
{
  "session_id": "session_20240101_120000",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:30:00",
  "message_count": 10,
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

**Conexões**:
```
history_manager.py
├──→ json.dump() → Salvar JSON
├──→ json.load() → Carregar JSON
├──→ Path.mkdir() → Criar diretório
└──→ logging → Logs de operações
```

---

### 7. `model_config.py` - Camada de Configuração

**Responsabilidade**: Configurações centralizadas do modelo

**Constantes Principais**:
- `SYSTEM_PROMPT`: Persona do assistente
- `DEFAULT_TEMPERATURE`: Temperatura padrão
- `DEFAULT_MODEL`: Modelo padrão
- `MODEL_RULES`: Regras e limites
- `CONTEXT_PROMPTS`: Prompts por contexto
- `VALIDATION_RULES`: Regras de validação

**Funções Principais**:
- `get_system_prompt()`: Retorna prompt com contexto
- `validate_temperature()`: Valida temperatura
- `get_model_parameters()`: Parâmetros do Ollama
- `get_behavior_settings()`: Configurações de comportamento

**Conexões**:
```
model_config.py
└──→ [Usado por todos os módulos]
    ├──→ llm_handler → Prompts e parâmetros
    ├──→ ollama_service → Timeout
    ├──→ input_validator → Regras de validação
    └──→ app.py → Configurações padrão
```

---

### 8. `logging_config.py` - Camada de Configuração

**Responsabilidade**: Configuração de logging

**Funções Principais**:
- `setup_logging()`: Configura sistema de logs
- `get_logger()`: Retorna logger configurado

**Características**:
- Rotação automática de arquivos (10MB, 5 backups)
- Logs em arquivo (`logs/app.log`)
- Níveis configuráveis (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Formato estruturado com timestamps

**Conexões**:
```
logging_config.py
└──→ [Usado por todos os módulos]
    ├──→ logging.RotatingFileHandler
    ├──→ logging.StreamHandler
    └──→ logging.Formatter
```

---

### 9. `styles.py` - Camada de Apresentação

**Responsabilidade**: Estilos CSS customizados

**Conteúdo**:
- `CUSTOM_CSS`: String com estilos CSS
- Estilos para sidebar, chat, dashboard
- Suporte a temas claro/escuro

**Conexões**:
```
styles.py
└──→ app.py → st.markdown(CUSTOM_CSS)
```

---

##  Conexões e Dependências

### Mapa de Dependências

```
app.py
│
├─→ llm_handler.py
│   ├─→ ollama_service.py
│   │   ├─→ requests
│   │   └─→ model_config.py
│   ├─→ model_config.py
│   └─→ input_validator.py
│       └─→ model_config.py
│
├─→ audio_transcriber.py
│   ├─→ whisper (opcional)
│   └─→ openai (opcional)
│
├─→ input_validator.py
│   └─→ model_config.py
│
├─→ history_manager.py
│
├─→ logging_config.py
│
└─→ styles.py
```

### Dependências Externas

```
requests          → HTTP client para Ollama
streamlit         → Framework web
python-dotenv     → Variáveis de ambiente
openai-whisper    → Transcrição local (opcional)
openai            → API OpenAI (opcional)
```

---

##  Fluxo de Execução

### Passo a Passo: Inicialização

1. **Carregamento de Variáveis de Ambiente**
   - `app.py` → `load_dotenv()`
   - Lê `.env` se existir

2. **Configuração de Logging**
   - `app.py` → `logging_config.setup_logging()`
   - Cria diretório `logs/`
   - Configura handlers de arquivo e console

3. **Importação de Módulos**
   - `app.py` importa todos os módulos
   - Fallbacks se módulos não disponíveis

4. **Configuração do Streamlit**
   - `st.set_page_config()`
   - Aplica CSS customizado

5. **Inicialização do Ollama Handler**
   - `app.py` → `create_llm_handler()`
   - `llm_handler` → `OllamaService()`
   - Verifica conexão silenciosamente

6. **Inicialização de Estado**
   - Cria `session_state` se não existir
   - Define valores padrão

### Passo a Passo: Envio de Mensagem

1. **Usuário digita mensagem**
   - `app.py` recebe via `st.chat_input()`

2. **Validação**
   - `app.py` → `sanitize_input()`
   - `app.py` → `validate_user_input()`
   - Se inválido: exibe erro e para

3. **Adição ao Histórico**
   - `app.py` adiciona mensagem do usuário ao `session_state.messages`

4. **Exibição Imediata**
   - `app.py` exibe mensagem do usuário na UI

5. **Geração de Resposta**
   - `app.py` → `llm_handler.generate_response()`
   - `llm_handler` valida e prepara mensagens
   - `llm_handler` → `ollama_service.chat()`
   - `ollama_service` faz requisição HTTP
   - Ollama processa e retorna resposta

6. **Processamento de Resposta**
   - `ollama_service` retorna JSON
   - `llm_handler` extrai texto
   - `llm_handler` retorna string

7. **Exibição e Persistência**
   - `app.py` exibe resposta na UI
   - `app.py` adiciona ao `session_state.messages`
   - `app.py` → `history_manager.auto_save_history()`
   - Salva em `chat_history/current.json`

8. **Atualização da Interface**
   - `app.py` → `st.rerun()`
   - Atualiza sidebar com histórico

---

## ⚙️ Configuração e Inicialização

### Arquivo `.env`

```env
# URL do servidor Ollama
OLLAMA_BASE_URL=http://localhost:11434

# Timeout para requisições (segundos)
OLLAMA_TIMEOUT=120

# Método de transcrição
TRANSCRIPTION_METHOD=whisper

# Nível de log
LOG_LEVEL=INFO

# OpenAI API Key (opcional)
OPENAI_API_KEY=sk-...
```

### Ordem de Prioridade de Configuração

1. **Variável de Ambiente** (`.env`) - Maior prioridade
2. **`model_config.py`** - Valores padrão do projeto
3. **Hardcoded** - Fallback final

### Inicialização de Diretórios

```
projeto-sdk-mk00/
├── logs/              # Criado automaticamente
│   └── app.log
├── chat_history/      # Criado automaticamente
│   └── current.json
└── __pycache__/       # Criado pelo Python
```

---

##  Tecnologias Utilizadas

### Backend

- **Python 3.8+**: Linguagem principal
- **Streamlit**: Framework web
- **Requests**: Cliente HTTP
- **Ollama**: Servidor de modelos locais

### Processamento de Áudio

- **OpenAI Whisper**: Transcrição local
- **OpenAI API**: Transcrição via API

### Persistência

- **JSON**: Formato de histórico
- **Pathlib**: Manipulação de caminhos

### Logging

- **logging**: Módulo padrão Python
- **RotatingFileHandler**: Rotação de logs

### Testes

- **unittest**: Framework de testes
- **unittest.mock**: Mocks para testes

---

##  Diagrama de Arquitetura

### Diagrama Simplificado

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO                              │
│                  (Navegador)                           │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              app.py (Streamlit)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   UI/UX      │  │  Validação   │  │  Persistência│  │
│  │  Renderização│  │  Sanitização │  │  Histórico   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└──────┬───────────────────┬───────────────────┬──────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│llm_handler   │  │input_validator│ │history_manager│
│              │  │              │  │              │
│- Adaptação   │  │- Validação   │  │- JSON        │
│- Prompts     │  │- Sanitização │  │- Sessões     │
└──────┬───────┘  └──────────────┘  └──────────────┘
       │
       ▼
┌──────────────┐
│ollama_service│
│              │
│- HTTP        │
│- API Calls   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Ollama     │
│   Server     │
│              │
│- Modelos     │
│- Processamento│
└──────────────┘
```

### Fluxo de Dados Detalhado

```
[Usuário] → [app.py]
              │
              ├─→ [input_validator] → Validação
              │
              ├─→ [llm_handler] → Preparação
              │     │
              │     └─→ [ollama_service] → HTTP
              │           │
              │           └─→ [Ollama API] → Processamento
              │           │
              │           └─→ Resposta JSON
              │     │
              │     └─→ Processamento
              │
              ├─→ [history_manager] → Persistência
              │
              └─→ [UI Update] → Exibição
```

---

##  Resumo para Apresentação

### Pontos Principais

1. **Arquitetura em Camadas**: Separação clara de responsabilidades
2. **Modularidade**: Cada módulo tem função específica
3. **Configuração Centralizada**: `model_config.py` como fonte única
4. **Robustez**: Validação, logging e tratamento de erros
5. **Extensibilidade**: Fácil adicionar novos recursos
6. **Testabilidade**: Testes unitários para todos os módulos

### Fluxo Simplificado

```
Input → Validação → Processamento → Resposta → Persistência → UI
```

### Tecnologias-Chave

- **Streamlit**: Interface web rápida
- **Ollama**: Modelos locais de IA
- **Python**: Linguagem principal
- **JSON**: Persistência simples

---

##  Detalhes Técnicos Adicionais

### Tratamento de Erros

Cada camada trata erros apropriadamente:

- **app.py**: Exibe mensagens amigáveis ao usuário
- **llm_handler**: Retorna mensagens de erro estruturadas
- **ollama_service**: Propaga erros HTTP com contexto
- **audio_transcriber**: Garante limpeza de arquivos mesmo em erro

### Logging Estruturado

Todos os módulos usam logging:

- **Nível DEBUG**: Detalhes de operações
- **Nível INFO**: Operações importantes
- **Nível WARNING**: Avisos não críticos
- **Nível ERROR**: Erros que precisam atenção

### Validação em Múltiplas Camadas

1. **Frontend**: Validação básica no `app.py`
2. **Aplicação**: Validação completa no `input_validator`
3. **Serviço**: Validação de formato no `ollama_service`

---

##  Referências

- **Streamlit**: https://streamlit.io/
- **Ollama**: https://ollama.ai/
- **OpenAI Whisper**: https://github.com/openai/whisper
- **Python Logging**: https://docs.python.org/3/library/logging.html

---

**Documento gerado para relatório e apresentação técnica do projeto**

