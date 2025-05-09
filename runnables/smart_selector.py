from langchain.schema.runnable import Runnable
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import RunnableLambda

from schemas import ChatRequest


class SmartSelector(Runnable[ChatRequest, ChatRequest]):
    """
    A simple selector that routes requests to either Cypher or semantic retrieval
    """

    def __init__(self, llm: BaseLanguageModel):
        def dummy_function(request: ChatRequest) -> ChatRequest:
            cypher_keywords = ["graph"]
            if any(kw in request.message.lower() for kw in cypher_keywords):
                request.metadata["route"] = "cypher"
            else:
                request.metadata["route"] = "semantic"
            return request

        self.chain = RunnableLambda(dummy_function)

    def invoke(self, __input, config=None, **kwargs):
        return self.chain.invoke(__input)
