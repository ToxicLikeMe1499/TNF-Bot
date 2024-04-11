import argparse
from datetime import datetime
import os
import signal
import time
import colorama
import subprocess
import mysql.connector
import nextcord
from nextcord.ext import commands
import readchar

from assets.config import F, S, environ, logo

def end_state(DB):
    DB.close()

def get_time():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

def loading_animation():
    print("Loading MySQL [", end="", flush=True)
    for _ in range(35):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print("                    ]", end="\r", flush=True)  # Clear the dots
    print(" " * 25, end="\r", flush=True)
    print(F.y + S.D + "[" + get_time() + "] " + F.g + S.B + "[SUCCESSFULLY]" + F.R_ALL + " MySQL Verbunden")

os.system("title " + "Starting Bot")
os.system("cls")
print("--------------------------------------------------------------------------------------------------------------")
print(F.b + S.D + logo.logo + F.R_ALL)
print("--------------------------------------------------------------------------------------------------------------")
print(" ")
print(F.y + S.D + "[" + get_time() + "] " + S.N + "[INFO]" + F.R + " Nextcord verison:")
print(F.y + S.D + "[" + get_time() + "] " + F.R_ALL + "       " + nextcord.__version__)
print(" ")
print(F.y + S.D + "[" + get_time() + "] " + S.N + "[INFO]" + F.R + " Colorama version:")
print(F.y + S.D + "[" + get_time() + "] " + F.R_ALL + "       " + colorama.__version__)
print(" ")
print(F.y + S.D + "[" + get_time() + "] " + S.N + "[INFO]" + F.R + " MySQL version:")
print(F.y + S.D + "[" + get_time() + "] " + F.R_ALL + "       " + mysql.connector.__version__)
print(" ")
print("--------------------------------------------------------------------------------------------------------------")

parser = argparse.ArgumentParser(description="Script with custom -t and -s options.")
parser.add_argument("-t", "--alternate_action", action="store_true", help="Run without tasks.")
parser.add_argument("-s", "--alternate_server", action="store_true", help="Run as server.")
args = parser.parse_args()

intents = nextcord.Intents.all()
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
bot.remove_command("help")

cogs_c = "cogs.commands"
cogs_e = "cogs.events"
cogs_t = "cogs.tasks"
cogs_o = "cogs.other"

cogs_1 = [
    f"{cogs_c}.bewerbungen",
    f"{cogs_c}.giveaway",
    f"{cogs_c}.ping",
    f"{cogs_c}.embed",
    f"{cogs_e}.on_message",
    f"{cogs_e}.on_error",
    f"{cogs_e}.welcome",
    f"{cogs_t}.tasks"
]

cogs = []

if args.alternate_action:
    for cog in cogs_1:
        if not cog.startswith(f"{cogs_t}."):
            cogs.append(cog)
else:
    cogs = cogs_1

print(" ")
print(F.y + S.D + "[" + get_time() + "] " + S.N + "[INFO]" + F.R + " Laden von Cogs . . .")
for cog in cogs:
    if cog.startswith("cogs.commands.embeds"):
        try:
            bot.load_extension(cog)
        except Exception as e:
            cog=cog.split(".")
            print(F.y + S.D + "[" + get_time() + "] " + S.N + F.r + "       [ERROR]" + F.R + " Konnte den Cog " + cog[3] + " nicht laden: " + str(e) + "!")
        else:
            cog = cog.split(".")
            print(F.y + S.D + "[" + get_time() + "] " + S.B + F.g + "       [SUCCESSFULY]" + F.R_ALL + " Embed " + cog[3] + " wurde geladen.")

    elif any(cog.startswith(i) for i in [cogs_c, cogs_e, cogs_t, cogs_o]):
        try:
            bot.load_extension(cog)
        except Exception as e:
            cog=cog.split(".")
            print(F.y + S.D + "[" + get_time() + "] " + S.N + F.r + "       [ERROR]" + F.R + " Konnte den Cog " + cog[2] + " nicht laden: " + str(e) + "!")
        else:
            cog = cog.split(".")
            print(F.y + S.D + "[" + get_time() + "] " + F.g + S.B + "       [SUCCESSFULY]" + F.R_ALL + " Cog " + cog[2] + " wurde geladen.")
    else:
        print(F.y + S.D + "[" + get_time() + "] " + S.N + F.r + "       [ERROR]" + F.R + cog + " ist eine unbekannte Datei")

print(" ")
print("--------------------------------------------------------------------------------------------------------------")

def handler(signum, frame):
    msg = "\nCtrl-c was pressed. Do you really want to exit? y/n "
    print(msg, end="", flush=True)
    res = readchar.readchar()
    if res == 'y':
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True) # clear the printed line
        print("    ", end="\r", flush=True)
        print("--------------------------------------------------------------------------------------------------------------")
        print(" ")
        print(" ")
        print(F.y + S.D + "[" + get_time() + "] " + F.g + S.B + "[SUCCESSFULY]" + F.R_ALL + " Bot wurde gestopt.")
        print(" ")
        print(" ")
        print("--------------------------------------------------------------------------------------------------------------")
        exit()
    else:
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True) # clear the printed line
        print("    ", end="\r", flush=True)

signal.signal(signal.SIGINT, handler)

@bot.event
async def on_ready():
    print(" ")
    print(F.y + S.D + "[" + get_time() + "] " + F.g + S.B + "[SUCCESSFULY]" + F.R_ALL + " Bot wurde gestartet.")
    print(" ")

    try:
        DB = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Mama1978",
            database="ehrv"
        )
        print(F.y + S.D + "[" + get_time() + "] " + F.g + S.B + "[SUCCESSFULY]" + F.R_ALL + " MySQL Verbunden")
        end_state(DB)
    except:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bat_file_path = os.path.join(script_dir, "assets", "sql.bat")
        subprocess.call([bat_file_path], shell=True)
        loading_animation()

    print(" ")
    print(F.y + S.D + "[" + get_time() + "] " + S.N + "[INFO]" + F.R + " Eingelogt als:")
    print(F.y + S.D + "[" + get_time() + "] " + F.R_ALL + "       " + bot.user.name)
    print(" ")
    print(F.y + S.D + "[" + get_time() + "] " + S.N + F.y + "[INFO]" + F.R + " Bot ID:")
    print(F.y + S.D + "[" + get_time() + "] " + F.R_ALL + "       " + str(bot.user.id))
    print(" ")
    print("--------------------------------------------------------------------------------------------------------------")
    #await bot.sync_application_commands(guild_id=1180167998342975578)

    if args.alternate_server:
        os.system("c:\\Users\\Thoma\\Downloads\\nircmd\\nircmd monitor off")

environ()
bot.run(os.environ["TOKEN"])