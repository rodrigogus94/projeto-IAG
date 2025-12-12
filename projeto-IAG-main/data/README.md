# 📁 Estrutura de Dados do Projeto

Esta pasta contém todos os dados gerados e utilizados pelo projeto.

## 📂 Estrutura de Pastas

```
data/
├── chat_history/     # Históricos de conversas (JSON)
├── logs/             # Arquivos de log do sistema
├── exports/          # Conversas exportadas (PDF, TXT, JSON)
├── cache/            # Cache de respostas e dados temporários
└── temp/             # Arquivos temporários
```

## 📋 Descrição das Pastas

### `chat_history/`
**Propósito**: Armazenar históricos de conversas

**Conteúdo**:
- Arquivos JSON com histórico de conversas
- Formato: `session_YYYYMMDD_HHMMSS.json`
- Estrutura:
  ```json
  {
    "session_id": "session_20240101_120000",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:30:00",
    "message_count": 10,
    "messages": [...]
  }
  ```

**Gerenciado por**: `src/core/history_manager.py`

---

### `logs/`
**Propósito**: Arquivos de log do sistema

**Conteúdo**:
- `app.log` - Log principal da aplicação
- Rotação automática (máximo 10MB por arquivo, 5 backups)
- Níveis: DEBUG, INFO, WARNING, ERROR, CRITICAL

**Gerenciado por**: `src/config/logging_config.py`

**Configuração**: Via variável `LOG_LEVEL` no `.env`

---

### `exports/`
**Propósito**: Conversas exportadas em diferentes formatos

**Conteúdo**:
- PDFs de conversas exportadas
- Arquivos TXT de conversas
- JSONs de conversas exportadas
- Outros formatos de exportação

**Uso**: Para exportar conversas da interface (funcionalidade futura)

---

### `cache/`
**Propósito**: Cache de respostas e dados temporários

**Conteúdo**:
- Cache de respostas frequentes
- Dados temporários para melhorar performance
- Cache de modelos e configurações

**Uso**: Para otimização de performance (funcionalidade futura)

---

### `temp/`
**Propósito**: Arquivos temporários

**Conteúdo**:
- Arquivos de áudio temporários (transcrição)
- Arquivos temporários de processamento
- Dados temporários que serão limpos automaticamente

**Limpeza**: Arquivos são limpos automaticamente após uso

---

## 🔒 Segurança

### Arquivos Sensíveis
- **Históricos de conversas** podem conter informações sensíveis
- **Logs** podem conter dados de requisições
- **Cache** pode conter respostas do modelo

### Recomendações
- ✅ Adicione `data/` ao `.gitignore` (exceto este README)
- ✅ Mantenha backups seguros dos dados importantes
- ✅ Limpe arquivos temporários regularmente
- ✅ Não compartilhe dados sensíveis

---

## 📊 Estatísticas

Para verificar o uso de espaço:

```powershell
# Windows PowerShell
Get-ChildItem -Path data -Recurse | Measure-Object -Property Length -Sum | Select-Object @{Name="Size(MB)";Expression={[math]::Round($_.Sum / 1MB, 2)}}
```

---

## 🧹 Limpeza

### Limpar arquivos temporários
```powershell
Remove-Item -Path "data\temp\*" -Force
```

### Limpar cache
```powershell
Remove-Item -Path "data\cache\*" -Force
```

### Limpar logs antigos
```powershell
# Manter apenas os últimos 30 dias
Get-ChildItem -Path "data\logs" -Filter "*.log*" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
```

---

## 📝 Notas

- Todas as pastas são criadas automaticamente quando necessário
- Os arquivos são gerenciados pelos respectivos módulos
- A estrutura pode ser expandida conforme necessário

---

**Última atualização**: 2024

