
from retriever import Retriever
from augmentation import Augmentation
from generation import Generation

from agentRAG.agenticRAGemini import AgentRAGemini


query = "O que é direito constitucional fala do abandono afetivo?"
dataset = AgentRAGemini().query(query)

dataset_escolhido = dataset['dataset_name']

retriever = Retriever(collection_name=dataset_escolhido)
augmentation = Augmentation()
generation = Generation(model="gemini-2.5-flash")


# Buscar documentos
chunks = retriever.search(query, n_results=10, show_metadata=False)
prompt = augmentation.generate_prompt(query, chunks)

# Gerar resposta
response = generation.generate(prompt)

print(response)       
