# Correção dos Scripts run_app - Problema com Ollama

## Problemas Identificados

### 1. **Verificação Silenciosa do Ollama**

**Problema**: O script `run_app.bat` suprimia toda a saída do script de verificação (`>nul 2>&1`), ocultando erros importantes.

**Antes**:
```batch
python "%SCRIPT_DIR%scripts\check_ollama.py" >nul 2>&1
```

**Depois**:
```batch
python "%SCRIPT_DIR%scripts\check_ollama.py" --verbose
```

### 2. **Script check_ollama.py Muito Simples**

**Problema**: O script não mostrava detalhes dos erros, dificultando o diagnóstico.

**Melhorias implementadas**:
- Adicionado modo `--verbose` para mostrar mensagens detalhadas
- Timeout aumentado de 2 para 5 segundos (mais realista)
- Tratamento específico de diferentes tipos de erro (ConnectionError, Timeout, HTTPError)
- Mostra quantos modelos foram encontrados quando o Ollama está rodando

### 3. **Não Verificava se Ollama Já Estava Rodando**

**Problema**: O script tentava iniciar o Ollama mesmo quando ele já estava rodando como processo/serviço.

**Solução**: 
- **Windows**: Verifica se `ollama.exe` está rodando usando `tasklist`
- **Linux/Mac**: Verifica se o processo `ollama` está rodando usando `pgrep`

### 4. **Timeout Insuficiente**

**Problema**: O timeout de 5 segundos pode não ser suficiente para o Ollama iniciar completamente.

**Solução**: Aumentado para 10 segundos, com mensagens informativas sobre o tempo de inicialização.

### 5. **Falta de Informações sobre Serviço do Windows**

**Problema**: No Windows, o Ollama geralmente roda como serviço automaticamente, mas o script não informava isso.

**Solução**: Adicionadas mensagens informativas explicando que:
- O Ollama pode estar rodando como serviço
- Pode levar 15-30 segundos para iniciar completamente
- Como verificar no Gerenciador de Tarefas

## Correções Implementadas

### `scripts/check_ollama.py`

✅ Adicionado modo `--verbose` para diagnóstico detalhado
✅ Timeout aumentado de 2 para 5 segundos
✅ Tratamento específico de diferentes tipos de erro
✅ Mostra informações sobre modelos encontrados

### `run_app.bat` (Windows)

✅ Verificação verbosa do Ollama (mostra erros)
✅ Verifica se `ollama.exe` já está rodando antes de tentar iniciar
✅ Timeout aumentado para 10 segundos
✅ Mensagens informativas sobre serviço do Windows
✅ Melhor tratamento de erros

### `run_app.sh` (Linux/Mac)

✅ Verificação verbosa do Ollama
✅ Verifica se processo `ollama` já está rodando usando `pgrep`
✅ Timeout aumentado para 10 segundos
✅ Melhor tratamento de erros

## Como Usar

### Windows

```batch
run_app.bat
```

O script agora:
1. Verifica se o Python está instalado
2. Verifica/instala dependências
3. **Verifica o Ollama com mensagens detalhadas**
4. Se não estiver rodando, tenta iniciar automaticamente
5. Verifica se já está rodando como processo antes de tentar iniciar
6. Inicia a aplicação Streamlit

### Linux/Mac

```bash
chmod +x run_app.sh
./run_app.sh
```

## Diagnóstico Manual

Se o Ollama ainda não estiver funcionando, execute o diagnóstico:

```bash
python scripts/diagnose_ollama.py
```

Ou com modo verbose:

```bash
python scripts/check_ollama.py --verbose
```

## Problemas Comuns e Soluções

### 1. "Ollama não encontrado no PATH"

**Solução**:
- Windows: Instale o Ollama de https://ollama.ai/ (geralmente adiciona ao PATH automaticamente)
- Linux/Mac: Execute `curl -fsSL https://ollama.ai/install.sh | sh`

### 2. "Ollama está rodando mas não responde"

**Possíveis causas**:
- Ollama ainda está iniciando (aguarde 15-30 segundos)
- Porta 11434 está bloqueada pelo firewall
- Ollama está rodando em outra porta

**Solução**:
- Aguarde alguns segundos e tente novamente
- Verifique o firewall do Windows/Linux
- Verifique se há outro processo usando a porta 11434

### 3. "Processo ollama.exe já está rodando"

**Isso é normal no Windows!** O Ollama geralmente roda como serviço.

**Solução**: Aguarde alguns segundos para o serviço iniciar completamente. O script agora faz isso automaticamente.

### 4. Verificar se Ollama está rodando manualmente

**Windows**:
```batch
tasklist | findstr ollama
```

**Linux/Mac**:
```bash
pgrep -a ollama
```

**Testar conexão**:
```bash
curl http://localhost:11434/api/tags
```

## Melhorias Futuras

- [ ] Detectar automaticamente a porta do Ollama se não for a padrão
- [ ] Suporte para múltiplas instâncias do Ollama
- [ ] Verificação de versão do Ollama
- [ ] Cache de status do Ollama para evitar verificações repetidas

