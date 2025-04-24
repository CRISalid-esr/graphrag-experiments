from abc import ABC, abstractmethod

from schemas import ChatRequest, ChatResponse


class GraphRagService(ABC):
    """
    Abstract base class for GraphRAG services.
    """

    @abstractmethod
    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: the chat request containing the message and history
        :return: the chat response containing the reply
        """
