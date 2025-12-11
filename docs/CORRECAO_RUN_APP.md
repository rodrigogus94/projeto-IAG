# Correção do Script run_app.bat - Problema com Inicialização do Ollama

## Problemas Identificados

### 1. **Verificação de Processo Incorreta**
- **Problema**: A verificação `if "%ERRORLEVEL%"=="0"` não estava funcionando corretamente
- **Causa**: O `ERRORLEVEL` pode não ser atualizado imediatamente após o `find`
- **Solução**: Melhorada a verificação usando variável intermediária

### 2. **Inicialização do Ollama no Windows**
- **Problema**: O script tentava iniciar o Ollama com `ollama serve`, mas no Windows o Ollama geralmente roda como serviço
- **Causa**: No Windows, o Ollama é instalado como serviço e não precisa de `ollama serve` manualmente
- **Solução**: Adicionada verificação e inicialização do serviço do Windows antes de tentar iniciar manualmente

### 3. **Tempo de Espera Insuficiente**
- **Problema**: O script aguardava apenas 10 segundos, mas o Ollama pode levar mais tempo para iniciar
- **Causa**: O Ollama pode levar 15-30 segundos para iniciar completamente no Windows
- **Solução**: Aumentado o tempo de espera e adicionadas múltiplas verificações

### 4. **Falta de Verificação do Serviço do Windows**
- **Problema**: O script não verificava se o serviço do Windows estava rodando
- **Causa**: O Ollama no Windows pode estar rodando como serviço sem processo visível
- **Solução**: Adicionada verificação do serviço usando `sc query OllamaService`

## Correções Implementadas

### 1. **Melhor Verificação de Processo**
```batch
REM Verificar se o Ollama ja esta rodando como processo (melhor verificacao)
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe" >NUL
set OLLAMA_RUNNING=%ERRORLEVEL%
```

### 2. **Verificação do Serviço do Windows**
```batch
REM Verificar tambem se o servico do Windows esta rodando
sc query OllamaService >nul 2>&1
set SERVICE_EXISTS=%ERRORLEVEL%
```

### 3. **Tentativa de Iniciar o Serviço**
```batch
REM Tentar iniciar o servico do Windows primeiro (se existir)
if "%SERVICE_EXISTS%"=="0" (
    echo [INFO] Servico Ollama encontrado. Tentando iniciar servico...
    sc start OllamaService >nul 2>&1
    ...
)
```

### 4. **Tempo de Espera Aumentado**
- Aguarda 15 segundos após detectar processo
- Aguarda 20 segundos após tentar iniciar
- Múltiplas verificações com intervalos

### 5. **Método Alternativo de Inicialização**
- Primeiro tenta iniciar o serviço do Windows
- Se não funcionar, tenta iniciar em background com `start /B`
- Se ainda não funcionar, abre novo terminal

## Script Auxiliar Criado

Foi criado o script `scripts/start_ollama_windows.bat` que pode ser executado separadamente para iniciar o Ollama. Este script:

1. Verifica se o Ollama está instalado
2. Verifica se já está rodando
3. Tenta iniciar o serviço do Windows
4. Tenta iniciar manualmente em background
5. Tenta abrir em novo terminal
6. Verifica se está respondendo

## Como Usar

### Opção 1: Usar o run_app.bat (Recomendado)
```batch
run_app.bat
```
O script agora detecta e inicia o Ollama automaticamente.

### Opção 2: Iniciar Ollama Separadamente
```batch
scripts\start_ollama_windows.bat
```

### Opção 3: Iniciar Manualmente
1. Abra o menu Iniciar do Windows
2. Procure por "Ollama"
3. Clique no aplicativo Ollama

Ou execute em um terminal:
```batch
ollama serve
```

## Verificação

Para verificar se o Ollama está funcionando:

```batch
python scripts\check_ollama.py --verbose
```

Ou acesse no navegador:
```
http://localhost:11434/api/tags
```

## Problemas Comuns

### "Ollama não encontrado no PATH"
- Instale o Ollama de https://ollama.ai/
- Ou adicione o Ollama ao PATH do sistema

### "Não foi possível iniciar o serviço"
- Execute o script como Administrador
- Ou inicie o Ollama manualmente pelo menu Iniciar

### "Ollama está rodando mas não está respondendo"
- Aguarde mais tempo (pode levar 30 segundos)
- Verifique o Gerenciador de Tarefas
- Reinicie o Ollama

### "Porta 11434 já está em uso"
- Outro processo está usando a porta
- Feche outros programas que possam estar usando a porta
- Ou reinicie o Windows

## Melhorias no check_ollama.py

O script de verificação também foi melhorado para:
- Mostrar mais informações de diagnóstico
- Listar modelos disponíveis
- Dar sugestões específicas para Windows
- Mostrar mensagens mais claras

## Testes Recomendados

1. Execute `run_app.bat` e verifique se o Ollama inicia automaticamente
2. Execute `scripts\check_ollama.py --verbose` para verificar status
3. Teste iniciar o Ollama manualmente e verificar se o script detecta
4. Teste com o Ollama já rodando para verificar se detecta corretamente

