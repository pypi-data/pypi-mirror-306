import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from typing import Any, Dict, List, overload, Literal, cast, AnyStr
import re
from datetime import datetime
from .ENUMS_MODELS import AvailModels


terminal_file = open("terminal.txt", "w")
original_write = sys.stdout.write


def writer(*args):
    original_write(*args)  # Write to the original stdout
    terminal_file.write(''.join(map(str, args)))  # Write to the terminal.txt file
    terminal_file.flush()  # Make sure the write is persisted


sys.stdout.write, sys.stderr.write = writer, writer


def simple_msgs(msgs: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [{"role": r, "content": re.sub(r"\s+", " ", c)} for m in msgs for r, c in m.items()]


class Client:
    """
    ## Providers
    - anthropic
    - openai
    - deepseek
    - deepinfra
    - google
    """

    def __init__(
        self,
        model: AvailModels,
        **kwargs,
    ) -> None:
        ...
        self.provider = model.split("|")[0]
        self.model = model.split("|")[1]
        self.openai_canonical = ['openai', 'deepseek', "deepinfra", "groq", "ollama"]

    def chat(self, messages, *, system="", max_tokens=4096, temperature=0.5, stream=False, **kwargs) -> Any:
        if any(role in messages[0] for role in ['user', 'assistant', 'system']):
            messages = simple_msgs(messages)

        if system and self.provider in self.openai_canonical:
            messages = [{"role": "system", "content": system}] + messages

        kwargs = {**kwargs, "max_tokens": max_tokens, "temperature": temperature, "messages": messages}

        match self.provider:
            case "anthropic":
                return Anthropic().messages.create(model=self.model, system=system, **kwargs).content[0].text
            case "openai" | "deepseek" | "ollama" | "deepinfra":
                client = self._get_openai_client()
                if stream:
                    return self._stream_openai_responses(client, model=self.model, **kwargs)
                return client.chat.completions.create(model=self.model, **kwargs).choices[0].message.content
            case "google":
                # TODO: implement google stream
                pass

    def _get_openai_client(self):
        from openai import OpenAI

        match self.provider:
            case "openai":
                return OpenAI()
            case "deepseek":
                return OpenAI(base_url="https://api.deepseek.com", api_key=os.environ.get("DEEPSEEK_API_KEY"))
            case "ollama":
                return OpenAI(base_url="http://localhost:11434/v1")
            case "deepinfra":
                return OpenAI(base_url="https://api.deepinfra.com/v1/openai", api_key=os.environ.get("DEEPINFRA_API_KEY"))

    def _stream_openai_responses(self, client, **kwargs):
        from openai import OpenAI

        response = client.chat.completions.create(stream=True, extra_body={"options": {"main_gpu": -1, "low_vram": True}}, **kwargs)
        for res in response:
            # print(res)
            yield res.choices[0].delta.content


if __name__ == "__main__":
    # CONTEXT = tools.get_youtube_transcript("gaWxyWwziwE")
    CONTEXT = ""
    SYS = f"""
    you are an openAPI spec generator V3, give optimal response.
    # CONTEXT:\n {CONTEXT}
    """
    
    Client("")
    # print((CONTEXT))
    # CONTEXT = 'tools.get_youtube_transcript("wiLJ1-cQgFM")'
    resp = Client("deepinfra|nvidia/Llama-3.1-Nemotron-70B-Instruct").chat(
        system=SYS,
        messages=[
            {"user": """ Provide an OpenAPI 3.0 specification for a news aggregation and delivery API. """},
        ],
        stream=True,
        max_tokens=2048,
    )
    # for r in resp:
    #     print(r)

    # os.system("code output.md")
    open("temp.md", "w")
    for r in resp:
        if r:
            print(r, end="")
            open("temp.md", "a").write(r)
