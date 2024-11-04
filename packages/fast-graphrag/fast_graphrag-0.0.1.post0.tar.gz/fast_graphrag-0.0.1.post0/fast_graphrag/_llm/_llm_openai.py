"""LLM Services module."""

from dataclasses import dataclass, field
from typing import Any, Optional, Tuple, Type, cast

import instructor
import numpy as np
from openai import APIConnectionError, AsyncOpenAI, RateLimitError
from pydantic import BaseModel
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from fast_graphrag._exceptions import LLMServiceNoResponseError
from fast_graphrag._types import BTResponseModel, GTResponseModel
from fast_graphrag._utils import logger

from ._base import BaseEmbeddingService, BaseLLMService


@dataclass
class OpenAILLMService(BaseLLMService):
    """LLM Service for OpenAI LLMs."""

    def __post_init__(self):
        # Patch the OpenAI client with instructor
        openi_client = AsyncOpenAI()
        self.llm_async_client = instructor.from_openai(openi_client)
        logger.debug("Initialized OpenAILLMService with patched OpenAI client.")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
    )
    async def send_message(
        self,
        prompt: str,
        model: str | None = None,
        system_prompt: str | None = None,
        history_messages: list[dict[str, str]] | None = None,
        response_model: Type[GTResponseModel] | None = None,
        **kwargs: Any,
    ) -> Tuple[GTResponseModel, list[dict[str, str]]]:
        """Send a message to the language model and receive a response.

        Args:
            prompt (str): The input message to send to the language model.
            model (str): The name of the model to use. Defaults to "gpt-4o-mini".
            system_prompt (str, optional): The system prompt to set the context for the conversation. Defaults to None.
            history_messages (list, optional): A list of previous messages in the conversation. Defaults to empty.
            response_model (Type[T], optional): The Pydantic model to parse the response. Defaults to None.
            **kwargs: Additional keyword arguments that may be required by specific LLM implementations.

        Returns:
            str: The response from the language model.
        """
        logger.debug(f"Sending message with prompt: {prompt}")
        if model is None:
            model = "gpt-4o-mini"
        messages: list[dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            logger.debug(f"Added system prompt: {system_prompt}")

        if history_messages:
            messages.extend(history_messages)
            logger.debug(f"Added history messages: {history_messages}")

        messages.append({"role": "user", "content": prompt})

        llm_response: GTResponseModel = await self.llm_async_client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore
            response_model=response_model.Model
            if response_model and issubclass(response_model, BTResponseModel)
            else response_model,
            **kwargs,
        )

        if not llm_response:
            logger.error("No response received from the language model.")
            raise LLMServiceNoResponseError("No response received from the language model.")

        messages.append(
            {
                "role": "assistant",
                "content": llm_response.model_dump_json() if isinstance(llm_response, BaseModel) else str(llm_response),
            }
        )
        logger.debug(f"Received response: {llm_response}")

        if response_model and issubclass(response_model, BTResponseModel):
            llm_response = cast(
                GTResponseModel, cast(BTResponseModel.Model, llm_response).to_dataclass(llm_response)
            )

        return llm_response, messages


@dataclass
class OpenAIEmbeddingService(BaseEmbeddingService):
    """Base class for Language Model implementations."""

    embedding_async_client: AsyncOpenAI = field(default_factory=AsyncOpenAI)
    embedding_dim: int = 1536

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
    )
    async def get_embedding(
        self, texts: list[str], model: Optional[str] = None
    ) -> np.ndarray[Any, np.dtype[np.float32]]:
        """Get the embedding representation of the input text.

        Args:
            texts (str): The input text to embed.
            model (str): The name of the model to use. Defaults to "text-embedding-3-small".

        Returns:
            list[float]: The embedding vector as a list of floats.
        """
        logger.debug(f"Getting embedding for texts: {texts}")
        if model is None:
            model = "text-embedding-3-small"
        response = await self.embedding_async_client.embeddings.create(
            model=model, input=texts, encoding_format="float"
        )
        logger.debug(f"Received embedding response: {len(response.data)} embeddings")

        return np.array([dp.embedding for dp in response.data])
