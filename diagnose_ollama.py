"""
Script de diagnóstico para verificar a conexão com o Ollama
Execute este script para identificar problemas de conexão
"""

import sys
import requests
from ollama_service import OllamaService
from llm_handler import create_llm_handler

def diagnose_ollama(base_url: str = "http://localhost:11434"):
    """
    Executa diagnóstico completo da conexão com o Ollama.
    
    Args:
        base_url: URL base do servidor Ollama
    """
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DE CONEXÃO COM OLLAMA")
    print("=" * 60)
    print(f"\n📍 URL configurada: {base_url}\n")
    
    # Teste 1: Verificar se a URL é acessível
    print("1️⃣ Testando conectividade básica...")
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        print(f"   ✅ Resposta HTTP: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ ERRO: Não foi possível conectar ao Ollama")
        print("   💡 Verifique se o Ollama está rodando:")
        print("      - Windows: Verifique se o Ollama está instalado e rodando")
        print("      - Execute: ollama serve")
        print("      - Ou inicie o Ollama pelo menu iniciar")
        return False
    except requests.exceptions.Timeout:
        print("   ❌ ERRO: Timeout ao conectar")
        print("   💡 O servidor pode estar sobrecarregado ou inacessível")
        return False
    except Exception as e:
        print(f"   ❌ ERRO: {str(e)}")
        return False
    
    # Teste 2: Verificar OllamaService
    print("\n2️⃣ Testando OllamaService...")
    try:
        service = OllamaService(base_url=base_url)
        models = service.list_models()
        print(f"   ✅ OllamaService funcionando")
        print(f"   📦 Modelos encontrados: {len(models)}")
        if models:
            print("   Modelos disponíveis:")
            for model in models[:5]:  # Mostrar apenas os 5 primeiros
                name = model.get("name", "Desconhecido")
                size = model.get("size", 0)
                size_gb = size / (1024**3) if size else 0
                print(f"      - {name} ({size_gb:.2f} GB)")
        else:
            print("   ⚠️ Nenhum modelo encontrado")
            print("   💡 Baixe um modelo com: ollama pull llama2")
    except Exception as e:
        print(f"   ❌ ERRO no OllamaService: {str(e)}")
        return False
    
    # Teste 3: Verificar OllamaLLMHandler
    print("\n3️⃣ Testando OllamaLLMHandler...")
    try:
        handler = create_llm_handler(base_url)
        if handler.is_configured():
            print("   ✅ Handler configurado corretamente")
            status = handler.get_connection_status()
            print(f"   📊 Status: {status['message']}")
        else:
            print("   ❌ Handler não está configurado")
            return False
    except Exception as e:
        print(f"   ❌ ERRO no Handler: {str(e)}")
        return False
    
    # Teste 4: Teste de geração simples (opcional)
    print("\n4️⃣ Testando geração de resposta (opcional)...")
    try:
        handler = create_llm_handler(base_url)
        available_models = handler.list_available_models()
        if available_models:
            test_model = available_models[0]
            print(f"   🧪 Testando com modelo: {test_model}")
            response = handler.generate_response(
                user_input="Olá, você está funcionando?",
                model=test_model,
                temperature=0.7
            )
            if response and len(response) > 0:
                print(f"   ✅ Resposta recebida ({len(response)} caracteres)")
                print(f"   📝 Preview: {response[:100]}...")
            else:
                print("   ⚠️ Resposta vazia recebida")
        else:
            print("   ⚠️ Nenhum modelo disponível para teste")
    except Exception as e:
        print(f"   ⚠️ Erro no teste de geração: {str(e)}")
        print("   (Isso pode ser normal se não houver modelos instalados)")
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO CONCLUÍDO")
    print("=" * 60)
    return True

if __name__ == "__main__":
    # Permitir URL customizada via argumento
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:11434"
    diagnose_ollama(url)

