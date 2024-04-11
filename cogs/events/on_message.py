import nextcord
from datetime import datetime
from assets.config import F, S
from nextcord.ext import commands

def get_time():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"{F.y}{S.D}[{dt_string}]{F.R_ALL} "


class message_loger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg_author = None
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        elif message.content.startswith("!"):
            await self.bot.process_commands(message)
            command = message.content.split("!")
            print(get_time() + F.W + S.D + message.author.display_name + F.R_ALL + " nutzte " + command[1])
        else:
            if message.author == self.msg_author:
                print(get_time() + F.W + S.D + message.author.display_name + ": " + F.R_ALL + message.content)
            else:
                print(" ")
                print(get_time() + F.W + S.D + message.author.display_name + ": " + F.R_ALL + message.content)
                self.msg_author = message.author

def setup(bot):
    bot.add_cog(message_loger(bot))