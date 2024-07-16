import os

from dotenv import load_dotenv
import discord

from client import Client
from utils.path import path


load_dotenv(path(".env"))
token = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = Client(command_prefix="/", intents=intents)
client.run(token)