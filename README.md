# Wrapper for the moonlist api
> Wrapper for the moonlist api with webhook and auto post data supporting

# How to install?
> From pip:
> ```
> pip install mlc
> ```
> From source:
> ```
> pip install git+https://github.com/VadyChel/MoonlistClient
> ```

# Examples
Simple usage:
```py
from mlc import MoonlistClient, HTTPException
from discord.ext import commands, tasks


class MLCExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mclient = MoonlistClient(
            bot=self.bot,
            api_key="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            autopost=False        
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
    client.add_cog(MLCExample(client))
```

Other examples you can see in [examples directory](https://github.com/VadyChel/MoonbotsClient/tree/main/examples)
