from langchain.schema.runnable import Runnable
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Neo4jVector
from langchain_core.embeddings import Embeddings
from langchain_core.runnables import RunnableLambda

from config import config as app_config
from schemas import ChatRequest, ChatResponse


class SemanticRetrieval(Runnable[ChatRequest, ChatResponse]):
    """
    Runnable to perform semantic retrieval using a language model, with prettified output.
    """

    _embedding_model: Embeddings = None

    def __init__(self):

        self.vector_retriever = Neo4jVector.from_existing_index(
            embedding=self._get_model(),
            url=app_config["NEO4J_URI"],
            username=app_config["NEO4J_USERNAME"],
            password=app_config["NEO4J_PASSWORD"],
            index_name="title_embedding_index",
            node_label="Literal",
            text_node_property="value",
            embedding_node_property="title_embedding",
            retrieval_query="""
               // nodes and scores are passed from the vector retrieval step
               WITH node AS literal, score AS similarity
               MATCH (literal)<-[:HAS_TITLE]-(doc:Document)
                     -[:HAS_CONTRIBUTION]->(contrib:Contribution)
                     <-[:HAS_CONTRIBUTION]-(author:Person)
               RETURN literal.value AS text, similarity AS score,
                   {author_names: collect(DISTINCT author.display_name)} AS metadata
           """
        )

        retriever = self.vector_retriever.as_retriever(
            search_kwargs={"k": int(app_config["LANGCHAIN_VECTOR_TOPK"])}
        )

        self.chain: Runnable[ChatRequest, ChatResponse] = (
                RunnableLambda(self._convert_input)
                | retriever
                | RunnableLambda(self._format_docs)
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
        raw_text = "\n".join(
            f"- {doc.page_content} de {', '.join(doc.metadata['author_names'])}"
            for doc in docs
        )
        return raw_text

    @staticmethod
    def _convert_to_response(prettified_text: str) -> ChatResponse:
        return ChatResponse(reply=prettified_text, query=None)

    def invoke(self, __input, config=None, **kwargs):
        return self.chain.invoke(__input, config=config)
