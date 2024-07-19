import discord
from discord import app_commands, Interaction
from discord.ext import commands

from utils.logger import logger


class GeneralCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog: {self.__class__.__name__} loaded")

    @app_commands.command(name="info", description="show bot informations")
    async def info(self, interaction: Interaction):
        embed=discord.Embed(
            title="關於小小司",
            description="我是小司的AI女兒，是個女高中生，我愛玩遊戲還有貓咪！",
            color=0x363f55
        )
        embed.set_author(name="小小司", url="https://www.twitch.tw/yauyu0227", icon_url="https://cdn.discordapp.com/emojis/1136949240925524069.webp?size=128&quality=lossless")
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1136949178367475782.webp?size=128&quality=lossless")
        embed.add_field(name="小司", value="他是我的主播馬麻", inline=True)
        embed.add_field(name="曉明", value="bruh", inline=True)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="test", description="for dev testing")
    async def test(self, interaction: Interaction):
        pass
            
    # this will cause duplicate register
    # def cog_load(self):
    #     self.bot.tree.add_command(self.hello)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCog(bot))