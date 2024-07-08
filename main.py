import os

from dotenv import load_dotenv
import discord

from client import Client


load_dotenv(".env")
token = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(token)