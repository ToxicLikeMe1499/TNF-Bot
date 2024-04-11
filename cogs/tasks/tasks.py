from datetime import datetime
import os
import subprocess
import asyncio
import random
import mysql.connector
import nextcord
from assets.config import F, S
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext import tasks

def get_time():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

class ss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.o_staff.start()
        self.member.start()
        self.status.start()
        self.o_staff_active = True
        self.member_active = True
        self.status_active = True

    @nextcord.slash_command(
        name="start_task",
        description="Startet eine Task",
        default_member_permissions=nextcord.Permissions(manage_channels=True),
        guild_ids=[1180167998342975578]
    )
    async def start_task(
        self,
        interaction: Interaction,
        option: str = nextcord.SlashOption(
            name="task",
            description="Welche Task soll gestartet werden?",
            required=True,
            choices=["Online Teamler Zähler", "Member Zähler", "Status"]
        )
    ):
        if option == "Online Teamler Zähler":
            if self.o_staff_active == True:
                em = nextcord.Embed(title="Fehler", description="Der Online Teamler Counter ist bereits Aktiviert", color=0xFF0000)
                await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                self.o_staff.start()
                self.o_staff_active = True
                em = nextcord.Embed(title="Erfolgreich", description="Der Online Tramler Counter ist nun Aktiviert", color=0x00FF00)
                await interaction.response.send_message(embed=em, ephemeral=True)
        elif option == "Member Zähler":
            if self.member_active == True:
                em = nextcord.Embed(title="Fehler", description="Der Member Counter ist bereits Aktiviert", color=0xFF0000)
                await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                self.member.start()
                self.member_active = True
                em = nextcord.Embed(title="Erfolgreich", description="Der Member Counter ist nun Aktiviert", color=0x00FF00)
                await interaction.response.send_message(embed=em, ephemeral=True)
        elif option == "Status":
            if self.status_active == True:
                em = nextcord.Embed(title="Fehler", description="Der Status ist bereits Aktiviert", color=0xFF0000)
                await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                self.status.start()
                self.status_active = True
                em = nextcord.Embed(title="Erfolgreich", description="Der Status ist nun Aktiviert", color=0x00FF00)
                await interaction.response.send_message(embed=em, ephemeral=True)
        else:
            return


    @nextcord.slash_command(
        name="stop_task",
        description="Stopt eine Task",
        default_member_permissions=nextcord.Permissions(manage_channels=True),
        guild_ids=[1180167998342975578]
    )
    async def stop_task(
        self,
        interaction: Interaction,
        option: str = nextcord.SlashOption(
            name="task",
            description="Welche Task soll gestopt werden?",
            required=True,
            choices=["Online Teamler Zähler", "Member Zähler", "Status"]
        )
    ):
        if option == "Online Teamler Zähler":
            if self.o_staff_active == False:
                em = nextcord.Embed(title="Fehler", description="Der Online Teamler Counter ist bereits Deaktiviert", color=0xFF0000)
                await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                self.o_staff.cancel()
                self.o_staff.stop()
                self.o_staff_active = False
                em = nextcord.Embed(title="Erfolgreich", description="Der Online Teamler Counter ist nun Deaktiviert", color=0x00FF00)
                await interaction.response.send_message(embed=em, ephemeral=True)
        elif option == "Member Zähler":
            if self.member_active == False:
                em = nextcord.Embed(title="Fehler", description="Der Member Counter ist bereits Deaktiviert", color=0xFF0000)
                await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                self.member.cancel()
                self.member.stop()
                self.member_active = False
                em = nextcord.Embed(title="Erfolgreich", description="Der Member Counter ist nun Deaktiviert", color=0x00FF00)
                await interaction.response.send_message(embed=em, ephemeral=True)
        elif option == "Status":
            if self.status_active == False:
                em = nextcord.Embed(title="Fehler", description="Der Status ist bereits Deaktiviert", color=0xFF0000)
                await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                self.status.cancel()
                self.status.stop()
                self.status_active = False
                await self.bot.change_presence(activity=None)
                em = nextcord.Embed(title="Erfolgreich", description="Der Status ist nun Deaktiviert", color=0x00FF00)
                await interaction.response.send_message(embed=em, ephemeral=True)
        else:
            return
    
    @tasks.loop(minutes=5, reconnect=False)
    async def o_staff(self):
        await self.bot.wait_until_ready()
        o_staff_count = 0
        channel = self.bot.get_channel(1216095163647131729)
        guild = self.bot.get_guild(1180167998342975578)
        role = guild.get_role(1216019611615756368)
        for member in role.members:
            if member.status == nextcord.Status.online:
                o_staff_count += 1
            elif member.status != nextcord.Status.online:
                pass
        await channel.edit(name=f"🔰・Online Staff | {o_staff_count}")
    
    @tasks.loop(minutes=5, reconnect=False)
    async def member(self):
        await self.bot.wait_until_ready()
        mem_count = 0
        channel = self.bot.get_channel(1216096624216899704)
        guild = self.bot.get_guild(1180167998342975578)
        role = guild.get_role(1188059178946793502)
        for i in role.members:
            mem_count += 1
        await channel.edit(name=f"🍿・Clan Member | {mem_count}")

    @tasks.loop(minutes=5)
    async def status(self):
        await self.bot.wait_until_ready()
        states = ["p|minevale.de - TNF|https://www.minevale.de", "w|Texture Not Found"]
        state = random.choice(states)
        if state.startswith("p|"):
            state = state.split("|")
            activity = nextcord.Activity(
                type=nextcord.ActivityType.playing,
                name=state[1],
                url=state[2]
            )
            await self.bot.change_presence(activity=activity)
            os.system(f"title {state[1]} ‖ {state[2]}")

        elif state.startswith("w|"):
            state = state.split("|")
            activity = nextcord.Activity(
                type=nextcord.ActivityType.watching,
                name=state[1]
            )
            await self.bot.change_presence(activity=activity)
            os.system(f"title {state[1]}")

def setup(bot):
    bot.add_cog(ss(bot))