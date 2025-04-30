from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j_graphrag.llm import VertexAILLM
from vertexai.generative_models import GenerationConfig

from schemas import ChatRequest, ChatResponse
from services.graphrag_service import GraphRagService


class VertexAINeo4jGraphRagService(GraphRagService):
    """
    Neo4j GraphRAG service implementation, using a VertexAI model and a Text2Cypher approach.
    """

    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: ChatRequest object from the client side with the question to answer
        :return: ChatResponse object with the answer to the question
        """
        last_message = request.message

        reply = self._text2cypher_query_graphrag(last_message)

        return ChatResponse(reply=reply)

    def _text2cypher_query_graphrag(self, question: str) -> str:
        """
        Queries the Neo4j database using a Text2Cypher process.
        :param question: The question to answer
        :return: The answer to the question
        """

        auth_params = (self.config['NEO4J_USERNAME'], self.config['NEO4J_PASSWORD'])
        with GraphDatabase.driver(self.config['NEO4J_URI'], auth=auth_params) as driver:
            load_dotenv(override=True)
            model_name = self.config['VERTEXAI_MODEL_NAME']
            generation_config = GenerationConfig(temperature= \
                                                     float(self.config['VERTEXAI_MODEL_TEMP']))

            llm = VertexAILLM(model_name=model_name,
                              generation_config=generation_config)

            return self._query_rag(driver, llm, question)
