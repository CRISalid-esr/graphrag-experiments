from schemas import ChatRequest, ChatResponse
from services.graphrag_service import GraphRagService


class BasicNeo4jGraphRagService(GraphRagService):
    """
    Basic Neo4j GraphRAG service implementation.
    """

    def run(self, request: ChatRequest) -> ChatResponse:
        last_message = request.message
        return ChatResponse(reply=f"Neo4j says: you said '{last_message}'")
