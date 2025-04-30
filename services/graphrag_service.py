import logging
from abc import ABC, abstractmethod

from dotenv import dotenv_values
from neo4j_graphrag.exceptions import RagInitializationError, LLMGenerationError, \
    Text2CypherRetrievalError
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import Text2CypherRetriever

from schemas import ChatRequest, ChatResponse


class GraphRagService(ABC):
    """
    Abstract base class for GraphRAG services.
    """

    def __init__(self):
        self.config = dotenv_values(".env")

    @abstractmethod
    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: the chat request containing the message and history
        :return: the chat response containing the reply
        """

    def _get_retriever(self, driver, llm):
        return Text2CypherRetriever(
            driver=driver,
            llm=llm,
            neo4j_schema=self.config['NEO4J_SCHEMA'],
        )

    def _query_rag(self, driver, llm, question):
        try:
            rag = GraphRAG(retriever=self._get_retriever(driver, llm), llm=llm)
            response = rag.search(query_text=question).answer
            return response
        except (RagInitializationError, LLMGenerationError, Text2CypherRetrievalError) as e:
            logging.error("RAG failure: %s", e)
            return "Une erreur est survenue. Je ne peux pas fournir l'information demandée."
