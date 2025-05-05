from neo4j import GraphDatabase
from neo4j_graphrag.llm import OllamaLLM

from services.neo4j_graphrag_service import Neo4jGraphRagService


class OllamaNeo4jGraphRagService(Neo4jGraphRagService):
    """
    Neo4j GraphRAG service implementation, using a local Ollama model and a Text2Cypher approach.
    """

    def _text2cypher_query_graphrag(self, question: str) -> str:
        # pylint: disable=duplicate-code
        """
        Queries the Neo4j database using a Text2Cypher process.
        :param question: The question to answer
        :return: The answer to the question
        """

        auth_params = (self.config['NEO4J_USERNAME'], self.config['NEO4J_PASSWORD'])
        with GraphDatabase.driver(self.config['NEO4J_URI'], auth=auth_params) as driver:
            model_params = {"temperature": float(self.config['OLLAMA_MODEL_TEMP'])}
            llm = OllamaLLM(model_name=self.config['OLLAMA_MODEL_NAME'], model_params=model_params)
            return self._query_rag(driver, llm, question)
