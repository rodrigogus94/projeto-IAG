# 🚀 Como Iniciar o Ollama - Guia Rápido

## 📥 Passo 1: Instalar o Ollama

Se o Ollama não está instalado:

1. **Acesse**: https://ollama.ai/download
2. **Baixe** o instalador para Windows
3. **Execute** o instalador e siga as instruções
4. O Ollama será instalado e adicionado ao PATH automaticamente

---

## ▶️ Passo 2: Iniciar o Ollama

### Opção A: Pelo Menu Iniciar (Mais Fácil) ⭐

1. Pressione a tecla **Windows**
2. Digite **"Ollama"**
3. Clique no aplicativo **Ollama**
4. O Ollama iniciará automaticamente em segundo plano

### Opção B: Pelo Terminal/PowerShell

1. Abra o **PowerShell** ou **Prompt de Comando**
2. Execute:
   ```powershell
   ollama serve
   ```
3. Deixe o terminal aberto (o Ollama rodará enquanto o terminal estiver aberto)
4. Você verá uma mensagem como: `Ollama is running on http://localhost:11434`

---

## ✅ Passo 3: Verificar se Está Funcionando

### Teste 1: Verificar se está rodando
```powershell
ollama list
```
Se retornar uma lista (mesmo que vazia), o Ollama está rodando! ✅

### Teste 2: Testar a API
No navegador, acesse:
```
http://localhost:11434/api/tags
```
Deve retornar um JSON com os modelos disponíveis.

### Teste 3: Usando o script de diagnóstico do projeto
```powershell
python scripts/diagnose_ollama.py
```

---

## 📦 Passo 4: Baixar um Modelo (Obrigatório)

Se não houver modelos instalados, você precisa baixar pelo menos um:

```powershell
# Modelo recomendado para começar
ollama pull llama2

# Ou outros modelos populares:
ollama pull mistral
ollama pull codellama
ollama pull phi
```

**Nota**: O primeiro download pode demorar alguns minutos dependendo do tamanho do modelo.

---

## 🔧 Passo 5: Configurar o Projeto

Após iniciar o Ollama:

1. **Inicie a aplicação Streamlit**:
   ```powershell
   streamlit run src/app.py
   ```

2. **Na sidebar**, expanda "⚙️ Configurações"

3. **Clique em "🔄 Reconectar ao Ollama"**

4. O status deve mudar para "✅ Conectado ao Ollama"

---

## 🐛 Problemas Comuns

### ❌ "Ollama não é reconhecido como comando"

**Solução**:
- O Ollama não está instalado ou não está no PATH
- Reinstale o Ollama de https://ollama.ai/download
- Reinicie o terminal após instalar

### ❌ "Porta 11434 já está em uso"

**Solução**:
- Outro processo está usando a porta
- Feche outros programas que possam estar usando a porta
- Ou reinicie o computador

### ❌ "Impossível conectar-se ao servidor remoto"

**Solução**:
- O Ollama não está rodando
- Inicie o Ollama usando uma das opções acima
- Verifique se o firewall não está bloqueando

### ❌ "Nenhum modelo encontrado"

**Solução**:
- Baixe pelo menos um modelo:
  ```powershell
  ollama pull llama2
  ```

---

## 💡 Dicas

### Iniciar o Ollama Automaticamente ao Ligar o Computador

1. Pressione `Win + R`
2. Digite `shell:startup` e pressione Enter
3. Crie um atalho do Ollama nesta pasta
4. O Ollama iniciará automaticamente ao iniciar o Windows

### Verificar Modelos Instalados

```powershell
ollama list
```

### Remover um Modelo

```powershell
ollama rm nome_do_modelo
```

### Ver Informações de um Modelo

```powershell
ollama show nome_do_modelo
```

---

## 📚 Recursos Adicionais

- **Documentação oficial**: https://github.com/ollama/ollama
- **Lista de modelos**: https://ollama.ai/library
- **Documentação do projeto**: `docs/INICIAR_OLLAMA.md`

---

## ✅ Checklist Rápido

- [ ] Ollama instalado
- [ ] Ollama rodando (verificar com `ollama list`)
- [ ] Pelo menos um modelo baixado (`ollama pull llama2`)
- [ ] Aplicação Streamlit iniciada
- [ ] Conectado ao Ollama nas configurações

---

**Pronto! Agora você pode usar o chat com IA! 🎉**



