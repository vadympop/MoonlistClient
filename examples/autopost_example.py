from moonlistclient import MoonlistClient
from discord.ext import commands


class MLCExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mclient = MoonlistClient(
            bot=self.bot,
            api_key="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            autopost=True
        )

    @commands.Cog.listener()
    async def on_post_stat(self):
        print("Bot stat was posted")


def setup(client):
    client.add_cog(MLCExample(client))