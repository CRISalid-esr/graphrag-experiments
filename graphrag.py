from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from langchain.chains.base import Chain
from starlette.responses import FileResponse

from chains.semantic_cypher_branch import SemanticCypherBranch
from schemas import ChatRequest, ChatResponse


class GraphRag(FastAPI):
    """
    GraphRag app managing the LangChain chain routing and static frontend.
    """

    def __init__(self):
        super().__init__()
        self.chain_instance: Chain | None = None
        self._mount_gui()
        self._include_routes()
        self._add_event_handlers()

    def _mount_gui(self):
        self.mount("/static", StaticFiles(directory="chat-client/build/static"), name="static")

    def _include_routes(self):
        @self.get("/chat", include_in_schema=False)
        def serve_chat():
            return FileResponse("chat-client/build/index.html")

        @self.post("/api", response_model=ChatResponse)
        def chat_api(request: ChatRequest):
            return self.chain_instance.invoke(request)

    def _get_chain(self) -> Chain:
        if self.chain_instance is None:
            self.chain_instance = SemanticCypherBranch()
        return self.chain_instance

    def _add_event_handlers(self):
        self.add_event_handler("startup", self._on_startup)

    async def _on_startup(self):
        print("GraphRag application is starting up")
        self.chain_instance = self._get_chain()
        print("SemanticCypherBranch chain initialized successfully")
