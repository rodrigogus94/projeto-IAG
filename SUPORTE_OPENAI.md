# 🚀 Suporte a Modelos OpenAI - Documentação

## 📋 Resumo

Foi adicionado suporte completo para modelos LLM da OpenAI no projeto, permitindo escolher entre modelos locais (Ollama) e modelos da OpenAI.

## ✨ Funcionalidades Adicionadas

### 1. Seleção de Provedor
- **Ollama**: Modelos locais (padrão)
- **OpenAI**: Modelos da OpenAI (gpt-4o, gpt-3.5-turbo, etc.)

### 2. Modelos OpenAI Disponíveis
- `gpt-4o` - Modelo mais avançado
- `gpt-4o-mini` - Versão mais rápida e econômica
- `gpt-4-turbo` - Versão turbo do GPT-4
- `gpt-4` - GPT-4 padrão
- `gpt-3.5-turbo` - Modelo rápido e econômico
- `gpt-3.5-turbo-16k` - Versão com contexto maior

## 📁 Arquivos Criados

1. **`src/core/openai_service.py`**
   - Serviço para comunicação com a API da OpenAI
   - Similar ao `ollama_service.py`
   - Suporta chat com histórico e streaming

2. **`src/core/openai_handler.py`**
   - Handler que adapta OpenAIService para a interface do app.py
   - Similar ao `llm_handler.py`
   - Implementa a mesma interface para compatibilidade

## 🔧 Como Usar

### 1. Configurar API Key da OpenAI

**Opção A: Arquivo .env (Recomendado)**
```env
OPENAI_API_KEY=sk-sua-chave-api-aqui
```

**Opção B: Interface do Streamlit**
- Vá em "⚙️ Configurações"
- Selecione "openai" como provedor
- Digite sua API key no campo "OpenAI API Key"

### 2. Selecionar Provedor

1. Abra a aplicação Streamlit
2. Na sidebar, expanda "⚙️ Configurações"
3. Em "🤖 Provedor de IA", escolha:
   - **Ollama**: Para modelos locais
   - **OpenAI**: Para modelos da OpenAI

### 3. Conectar à OpenAI

1. Selecione "OpenAI" como provedor
2. Configure sua API key (se ainda não estiver no .env)
3. Clique em "🔄 Conectar à OpenAI"
4. Aguarde a confirmação de conexão

### 4. Selecionar Modelo

Após conectar, você verá a lista de modelos disponíveis:
- **Ollama**: Modelos instalados localmente
- **OpenAI**: Modelos disponíveis da OpenAI

## 🎯 Diferenças entre Ollama e OpenAI

| Característica | Ollama | OpenAI |
|----------------|--------|--------|
| **Localização** | Local | Nuvem |
| **Custo** | Gratuito | Pago por uso |
| **Velocidade** | Depende do hardware | Rápido |
| **Privacidade** | Totalmente local | Dados enviados à OpenAI |
| **Modelos** | Modelos open-source | Modelos proprietários |
| **Internet** | Não requer | Requer conexão |

## ⚙️ Configuração

### Variáveis de Ambiente

```env
# Ollama (opcional, padrão: http://localhost:11434)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=120

# OpenAI (obrigatório para usar OpenAI)
OPENAI_API_KEY=sk-sua-chave-api-aqui
```

### Timeout

O timeout é compartilhado entre Ollama e OpenAI e pode ser configurado via:
- Variável de ambiente `OLLAMA_TIMEOUT`
- Arquivo `model_config.py`

## 🔍 Status da Conexão

O status mostra:
- ✅ **Conectado**: Provedor funcionando corretamente
- ❌ **Erro**: Problema de conexão ou configuração
- 📦 **Modelos**: Quantidade de modelos disponíveis
- 💡 **Sugestões**: Dicas para resolver problemas

## 🐛 Solução de Problemas

### "OPENAI_API_KEY não configurada"
**Solução**: Configure a API key no arquivo `.env` ou na interface

### "Erro ao conectar à OpenAI"
**Soluções**:
1. Verifique se a API key está correta
2. Verifique sua conexão com a internet
3. Verifique se sua conta OpenAI tem créditos disponíveis

### "Nenhum modelo disponível"
**Solução**: 
- Para Ollama: Baixe modelos com `ollama pull <modelo>`
- Para OpenAI: Verifique sua API key e conexão

## 📝 Notas Importantes

1. **Custos**: O uso da OpenAI API é pago. Verifique os preços em https://openai.com/pricing
2. **Privacidade**: Dados enviados à OpenAI são processados em seus servidores
3. **Rate Limits**: A OpenAI tem limites de requisições por minuto/hora
4. **Modelos**: Alguns modelos podem não estar disponíveis dependendo da sua conta

## 🔄 Alternando entre Provedores

Você pode alternar entre Ollama e OpenAI a qualquer momento:
1. Vá em "⚙️ Configurações"
2. Selecione o provedor desejado
3. Configure e conecte
4. Selecione o modelo

O histórico de conversas é mantido ao alternar entre provedores.

## 🚀 Próximos Passos

- [ ] Adicionar mais modelos OpenAI (quando disponíveis)
- [ ] Suporte a streaming na UI
- [ ] Cache de respostas
- [ ] Métricas de uso e custos

---

**Desenvolvido para o Projeto IAG - Chat Assistente com IA**

