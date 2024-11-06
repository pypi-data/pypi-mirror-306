from typing import Literal, Union, TypeAlias, Optional
from genotype import Model


OpenAIModelV1 : TypeAlias = Union[Literal["gpt-4o"], Literal["gpt-4o-2024-05-13"], Literal["gpt-4-turbo"], Literal["gpt-4-turbo-2024-04-09"], Literal["gpt-4-0125-preview"], Literal["gpt-4-turbo-preview"], Literal["gpt-4-1106-preview"], Literal["gpt-4-vision-preview"], Literal["gpt-4"], Literal["gpt-4-0314"], Literal["gpt-4-0613"], Literal["gpt-4-32k"], Literal["gpt-4-32k-0314"], Literal["gpt-4-32k-0613"], Literal["gpt-3.5-turbo"], Literal["gpt-3.5-turbo-16k"], Literal["gpt-3.5-turbo-0301"], Literal["gpt-3.5-turbo-0613"], Literal["gpt-3.5-turbo-1106"], Literal["gpt-3.5-turbo-0125"], Literal["gpt-3.5-turbo-16k-0"]]
"""OpenAI model identifier."""


class OpenAISettingsV1(Model):
    """OpenAI model settings."""

    type: Literal["openai"]
    """Settings type."""
    model: Optional[OpenAIModelV1] = None
    """Model identifier."""


OpenAIProviders : TypeAlias = Union[Literal["openai"], Literal["azure"]]
"""OpenAI provider enum."""
