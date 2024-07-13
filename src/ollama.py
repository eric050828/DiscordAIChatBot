import os
import requests

from memory import Memory
from utils import config
from utils.logger import logger
from utils.path import path

ollama_url = config.get_config("default", "ollama_url")
memory = Memory()

def get_system_prompt(user, prompt):
    with open(path("modelfile", "systemPrompt.txt"), "r") as system_file:
        system_prompt = system_file.read()
    with open(path("modelfile", "persona.txt"), "r") as persona_file:  # TODO: change to save in chromaDB
        persona =  persona_file.read()
    user_query_results = memory.query_memory([prompt], "chatHistory", str(user.id), 3)
    model_query_results = memory.query_memory([prompt], "chatHistory", memory.name, 3)
    return system_prompt.format(
                username=user.name,
                persona=persona,
                user_query_results=user_query_results,
                model_query_results=model_query_results,
            )

def get_prompt_template():
    with open(path("modelfile", "promptTemplate.txt"), "r") as f:
        return f.read()

def get_prompt(username, prompt):
    final_prompt = "{username}: {prompt}"

    return final_prompt.format(
        username=username,
        prompt=prompt
    )

def get_context(query):
    return 

def get_response(user, prompt: str, images: list, stream: bool = False):
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "prompt": get_prompt(user.name, prompt),
        "model": config.get_config("model", "model_name"),
        "stream": stream,
        "system": get_system_prompt(user, prompt),
        "template": get_prompt_template(),
        "context": memory.context,
        "options": {
            "mirostat": config.get_config("model", "mirostat", int),
            "mirostat_eta": config.get_config("model", "mirostat_eta", float),
            "mirostat_tau": config.get_config("model", "mirostat_tau", float),
            "num_ctx": config.get_config("model", "num_ctx", int),
            "repeat_last_n": config.get_config("model", "repeat_last_n", int),
            "repeat_penalty": config.get_config("model", "repeat_penalty", float),
            "temperature": config.get_config("model", "temperature", float),
            "seed": config.get_config("model", "seed", int),
            "stop": ["<|start_header_id|>", "<|end_header_id|>", "<|eot_id|>"],
            "tfs_z": config.get_config("model", "tfs_z", int),
            "num_predict": config.get_config("model", "num_predict", int),
            "top_k": config.get_config("model", "top_k", int),
            "top_p": config.get_config("model", "top_p", float),
        }
    }
    response_content = "bruh 又出bug了，快點叫曉明弄好啦，他又在睡噢"
    logger.info(f"Generating response for system prompt: {data['system']}\nprompt: {data['prompt']}")
    try:
        response = requests.post(ollama_url, headers=headers, json=data).json()
        response_content = response["response"]
        logger.info(f"Generation complete: {response_content}")
        memory.save_chat("user", prompt)
        memory.save_chat("assistant", response_content)
        memory.update_or_create_entry("chatHistory", str(user.id), prompt)
        memory.update_or_create_entry("chatHistory", memory.name, response_content)
        memory.context = response["context"]
        return response_content
    
    except KeyError:
        logger.exception(f"Error occured when generating response\n{response['error']}")
        
    except Exception:
        logger.exception("Uncaught exception")
        
    finally:
        return response_content