# pylint: disable=cyclic-import
from langchain_ollama import ChatOllama
from schemas import ChatRequest, ChatResponse
from services.langchain_graphrag_service import LangchainGraphRagService

class OllamaLangChainGraphRagService(LangchainGraphRagService):
    """
    LangChain GraphRAG service implementation, using a local Ollama model.
    """

    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: ChatRequest object from the client side with the question to answer
        :return: ChatResponse object with the answer to the question
        """
        last_message = request.message
        llm = ChatOllama(
            model=self.config["OLLAMA_MODEL_NAME"],
            temperature=self.config["OLLAMA_MODEL_TEMP"],
            num_predict=500,
        )

        rag_reply, cypher_query = self._query_rag(llm,last_message)
        reply = self._create_reply(cypher_query, rag_reply)
        return ChatResponse(reply=reply)
