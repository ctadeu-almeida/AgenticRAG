import streamlit as st
from retriever import Retriever
from augmentation import Augmentation
from generation import Generation
from agentRAG.agenticRAG import AgentRAG


# Configuração da página
st.set_page_config(page_title="RAG Chat", page_icon="🤖")

# Título
st.title("🤖 AgenticRAG Chat Assistant")

# Inicializar histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua pergunta..."):
    # Adicionar pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Processar e responder
    with st.chat_message("assistant"):
        try:
            with st.spinner("Processando..."):

                dataset = AgentRAG().query(prompt)
                dataset_escolhido = dataset['dataset_name']
                query_traduzida = dataset['query']

                retriever = Retriever(collection_name=dataset_escolhido)
                augmentation = Augmentation()
                generation = Generation(model="gemini-2.5-flash")

               # Buscar documentos
                chunks = retriever.search(query_traduzida, n_results=10, show_metadata=False)
                prompt_augmented = augmentation.generate_prompt(query_traduzida, chunks)

                # Gerar resposta
                response = generation.generate(prompt_augmented)

                st.markdown(response)

            # Adicionar resposta ao histórico
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            error_msg = f"❌ **Erro ao processar sua pergunta:**\n\n{str(e)}\n\n"
            error_msg += "**Possíveis soluções:**\n"
            error_msg += "- Verifique sua conexão com a internet\n"
            error_msg += "- Verifique se a API key do Gemini está correta\n"
            error_msg += "- Tente novamente em alguns segundos\n"
            error_msg += "- Verifique se há proxy/firewall bloqueando a conexão"

            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
