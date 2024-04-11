import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext import application_checks
from datetime import datetime

def get_time():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

class scammer_view1(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(
        label="Scammer Reporten",
        style=nextcord.ButtonStyle.blurple,
        custom_id="scammer_view1:report"
    )
    async def report(self, interaction: Interaction, button: nextcord.ui.Button):
        await interaction.response.send_modal(ScamModal())

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
            view=scammer_view2(
                name=self.scammer_name,
                date=self.scamm_date,
                type=self.scamm_type,
                info=self.scamm_infos,
                proof1=self.scamm_proof1,
                proof2=self.scamm_proof2,
                proof3=self.scamm_proof3
            )
        )

class scammer_view2(nextcord.ui.View):
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

class apply_main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.bot.add_view(scammer_view1())
        self.bot.add_view(scammer_view2(name=None, date=None, type=None, info=None, proof1=None, proof2=None, proof3=None))
    
    @nextcord.slash_command(name="embed", description="Managed ein Embed (keinen nutzen)", default_member_permissions=nextcord.Permissions(manage_messages=True))
    async def embed(self):
        return

    @embed.subcommand(name="senden", description="Sendet ein Embed")
    @application_checks.has_permissions(manage_messages=True)
    async def send(
        self, 
        interaction: Interaction, 
        option: str = nextcord.SlashOption(
            name="embed",
            description="Welches Embed soll gesendet werden?",
            required=True,
            choices=["regeln", "support", "reaction_rollen", "bewerben", "ränge", "scamm"]
        )
    ):
        if option == "scamm":
            em = nextcord.Embed(title="Scammer Report", description='Du willst einen scammer reporten?\nDann bist du heir Genau richtig!\nDrücke einfach unten auf "Scammer Reporten" und fülle das formular aus. \nWir leiten das an unser Team weiter zur überprüfung', color=nextcord.Color.blurple())
            em.set_footer(text="LG das TextureNotFound Team", icon_url=interaction.guild.icon)
            message = await interaction.response.send_message(embed=em, view=scammer_view1())
            await message.pin()
    
def setup(bot):
    bot.add_cog(apply_main(bot))