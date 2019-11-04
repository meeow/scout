import base64
import discord
import yaml
import time
from discord.ext import commands

import get_player_stats
import get_team_stats

# Temp token, implement better security later
token = b'TmpNNU5qWTNOemM1TmpreE16UTNPVGN3LlhidW5GZy5LVWtPUzVqUjhXVTFBRGYzd1VjVl9CT3M4ckU='
token = base64.b64decode(token).decode('utf-8')
EMBED_COLOR = 0xeee657

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

# TODO: work in progress
# Blocked by top_heroes
@bot.command()
async def team(ctx, team):
    stats = get_team_stats.get_team_stats(team)
    for player in stats:
        print(player, stats[player])
        embed = discord.Embed(title=player, color=EMBED_COLOR)
        test = ''
        try:
            test = stats[player]['damage']
        except:
            test = "no data"

        embed.add_field(
            name="Damage",
            value=test
        )
        #time.sleep(0.1)
        await ctx.send(embed=embed)

# Help command
bot.remove_command('help') # Remove default help command
@bot.command() 
async def help(ctx):
    commands = {}

    # Load help file
    with open('help.yml', 'r') as f:
        commands = yaml.safe_load(f)

    # Make an embed object (stylized discord message)
    embed = discord.Embed(title="Help", color=EMBED_COLOR)

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


