import os
import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

DEFAULT_MODEL = "mistralai/mistral-7b-instruct"


def get_openrouter_key():
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY not set")
    return key


# openrouter.py

def generate_openrouter_reply(
    messages,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.5, # Reduced for stability
    max_tokens: int = 1000,
):
    api_key = get_openrouter_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "DEKAI",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        # 1. STOP THE LOOPING: Add stop sequences
        "stop": ["</s>", "[s]", "User:", "Assistant:", "Instruction:"],
        # 2. REPETITION PENALTY: Prevents the "hello there hello there" loop
        "frequency_penalty": 0.5, 
        "presence_penalty": 0.5,
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    content = data["choices"][0]["message"]["content"]
    
    # 3. CLEANING: If the model still leaks the prompt, cut it off
    if "[s]" in content:
        content = content.split("[s]")[0]
        
    return content.strip()
