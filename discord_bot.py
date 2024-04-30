import discord #import du module
import config
from discord.ext import commands
from blagues_api import BlaguesAPI

blagues = BlaguesAPI(config.api_key_blagues)

#Intents
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.message_content = True
# guilds = serveurs discords
intents.guilds = True
intents.members = True
# fonction "on_ready" pour confirmer la bonne connexion du bot sur votre serveur
@bot.event
async def on_ready():
 print (f"{bot.user.name} s'est bien connecté !")

#écoute la commande !ping et retourne Pong !
@bot.command()
async def ping(ctx):
    await ctx.reply('Pong !')

#écoute la commande !touché et retourne Coulé !
@bot.command()
async def touché(ctx):
    await ctx.reply('Coulé !')

#écoute la commande membres et retourne les membres du serveur
@bot.command()
async def membres(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            message = member.global_name + " | " + member.top_role.name
            await ctx.reply(message)

#écoute la commande !joke et retourne une blague avec l'api BlaguesAPI
@bot.command()
async def joke(ctx):
    blague = await blagues.random_categorized("limit")
    await ctx.reply(blague.joke + "\n||" + blague.answer+"||")

lstHello = ["bonjour", "salut"]

#écoute les message si l'utilisateur est différent du bot lui meme envoie un émoji si l'uitlisateur envoie un message pour dire bonjour
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.lower() in lstHello:
        await message.channel.send(':wave:', reference=message)
  
    await bot.process_commands(message)


last_user = ""

#écoute les membres qui rejoingnent le serveur et le souhaite bienvenue
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1234838275382972468)
    global last_user
    last_user = member.mention
    await channel.send(f':wave: {member.mention}')

#écoute la commande !bienvenue et souhaite bienvenue au dernier utilisateur qui a rejoint le serveur si il y en a un
@bot.command()
async def welcome(ctx):
    if(last_user != ""):
        await ctx.reply(f':wave: {last_user}')

#connexion du bot au serveur avec au token
bot.run(config.api_key_discord)