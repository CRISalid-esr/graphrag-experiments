import json

from langchain.schema.runnable import Runnable
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import RunnableLambda

from config import config as app_config
from prompts.prompt_builder import PromptBuilder
from schemas import ChatRequest


class SmartSelector(Runnable[ChatRequest, ChatRequest]):
    """
    A simple selector that routes requests to either Cypher or semantic retrieval
    """
    _examples = None

    def __init__(self, llm: BaseLanguageModel):
        if SmartSelector._examples is None:
            with open(app_config["SELECTOR_EXAMPLES"], 'rt', encoding='utf-8') as f:
                SmartSelector._examples = json.load(f)

        selector_prompt = PromptBuilder().from_file(
            app_config["SELECTOR_PROMPT"]).with_variables(["examples", "query"]).build()

        self.selector_chain = selector_prompt | llm

        self.chain: Runnable[ChatRequest, ChatRequest] = (
                RunnableLambda(self._convert_input)
                | RunnableLambda(self._return_request_with_metadata)
        )

    @classmethod
    def _convert_input(cls, chat_request: ChatRequest) -> dict:
        return {
            "examples": cls._examples,
            "query": chat_request.message,
            "request": chat_request
        }

    def _return_request_with_metadata(self, __input: dict) -> ChatRequest:
        request = __input["request"]
        request.metadata["route"] = self.selector_chain.invoke(__input).content
        return request

    def invoke(self, __input, config=None, **kwargs):
        return self.chain.invoke(__input)
