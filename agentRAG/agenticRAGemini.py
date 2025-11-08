import os
from google import genai
import json
from dotenv import load_dotenv
import httpx

from .agenticRAGAbstract import AgentRAGAbstract

load_dotenv()


class AgentRAGemini(AgentRAGAbstract):

    def __init__(self):
        super().__init__()

        # Configurar API key do Gemini
        self.model = "gemini-2.5-flash"

        # Criar client httpx com configuração SSL mais permissiva
        http_client = httpx.Client(
            verify=True,
            timeout=60.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )

        self.client = genai.Client(
            api_key=os.getenv('GEMINI_API_KEY'),
            http_options={'client': http_client}
        )



    def create_prompt(self, query):
                # Construir descrição dos datasets
        prompt = f'''
            🎯 Sua missão:
            Com base na solicitação do usuário "{query}" escolha
            somente um dataset é mais apropriado da lista abaixo:
            '''
            

        for dataset in self.datasets.datasets:
            prompt += f"- {dataset['description']} escreva -> {dataset['dataset']}. Dataset Locale: {dataset['locale']}"

                
        prompt += r"""\n
        Eu quero como saida um json com as seguintes informações do dataset escolhido:
        - dataset_name: 
        - locale:
        - query: 

        A query deve ser traduzida para o locale do dataset escolhido.
        Não adicione explicações, justificativas ou qualquer outro texto.
        Não adicione caracteres especiais ou caracteres de escape.
        Não adicione ```json ou ``` envolvendo o json de resposta, se vc colocar isso vc será demitido.

        Exemplo de saida:
        {"dataset_name": "dataset", "locale": "en", "query": "This is my question"}

        É IMPERATIVO:
        Não escreva nada além do json de resposta.
        """

        return prompt

    def query(self, query):
        """
        Implementa o método abstrato query para conectar com o Gemini
        """
        try:
            # Criar prompt com contexto
            prompt = self.create_prompt(query)

            response = self.client.models.generate_content(
                model=f"models/{self.model}",
                contents=[prompt]
            )

            response = json.loads(response.text)
            return response

        except httpx.ConnectError as e:
            print(f"❌ Erro de conexão SSL: {e}")
            print("⚠️ Possíveis soluções:")
            print("1. Verifique sua conexão com a internet")
            print("2. Verifique se há proxy/firewall bloqueando")
            print("3. Tente novamente em alguns segundos")
            raise Exception(f"Erro de conexão com API Gemini: {str(e)}")

        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar resposta JSON: {e}")
            print(f"Resposta recebida: {response.text if 'response' in locals() else 'N/A'}")
            raise Exception(f"Resposta inválida da API: {str(e)}")

        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            raise
            

