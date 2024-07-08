import json
import requests

from utils import config

ollama_url = config.get_config("server", "ollama_url")

def get_system_prompt():
    with open("modelfile/systemPrompt.txt", "r") as f:
        return f.read()

def get_prompt_template():
    with open("modelfile/promptTemplate.txt", "r") as f:
        return f.read()


def get_response(prompt):
    print(f"generating response: {prompt}")
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "model": config.get_config("model", "model_name"),
        "stream": False,
        "system": get_system_prompt(),
        "template": get_prompt_template(),
        "options": {
            "mirostat": config.get_config("model", "mirostat", int),
            "mirostat_eta": config.get_config("model", "mirostat_eta", float),
            "mirostat_tau": config.get_config("model", "mirostat_tau", float),
            "num_ctx": config.get_config("model", "num_ctx", int),
            "repeat_last_n": config.get_config("model", "repeat_last_n", int),
            "repeat_penalty": config.get_config("model", "repeat_penalty", float),
            "temperature": config.get_config("model", "temperature", float),
            "seed": config.get_config("model", "seed", int),
            "tfs_z": config.get_config("model", "tfs_z", int),
            "num_predict": config.get_config("model", "num_predict", int),
            "top_k": config.get_config("model", "top_k", int),
            "top_p": config.get_config("model", "top_p", float),
        }
    }
    response = requests.post(ollama_url, headers=headers, json=data)
    print(response.json())
    return response.json()["response"]
