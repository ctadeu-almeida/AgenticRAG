from dotenv import load_dotenv 
from crewai import Crew, Agent, Task, Process
from datasets import Datasets
from .agenticRAGAbstract import AgentRAGAbstract

import json

load_dotenv()

class AgentRAGCrewAI(AgentRAGAbstract):

    def __init__(self):
        self.llm = "gpt-5-mini"
        self.datasets = Datasets()
        
    def create_crew(self, query):
        
        router = Agent(
            role="Agente Roteador de RAG",
            goal=(
                "Decidir, com base na solicitação do usuário, "
                "qual base vetorial de conhecimento deve ser usada "
                "para responder da forma mais adequada."
            ),
            backstory=(
                "Você é um especialista em recuperação de informação e agente RAG. "
                "Sua função é interpretar a solicitação e determinar de forma precisa qual "
                "dataset de conhecimento deve ser consultado. "
            ),
            reasoning=True,
            verbose=True,
            llm=self.llm
        )
        
        description, frase_dataset_name = self.create_description(query)
        
        task = Task(
            name="Decidir dataset RAG",
            agent=router,
            description=description,
            expected_output="Um json com as informações do dataset escolhido e com a query traduzida para o locale do dataset escolhido",
            llm=self.llm
        )

        self.crew = Crew(
            agents=[router],
            tasks=[task],
            process=Process.sequential
        )

    def create_description(self, query):
                # Construir descrição dos datasets
        description = f'''
            🎯 Sua missão:
            Com base na solicitação do usuário "{query}" escolha
            somente um dataset é mais apropriado da lista abaixo:
            '''
            

        for dataset in self.datasets.datasets:
            description += f"- {dataset['description']} escreva -> {dataset['dataset']}. Dataset Locale: {dataset['locale']}"

                
        description += r"""\n
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

        return description



    def kickoff(self, query):
        self.create_crew(query)
        # inputs deve conter a chave 'query'
        response = self.crew.kickoff()
        return response

    def query(self, query):
        response = self.kickoff(query)
        
        #converta o json em string para que possa ser convertido em um objeto json
        response.raw = json.dumps(response.raw)
        
        return response.raw


