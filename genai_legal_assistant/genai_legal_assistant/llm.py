import os
import openai
from typing import Optional


def get_openai_api_key() -> Optional[str]:
    return os.environ.get("OPENAI_API_KEY")


def openai_completion(prompt: str, model: str = "gpt-4", max_tokens: int = 500) -> str:
    key = get_openai_api_key()
    if not key:
        return "[No API key set] LLM unavailable. Install OPENAI_API_KEY to enable full explanations."
    openai.api_key = key
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "You are a helpful legal assistant for Indian SMEs."},
                  {"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()


def summarize_contract(text: str) -> str:
    prompt = f"Summarize the following contract in simple business English for an Indian SME:\n\n{text[:4000]}"
    return openai_completion(prompt, model="gpt-4")


def explain_clause(clause_text: str) -> str:
    prompt = f"Explain the following contract clause in simple business English, list risks and suggest an alternative clause:\n\n{clause_text}"
    return openai_completion(prompt, model="gpt-4")
