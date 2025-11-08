"""
Script de teste para verificar conectividade com Google Gemini API
"""

import os
from dotenv import load_dotenv
import httpx

load_dotenv()

def test_basic_connection():
    """Testa conexão básica com a API do Gemini"""
    print("🔍 Testando conexão com Google Gemini API...\n")

    # Verificar API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY não encontrada no arquivo .env")
        return False

    print(f"✅ API Key encontrada: {api_key[:20]}...")

    # Testar conexão HTTP básica
    print("\n🔗 Testando conexão HTTP básica...")
    try:
        with httpx.Client(verify=True, timeout=30.0) as client:
            url = "https://generativelanguage.googleapis.com/v1beta/models"
            params = {"key": api_key}

            response = client.get(url, params=params)

            if response.status_code == 200:
                print("✅ Conexão HTTP bem-sucedida!")
                print(f"Status: {response.status_code}")
                return True
            else:
                print(f"⚠️ Resposta inesperada: {response.status_code}")
                print(f"Corpo: {response.text[:200]}")
                return False

    except httpx.ConnectError as e:
        print(f"❌ Erro de conexão SSL: {e}")
        print("\n⚠️ Possíveis causas:")
        print("1. Firewall ou proxy bloqueando HTTPS")
        print("2. Certificados SSL desatualizados")
        print("3. Problemas de rede temporários")
        print("\n💡 Soluções:")
        print("- Desabilite temporariamente firewall/antivírus")
        print("- Verifique configurações de proxy")
        print("- Tente em outra rede (ex: hotspot do celular)")
        return False

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_gemini_api():
    """Testa chamada completa à API do Gemini"""
    print("\n\n🤖 Testando chamada à API Gemini...")

    try:
        from google import genai

        api_key = os.getenv('GEMINI_API_KEY')

        # Configurar client com timeout maior
        http_client = httpx.Client(
            verify=True,
            timeout=60.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )

        client = genai.Client(
            api_key=api_key,
            http_options={'client': http_client}
        )

        response = client.models.generate_content(
            model="models/gemini-2.0-flash-exp",
            contents=["Say hello in Portuguese"]
        )

        print("✅ Chamada à API bem-sucedida!")
        print(f"Resposta: {response.text[:200]}...")
        return True

    except httpx.ConnectError as e:
        print(f"❌ Erro de conexão: {e}")
        return False

    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DE CONECTIVIDADE - Google Gemini API")
    print("=" * 60)

    # Teste 1: Conexão básica
    test1_ok = test_basic_connection()

    # Teste 2: API Gemini completa
    if test1_ok:
        test2_ok = test_gemini_api()
    else:
        print("\n⏭️ Pulando teste da API Gemini devido a falha de conexão básica")
        test2_ok = False

    # Resultado final
    print("\n" + "=" * 60)
    if test1_ok and test2_ok:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("Sua aplicação deve funcionar corretamente.")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("Verifique as mensagens acima para diagnosticar o problema.")
    print("=" * 60)
