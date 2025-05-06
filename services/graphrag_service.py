from abc import ABC, abstractmethod
import json
from dotenv import dotenv_values, load_dotenv
from schemas import ChatRequest, ChatResponse


class GraphRagService(ABC):
    """
    Abstract base class for GraphRAG services.
    """

    def __init__(self):
        load_dotenv()
        self.config = dotenv_values(".env")
        with open(self.config["NEO4J_EXAMPLES"], 'rt', encoding='utf-8') as f:
            self.config["NEO4J_EXAMPLES_LIST"] = json.load(f)

    @abstractmethod
    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: the chat request containing the message and history
        :return: the chat response containing the reply
        """
