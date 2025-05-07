import logging
from abc import abstractmethod

from neo4j_graphrag.exceptions import RagInitializationError, LLMGenerationError, \
    Text2CypherRetrievalError
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import Text2CypherRetriever

from schemas import ChatRequest, ChatResponse
from services import GraphRagService


class Neo4jGraphRagService(GraphRagService):
    """
    Abstract base class for Neo4j GraphRAG services.
    """

    @abstractmethod
    def _text2cypher_query_graphrag(self,question):
        """
        Queries the Neo4j database using a Text2Cypher process.
        :param question: The question to answer
        :return: The answer to the question
        """


    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: the chat request containing the message and history
        :return: the chat response containing the reply
        """
        last_message = request.message

        rag_reply, cypher_query = self._text2cypher_query_graphrag(last_message)
        return ChatResponse(reply=rag_reply, query=cypher_query)

    def _get_retriever(self, driver, llm):
        return Text2CypherRetriever(
            driver=driver,
            llm=llm,
            neo4j_schema=self.config['NEO4J_SCHEMA'],
            examples=self.config['NEO4J_EXAMPLES_LIST']
        )

    def _query_rag(self, driver, llm, question):
        try:
            rag = GraphRAG(retriever=self._get_retriever(driver, llm), llm=llm)
            response = rag.search(query_text=question, return_context=True)
            return response.answer, response.retriever_result.metadata['cypher']
        except (RagInitializationError, LLMGenerationError, Text2CypherRetrievalError) as e:
            logging.error("RAG failure: %s", e)
            return "Une erreur est survenue. Je ne peux pas fournir l'information demandée.", None
