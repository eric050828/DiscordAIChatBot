from discord import app_commands, Interaction
from discord.ext import commands

from logger import logger


class VoiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog: {self.__class__.__name__} loaded")
    
    @app_commands.command(name="join", description="add the bot to the voice channel you are in")
    async def join(self, interaction: Interaction):
        channel = interaction.user.voice.channel
        if channel is None:
            logger.error("Voice channel not found")
            await interaction.response.send_message("bruh 你還沒進語音 我進不去啦")
            return
        if self.bot.voice_clients:
            await self.bot.voice_clients[0].move_to(channel)
        else:
            vc = await channel.connect()
            vc.move_to(channel)
        await interaction.response.send_message(interaction.guild.get_emoji(1143919502032122006))

    @app_commands.command(name="leave", description="kick the bot from the current voice channel")
    async def leave(self, interaction: Interaction):
        if self.bot.voice_clients:
            await self.bot.voice_clients[0].disconnect()

async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceCog(bot))