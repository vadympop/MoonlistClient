from mbc import MoonbotsClient
from discord.ext import commands


class MBCExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mclient = MoonbotsClient(
            bot=self.bot,
            api_key="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            autopost=True
        )

    @commands.Cog.listener()
    async def on_post_stat(self):
        print("Bot stat was posted")


def setup(client):
    client.add_cog(MBCExample(client))