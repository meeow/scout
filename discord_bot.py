import base64
import discord
from discord.ext import commands

token = b'TmpNNU5qWTNOemM1TmpreE16UTNPVGN3LlhidW5GZy5LVWtPUzVqUjhXVTFBRGYzd1VjVl9CT3M4ckU='
token = base64.b64decode(token).decode('utf-8')

bot = commands.Bot(command_prefix='!')

# On Ready
@bot.event
async def on_ready():
    status = 'Say !help' #'DOWN FOR MAINT' # Set the bot status msg
    await bot.change_presence(activity=discord.Game(name=status))
    print('Logged in as: {}'.format(bot.user.name))
    print("Currently active on servers:\n{}".format('\n'.join([guild.name for guild in bot.guilds])))
    print('-' * 20)

# Help
bot.remove_command('help')
@bot.command()
async def help(ctx):
    title = "Help"
    description = "List of commands are:" 
    embed = discord.Embed(title=title, description=description, color=0xeee657)

    embed.add_field(
        name="!help", 
        value='''Display commands.`''', 
        inline=False)

    await ctx.send(embed=embed)

bot.run(token)


