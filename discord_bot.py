import base64
import discord
import yaml
from discord.ext import commands

import get_player_stats

# Temp token, implement better security later
token = b'TmpNNU5qWTNOemM1TmpreE16UTNPVGN3LlhidW5GZy5LVWtPUzVqUjhXVTFBRGYzd1VjVl9CT3M4ckU='
token = base64.b64decode(token).decode('utf-8')

bot = commands.Bot(command_prefix='$')

# Run this when the bot loads
@bot.event
async def on_ready():
    status = 'Say $help' # Set the bot status msg
    await bot.change_presence(activity=discord.Game(name=status))
    print('Logged in as: {}'.format(bot.user.name))
    print("Currently active on servers:\n{}".format('\n'.join([guild.name for guild in bot.guilds])))
    print('-' * 20)

@bot.command()
async def summary(ctx, btag):
    stats = get_player_stats.get_summary_stats(btag)
    await ctx.send(stats)

# Help command
bot.remove_command('help') # Remove default help command
@bot.command() 
async def help(ctx):
    commands = {}

    # Load help file
    with open('help.yml', 'r') as f:
        commands = yaml.safe_load(f)

    # Make an embed object (stylized discord message)
    embed = discord.Embed(title="Help", color=0xeee657)

    for command in commands:
        command_name = list(command.keys())[0]
        command_desc = command[command_name]
        embed.add_field(
            name=command_name, 
            value="\n".join(command_desc), 
            inline=False)

    # Send the help message back to the channel from where it was called
    await ctx.send(embed=embed)

# Start bot
bot.run(token)


