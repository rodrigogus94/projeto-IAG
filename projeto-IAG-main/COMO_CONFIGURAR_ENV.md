# 🔧 Como Configurar o Arquivo .env

## ✅ Arquivo .env Criado!

O arquivo `.env` foi criado com sucesso na raiz do projeto.

## 📝 Próximos Passos

### 1. Abrir o Arquivo .env

O arquivo está localizado em:
```
projeto-IAG-main/projeto-IAG-main/.env
```

### 2. Configurar a Chave da OpenAI

1. **Obter uma chave da OpenAI**:
   - Acesse: https://platform.openai.com/api-keys
   - Faça login na sua conta OpenAI
   - Clique em "Create new secret key"
   - Copie a chave (ela começa com `sk-`)

2. **Editar o arquivo .env**:
   - Abra o arquivo `.env` em um editor de texto
   - Encontre a linha: `OPENAI_API_KEY=sk-sua-chave-api-aqui`
   - Substitua `sk-sua-chave-api-aqui` pela sua chave real
   - Exemplo: `OPENAI_API_KEY=sk-abc123def456...`

3. **Salvar o arquivo**

### 3. Outras Configurações (Opcional)

O arquivo `.env` já vem com valores padrão, mas você pode ajustar:

```env
# URL do Ollama (padrão: http://localhost:11434)
OLLAMA_BASE_URL=http://localhost:11434

# Timeout em segundos (padrão: 120)
OLLAMA_TIMEOUT=120

# Método de transcrição: "whisper" ou "openai"
TRANSCRIPTION_METHOD=whisper

# Nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO
```

## 🔒 Segurança

⚠️ **IMPORTANTE**: 
- **NUNCA** commite o arquivo `.env` no Git
- O arquivo `.env` já está no `.gitignore` (protegido)
- Mantenha suas chaves de API seguras e privadas
- Não compartilhe o arquivo `.env` com outras pessoas

## ✅ Verificar se Está Funcionando

Após configurar:

1. **Inicie o Streamlit**:
   ```powershell
   streamlit run src/app.py
   ```

2. **Na interface**:
   - Vá em "⚙️ Configurações"
   - Selecione "openai" como provedor
   - Clique em "🔄 Conectar à OpenAI"
   - Se aparecer "✅ Conectado à OpenAI", está funcionando!

## 🐛 Problemas Comuns

### "OPENAI_API_KEY não encontrada"
- Verifique se o arquivo `.env` está na raiz do projeto
- Verifique se a chave está correta (começa com `sk-`)
- Reinicie o Streamlit após editar o `.env`

### "Erro ao conectar à OpenAI"
- Verifique se a chave está correta
- Verifique se sua conta OpenAI tem créditos
- Verifique sua conexão com a internet

## 📚 Recursos

- **Obter chave OpenAI**: https://platform.openai.com/api-keys
- **Preços OpenAI**: https://openai.com/pricing
- **Documentação**: `SUPORTE_OPENAI.md`

---

**Pronto! Agora você pode usar modelos da OpenAI! 🚀**

