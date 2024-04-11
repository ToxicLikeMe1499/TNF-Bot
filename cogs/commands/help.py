import nextcord
import time
from nextcord.ext import commands
from nextcord import Interaction

class HelpMenuView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.select(placeholder="Wähle eine Option aus", min_values=1, max_values=1, options=[
        nextcord.SelectOption(label="Allgemeines", description="Die Allgemeinen Commands"),
        nextcord.SelectOption(label="Abbrechen", description="Bricht den Vorgang ab")
    ])
    async def select_callback(self, select: nextcord.ui.Select, interaction: Interaction):
        selected_label = select.values[0]

        if selected_label == "Allgemeines":
            em = nextcord.Embed(
                title="Hilfe Menu - Allgemeines",
                color=0x3498db,
                description="""
!help            | Zeigt dieses Menu
!ping            | Gibt den aktuellen Ping wieder
"""
            )
            await interaction.response.edit_message(embed=em, view=HelpMenuView())
        elif selected_label == "Abbrechen":
            await interaction.response.edit_message("Hilfe Menü abgebrochen.")
            self.stop()  # Löscht das Menü nach dem Anzeigen der Informationen

class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        em = nextcord.Embed(
            title="Hilfe Menu",
            color=0x3498db,
            description="""
Willkommen im Hilfe Menu von `Emergency Hamburg Trade Bank`.
Du kannst hier alle Commands finden, die wir zu bieten haben.
Wähle einfach im unteren Feld eine Kategorie aus, und es zeigt dir alle passenden Commands dazu an.

***Die Kategorien***:
-  Allgemeines     | Zeigt alle allgemeinen Commands an.
-  Abrechen        | Schließt das Interaktions Menu.

Wir wünschen dir noch viel Spaß, das EHTB Team.
"""
        )
        view = HelpMenuView()
        await ctx.send(embed=em, view=view)
        await ctx.message.delete()
    
    @nextcord.slash_command(name="help", description="Ruft das Hilfe Menu auf", guild_ids=["1196248369421615197"])
    async def s_help(self, interaction: Interaction):
        em = nextcord.Embed(
            title="Hilfe Menu",
            color=0x3498db,
            description="""
Willkommen im Hilfe Menu von `Emergency Hamburg Trade Bank`.
Du kannst hier alle Commands finden, die wir zu bieten haben.
Wähle einfach im unteren Feld eine Kategorie aus, und es zeigt dir alle passenden Commands dazu an.

***Die Kategorien***:
-  Allgemeines     | Zeigt alle allgemeinen Commands an.
-  Abrechen        | Schließt das Interaktions Menu.

Wir wünschen dir noch viel Spaß, das EHTB Team.
"""
        )
        view = HelpMenuView()
        await interaction.response.send_message(embed=em, view=view)
        await interaction.message.delete()

def setup(bot):
    bot.add_cog(HelpMenu(bot))
