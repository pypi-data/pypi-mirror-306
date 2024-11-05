from typing import Dict, Literal, TypedDict, Union

try:
    from openai.types.chat import ChatCompletionMessageParam  # type: ignore
except ImportError:
    ChatCompletionMessageParam = Dict[str,str] # type: ignore

def to_user_message(s: str) -> ChatCompletionMessageParam: # type: ignore
    return {
        "role": "user",
        "content": s,
    }

def to_system_message(s: str) -> ChatCompletionMessageParam: # type: ignore
    return {
        "role": "system",
        "content": s,
    }

def to_assistant_message(s: str) -> ChatCompletionMessageParam: # type: ignore
    return {
        "role": "assistant",
        "content": s,
    }

def to_tool_message(s: str) -> ChatCompletionMessageParam: # type: ignore
    return { # type: ignore
        "role": "tool",
        "content": s,
    }

def to_function_message(s: str) -> ChatCompletionMessageParam: # type: ignore
    return { # type: ignore
        "role": "function",
        "content": s,
    }