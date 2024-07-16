import base64
import os

from discord import Message
from discord.ext import commands

from ollama import get_response
from utils.logger import logger
from utils.path import path


class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")
        logger.info(f"{len(self.tree.get_commands())} commands synced")
        
    async def setup_hook(self):
        for cogfile in os.listdir(path("src", "cogs")):
            if not cogfile.endswith(".py"): continue
            extension = f"cogs.{cogfile[:-3]}"
            try:
                await self.load_extension(extension)
            except Exception as e:
                logger.error(f"Failed to load extension {extension}: {e}")
        await self.tree.sync()
    
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
        await self.process_commands(message)