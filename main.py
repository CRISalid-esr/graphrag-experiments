from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from schemas import ChatRequest, ChatResponse
from services import GraphRagService, BasicNeo4jGraphRagService

app = FastAPI()

app.mount("/chat", StaticFiles(directory="chat-client/build"), name="chat-client")
app.mount("/static", StaticFiles(directory="chat-client/build/static"), name="static")


def get_graph_service() -> GraphRagService:
    """
    Defines the concrete GraphRAG service to be used.
    :return: an instance of GraphRagService
    """
    return BasicNeo4jGraphRagService()


@app.post("/api", response_model=ChatResponse)
def chat_api(
        request: ChatRequest,
        service: GraphRagService = Depends(get_graph_service)
):
    """
    API endpoint for processing chat requests.
    :param request:
        The chat request containing the message and history.
    :param service:
        The GraphRAG service to process the request.
    :return:
        The chat response containing the reply.
    """
    return service.run(request)
