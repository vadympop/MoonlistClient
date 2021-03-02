from mbc import MoonbotsClient, HTTPException
from discord.ext import commands, tasks


class MBCExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mclient = MoonbotsClient(
            bot=self.bot,
            api_key="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        )
        self.post_stat_loop.start()

    @tasks.loop(hours=3)
    async def post_stat_loop(self):
        await self.bot.wait_until_ready()
        try:
            await self.mclient.post_stat()
        except HTTPException:
            print("Failed to post bot stat")


def setup(client):
    client.add_cog(MBCExample(client))