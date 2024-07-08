import discord
from discord import Message
from discord.ext import commands

from ollama import get_response

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        if self.user in message.mentions:
            prompt = "".join(message.content.split(" ")[1:])
            response = get_response(prompt)
            await message.channel.send(response)