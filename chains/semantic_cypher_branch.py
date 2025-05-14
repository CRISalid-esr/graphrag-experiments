from langchain.schema.runnable import RunnableBranch
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import RunnableLambda, Runnable

from factories.graph_client_factory import GraphClientFactory
from factories.llm_client_factory import LLMClientFactory
from runnables.cypher_retrieval import CypherRetrieval
from runnables.semantic_retrieval import SemanticRetrieval
from runnables.smart_selector import SmartSelector
from schemas import ChatRequest, ChatResponse


class SemanticCypherBranch(Runnable[ChatRequest, ChatResponse]):
    """
    A runnable that selects between Cypher and semantic retrieval based on the input request.
    """

    def __init__(self):
        llm: BaseLanguageModel = LLMClientFactory.get_llm_client("openai")  # or "gemini", etc.
        graph = GraphClientFactory.get_client()

        self.chain = SmartSelector(llm) | RunnableBranch(
            (lambda x: x.metadata["route"] == "cypher", CypherRetrieval(llm=llm, graph=graph)),
            (lambda x: x.metadata["route"] == "semantic", SemanticRetrieval(llm=llm)),
            RunnableLambda(lambda x: "Invalid route")
        )

    def invoke(self, __input, config=None, **kwargs):
        return self.chain.invoke(__input)
