import logging
from abc import abstractmethod

from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_core.prompts.prompt import PromptTemplate
from pydantic import ValidationError

from schemas import ChatRequest, ChatResponse
from services import GraphRagService


class LangchainGraphRagService(GraphRagService):
    """
    Abstract base class for LangChain GraphRAG services.
    """
    @abstractmethod
    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: the chat request containing the message and history
        :return: the chat response containing the reply
        """

    def _query_rag(self, llm, question):
        url = self.config["NEO4J_URI"]
        username = self.config["NEO4J_USERNAME"]
        password = self.config["NEO4J_PASSWORD"]
        graph = Neo4jGraph(url=url, username=username, password=password)

        cypher_generation_template = """Task:Generate Cypher statement to query a graph database.
        Instructions:
        Use only the provided relationship types and properties in the schema.
        Do not use any other relationship types or properties that are not provided.
        Schema:
        {schema}
        
        Note: Do not include any explanations or apologies in your responses.
        Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
        Do not include any text except the generated Cypher statement.

        The question is:
        {question}"""

        cypher_generation_prompt = PromptTemplate(
            input_variables=[self.config["NEO4J_SCHEMA"], question],
            template=cypher_generation_template
        )

        chain = GraphCypherQAChain.from_llm(
            llm,
            graph=graph,
            verbose=True,
            cypher_prompt=cypher_generation_prompt,
            allow_dangerous_requests=True,
        )

        try:
            result = chain.invoke(question)
            return result["result"]
        except (ValidationError, ValueError) as e:
            logging.error("RAG failure: %s", e)
            return "Une erreur est survenue. Je ne peux pas fournir l'information demandée."
