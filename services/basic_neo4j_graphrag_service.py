from schemas import ChatRequest, ChatResponse
from services.neo4j_graphrag_service import Neo4jGraphRagService


class BasicNeo4jGraphRagService(Neo4jGraphRagService):
    """
    Basic Neo4j GraphRAG service implementation.
    """

    def run(self, request: ChatRequest) -> ChatResponse:
        last_message = request.message
        return ChatResponse(reply=f"Vous avez demandé '{last_message}'. Vous aurez la réponse "
                                  f"quand le code du GraphRag sera écrit au plus vite.")
