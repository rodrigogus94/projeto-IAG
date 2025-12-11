# Script para criar arquivo .env a partir do template
# Execute: .\criar_env.ps1

$envContent = @"
# ============================================================================
# Configurações do Projeto IAG - Chat Assistente com IA
# ============================================================================

# ============================================================================
# Configuração do Ollama (Modelos Locais)
# ============================================================================
# URL do servidor Ollama (padrão: http://localhost:11434)
OLLAMA_BASE_URL=http://localhost:11434

# Timeout para requisições ao Ollama em segundos (padrão: 120)
# Para modelos grandes, aumente este valor (ex: 180, 240)
OLLAMA_TIMEOUT=120

# ============================================================================
# Configuração da OpenAI (Modelos da OpenAI)
# ============================================================================
# Chave da API OpenAI (obrigatória para usar modelos OpenAI)
# Obtenha sua chave em: https://platform.openai.com/api-keys
# IMPORTANTE: Substitua 'sk-sua-chave-api-aqui' pela sua chave real
# A chave deve começar com "sk-" seguida de caracteres alfanuméricos
OPENAI_API_KEY=sk-sua-chave-api-aqui

# ============================================================================
# Configuração de Transcrição de Áudio
# ============================================================================
# Método de transcrição: "whisper" (local) ou "openai" (API)
# Whisper: Processa localmente, não requer API key
# OpenAI: Usa API da OpenAI, requer OPENAI_API_KEY
TRANSCRIPTION_METHOD=whisper

# ============================================================================
# Configuração de Logging
# ============================================================================
# Nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
# DEBUG: Mostra todas as informações (útil para desenvolvimento)
# INFO: Mostra informações gerais (recomendado para produção)
LOG_LEVEL=INFO

# ============================================================================
# Notas Importantes
# ============================================================================
# 1. NUNCA commite este arquivo no Git (deve estar no .gitignore)
# 2. Mantenha suas chaves de API seguras e privadas
# 3. Para usar modelos OpenAI, você precisa de uma conta OpenAI com créditos
# 4. Para obter uma chave OpenAI: https://platform.openai.com/api-keys
# 5. Verifique os preços da OpenAI em: https://openai.com/pricing
"@

# Verificar se .env já existe
if (Test-Path .env) {
    $resposta = Read-Host "O arquivo .env já existe. Deseja sobrescrever? (s/N)"
    if ($resposta -ne "s" -and $resposta -ne "S") {
        Write-Host "Operação cancelada." -ForegroundColor Yellow
        exit
    }
}

# Criar arquivo .env
$envContent | Out-File -FilePath .env -Encoding UTF8

Write-Host "✅ Arquivo .env criado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 PRÓXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "1. Abra o arquivo .env" -ForegroundColor White
Write-Host "2. Substitua 'sk-sua-chave-api-aqui' pela sua chave real da OpenAI" -ForegroundColor White
Write-Host "3. A chave pode ser obtida em: https://platform.openai.com/api-keys" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANTE: NUNCA commite o arquivo .env no Git!" -ForegroundColor Yellow

