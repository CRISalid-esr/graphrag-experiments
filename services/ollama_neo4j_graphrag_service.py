from neo4j import GraphDatabase

from neo4j_graphrag.llm import OllamaLLM
from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.generation import GraphRAG

from dotenv import dotenv_values

from schemas import ChatRequest, ChatResponse
from services.graphrag_service import GraphRagService


class OllamaNeo4jGraphRagService(GraphRagService):
    """
    Neo4j GraphRAG service implementation, using a local Ollama model and a Text2Cypher approach.
    """
    def __init__(self):
        self.config = dotenv_values(".env")

    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: ChatRequest object from the client side with the question to answer
        :return: ChatResponse object with the answer to the question
        """
        last_message = request.message

        reply = self.text2cypher_query_graphrag(last_message)

        return ChatResponse(reply=reply)

    def text2cypher_query_graphrag(self, question: str) -> str:
        """
        Queries the Neo4j database using a Text2Cypher process.
        :param question: The question to answer
        :return: The answer to the question
        """
        auth_params = (self.config['NEO4J_USERNAME'],self.config['NEO4J_PASSWORD'])
        driver = GraphDatabase.driver(self.config['NEO4J_URI'],auth=auth_params)

        model_params = {"temperature": float(self.config['MODEL_TEMP'])}
        llm = OllamaLLM(model_name=self.config['MODEL_NAME'], model_params=model_params)

        retriever = Text2CypherRetriever(
            driver=driver,
            llm=llm,
            neo4j_schema=self.config['NEO4J_SCHEMA'],
            #examples=examples,
        )

        rag = GraphRAG(retriever=retriever, llm=llm)

        response = rag.search(query_text=question)
        driver.close()
        return response.answer
