import json

from langchain.schema.runnable import Runnable
from langchain_community.graphs import Neo4jGraph
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import RunnableLambda
from langchain_neo4j import GraphCypherQAChain

from config import config as app_config
from prompts.prompt_builder import PromptBuilder
from schemas import ChatRequest, ChatResponse


class CypherRetrieval(Runnable[ChatRequest, ChatResponse]):
    """
    Runnable to retrieve Cypher queries from a Neo4j database using a language model.
    """
    _examples = None

    def __init__(self, llm: BaseLanguageModel, graph: Neo4jGraph):
        if CypherRetrieval._examples is None:
            with open(app_config["NEO4J_EXAMPLES"], 'rt', encoding='utf-8') as f:
                CypherRetrieval._examples = json.load(f)

        cypher_prompt = PromptBuilder().from_file(
            app_config["NEO4J_CYPHER_PROMPT"]).with_variables(
            ["schema", "examples", "query"]).build()

        qa_prompt = PromptBuilder().from_file(
            app_config["NEO4J_QA_PROMPT"]).with_variables(
            ["schema", "question"]).build()

        self.inner_chain = GraphCypherQAChain.from_llm(
            llm,
            graph=graph,
            verbose=True,
            cypher_prompt=cypher_prompt,
            qa_prompt=qa_prompt,
            return_intermediate_steps=True,
            allow_dangerous_requests=True,
            validate_cypher=True,
            top_k=int(app_config["LANGCHAIN_CYPHER_TOPK"]),
        )

        self.chain: Runnable[ChatRequest, ChatResponse] = (
                RunnableLambda(self._convert_input)
                | self.inner_chain
                | RunnableLambda(self._convert_output)
        )

    @classmethod
    def _convert_input(cls, chat_request: ChatRequest) -> dict:
        return {
            "schema": app_config["NEO4J_SCHEMA"],
            "examples": cls._examples,
            "query": chat_request.message
        }

    @staticmethod
    def _convert_output(result: dict) -> ChatResponse:
        return ChatResponse(
            reply=result["result"],
            query=result["intermediate_steps"][0]["query"]
        )

    def invoke(self, __input, config=None, **kwargs):
        return self.chain.invoke(__input, config=config)
