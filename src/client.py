import base64

import discord
from discord import Message
from discord.ext import commands

from ollama import get_response
from utils.logger import logger


class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        logger.info(f"Logged on as {self.user}")
    
    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        
        if self.user in message.mentions:
            logger.info(f"{message.author}: {message.content}")
            prompt = " ".join(message.content.split(" ")[1:])
            images = [base64.b64encode(await attachment.read()).decode("utf-8") for attachment in message.attachments]
            response = await get_response(
                user=message.author,
                prompt=prompt,
                images=images,
            )
            await message.channel.send(response)