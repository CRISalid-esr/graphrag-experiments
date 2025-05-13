from langchain.schema.runnable import Runnable
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Neo4jVector
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import RunnableLambda

from config import config as app_config
from prompts.vector_retrieval_prettifier_prompt import VectorRetrievalPrettifierPrompt
from schemas import ChatRequest, ChatResponse


class SemanticRetrieval(Runnable[ChatRequest, ChatResponse]):
    """
    Runnable to perform semantic retrieval using a language model, with prettified output.
    """

    _embedding_model: Embeddings = None

    def __init__(self, llm: BaseLanguageModel):

        self.vector_retriever = Neo4jVector.from_existing_index(
            embedding=self._get_model(),
            url=app_config["NEO4J_URI"],
            username=app_config["NEO4J_USERNAME"],
            password=app_config["NEO4J_PASSWORD"],
            index_name="title_embedding_index",
            node_label="Literal",
            text_node_property="value",
            embedding_node_property="title_embedding",
        )

        retriever = self.vector_retriever.as_retriever(
            search_kwargs={"k": int(app_config["LANGCHAIN_VECTOR_TOPK"])}
        )

        prettify_prompt = VectorRetrievalPrettifierPrompt.from_file(
            app_config["PRETTIFIER_PROMPT"]
        )

        prettify_chain = prettify_prompt | llm

        self.chain: Runnable[ChatRequest, ChatResponse] = (
                RunnableLambda(self._convert_input)
                | retriever
                | RunnableLambda(self._format_docs)
                | prettify_chain
                | RunnableLambda(self._convert_to_response)
        )

    @classmethod
    def _get_model(cls) -> Embeddings:
        if cls._embedding_model is None:
            cls._embedding_model = HuggingFaceEmbeddings(model_name=app_config['BERT_MODEL'])
        return cls._embedding_model

    @classmethod
    def _convert_input(cls, chat_request: ChatRequest) -> str:
        return chat_request.message

    @staticmethod
    def _format_docs(docs: list) -> dict:
        if not docs:
            return {"raw": "No similar titles found."}
        raw_text = "\n".join(f"- {doc.page_content}" for doc in docs)
        return {"list": raw_text}

    @staticmethod
    def _convert_to_response(prettified_text: str) -> ChatResponse:
        return ChatResponse(reply=prettified_text.content, query=None)

    def invoke(self, __input, config=None, **kwargs):
        return self.chain.invoke(__input, config=config)
