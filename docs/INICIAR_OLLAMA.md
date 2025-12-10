# Como Iniciar o Ollama no Windows

## Problema

O erro `WinError 10061` significa que o Ollama não está rodando ou não está acessível na porta 11434.

## Soluções

### Método 1: Iniciar pelo Menu Iniciar (Mais Fácil)

1. **Pressione a tecla Windows** no teclado
2. **Digite "Ollama"** na busca
3. **Clique no aplicativo Ollama** para abrir
4. O Ollama iniciará automaticamente em segundo plano
5. Verifique se está rodando: abra o navegador e acesse `http://localhost:11434`

### Método 2: Iniciar pelo Terminal/PowerShell

1. **Abra o PowerShell** ou **Prompt de Comando**
2. **Execute o comando**:
   ```powershell
   ollama serve
   ```
3. Deixe o terminal aberto (o Ollama rodará enquanto o terminal estiver aberto)
4. Você verá uma mensagem como: `Ollama is running on http://localhost:11434`

### Método 3: Verificar se o Ollama está Instalado

Se o comando `ollama serve` não funcionar, o Ollama pode não estar instalado:

1. **Baixe o Ollama**:

   - Acesse: https://ollama.ai/download
   - Baixe o instalador para Windows
   - Execute o instalador e siga as instruções

2. **Após instalar**, use o Método 1 ou 2 acima

### Verificar se está Funcionando

Execute no PowerShell:

```powershell
ollama list
```

Se retornar uma lista (mesmo que vazia), o Ollama está rodando!

### Testar a API Diretamente

No navegador, acesse:

```
http://localhost:11434/api/tags
```

Deve retornar um JSON com os modelos disponíveis.

### Baixar um Modelo (Opcional)

Se não houver modelos instalados, baixe um:

```powershell
ollama pull llama2
# ou
ollama pull mistral
```

## Após Iniciar o Ollama

1. **Volte para a aplicação Streamlit**
2. **Clique em " Reconectar ao Ollama"** nas configurações
3. O status deve mudar para " Conectado ao Ollama"

## Problemas Comuns

### "Ollama não é reconhecido como comando"

- O Ollama não está instalado ou não está no PATH
- Reinstale o Ollama ou adicione ao PATH do sistema

### "Porta 11434 já está em uso"

- Outro processo está usando a porta
- Feche outros programas que possam estar usando a porta
- Ou altere a porta do Ollama (requer configuração adicional)

### "Firewall bloqueando"

- O Windows Defender pode estar bloqueando
- Adicione exceção no firewall para o Ollama

## Dica

Para iniciar o Ollama automaticamente ao ligar o computador:

1. Pressione `Win + R`
2. Digite `shell:startup` e pressione Enter
3. Crie um atalho do Ollama nesta pasta
4. O Ollama iniciará automaticamente ao iniciar o Windows
