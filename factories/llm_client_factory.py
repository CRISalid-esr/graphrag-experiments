from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI

from config import config


class LLMClientFactory:
    """
    Factory class to create a language model client.
    """

    @staticmethod
    def get_llm_client(provider: str) -> BaseLanguageModel:
        """
        Factory method to create a language model client based on the provider.
        :param provider: The name of the provider (e.g., "openai").
        :return: An instance of a language model client.
        """
        provider = provider.lower()

        if provider == "openai":
            model_name = config['OPENAI_MODEL_NAME']
            temperature = float(config['OPENAI_MODEL_TEMP'])

            return ChatOpenAI(
                model=model_name,
                temperature=temperature,
                max_tokens=1000,
            )

        raise ValueError(f"Unknown provider: {provider}")
