# file: prompts/prompt_builder.py

from pathlib import Path
from typing import Union, Optional, Any

from langchain_core.prompts import PromptTemplate


class PromptBuilder:
    """
    A builder class to build a prompt template from a file.
    """

    def __init__(self):
        self._input_variables: Optional[list[str]] = None
        self._template: Optional[str] = None

    def with_variables(self, variables: list[str]) -> "PromptBuilder":
        """
        Set the input variables for the prompt template.
        :param variables:  A list of input variable names.
        :return: self: The current instance of PromptBuilder.
        """
        self._input_variables = variables
        return self

    def from_file(self, template_file: Union[str, Path],
                  encoding: Optional[str] = "utf-8") -> "PromptBuilder":
        """
        Read the prompt template from a file.
        :param template_file: The path to the template file.
        :param encoding: The encoding of the file. Default is 'utf-8'.
        :return: self: The current instance of PromptBuilder.
        """
        path = Path(template_file)
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {template_file}")

        self._template = path.read_text(encoding=encoding)
        return self

    def build(self, **kwargs: Any) -> PromptTemplate:
        """
        Build the prompt template.
        :param kwargs: Additional keyword arguments to pass to the PromptTemplate.
        :return: PromptTemplate: The constructed PromptTemplate object.
        """
        if not self._input_variables:
            raise ValueError("PromptBuilder: input variables have not been provided.")
        if not self._template:
            raise ValueError("PromptBuilder: template file has not been provided or read.")

        return PromptTemplate(
            input_variables=self._input_variables,
            template=self._template,
            **kwargs
        )
