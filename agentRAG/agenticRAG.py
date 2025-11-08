from .agenticRAGAbstract import AgentRAGAbstract
from .agenticRAGemini import AgentRAGemini

class AgentRAG(AgentRAGAbstract):

    def __init__(self):
        pass
        

    def query(self, query):
        agent = AgentRAGemini()
        return agent.query(query)
