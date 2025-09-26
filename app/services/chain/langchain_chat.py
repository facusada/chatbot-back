from typing import Iterable

from langchain_core.prompts import ChatPromptTemplate

from app.schemas.chat import Message
from app.services.chain.prompt_templates import render_prompt
from app.services.llm.base import BaseLLMClient, LLMResult


class LangChainChat:
    """Thin wrapper that uses LangChain templates before calling the LLM client."""

    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client = llm_client
        self._prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_prompt}"),
                ("human", "{conversation}"),
            ]
        )

    async def arun(
        self,
        history: Iterable[Message],
        latest_user_message: str,
        context: dict | None = None,
    ) -> LLMResult:
        rendered_prompt = render_prompt(history, latest_user_message, context)
        prompt_value = self._prompt_template.format_prompt(
            system_prompt="Integración LangChain", conversation=rendered_prompt
        )
        prompt_text = "\n".join(message.content for message in prompt_value.to_messages())
        return await self.llm_client.agenerate(prompt_text)
