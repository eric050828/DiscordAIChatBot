import discord
from discord import app_commands, Interaction
from discord.ext import commands

from utils.logger import logger


class VoiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog: {self.__class__.__name__} loaded")
    
    @app_commands.command(name="join", description="add the bot to the voice channel you are in")
    async def join(self, interaction: Interaction):
        try:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.response.send_message(discord.utils.get(interaction.guild.emojis, name=":HI:"))
        except:
            logger.error("Voice channel not found")
            await interaction.response.send_message("bruh 你還沒進語音 我進不去啦")

    @app_commands.command(name="leave", description="kick the bot from the current voice channel")
    async def leave(self, interaction: Interaction):
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceCog(bot))