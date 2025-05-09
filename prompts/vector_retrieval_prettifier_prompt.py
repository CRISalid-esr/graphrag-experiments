from pathlib import Path
from typing import Union, Optional, Any

from langchain_core.prompts import PromptTemplate


class VectorRetrievalPrettifierPrompt(PromptTemplate):
    """
    Prompt template for prettifying output of vector retrieval.
    """

    @classmethod
    def from_file(
            cls,
            template_file: Union[str, Path],
            input_variables: Optional[list[str]] = None,
            encoding: Optional[str] = None,
            **kwargs: Any,
    ) -> PromptTemplate:
        path = Path(template_file)
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {template_file}")

        template = path.read_text(encoding="utf-8")
        return cls(
            input_variables=["list"],
            template=template
        )
