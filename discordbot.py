import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
import asyncio
from datetime import datetime

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Crée une instance du bot
bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

# Événement lorsque le bot est prêt et connecté au serveur Discord
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name} ({bot.user.id})')

# Tâche planifiée pour changer le pseudo de l'utilisateur toutes les 3 secondes
@tasks.loop(seconds=3)
async def change_username():
    guild_id = 1234567890  # Remplacez par l'ID de votre serveur Discord
    user_id = 1234567890  # Remplacez par l'ID de l'utilisateur cible
    guild = bot.get_guild(guild_id)
    user = guild.get_member(user_id)
    if user:
        current_time = datetime.now().strftime("%H:%M:%S")
        await user.edit(nick=current_time)

# Commande slash pour changer le pseudo de l'utilisateur
@slash.slash(name="time",
             description="Change le pseudo de l'utilisateur en l'heure actuelle",
             options=[
                 {
                     "name": "utilisateur",
                     "description": "Utilisateur cible",
                     "type": 6,
                     "required": True
                 }
             ])
async def time(ctx: SlashContext, utilisateur: discord.Member):
    await ctx.defer()
    if ctx.guild:
        change_username.start()
        await asyncio.sleep(10)  # Peut être ajusté en fonction de vos besoins
        change_username.stop()
    else:
        await ctx.send("Cette commande ne peut être utilisée que dans un serveur.")

# Remplacez "TOKEN" par votre propre jeton de bot Discord
bot.run('TOKEN')
