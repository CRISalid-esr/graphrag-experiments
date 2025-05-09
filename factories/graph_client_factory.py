from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

from config import config

load_dotenv()  # Optional if you've already loaded it in config.py


class GraphClientFactory:
    """
    Factory class to create a Neo4jGraph client.
    """

    @staticmethod
    def get_client() -> Neo4jGraph:
        """
        Factory method to create a Neo4jGraph client.
        :return: An instance of Neo4jGraph.
        """
        uri = config["NEO4J_URI"]
        username = config["NEO4J_USERNAME"]
        password = config["NEO4J_PASSWORD"]

        return Neo4jGraph(url=uri, username=username, password=password)
