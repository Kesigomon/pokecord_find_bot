import csv
import hashlib
import os
import re

from discord.ext import commands


class Main(commands.Cog):
    pattern1 = re.compile(r"^.*?/(\d*)/(\d*)$")
    with open("./db2.csv", encoding="utf-8") as f:
        data = dict(csv.reader(f))

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    async def do_hash(self, url):
        data = await self.bot.http.get_from_cdn(url)
        return hashlib.md5(data).hexdigest()

    @commands.Cog.listener()
    async def on_ready(self):
        print("ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != 365975655608745985 or not message.embeds:
            return
        print("pokecord!")
        embed = message.embeds[0]
        if embed.title == "A wild pok\u00e9mon has appeared!":
            key = await self.do_hash(embed.image.url)
            await message.channel.send(f"このポケモンの名前は{self.data[key]}です")

    @commands.command()
    async def stop(self, ctx):
        if await self.bot.is_owner(ctx.author):
            await ctx.send("停止")
            await self.bot.close()



bot = commands.Bot("kp!")
bot.remove_command("help")
bot.add_cog(Main(bot))
bot.run(os.environ["token_pokecord"])
