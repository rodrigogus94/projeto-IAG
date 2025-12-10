# Chat Assistente com IA - Projeto IAG

Aplicação web de chat interativo com IA usando Streamlit e Ollama. Interface moderna e intuitiva para conversar com modelos de linguagem locais através do Ollama, com suporte para transcrição de áudio.

## Características

- **Interface Moderna**: Interface web responsiva construída com Streamlit
- **Ollama Integration**: Suporte completo para modelos locais via Ollama
- **Múltiplos Modelos**: Lista dinamicamente modelos disponíveis no Ollama
- **Transcrição de Áudio**: Suporte para entrada por voz usando Whisper (local) ou OpenAI API
- **Histórico Completo**: Mantém contexto completo da conversa
- **Persistência de Histórico**: Histórico salvo automaticamente em arquivos JSON
- **Validação de Inputs**: Validação automática de mensagens antes de enviar ao modelo
- **Logging Estruturado**: Sistema completo de logs com rotação automática
- **Testes Unitários**: Suite completa de testes para garantir qualidade
- **Streaming de Respostas**: Infraestrutura pronta para streaming (pode ser ativado)
- **Configuração Flexível**: Suporte para variáveis de ambiente (.env) ou configuração manual
- **Arquitetura Modular**: Código organizado e separado por responsabilidades
- **Timeout Configurável**: Timeout ajustável via model_config.py ou .env

## Pré-requisitos

- Python 3.8 ou superior
- Ollama instalado e rodando (https://ollama.ai/)
- pip (gerenciador de pacotes Python)
- (Opcional) OpenAI API Key para transcrição de áudio via API

## Instalação

1. **Clone ou baixe o projeto**

2. **Instale o Ollama** (se ainda não tiver):

   - Windows/Mac: Baixe de https://ollama.ai/
   - Linux: `curl -fsSL https://ollama.ai/install.sh | sh`

3. **Baixe um modelo do Ollama**:

   ```bash
   ollama pull llama2
   # ou
   ollama pull mistral
   # ou qualquer outro modelo disponível
   ```

4. **Instale as dependências do Python**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure variáveis de ambiente (opcional)**:

   Crie um arquivo `.env` na raiz do projeto:

   ```env
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_TIMEOUT=120
   TRANSCRIPTION_METHOD=whisper
   LOG_LEVEL=INFO
   # Opcional: para transcrição via OpenAI API
   OPENAI_API_KEY=sk-sua-chave-api-aqui
   ```

   **Variáveis disponíveis**:
   - `OLLAMA_BASE_URL`: URL do servidor Ollama (padrão: http://localhost:11434)
   - `OLLAMA_TIMEOUT`: Timeout para requisições em segundos (padrão: 120, vem de model_config.py)
   - `TRANSCRIPTION_METHOD`: Método de transcrição ("whisper" ou "openai")
   - `LOG_LEVEL`: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   - `OPENAI_API_KEY`: Chave da API OpenAI (opcional, apenas para transcrição via API)

## Como Usar

1. **Certifique-se de que o Ollama está rodando**:

   ```bash
   ollama serve
   ```

2. **Inicie a aplicação**:

   ```bash
   streamlit run app.py
   ```

3. **Configure a conexão**:

   - Na sidebar, expanda "⚙️ Configurações"
   - Verifique se a URL do Ollama está correta (padrão: http://localhost:11434)
   - Clique em " Reconectar ao Ollama" se necessário
   - Selecione o modelo desejado (será listado automaticamente)

4. **Comece a conversar**:
   - Digite sua mensagem no campo de input
   - Ou use o microfone para gravar uma mensagem de voz
   - A IA responderá mantendo o contexto da conversa
   - Use " Limpar Chat" para reiniciar a conversa

## Configurações

### Modelos Ollama

O aplicativo lista automaticamente os modelos disponíveis no seu Ollama. Para baixar novos modelos:

```bash
ollama pull llama2
ollama pull mistral
ollama pull codellama
# etc.
```

### Transcrição de Áudio

Dois métodos disponíveis:

1. **Whisper Local** (padrão):

   - Usa `openai-whisper` instalado localmente
   - Não requer API Key
   - Processa localmente (pode ser mais lento)

2. **OpenAI API**:
   - Usa a API da OpenAI para transcrição
   - Requer `OPENAI_API_KEY` no `.env`
   - Mais rápido, mas requer conexão com internet

Configure no menu de configurações ou via variável de ambiente `TRANSCRIPTION_METHOD`.

### Parâmetros

- **Temperature**: Controla a criatividade (0.0 = determinístico, 2.0 = muito criativo)
- **Modelo**: Selecione entre os modelos disponíveis no Ollama
- **Timeout**: Configurável via `model_config.py` ou variável de ambiente `OLLAMA_TIMEOUT`

### Timeout

O timeout pode ser configurado de duas formas:

1. **Via `model_config.py`** (recomendado para valores padrão):
   ```python
   MODEL_RULES = {
       "timeout_seconds": 120,  # Timeout padrão em segundos
       # ...
   }
   ```

2. **Via `.env`** (sobrescreve o model_config.py):
   ```env
   OLLAMA_TIMEOUT=180
   ```

   **Valores recomendados**:
   - Modelos pequenos: 60-90 segundos
   - Modelos médios: 120-180 segundos
   - Modelos grandes: 180-300 segundos

   O timeout para chat é automaticamente dobrado (ex: 120s → 240s) para dar mais tempo à geração de respostas.

## Estrutura do Projeto

```
projeto-sdk-mk00/
├── app.py                  # Interface Streamlit principal
├── llm_handler.py          # Handler que integra OllamaService
├── ollama_service.py       # Serviço para comunicação com Ollama
├── audio_transcriber.py    # Módulo de transcrição de áudio
├── model_config.py         # Configurações centralizadas do modelo
├── input_validator.py      # Validação de inputs do usuário
├── history_manager.py      # Gerenciamento de persistência de histórico
├── logging_config.py       # Configuração de logging estruturado
├── styles.py               # Estilos CSS customizados
├── diagnose_ollama.py      # Script de diagnóstico do Ollama
├── run_tests.py            # Script para executar todos os testes
├── test_*.py               # Testes unitários
├── requirements.txt        # Dependências do projeto
├── .env                    # Variáveis de ambiente (criar)
├── logs/                   # Diretório de logs (criado automaticamente)
│   └── app.log            # Arquivo de log principal
├── chat_history/           # Diretório de históricos (criado automaticamente)
│   └── *.json             # Arquivos de histórico de conversas
├── README.md               # Este arquivo
├── README_TESTES.md        # Documentação dos testes
├── MELHORIAS_IMPLEMENTADAS.md  # Documentação das melhorias
└── CORRECAO_TIMEOUT.md     # Documentação sobre timeout
```

## Arquitetura

O projeto segue uma arquitetura modular:

- **`app.py`**: Gerencia a interface do usuário, estado da aplicação e interações
- **`llm_handler.py`**: Adapta OllamaService para a interface esperada pelo app
- **`ollama_service.py`**: Encapsula toda a lógica de comunicação com a API do Ollama
- **`audio_transcriber.py`**: Gerencia transcrição de áudio (Whisper/OpenAI)
- **`model_config.py`**: **Centraliza todas as configurações do modelo** - regras, parâmetros, system prompts e instruções
- **`input_validator.py`**: Validação e sanitização de inputs do usuário
- **`history_manager.py`**: Gerenciamento de persistência de histórico de conversas
- **`logging_config.py`**: Configuração centralizada de logging estruturado
- **`styles.py`**: Centraliza todos os estilos CSS customizados
- **`diagnose_ollama.py`**: Script de diagnóstico para problemas de conexão

### Configuração do Modelo (`model_config.py`)

O arquivo `model_config.py` é o **centro de controle** para todas as configurações do modelo:

- **System Prompts**: Persona e instruções do assistente
- **Parâmetros Padrão**: Temperatura, modelo padrão, limites
- **Regras de Comportamento**: Como o modelo deve se comportar
- **Prompts por Contexto**: Instruções específicas para diferentes situações
- **Validações**: Regras de validação de inputs
- **Configurações Avançadas**: Retry, cache, logging, etc.

**Para personalizar o comportamento do modelo**, edite o arquivo `model_config.py`:

- Ajuste o `SYSTEM_PROMPT` para mudar a persona do assistente
- Modifique `DEFAULT_TEMPERATURE` para alterar a criatividade padrão
- Configure `MODEL_RULES["timeout_seconds"]` para ajustar o timeout padrão
- Adicione novos contextos em `CONTEXT_PROMPTS`
- Configure regras de validação em `VALIDATION_RULES`

## Solução de Problemas

### Ollama não conecta

1. **Execute o script de diagnóstico**:

   ```bash
   python diagnose_ollama.py
   ```

   Este script verifica automaticamente todos os aspectos da conexão.

2. **Verifique se o Ollama está rodando**:

   ```bash
   ollama list
   ```

   Se retornar erro, inicie o Ollama:

   ```bash
   ollama serve
   ```

3. **Verifique a URL nas configurações**:

   - Padrão: `http://localhost:11434`
   - Se estiver usando Docker: `http://localhost:11434` (ou a porta configurada)
   - Se estiver em servidor remoto: `http://IP_DO_SERVIDOR:11434`

4. **Verifique o firewall**:

   - O Ollama usa a porta 11434 por padrão
   - Certifique-se de que a porta não está bloqueada

5. **Teste manualmente a API**:
   ```bash
   curl http://localhost:11434/api/tags
   ```
   Deve retornar uma lista de modelos em JSON.

### Nenhum modelo disponível

1. Baixe pelo menos um modelo:

   ```bash
   ollama pull llama2
   ```

2. Clique em " Reconectar ao Ollama" nas configurações

### Transcrição de áudio não funciona

1. **Para Whisper local**:

   - Verifique se `openai-whisper` está instalado: `pip install openai-whisper`
   - O primeiro uso pode demorar (baixa o modelo)

2. **Para OpenAI API**:
   - Verifique se `OPENAI_API_KEY` está configurada no `.env`
   - Verifique sua conexão com a internet

### Erro ao importar módulos

Certifique-se de que todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
```

### Timeout ao gerar respostas

Se você receber erros de timeout:

1. **Aumente o timeout** no `model_config.py`:
   ```python
   MODEL_RULES = {
       "timeout_seconds": 180,  # Aumente conforme necessário
       # ...
   }
   ```

2. **Ou configure via `.env`**:
   ```env
   OLLAMA_TIMEOUT=180
   ```

3. **Verifique o modelo**: Modelos maiores podem precisar de mais tempo
4. **Consulte** `CORRECAO_TIMEOUT.md` para mais detalhes

## Segurança

- **Nunca** commite o arquivo `.env` no controle de versão
- Mantenha suas API Keys seguras e privadas
- O arquivo `.env` deve estar no `.gitignore` por padrão
- O Ollama roda localmente por padrão (sem exposição externa)
- **Logs**: Por padrão, logs de respostas estão desabilitados (`log_responses: False`) para proteger dados sensíveis
- **Histórico**: Arquivos de histórico contêm conversas completas - mantenha-os seguros

## Desenvolvimento

### Funcionalidades Implementadas

-  **Logging Estruturado**: Sistema completo de logs com rotação automática
-  **Validação de Inputs**: Validação automática de mensagens e sanitização
-  **Persistência de Histórico**: Histórico salvo automaticamente em JSON
-  **Testes Unitários**: Suite completa de testes para todos os módulos principais
-  **Streaming de Respostas**: Infraestrutura pronta (pode ser ativado no código)
-  **Timeout Configurável**: Timeout ajustável via model_config.py ou .env
-  **Tratamento Robusto de Arquivos**: Context managers para garantir limpeza de arquivos temporários
-  **Diagnóstico Automático**: Script para diagnosticar problemas de conexão

### Melhorias Futuras

- [ ] Ativar streaming de respostas na UI
- [ ] Exportação de conversas em diferentes formatos
- [ ] Interface para visualizar e carregar históricos salvos
- [ ] Histórico persistente em banco de dados
- [ ] Suporte para múltiplos provedores de LLM
- [ ] Interface para gerenciar modelos Ollama
- [ ] Métricas e estatísticas de uso

### Executando Testes

Para executar os testes unitários:

```bash
# Executar todos os testes
python run_tests.py

# Ou usando unittest diretamente
python -m unittest discover -s . -p "test_*.py"

# Executar teste específico
python test_ollama_service.py
python test_llm_handler.py
python test_input_validator.py
python test_history_manager.py
```

Consulte `README_TESTES.md` para mais informações sobre os testes.

### Logging

Os logs são salvos automaticamente em `logs/app.log` com rotação automática (máximo 10MB por arquivo, 5 backups).

Configure o nível de log via `.env`:
```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Histórico de Conversas

O histórico é salvo automaticamente em `chat_history/current.json`. Você pode:

- **Carregar histórico**: Use `history_manager.load_history("session_id")`
- **Listar sessões**: Use `history_manager.list_history_sessions()`
- **Deletar histórico**: Use `history_manager.delete_history("session_id")`

Consulte `history_manager.py` para mais detalhes.

## Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Suporte

Para problemas ou dúvidas:

1. **Execute o diagnóstico**:
   ```bash
   python diagnose_ollama.py
   ```

2. **Verifique os logs**:
   - Logs em `logs/app.log`
   - Configure `LOG_LEVEL=DEBUG` no `.env` para mais detalhes

3. **Verifique se o Ollama está rodando**:
   ```bash
   ollama list
   ```

4. **Consulte a documentação**:
   - `README_TESTES.md` - Sobre testes
   - `MELHORIAS_IMPLEMENTADAS.md` - Lista de melhorias
   - `CORRECAO_TIMEOUT.md` - Solução de problemas de timeout
   - `INICIAR_OLLAMA.md` - Como iniciar o Ollama no Windows

5. **Documentação do Ollama**: https://github.com/ollama/ollama

## Agradecimentos

- [Streamlit](https://streamlit.io/) pela excelente framework
- [Ollama](https://ollama.ai/) pela plataforma de modelos locais
- [OpenAI Whisper](https://github.com/openai/whisper) pela transcrição de áudio

---

Desenvolvido com Streamlit e Ollama
