import discord
from discord import Message
from discord.ext import commands

from ollama import get_response, memory
from utils.logger import logger

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        logger.info(f"Logged on as {self.user}")
    
    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        memory.save_chat("user", message.content)
        if self.user in message.mentions:
            logger.info(f"{message.author}: {message.content}")
            prompt = " ".join(message.content.split(" ")[1:])
            response = get_response(
                username=message.author,
                prompt=prompt,
                images=message.attachments,
            )
            await message.channel.send(response)