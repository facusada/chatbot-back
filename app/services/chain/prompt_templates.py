from typing import Iterable

from app.schemas.chat import Message

DEFAULT_SYSTEM_PROMPT = (
    "Eres un asistente útil. Responde en español de forma clara y concisa, "
    "haciendo referencia al historial cuando tenga sentido."
)


def render_prompt(
    history: Iterable[Message],
    latest_user_message: str,
    context: dict | None = None,
) -> str:
    pieces: list[str] = [f"Sistema: {DEFAULT_SYSTEM_PROMPT}"]

    if context:
        ctx_lines = ", ".join(f"{key}={value}" for key, value in context.items())
        pieces.append(f"Contexto: {ctx_lines}")

    for message in history:
        pieces.append(f"{message.role.capitalize()}: {message.content}")

    pieces.append(f"Usuario: {latest_user_message}")
    pieces.append("Asistente:")
    return "\n".join(pieces)
