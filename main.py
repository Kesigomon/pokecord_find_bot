import csv
import hashlib
import os
import re

from discord.ext import commands


class Main(commands.Cog):
    pattern1 = re.compile(r"^.*?/(\d*)/(\d*)$")
    with open("./db.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        data = dict(reader)
        del reader

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    async def do_hash(self, url):
        data = await self.bot.http.get_from_cdn(url)
        return hashlib.md5(data).hexdigest()

    @commands.command()
    async def hash(self, ctx, url=None):
        if url is None:
            await ctx.send("URLを指定してください")
            mes = await self.bot.wait_for("message",
                                          check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            url = mes.content
        await ctx.send(await self.do_hash(url))


bot = commands.Bot("kt!")
bot.remove_command("help")
bot.add_cog(Main(bot))
bot.run(os.environ["pokebot_token"])