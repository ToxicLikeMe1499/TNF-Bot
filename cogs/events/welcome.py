import nextcord
from nextcord.ext import commands

class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        ch_welcome = self.bot.get_channel(1215938555314966528)
        em = nextcord.Embed(
            title=f"Willkommen im TNF Clan {member.mention}",
            description="""Wir sind ein Clan der, für deine sicherheit vor scammern eine hilfe ist.
Lies dir bitte zuerst unsere Regeld durch <#1215938810827903057>
DU wilst dich dirket bei uns bewerben, dann mache es dort <#1215940774278070282>

Fühl dich bei uns wohl und habe hoffentlich eine tolle zeit bei uns Dein TNF Team!""",
            color=0x5865F2,
            )
        em.set_footer(text="Der TNF | Der Clan der NIE zu sehen ist")
        em.set_author(
            name="TNF | Texture Not Found???",
            icon_url="https://cdn.discordapp.com/icons/1180167998342975578/0611d014991421a101fd306b30ae8866.png?size=1024"
            )
        await ch_welcome.send(embed=em)

def setup(bot):
    bot.add_cog(welcome(bot))