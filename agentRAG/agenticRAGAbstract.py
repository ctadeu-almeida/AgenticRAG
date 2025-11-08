from abc import ABC, abstractmethod
from datasets import Datasets


class AgentRAGAbstract(ABC):

    def __init__(self):
        self.datasets = Datasets()
        

    @abstractmethod
    def query(self, query):
        pass

