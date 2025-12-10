# Chat Assistente com IA - Projeto IAG

Aplicação web de chat interativo com IA usando Streamlit e Ollama. Interface moderna e intuitiva para conversar com modelos de linguagem locais através do Ollama, com suporte para transcrição de áudio.

## Características

- **Interface Moderna**: Interface web responsiva construída com Streamlit
- **Ollama Integration**: Suporte completo para modelos locais via Ollama
- **Múltiplos Modelos**: Lista dinamicamente modelos disponíveis no Ollama
- **Transcrição de Áudio**: Suporte para entrada por voz usando Whisper (local) ou OpenAI API
- **Histórico Completo**: Mantém contexto completo da conversa
- **Configuração Flexível**: Suporte para variáveis de ambiente (.env) ou configuração manual
- **Arquitetura Modular**: Código organizado e separado por responsabilidades

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
   TRANSCRIPTION_METHOD=whisper
   # Opcional: para transcrição via OpenAI API
   OPENAI_API_KEY=sk-sua-chave-api-aqui
   ```

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
   - Clique em "🔄 Reconectar ao Ollama" se necessário
   - Selecione o modelo desejado (será listado automaticamente)

4. **Comece a conversar**:
   - Digite sua mensagem no campo de input
   - Ou use o microfone para gravar uma mensagem de voz
   - A IA responderá mantendo o contexto da conversa
   - Use "🗑️ Limpar Chat" para reiniciar a conversa

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

## Estrutura do Projeto

```
projeto-sdk-mk01/
├── app.py              # Interface Streamlit principal
├── llm_handler.py      # Handler que integra OllamaService
├── ollama_service.py    # Serviço para comunicação com Ollama
├── audio_transcriber.py # Módulo de transcrição de áudio
├── model_config.py     # Configurações centralizadas do modelo (regras, parâmetros, prompts)
├── styles.py           # Estilos CSS customizados
├── requirements.txt    # Dependências do projeto
├── .env                # Variáveis de ambiente (criar)
└── README.md           # Este arquivo
```

## Arquitetura

O projeto segue uma arquitetura modular:

- **`app.py`**: Gerencia a interface do usuário, estado da aplicação e interações
- **`llm_handler.py`**: Adapta OllamaService para a interface esperada pelo app
- **`ollama_service.py`**: Encapsula toda a lógica de comunicação com a API do Ollama
- **`audio_transcriber.py`**: Gerencia transcrição de áudio (Whisper/OpenAI)
- **`model_config.py`**: **Centraliza todas as configurações do modelo** - regras, parâmetros, system prompts e instruções
- **`styles.py`**: Centraliza todos os estilos CSS customizados

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

2. Clique em "🔄 Reconectar ao Ollama" nas configurações

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

## Segurança

- **Nunca** commite o arquivo `.env` no controle de versão
- Mantenha suas API Keys seguras e privadas
- O arquivo `.env` deve estar no `.gitignore` por padrão
- O Ollama roda localmente por padrão (sem exposição externa)

## Desenvolvimento

### Melhorias Futuras

- [ ] Suporte para streaming de respostas
- [ ] Exportação de conversas
- [ ] Temas personalizáveis
- [ ] Histórico persistente em banco de dados
- [ ] Suporte para múltiplos provedores de LLM
- [ ] Interface para gerenciar modelos Ollama

## Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Suporte

Para problemas ou dúvidas:

1. Verifique se o Ollama está rodando e acessível
2. Confirme que todas as dependências estão instaladas
3. Verifique os logs de erro na interface
4. Consulte a documentação do Ollama: https://github.com/ollama/ollama

## Agradecimentos

- [Streamlit](https://streamlit.io/) pela excelente framework
- [Ollama](https://ollama.ai/) pela plataforma de modelos locais
- [OpenAI Whisper](https://github.com/openai/whisper) pela transcrição de áudio

---

Desenvolvido com Streamlit e Ollama
