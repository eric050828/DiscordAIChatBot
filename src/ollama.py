import aiohttp

from memory import Memory
from config import config
from logger import logger
from utils.path import path

ollama_url = config.server.ollama
memory = Memory()

def get_system_prompt(user, prompt):
    with open(path("modelfile", "systemPrompt.txt"), "r", encoding="utf-8") as system_file:
        system_prompt = system_file.read()
    with open(path("modelfile", "persona.txt"), "r", encoding="utf-8") as persona_file:  # TODO: change to save in chromaDB
        persona =  persona_file.read()
    user_query_results = memory.query_memory([prompt], "chatHistory", str(user.id))
    model_query_results = memory.query_memory([prompt], "chatHistory", memory.name)
    return system_prompt.format(
                username=user.name,
                persona=persona,
                user_query_results=user_query_results,
                model_query_results=model_query_results,
            )

def get_prompt_template():
    with open(path("modelfile", "promptTemplate.txt"), "r", encoding="utf-8") as f:
        return f.read()

def get_prompt(username, prompt):
    final_prompt = "{username}: {prompt}"

    return final_prompt.format(
        username=username,
        prompt=prompt
    )

def get_context(query):
    return 

async def get_response(user, prompt: str, images: list, stream: bool = False):
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "prompt": get_prompt(user.name, prompt),
        "model": config.model.model_name,
        "stream": stream,
        "system": get_system_prompt(user, prompt),
        "template": get_prompt_template(),
        "context": memory.context,
        "images": images,
        "options": {
            "mirostat": config.model.mirostat,
            "mirostat_eta": config.model.mirostat_eta,
            "mirostat_tau": config.model.mirostat_tau,
            "num_ctx": config.model.num_ctx,
            "repeat_last_n": config.model.repeat_last_n,
            "repeat_penalty": config.model.repeat_penalty,
            "temperature": config.model.temperature,
            "seed": config.model.seed,
            "stop": ["<|start_header_id|>", "<|end_header_id|>", "<|eot_id|>"],
            "tfs_z": config.model.tfs_z,
            "num_predict": config.model.num_predict,
            "top_k": config.model.top_k,
            "top_p": config.model.top_p,
        }
    }
    response_content = "bruh 又出bug了，快點叫曉明弄好啦，他又在睡噢"
    logger.info(f"Generating response for system prompt: {data['system']}\nprompt: {data['prompt']}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(ollama_url, json=data) as resp:
                response = await resp.json()
                response_content = response["response"]
                logger.info(f"Generation complete: {response_content}")
                memory.save_chat("user", prompt)
                memory.save_chat("assistant", response_content)
                memory.create_entry("chatHistory", str(user.id), prompt)
                memory.create_entry("chatHistory", memory.name, response_content)
                memory.context = response["context"]
                return response_content
    
    except KeyError:
        logger.exception(f"Error occured when generating response\n{response['error']}")
        
    except Exception:
        logger.exception("Uncaught exception")
        
    finally:
        return response_content