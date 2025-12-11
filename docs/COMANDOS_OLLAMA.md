# Comandos para Rodar o Ollama Manualmente

## Windows

### Método 1: Via Menu Iniciar (Mais Fácil)
1. Pressione a tecla **Windows**
2. Digite **"Ollama"**
3. Clique no aplicativo **Ollama**
4. O Ollama iniciará automaticamente em segundo plano

### Método 2: Via Prompt de Comando / PowerShell
Abra o **Prompt de Comando** ou **PowerShell** e execute:

```batch
ollama serve
```

**Nota**: Deixe o terminal aberto enquanto o Ollama estiver rodando.

### Método 3: Via Serviço do Windows
Verificar status do serviço:
```batch
sc query OllamaService
```

Iniciar o serviço:
```batch
sc start OllamaService
```

**Nota**: Pode precisar de privilégios de administrador.

### Método 4: Via Gerenciador de Tarefas
1. Pressione `Ctrl + Shift + Esc` para abrir o Gerenciador de Tarefas
2. Clique em "Executar nova tarefa"
3. Digite: `ollama serve`
4. Marque "Criar esta tarefa com privilégios administrativos" (se necessário)
5. Clique em OK

## Linux / macOS

### Método 1: Via Terminal
Abra o terminal e execute:

```bash
ollama serve
```

### Método 2: Em Background
Para rodar em background:

```bash
ollama serve &
```

### Método 3: Com nohup (persiste após fechar terminal)
```bash
nohup ollama serve > ollama.log 2>&1 &
```

## Verificar se o Ollama está Rodando

### Windows
```batch
# Verificar processo
tasklist | findstr ollama

# Verificar se está respondendo
curl http://localhost:11434/api/tags
```

### Linux / macOS
```bash
# Verificar processo
ps aux | grep ollama

# Verificar se está respondendo
curl http://localhost:11434/api/tags
```

### Python (Script)
```bash
python scripts/check_ollama.py --verbose
```

## Comandos Úteis do Ollama

### Listar modelos instalados
```bash
ollama list
```

### Baixar um modelo
```bash
ollama pull llama2
ollama pull mistral
ollama pull codellama
```

### Executar um modelo
```bash
ollama run llama2
```

### Parar o Ollama

#### Windows
```batch
# Encontrar o processo
tasklist | findstr ollama

# Matar o processo (substitua PID pelo número do processo)
taskkill /PID <PID> /F
```

#### Linux / macOS
```bash
# Encontrar o processo
ps aux | grep ollama

# Matar o processo (substitua PID pelo número do processo)
kill <PID>
```

## Testar a API do Ollama

### Via Navegador
Acesse:
```
http://localhost:11434/api/tags
```

Deve retornar um JSON com os modelos disponíveis.

### Via curl (Windows PowerShell)
```powershell
Invoke-WebRequest -Uri http://localhost:11434/api/tags
```

### Via curl (Linux / macOS)
```bash
curl http://localhost:11434/api/tags
```

### Via Python
```python
import requests
response = requests.get("http://localhost:11434/api/tags")
print(response.json())
```

## Solução de Problemas

### "Ollama não é reconhecido como comando"
- **Windows**: Instale o Ollama de https://ollama.ai/download
- **Linux**: Execute `curl -fsSL https://ollama.ai/install.sh | sh`
- **macOS**: Baixe o instalador de https://ollama.ai/download

### "Porta 11434 já está em uso"
- Outro processo está usando a porta
- Feche outros programas que possam estar usando a porta
- Ou reinicie o computador

### "Ollama não inicia"
- Verifique se o Ollama está instalado corretamente
- Tente executar como administrador (Windows)
- Verifique os logs de erro
- Reinicie o computador

### "Firewall bloqueando"
- **Windows**: Adicione exceção no Windows Defender Firewall
- **Linux**: Configure o firewall (ufw/iptables)
- **macOS**: Configure o Firewall nas Preferências do Sistema

## Iniciar Automaticamente ao Ligar o Computador

### Windows
1. Pressione `Win + R`
2. Digite `shell:startup` e pressione Enter
3. Crie um atalho do Ollama nesta pasta
4. O Ollama iniciará automaticamente ao iniciar o Windows

### Linux (systemd)
Crie um arquivo `/etc/systemd/system/ollama.service`:
```ini
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=seu_usuario
ExecStart=/usr/local/bin/ollama serve
Restart=always

[Install]
WantedBy=multi-user.target
```

Depois execute:
```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

### macOS (LaunchAgent)
Crie um arquivo `~/Library/LaunchAgents/com.ollama.agent.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ollama.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Depois execute:
```bash
launchctl load ~/Library/LaunchAgents/com.ollama.agent.plist
```

