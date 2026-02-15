import os
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def call_openai(prompt, system_prompt="You are a Bangla-speaking career assistant. Always respond in Bangla (Bengali) language.", model="gpt-4o-mini", json_mode=False):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4096
    }

    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=120)

    if response.status_code != 200:
        raise Exception(f"OpenAI API Error: {response.status_code} | {response.text}")

    return response.json()["choices"][0]["message"]["content"]
