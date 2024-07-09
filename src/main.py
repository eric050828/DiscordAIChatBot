import os

from dotenv import load_dotenv
import discord

from client import Client
from utils.path import path


load_dotenv(path(".env"))
token = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(token)