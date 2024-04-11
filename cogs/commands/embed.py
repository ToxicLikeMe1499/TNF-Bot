import mysql.connector
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from datetime import datetime

def get_time():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

class ScammView(nextcord.ui.View):
    def __init__(self, name: str, date: str, type: str, info: str, proof1: str, proof2: str, proof3: str):
        super().__init__(timeout=None)
        self.name = name
        self.date = date
        self.type = type
        self.info = info
        self.proof1 = proof1
        self.proof2 = proof2
        self.proof3 = proof3

    @nextcord.ui.button(
        label="Bestätigen",
        style=nextcord.ButtonStyle.green,
        custom_id="ScammView:green"
    )
    async def aprove_scammer(self, interaction: Interaction, button: nextcord.ui.Button):
        await interaction.message.delete()
        em = nextcord.Embed(title="Neuer Scammer", description="Es gibt nun einen neues scammer Alle infos hier")
        em.add_field(name="Name:", value=self.name, inline=False)
        em.add_field(name="Datum:", value=self.date, inline=False)
        em.add_field(name="Typ", value=self.type, inline=False)
        em.add_field(name="Beweiß", value=self.proo1)
        if not self.scamm_proof2 == None:
            em.add_field(name="Beweiß 2", value=self.scamm_proof2)
        else:
            pass
        if not self.proof3 == None:
            em.add_field(name="Beweiß 3", value=self.scamm_proof3)
        if not self.info == None:
            em.add_field(name="Infos", value=self.info)
        else:
            pass
        em.set_footer(text=f"Bestätigt von {interaction.user.mention}")
        await interaction.response.send_message(embed=em)
        
    @nextcord.ui.button(
        label="Ablehen",
        style=nextcord.ButtonStyle.red,
        custom_id="ScammView:red"
    )
    async def disaprove(self, interaction: Interaction, button: nextcord.ui.Button):
        await interaction.message.delete()

class ScamModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Scammer Report",
            timeout=900
        )
        self.scammer_name = nextcord.ui.TextInput(
            label="Wie heißt der scammer",
            min_length=3,
            max_length=17,
            required=True,
            placeholder=None
        )
        self.scamm_type = nextcord.ui.TextInput(
            label="Wie scammt er",
            required=True,
            placeholder="TPA falle"
        )
        self.scamm_date = nextcord.ui.TextInput(
            label="Wann ist es geschehen",
            min_length=16,
            max_length=18,
            required=True,
            placeholder=f"{get_time()}"
        )
        self.scamm_proof1 = nextcord.ui.TextInput(
            label="URL zu beweißen (Nur IMGBB)",
            required=False,
            placeholder="https://ibb.co/Pjxcz0b"
        )
        self.scamm_proof2 = nextcord.ui.TextInput(
            label="URL zu beweißen (Nur IMGBB)",
            required=False,
            placeholder="https://ibb.co/Pjxcz0b"
        )
        self.scamm_proof3 = nextcord.ui.TextInput(
            label="URL zu beweißen (Nur IMGBB)",
            required=False,
            placeholder="https://ibb.co/Pjxcz0b"
        )
        self.scamm_proof4 = nextcord.ui.TextInput(
            label="URL zu beweißen (Nur IMGBB)",
            required=False,
            placeholder="https://ibb.co/Pjxcz0b"
        )
        self.scamm_proof5 = nextcord.ui.TextInput(
            label="URL zu beweißen (Nur IMGBB)",
            required=False,
            placeholder="https://ibb.co/Pjxcz0b"
        )
        self.scamm_infos = nextcord.ui.TextInput(
            label="Weitere Infos",
            required=False
        )

        self.add_item(self.scammer_name)
        self.add_item(self.scamm_type)
        self.add_item(self.scamm_date)
        self.add_item(self.scamm_proof1)
        self.add_item(self.scamm_proof2)
        self.add_item(self.scamm_proof3)
        self.add_item(self.scamm_infos)
    
    async def callback(self, interaction: Interaction):
        channel = interaction.guild.get_channel(1227436524015194234)
        em = nextcord.Embed(title="Scammer Überprüfung", description=f"{Interaction.user.mention} hat {self.scammer_name} Reportet")
        em.add_field(name="Wann:", value=self.scamm_date)
        em.add_field(name="Was:", value=self.scamm_type)
        if not self.scamm_infos == None:
            em.add_field(name="Infos", value=self.scamm_infos)
        else:
            pass
        em.add_field(name="Beweiß", value=self.scamm_proof1)
        if not self.scamm_proof2 == None:
            em.add_field(name="Beweiß 2", value=self.scamm_proof2)
        else:
            pass
        if not self.scamm_proof3 == None:
            em.add_field(name="Beweiß 3", value=self.scamm_proof3)
        else:
            pass
        await channel.send(
            embed=em, 
            view=ScammView(
                name=self.scammer_name,
                date=self.scamm_date,
                type=self.scamm_type,
                info=self.scamm_infos,
                proof1=self.scamm_proof1,
                proof2=self.scamm_proof2,
                proof3=self.scamm_proof3
            )
        )

class view_bewerben1(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(
        label="Annehmen",
        style=nextcord.ButtonStyle.green,
        custom_id="view_bewerben1:green"
    )
    async def accept_apply(self, buuton: nextcord.ui.Button, interaction: Interaction):
        self.DB = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="Mama1978",
            database="tnf"
        )
        self.DB_Cursor = self.DB.cursor()
        sql = f"""UPDATE bewerbungen
        SET accepted = 1
        WHERE user_id = {int(interaction.message.content)};"""
        self.DB_Cursor.execute(sql)
        self.DB.commit()
        self.DB.close()
        user = interaction.message.guild.get_member(int(interaction.message.content))
        em = nextcord.Embed(
            title="Bewerbung wurde angenommen!",
            description=f"Diese bewerbung von {user.display_name} ({user.id}) wurde von {interaction.user.display_name} ({interaction.user.id} anngenommen)",
            color=0x00FF00
        )
        message = await interaction.message.edit("", embed=em, view=None)
        em = nextcord.Embed(
            title="Glückwunch zur Aufnahme in unseren Clan",
            description="Du wurdest Erfolgreich als Clan Mitglied aufgenommen. Hab viel spaß bei uns und wir freuen uns darauf dich zu haben.",
            color=nextcord.Color.green()
        )
        guild = message.guild
        role = guild.get_role(1188059178946793502)
        dm_channel = await user.create_dm()
        await dm_channel.send(embed=em)
        await user.add_roles(role)

    @nextcord.ui.button(
        label="Ablehnen",
        style=nextcord.ButtonStyle.red,
        custom_id="view_bewerben1:red"
    )
    async def deny_apply(self, buuton: nextcord.ui.Button, interaction: Interaction):
        self.DB = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="Mama1978",
            database="tnf"
        )
        self.DB_Cursor = self.DB.cursor()
        sql = f"""DELETE FROM bewerbungen
        WHERE user_id = {int(interaction.message.content)};"""
        self.DB_Cursor.execute(sql)
        self.DB.commit()
        self.DB.close()
        user = interaction.message.guild.get_member(int(interaction.message.content))
        em = nextcord.Embed(
            title="Bewerbung wurde abgelehnt!",
            description=f"Diese bewerbung von {user.display_name} ({user.id}) wurde von {interaction.user.display_name} ({interaction.user.id} abgelehnt)",
            color=0xFF0000
        )
        await interaction.message.edit("", embed=em, view=None)
        em = nextcord.Embed(
            title="Tut uns leid",
            description=f"{user.mention} du hast dich als TNF-Mitglied beworben und leider wurdest du nicht aufgenommen.\nViel Erfolg in deinen furtheren bewerbungen und versuche es bald wieder\nLG: Das TNF Team",
            color=nextcord.Color.red()
        )
        dm_channel = await user.create_dm()
        await dm_channel.send(embed=em)

class modal_bewerben(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Bewerben",
            timeout=300
        )
        self.minecraft = nextcord.ui.TextInput(
            label="Dein Minecraft name:",
            min_length=3,
            max_length=16,
            required=True,
            placeholder="notexture"
        )
        self.grund_beitreten = nextcord.ui.TextInput(
            label="Begründe warum du uns beitreten willst",
            min_length=30,
            max_length=480,
            required=True,
            placeholder=None
        )
        self.clans = nextcord.ui.TextInput(
            label="Warst du schon in einen clan? Welcher",
            min_length=1,
            max_length=5,
            required=False,
            placeholder="TNF"
        )
        self.grund_verlassen = nextcord.ui.TextInput(
            label="Grund für das Verlassen des vorherigen Clans",
            min_length=30,
            max_length=250,
            required=False,
            placeholder=None
        )
        self.alter = nextcord.ui.TextInput(
            label="Wie alt bist du",
            min_length=2,
            max_length=2,
            required=True,
            placeholder=None
        )
        self.add_item(self.minecraft)
        self.add_item(self.grund_beitreten)
        self.add_item(self.clans)
        self.add_item(self.grund_verlassen)
        self.add_item(self.alter)
    async def callback(self, interaction: Interaction):

        self.DB = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="Mama1978",
            database="tnf"
        )
        self.DB_Cursor = self.DB.cursor()

        sql = f"""INSERT INTO bewerbungen (
            user_name,
            user_id,
            minecraft,
            as_
        )
        VALUES (
            '{interaction.user.name}',
            {interaction.user.id},
            '{self.minecraft.value}',
            'Member'
        )"""

        self.DB_Cursor.execute(sql)
        self.DB.commit()
        self.DB.close()

        guild = interaction.guild
        channel = guild.get_channel(1222483894083911753)
        em = nextcord.Embed(
            title="Neue Bewerbung",
            colour=nextcord.Colour.yellow()
        )
        em.add_field(name="Minecraft Nutzername:", value=self.minecraft.value, inline=False)
        em.add_field(name="Grund zum beitreten von uns:", value=self.grund_beitreten.value, inline=False)
        em.add_field(name="Vorherige Clans:", value=self.clans.value, inline=False)
        em.add_field(name="Gründe des verlassen des vorherigen clans:", value=self.grund_verlassen.value, inline=False)
        em.add_field(name="Brot", value=self.alter.value, inline=False)
        await channel.send(interaction.user.id, embed=em, view=view_bewerben1())
        em = nextcord.Embed(
            title="Bewerbungsbestätigung",
            description="Deine Bewerbung wurde erfolgreich abgeschickt!\nWir werden dir in Kürze antworten.\nFalls du keine Antwort erhalten solltest melde dich bei uns im Support",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=em, ephemeral=True)

class view_bewerben(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(
        label="Bewerben",
        style=nextcord.ButtonStyle.green,
        custom_id="view_bewerben:green"
    )
    async def apply(self, button: nextcord.ui.Button, interaction: Interaction):
        self.DB = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="Mama1978",
            database="tnf"
        )
        self.DB_Cursor = self.DB.cursor()

        sql = f"""SELECT COUNT(*) FROM bewerbungen WHERE user_id = {interaction.user.id}"""
        self.DB_Cursor.execute(sql)
        count = self.DB_Cursor.fetchone()[0]
        self.DB.close()
        if count > 0:
            em = nextcord.Embed(
                title="Fehler",
                description="Du bist bereits member oder hast dich bereits beworben!",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=em, ephemeral=True)
        else:
            await interaction.response.send_modal(modal_bewerben())

class view_regeln(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(
        label="Akzeptieren",
        style=nextcord.ButtonStyle.green,
        custom_id="view_regeln1:green"
    )
    async def accept(self, button: nextcord.ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(1216027917331726446)
        await interaction.user.add_roles(role)
        em = nextcord.Embed(title="Erfolgreich", description=f"Du hast die rolle {role.mention} bekommen")
        await interaction.response.send_message(embed=em, ephemeral=True)
    
    @nextcord.ui.button(
        label="Ablehnen",
        style=nextcord.ButtonStyle.red,
        custom_id="view_regeln1:red"
    )
    async def decline(self, button: nextcord.ui.Button, interaction: Interaction):
        em = nextcord.Embed(title="Fehler", description="Du musst die Regeln annehmen sonst haua von chef :)", color=nextcord.Color.red())
        await interaction.response.send_message(embed=em, ephemeral=True)
        
class embeds_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(view_regeln())
        self.bot.add_view(view_bewerben())
        self.bot.add_view(view_bewerben1())
    
    @nextcord.slash_command(
        name="send_embed",
        description="Sendet ein Embed deiner wahl",
        guild_ids=[1180167998342975578],
        default_member_permissions=nextcord.Permissions(manage_messages=True)
    )
    async def send_embed(
        self,
        interaction: Interaction,
        option: str = nextcord.SlashOption(
            name="embed",
            description="Welches Embed soll gesendet werden?",
            required=True,
            choices=["regeln", "faq", "support", "request_rolle", "hilfe", "bewerben", "ränge", "scamm"]
        )
    ):
        if option == "scamm":
            await interaction.response.send_modal(ScamModal())    
        if option == "regeln":
            role = interaction.guild.get_role(1216019611615756368)
            em = nextcord.Embed(title="Discord Regeln - Teil 1", color=0xff4500)
            em.add_field(name="§1", value="Du musst 13 Jahre oder älter sein, um in unserem Clan zu sein. Dies ist eine Regel der ToS von Discord. Wenn du gegen diese Regel verstößt, wirst du dauerhaft gebannt.", inline=False)
            em.add_field(name="§2", value="Ein freundlicher und respektvoller Umgang mit User und Team ist Pflicht.", inline=False)
            em.add_field(name="§3", value="NSFW-Inhalte wie Pornographie ist bei uns verboten.", inline=False)
            em.add_field(name="§4", value="Soundboards oder Störgeräusche in einem VC sind verboten.", inline=False)
            em.add_field(name="§5", value="Werbung in DM und auf Server ist verboten und wird mit einem Ban bestraft.", inline=False)
            em.add_field(name="§6", value="Das Befolgen der [Discord-Nutzungsbedingungen (ToS)](https://discord.com/terms) und den [Community-Richtlinien (Guidelines)](https://discord.com/guidelines) ist Pflicht.", inline=False)
            em.add_field(name="§7", value="Wenn du in einem Sprachchannel Audio oder Screen aufnimmst, muss jeder im Raum damit einverstanden sein.", inline=False)
            em.add_field(name="§8", value="Rassistische und Nazistische Inhalte sind verboten.", inline=False)
            em.add_field(name="§9", value="Spamming ist verboten und wird mit einem Timeout bestraft.", inline=False)
            em.add_field(name="§10", value="Allgemein gilt, das Team hat Recht bei anweißungen ist diesem Folge zu leisten.", inline=False)
            em.add_field(name="§11", value="Identitätsdiebstahl ist verboten.", inline=False)
            em.add_field(name="§12", value="Reflinks sind verboten.", inline=False)
            em.add_field(name="§13", value=f"Es ist verboten alles über {role.mention} ohne Grund zu pingen.", inline=False)
            em.add_field(name="§14", value="Die Regel 7 trit auser Kraft, wenn man Beiweiße aufnimmt")
            em.set_author(name="TNF | Texture Not Found", url="https://cdn.discordapp.com/icons/1180167998342975578/0611d014991421a101fd306b30ae8866.png?size=1024")
            await interaction.response.send_message(embed=em, view=view_regeln())

        elif option == "ränge":

            owner_role = interaction.guild.get_role(1215970973111816322)
            kbfo_owner_role = interaction.guild.get_role(1188057072013680670)
            velo_owner_role = interaction.guild.get_role(1188057885998071830)
            role1 = interaction.guild.get_role(1215962841857786006)
            color01 = interaction.guild.get_role(1216001149543383041)
            color02 = interaction.guild.get_role(1216001151384813668)
            color03 = interaction.guild.get_role(1216001154127761408)
            color04 = interaction.guild.get_role(1216000031581278289)
            color05 = interaction.guild.get_role(1216000026317164646)
            color06 = interaction.guild.get_role(1216000031639994470)
            color07 = interaction.guild.get_role(1216000029224075274)
            color08 = interaction.guild.get_role(1216000027068071986)
            color09 = interaction.guild.get_role(1216000017219850370)
            color10 = interaction.guild.get_role(1216000029001515189)
            color11 = interaction.guild.get_role(1216000026371948575)
            color12 = interaction.guild.get_role(1216001147286851744)
            color13 = interaction.guild.get_role(1216001142010417292)
            color14 = interaction.guild.get_role(1215971199079682081)
            color15 = interaction.guild.get_role(1216000031581274264)
            color16 = interaction.guild.get_role(1216000029102309446)
            role2 = interaction.guild.get_role(1216000032357089341)
            admin_role = interaction.guild.get_role(1216000032357089341)
            mod_role = interaction.guild.get_role(1215964495630045274)
            event_role = interaction.guild.get_role(1215964061028712448)
            role3 = interaction.guild.get_role(1215965061378740275)
            desing_role = interaction.guild.get_role(1215931764359303189)
            dev_role = interaction.guild.get_role(1215998762301001799)
            role4 = interaction.guild.get_role(1215998762301001799)
            team_role = interaction.guild.get_role(1216019611615756368)
            bot_role = interaction.guild.get_role(1216020058275319858)
            role5 = interaction.guild.get_role(1188058692868911184)
            member_role = interaction.guild.get_role(1188059178946793502)
            guest_role = interaction.guild.get_role(1216027917331726446)


            em0 = nextcord.Embed(title="Unsere Ränge Teil 1/2", description=f"Hier hast du eine kleine übersicht über all unsere Ränge.", color=nextcord.Color.blurple())
            em1 = nextcord.Embed(title="Unsere Ränge Teil 2/2", color=nextcord.Color.blurple())
            em0.add_field(name=f"{owner_role.name}", value="Das ist der Owner des TNF clans", inline=False)
            em0.add_field(name=f"{kbfo_owner_role.name}", value="Der Owner von unserem Partner KBFO", inline=False)
            em0.add_field(name=f"{velo_owner_role.name}", value="Der Owner von unserem Partner Velo", inline=False)
            em0.add_field(name=f"{role1.name}", value="Eine Trennung die zur besseren übersich beiträgt", inline=False)
            em0.add_field(name=f"{color01.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color02.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color03.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color04.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color05.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color06.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color07.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color08.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color09.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color10.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color11.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em0.add_field(name=f"{color12.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em1.add_field(name=f"{color13.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em1.add_field(name=f"{color14.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em1.add_field(name=f"{color15.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em1.add_field(name=f"{color16.name}", value="Eine Custom-Role-Farbe Die bald kommen wird", inline=False)
            em1.add_field(name=f"{role2.name}", value="Eine Trennung die zur besseren übersich beiträgt", inline=False)
            em1.add_field(name=f"{admin_role.name}", value="Das sind die Adminstratoren", inline=False)
            em1.add_field(name=f"{mod_role.name}", value="Das sind die Offiziellen Moderatoren", inline=False)
            em1.add_field(name=f"{event_role.name}", value="Das sind die Event Manager", inline=False)
            em1.add_field(name=f"{role3.name}", value="Eine Trennung die zur besseren übersich beiträgt", inline=False)
            em1.add_field(name=f"{desing_role.name}", value="Das sind Die Desinger Diese machen das gute Desing", inline=False)
            em1.add_field(name=f"{dev_role.name}", value="Das sind Die Developer Zuständig für die bots und so", inline=False)
            em1.add_field(name=f"{role4.name}", value="Eine Trennung die zur besseren übersich beiträgt", inline=False)
            em1.add_field(name=f"{team_role.name}", value="Das ist die Untergruppe für Teamler", inline=False)
            em1.add_field(name=f"{bot_role.name}", value="Das sind die Custom-Made-Bots von den Developern", inline=False)
            em1.add_field(name=f"{role5.name}", value="Eine Trennung die zur besseren übersich beiträgt", inline=False)
            em1.add_field(name=f"{member_role.name}", value="Das sind unsere Großartigen Member", inline=False)
            em1.add_field(name=f"{guest_role.name}", value="Das sind die Gäste, noch ;)", inline=False)

            await interaction.response.send_message(embeds=[em0, em1])

        elif option == "bewerben":
            bewerbungschannel = interaction.guild.get_channel(1215940774278070282)
            em = nextcord.Embed(
                title="Bewerben",
                description="""Wenn du dich bei uns Bewerben möchtest bist du hier ganz richtig.
                Denn der TextureNotFound Clan sucht genau dich""",
                color=0x00FFFF
            )
            await interaction.response.send_message(embed=em, view=view_bewerben())
        else:
            pass

def setup(bot):
    bot.add_cog(embeds_command(bot))