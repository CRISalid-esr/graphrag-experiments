from langchain.schema.runnable import Runnable
from langchain_community.graphs import Neo4jGraph
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import RunnableLambda

from schemas import ChatRequest, ChatResponse


class SemanticRetrieval(Runnable[ChatRequest, ChatResponse]):
    """
    Runnable to perform semantic retrieval using a language model.
    """

    def __init__(self, llm: BaseLanguageModel, graph: Neo4jGraph):
        self.runnable = RunnableLambda(lambda x: ChatResponse(
            reply="This is a semantic retrieval response.",
            query=None
        ))

    def invoke(self, __input, config=None, **kwargs):
        return self.runnable.invoke(__input)
