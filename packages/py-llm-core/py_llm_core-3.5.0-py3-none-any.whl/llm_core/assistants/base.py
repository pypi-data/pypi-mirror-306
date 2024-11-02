# -*- coding: utf-8 -*-
from textwrap import dedent
from dataclasses import dataclass
from typing import Callable

from ..llm import (
    OpenAIChatModel,
    AzureOpenAIChatModel,
    MistralAIModel,
    OpenWeightsModel,
    AnthropicModel,
    GoogleAIModel,
)
from ..parsers import (
    BaseParser,
    OpenAIParser,
    AzureOpenAIParser,
    OpenWeightsParser,
    MistralAIParser,
    AnthropicParser,
    GoogleAIParser,
)


@dataclass
class BaseAssistant(BaseParser):
    target_cls: Callable
    model: str
    model_cls: Callable
    loader: Callable = None
    loader_kwargs: dict = None
    system_prompt: str = "You are a helpful assistant"
    prompt: str = ""
    tools: list = None

    def __post_init__(self):
        super().__post_init__()
        self.system_prompt = getattr(self.target_cls, "system_prompt", "")
        self.prompt = getattr(self.target_cls, "prompt", "")

    def process(self, **kwargs):
        system_prompt = dedent(self.system_prompt.format(**kwargs))
        prompt = dedent(self.prompt.format(**kwargs))

        self.llm.system_prompt = system_prompt

        if not self.target_json_schema["properties"]:
            return self.llm.ask(
                prompt,
                schema=self.target_json_schema,
                tools=self.tools,
                raw_tool_results=True,
            )

        completion = self.llm.ask(
            prompt,
            schema=self.target_json_schema,
            tools=self.tools,
        )

        instance = self.deserialize(completion.choices[0].message.content)

        return instance


@dataclass
class OpenAIAssistant(BaseAssistant, OpenAIParser):
    model: str = "gpt-4o-mini"
    model_cls: Callable = OpenAIChatModel


@dataclass
class AzureOpenAIAssistant(BaseAssistant, AzureOpenAIParser):
    model: str = "gpt-4o-mini"
    model_cls: Callable = AzureOpenAIChatModel


@dataclass
class MistralAIAssistant(BaseAssistant, MistralAIParser):
    model: str = "open-mistral-nemo"
    model_cls: Callable = MistralAIModel


@dataclass
class OpenWeightsAssistant(BaseAssistant, OpenWeightsParser):
    model: str = "mistral-7b-v0.3-q4"
    model_cls: Callable = OpenWeightsModel


@dataclass
class AnthropicAssistant(BaseAssistant, AnthropicParser):
    model: str = "claude-3-5-sonnet-20240620"
    model_cls: Callable = AnthropicModel


@dataclass
class GoogleAIAssistant(BaseAssistant, GoogleAIParser):
    model: str = "gemini-1.5-flash"
    model_cls: Callable = GoogleAIModel
