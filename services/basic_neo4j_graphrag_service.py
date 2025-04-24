from schemas import ChatRequest, ChatResponse
from services.graphrag_service import GraphRagService


class BasicNeo4jGraphRagService(GraphRagService):
    """
    Basic Neo4j GraphRAG service implementation.
    """

    def run(self, request: ChatRequest) -> ChatResponse:
        last_message = request.message
        return ChatResponse(reply=f"Vous avez demandé '{last_message}'. Vous aurez la réponse "
                                  f"quand le code du GraphRag sera écrit au plus vite.")
