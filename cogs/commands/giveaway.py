import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.ext import application_checks
from nextcord.abc import GuildChannel
from nextcord import Interaction
from nextcord import ChannelType
from nextcord import SlashOption
import asyncio
import humanfriendly
import time as pytime
import json
import random
import mysql.connector

class JoinGiveaway(nextcord.ui.View):
    def __init__(self, time, name, guild, epochEnd, bot):
        super().__init__(timeout=None)
        self.name = name
        self.guild = guild
        self.time = epochEnd
        self.bot = bot
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)
    
    @nextcord.ui.button(label="Beitreten", style=nextcord.ButtonStyle.blurple, custom_id="join")
    async def Join(self, button: nextcord.ui.Button, interaction: Interaction):
        self.DB = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="Mama1978",
            database="tnf"
        )
        self.DB_Cursor = self.DB.cursor()
        self.DB_Cursor.execute("SELECT participants FROM giveaways WHERE guild = %s AND prize = %s AND time = %s"), (self.guild, self.name, self.time) 
        data = await self.DB_Cursor.fetchone()
        if data:
            participants = data[0]
            try:
                participants = json.loads(participants)
            except:
                participants = []
            if interaction.user.id in participants:
                em = nextcord.Embed(title="Fehler", description="Du bist diesem Giveaway bereits beigetreten", color=0xFF0000)
                return await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                participants.append(interaction.user.id)
            await self.DB_Cursor.execute(f"UPDATE giveaways SET participants = {json.dumps(participants)} WHERE guild = {self.guild} AND prize = {self.name} AND time = {self.time}")
            em = nextcord.Embed(title="Erfolgreich", description="Gratulation!\nDu bist diesem giveaway erfolgreich beigetreten", color=0x00FF00)
            await interaction.response.send_message(embed=em, ephemeral=True)
        else:
            em = nextcord.Embed(title="Fehler", description="Hallo, Ich bin ein fehler.\n Bitte reporte mich im Support.\nDie netten leute dort werden es an die Entwikler weiterleiten\n`ErrorCode:367`", color=0xFFFF00)
            await interaction.response.send_message(embed=em, ephemeral=True)
        self.DB.commit()
        self.DB.close()
    
class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(seconds=5)
    async def giveawayCheck(self):
        self.DB = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="Mama1978",
            database="tnf"
        )
        self.DB_Cursor = self.DB.cursor()
        self.DB_Cursor.execute("SELECT time, prize, message, channel, guild, participants, winners, finished FROM giveaways")
        data = self.DB_Cursor.fetchall()
        if data:
            for table in data:
                time, prize, message, channel, guild, participants, winners, finished = table[0], table[1], table[2], table[3], table[4], table[5], table[6], table[7]
                if not finished:
                    if pytime.time() >= time:
                        guild = self.bot.get_guild(guild)
                        channel = guild.get_channel(channel)
                        if guild or channel is not None:
                            try:
                                participants = json.load(table[5])
                            except:
                                participants = []
                            if not len (participants) == 0:
                                if len(participants) < winners:
                                    winner = random.choices(participants, k=len(participants))
                                else:
                                    winner = random.choices(participants, k=winners)
                                winners= []
                                for user in winner:
                                    winners.append(guild.get_member(int(user)).name)
                                if winner is not None:
                                    self.DB_Cursor.execute(f"UPDATE giveaways SET finished = {True} WHERE guild = {guild.id} AND prize = {prize} AND message = {message}")
                                    msg = await channel.fetch_message(message)
                                    newEM = nextcord.Embed(title=":tada: Giveaway Ende! :tada:", description=f"`{', '.join(winners)}` hat `{prize}` gewonnen! \n:tada: Glückwunch :tada:", color=nextcord.Color.blurple())
                                    newEM.set_footer(text=f"Teilnehmer: {len(participants)}")
                                    await msg.edit(embed=newEM)
                            else:
                                self.DB_Cursor.execute(f"UPDATE giveaways SET finished = {True} WHERE guild = {guild.id} AND prize = {prize} AND message = {message}")
                                msg = channel.fetch_message(message)
                                newEM = nextcord.Embed(title="Giveaway Ende!", description=f"Es hat gewonnen warte mal... \nEs gibt keinen Gewinner???\nAber wie :texture_verwirrt:\nWarte es gab je keine Teilnehmer :texture_traurig: \nDas ist traurig", color=nextcord.Color.blurple())
                                newEM.set_footer(text=f"Gewinn: {prize}")
                                await msg.edit(embed=newEM)
        self.DB.commit()
        self.DB.close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(2)
        self.DB = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="Mama1978",
            database="tnf"
        )
        self.DB_Cursor = self.DB.cursor()
        self.DB_Cursor.execute("CREATE TABLE IF NOT EXISTS giveaways (time INTEGER, prize TEXT, message BIGINT, channel BIGINT, guild BIGINT, participants TEXT, winners INTEGER, finished BOOL)")
        self.DB.commit()
        self.DB.close()
        self.giveawayCheck.start()

    @nextcord.slash_command(name="giveaway", description="Giveaway Command", guild_ids=[1180167998342975578])
    async def giveaway(self, interaction: Interaction):
        return
    
    @giveaway.subcommand(name="start", description="Startet ein giveaway")
    @application_checks.bot_has_permissions(start_embedded_activities=True)
    async def start(
        self,
        interaction: Interaction,
        prize: str = SlashOption(
            name="preis",
            description="Der Gewinn",
            required=True
        ),
        channel: GuildChannel = SlashOption(
            name="kanal",
            channel_types=[ChannelType.text],
            description="In welchem Kanal soll das Giveaway sein",
            required=True
        ),
        time: str = SlashOption(
            name="dauer",
            description="Die Länge wie lang soll das giveaway gehen z.B. 2d (2 Tage), 6h (6 Stunden), 30min (30 Minuten)",
            required=True
        ),
        winners: int = SlashOption(
            name="gewinner",
            description="Die anzahl der gewinner (Standart 1)",
            required=False
        )
    ):
        time = humanfriendly.parse_timespan(time)
        epochEnd = pytime.time() + time
        disc_dt = str(epochEnd).split(".")
        disc_dt = f"<t:{disc_dt[0]}:R>"
        print(epochEnd)
        self.DB = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="Mama1978",
            database="tnf"
        )
        self.DB_Cursor = self.DB.cursor()
        if winners == None:
            winners = 1
        else:
            pass
        self.DB_Cursor.execute('INSERT INTO giveaways (time, prize, message, channel, guild, participants, winners, finished) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (epochEnd, prize, 24, f"{channel.id}", interaction.guild.id, "", winners, False))
        em = nextcord.Embed(title=":tada: Neues Giveaway :tada:", description=f"Ein neues Giveaway findet gerade stadt. \nEs gibt zu gewinnen {prize} \nEs geht bis {disc_dt} und es wird {winners} gewinner geben\n View Glück")
        await interaction.response.send_message(f"Giveaway wurde in {channel.mention} gestartet!", delete_after=10, ephemeral=True)
        view = JoinGiveaway(time, prize, interaction.guild.id, epochEnd, self.bot)
        msg = await channel.send(embed=em, view=view)
        view.message = msg
        await asyncio.sleep(2)
        self.DB_Cursor.execute("UPDATE giveaways SET message = %s WHERE guild = %s AND prize = %s AND time = %s", (msg.id, interaction.guild.id, prize, epochEnd))
        self.DB.commit()
        self.DB.close()

    @giveaway.subcommand(name="reroll", description="Wählt einen neuen gewinner")
    @application_checks.has_permissions(start_embedded_activities=True)
    async def reroll(
        self,
        interaction: Interaction,
        messageid: str = SlashOption(
            name="nachricht_id",
            description="Die nachricht id des Giveaways",
            required=True
        )
    ):
        try:
            message = int(messageid)
        except ValueError:
            em = nextcord.Embed(title="Fehler", description="Du hast keine Gültige Message ID angegeben", color=0xFF0000)
            return interaction.response.send_message(embed=em, ephemeral=True)
        self.DB = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="Mama1978",
            database="tnf"
        )
        self.DB_Cursor = self.DB.cursor()
        self.DB_Cursor.execute(f"SELECT participants, channel, prize, winners FROM giveaways WHERE message = {message} AND finished = {True}")
        data = self.DB_Cursor.fetchone()
        self.DB.close()
        if data:
            try:
                particiants = json.loads(data[0])
            except:
                particiants = []
            if len(particiants) == 0:
                em = nextcord.Embed(title="Fehler", description="Das Giveaway kann nicht neu ausgelost werden, da es keinen gab der ihm beigetreten ist!", color=0xFF0000)
                return await interaction.response.send_message(embed=em, ephemeral=True)
            if not len(particiants) == 0:
                if len(particiants) < data[3]:
                    winner = random.choices(particiants, k=len(particiants))
                else:
                    winner = random.choices(particiants, k=data[3])
                winners = []
                for user in winner:
                    winners.appand(interaction.guild.get_member(int(user)).name)
            channel = interaction.guild.get_channel(data[1])
            if winners and channel is not None:
                msg = await channel.fetch_message(data[0])
                em = nextcord.Embed(title=":tada: Giveaway Ende (reroll) :tada:", description=f"`{', '.join(winners)}` hat `{data[2]}` gewonnen! \n:tada: Glückwunch :tada:", color=nextcord.Color.blurple())
                em.set_footer(text=f"Teilnehmer: {len(particiants)} Reroll von:{interaction.user.name}")
                await msg.edit(embed=em)
            else:
                em = nextcord.Embed(title="Fehler", description="Kann kein Reroll durchführen, da der gewinner oder die nachricht nicht gefunden wurde!", color=0xFF0000)
                return await interaction.response.send_message(embed=em, ephemeral=True)
        else:
            em = nextcord.Embed(title="Fehler", description="Kann kein Reroll durchführen, da dieses Giveaway nicht existiert", color=0xFF0000)
            return await interaction.response.send_message(embed=em, ephemeral=True)

def setup(bot):
    bot.add_cog(Giveaway(bot))