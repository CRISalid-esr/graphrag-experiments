from abc import ABC, abstractmethod

from dotenv import dotenv_values, load_dotenv

from schemas import ChatRequest, ChatResponse


class GraphRagService(ABC):
    """
    Abstract base class for GraphRAG services.
    """

    def __init__(self):
        load_dotenv()
        self.config = dotenv_values(".env")

    @abstractmethod
    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: the chat request containing the message and history
        :return: the chat response containing the reply
        """

    def _create_reply(self, cypher_query, rag_reply):
        if cypher_query is not None:
            reply = "La requête Cypher était:\n" + cypher_query +\
                    ".\nLa réponse est :\n" + rag_reply
        else:
            reply = rag_reply
        return reply
