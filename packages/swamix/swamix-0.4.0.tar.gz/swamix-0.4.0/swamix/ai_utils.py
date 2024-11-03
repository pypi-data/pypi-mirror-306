import os, re
import requests
import web


def enumgrep(code: str) -> list:
    """
    Extracts values inside square brackets in a given code string.

    Args:
    code (str): The code string to search in.

    Returns:
    list: A list of values found inside square brackets.
    """
    pattern = r"Literal\[(.*?)\]"
    matches = re.findall(pattern, code, re.DOTALL)
    values = []
    for match in matches:
        # Remove any whitespace and split by comma
        match = re.sub(r'\s+', '', match)  # remove all whitespace
        values.extend([value.strip('"').strip("'") for value in match.split(",")])
    return [value for value in values if value != '']  # remove empty strings


# src = web.req("https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/refs/heads/main/src/anthropic/types/model.py")['data']
# src = web.req("https://raw.githubusercontent.com/openai/openai-python/refs/heads/main/src/openai/types/chat_model.py")['data']


# result = enumgrep(src)
# print(result)


def get_openai_models():
    """
    {
    "object": "list",
    "data": [
        {
            "id": "dall-e-3",
            "object": "model",
            "created": 1698785189,
            "owned_by": "system"
        },
        {
            "id": "gpt-4-1106-preview",
            "object": "model",
            "created": 1698957206,
            "owned_by": "system"
        },
        {
            "id": "dall-e-2",
            "object": "model",
            "created": 1698798177,
            "owned_by": "system"
        },
        {
            "id": "tts-1-hd-1106",
            "object": "model",
            "created": 1699053533,
            "owned_by": "system"
        },
        {
    """
    url = "https://api.openai.com/v1/models"
    headers = {'Authorization': 'Bearer {}'.format(os.environ['OPENAI_API_KEY'])}
    resp = requests.get(url, headers=headers).json()
    models = sorted(resp['data'], key=lambda d: d['created'], reverse=True)
    models = [d['id'] for d in models if "gpt" in d['id']]
    models = sorted(models, key=lambda s: len(s.split('-')))  # sort by length of alphanumeric only string
    return [f"openai|{m}" for m in models]


def get_anthropic_models():
    src = web.req("https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/refs/heads/main/src/anthropic/types/model.py")['data']
    models = enumgrep(src)
    return [f'anthropic|{m}' for m in models]


def get_deepseek_models():
    return ["deepseek|deepseek-chat", "deepseek|deepseek-coder"]


def get_deepinfra_models():
    url = "https://api.deepinfra.com/deploy/list?status=running"
    models = requests.get(url, headers={"Authorization": f"Bearer {os.environ['DEEPINFRA_API_KEY']}"}).json()
    return [f'deepinfra|{x["model_name"]}' for x in models]


def get_ollama_models():
    url = "http://localhost:11434/api/tags"

    return [f"ollama|{x['name']}" for x in requests.get(url).json()['models']]


def burn(literals=[], extra=[], f="ENUMS_MODELS.py"):
    import subprocess

    joins = ",\n".join([f'\t"{x}"' for x in literals + extra])
    template = f"""from typing import Literal\nAvailModels = Literal[\n{joins}\n]"""
    open(f, "w").write(template)
    # subprocess.run(["black", f], check=True)


if __name__ == "__main__":
    print()
    burn(
        [
            *get_openai_models(),
            *get_anthropic_models(),
            *get_deepseek_models(),
            *get_deepinfra_models(),
            *get_ollama_models(),
        ],
        ["google|gemini-1.5-flash", "google|gemini-1.5-pro"],
    )
    # print()
