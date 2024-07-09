import sqlite3
import discord
from discord.ext import commands
import json
import pretty_help
from pretty_help import EmojiMenu, PrettyHelp

with open("ext/config.json", "r") as f:
    data = json.load(f)
    TOKEN = data['TOKEN']
    PREFIX = data['PREFIX']
    VERSION = data['VERSION']
with open("ext/state.txt", "r") as file:
    state = file.read()

def get_prefix(bot, message):
    if not message.guild:
        return [PREFIX]

    db = sqlite3.connect("config/server_config.db")
    c = db.cursor()
    c.execute(f"SELECT prefix FROM guild_{message.guild.id}")
    res = c.fetchone()
    if res:
        prefix = str(res[0])
    else:
        prefix = ","

    return [prefix]
blocked_user_ids = [812091191519871057]
    

class Minepod(commands.Bot):

    
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        super().__init__(command_prefix=lambda bot, message: get_prefix(bot, message), intents=discord.Intents().all(), case_insensitive=True, help_command=None)

        self.cogslist = ["cogs.general", "cogs.currency", "cogs.fun", "cogs.staff", "cogs.databases", "cogs.help", "cogs.moderation", "cogs.minepod_commands"]


    async def on_ready(self):
        if "ENABLED" in state:
            servers = len(minepod.guilds)
            members = 0
            for guild in minepod.guilds:
                members = guild.member_count - 1

            await minepod.change_presence(activity = discord.Activity(
                type = discord.ActivityType.watching,
                name = f'{servers} servers and {members} members'
            ))
        else:
            await minepod.change_presence(activity=discord.Game(name=f"Bot is Disabled!"))
        print(f"Logged in as {self.user.name}")

    
    
    async def on_message(self, message):
        with open("ext/state.txt", "r") as file:
            state = file.read()
        description="The bot is undergoing maintenance, we will be back soon!\nIn the meantime you can go here to see when the bot will be back on!\nhttps://discord.gg/BHJFCpzSF2"
        #description="**MESSAGE FROM THE OWNER**\n\nThe bot is going through a whole remaking, for in depth join https://discord.gg/BHJFCpzSF2 for more information!\n\n- zhen#0002"
        if "DISABLED" in state:
            if message.author.id != 756267479214587975:
                if message.content.startswith(","):
                        embed = discord.Embed(color = discord.Color.red(), title="WAIT!!!", description=description)
                        await message.channel.send(embed=embed)
                        #https://discord.gg/BHJFCpzSF2
                        return
                else:
                    pass
        else:
            pass
        if "ENABLED" in state:
            servers = len(minepod.guilds)
            members = 0
            for guild in minepod.guilds:
                members += guild.member_count - 1

            await minepod.change_presence(activity = discord.Activity(
                type = discord.ActivityType.watching,
                name = f'{servers} servers and {members} members'
            ))
        else:
            await minepod.change_presence(activity=discord.Game(name=f"Bot is Disabled!"))
        await minepod.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = discord.Embed(color = discord.Color.blurple(), title = "Cooldown!!!", description="`You are on cooldown for another {:.2f} seconds!`".format(error.retry_after))
            msg.set_thumbnail(url="https://cdn.discordapp.com/attachments/1083561786046939206/1083948418474463292/13818704-newpiskel_l.png")
            await ctx.send(embed=msg)

    async def on_command_error(self, ctx, error):
        error_embed = discord.Embed(color=discord.Color.dark_red(), title="ERROR!", description=f"__`{error}`__")
        error_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1083561786046939206/1083565331768946838/5987-comand-block.png")
        await ctx.channel.send(embed=error_embed)

    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)

minepod = Minepod()


minepod.run(TOKEN)