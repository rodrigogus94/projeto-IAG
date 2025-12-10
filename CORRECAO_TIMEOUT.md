# Correção do Problema de Timeout

## Problema Identificado

O erro "Timeout ao comunicar com o Ollama. A requisição demorou mais de 10 segundos" ocorria porque:

1. O timeout padrão era muito curto (10 segundos) para geração de respostas
2. O timeout não estava sendo aplicado corretamente em todas as requisições
3. Modelos grandes podem demorar mais de 10 segundos para gerar respostas

## Correções Implementadas

### 1. Timeout Padrão Aumentado

- **Antes**: 10 segundos (muito curto)
- **Agora**: 60 segundos para operações normais, 120 segundos (dobrado) para chat

### 2. Timeout Configurável

Agora você pode configurar o timeout via variável de ambiente:

```bash
# No arquivo .env
OLLAMA_TIMEOUT=120  # em segundos (padrão: 120)
```

### 3. Timeout Específico para Chat

O método `chat()` agora usa um timeout dobrado (2x) porque a geração de respostas pode demorar mais:

- Timeout base: 60 segundos
- Timeout para chat: 120 segundos (60 * 2)

### 4. Timeout Explícito em Todas as Requisições

Todas as chamadas `requests.post()` e `requests.get()` agora passam o timeout explicitamente.

## Como Configurar

### Opção 1: Via Variável de Ambiente (Recomendado)

Crie ou edite o arquivo `.env` na raiz do projeto:

```env
OLLAMA_TIMEOUT=120
```

### Opção 2: Alterar no Código

Se preferir, você pode alterar diretamente no `app.py`:

```python
OLLAMA_TIMEOUT = 120  # Ajuste conforme necessário
```

## Valores Recomendados

- **Modelos pequenos/rápidos** (llama2:7b, mistral:7b): 60-90 segundos
- **Modelos médios** (llama2:13b): 120-180 segundos  
- **Modelos grandes** (llama2:70b): 180-300 segundos

## Verificação

Para verificar se o timeout está configurado corretamente:

1. Verifique os logs em `logs/app.log`
2. Procure por mensagens como: `"Iniciando chat com modelo X, timeout=120s"`

## Notas Importantes

- O timeout para **streaming** é ilimitado (None), pois o streaming pode demorar muito tempo
- Se você ainda receber erros de timeout, aumente o valor de `OLLAMA_TIMEOUT`
- Modelos maiores ou hardware mais lento podem precisar de timeouts maiores

## Troubleshooting

### Ainda recebo timeout mesmo com 120 segundos

1. Aumente o timeout para 180 ou 240 segundos
2. Verifique se o Ollama está processando (use `ollama ps` para ver processos)
3. Considere usar um modelo menor/mais rápido
4. Verifique se há outros processos usando recursos do sistema

### Como saber qual timeout usar?

Execute o diagnóstico:

```bash
python diagnose_ollama.py
```

Isso mostrará informações sobre a conexão e pode ajudar a identificar problemas.

