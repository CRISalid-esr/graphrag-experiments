# pylint: disable=cyclic-import
from langchain_openai import ChatOpenAI
from schemas import ChatRequest, ChatResponse
from services.langchain_graphrag_service import LangchainGraphRagService

class OpenaiLangChainGraphRagService(LangchainGraphRagService):
    """
    LangChain GraphRAG service implementation, using an OpenAi model.
    """

    def run(self, request: ChatRequest) -> ChatResponse:
        """
        Process the chat request and return a response.
        :param request: ChatRequest object from the client side with the question to answer
        :return: ChatResponse object with the answer to the question
        """
        last_message = request.message
        llm = ChatOpenAI(
            model=self.config["OPENAI_MODEL_NAME"],
            temperature=self.config["OPENAI_MODEL_TEMP"],
            max_tokens=1000,
        )

        rag_reply, cypher_query = self._query_rag(llm,last_message)
        reply = self._create_reply(cypher_query, rag_reply)
        return ChatResponse(reply=reply)
