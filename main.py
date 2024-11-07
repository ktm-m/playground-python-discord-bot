import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Yuqi is ready!')
    synced = await bot.tree.sync()
    print(f'{len(synced)} command(s)')


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(os.getenv('GREETING_GOODBYE_CH_ID')))
    text = f'Hi! {member.mention} welcome to the server!'
    embed = discord.Embed(title='Greetings!', description=text, color=discord.Color.yellow())

    await channel.send(text)
    await channel.send(embed=embed)
    await member.send(text)


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(os.getenv('GREETING_GOODBYE_CH_ID')))
    text = f'See you soon, {member.mention}.'
    await channel.send(text)


@bot.event
async def on_message(message):
    msg = message.content
    if msg == 'Hi!':
        await message.channel.send(f'Hello!, {message.author.name}')

    await bot.process_commands(message)


@bot.command
async def hello(ctx):
    await ctx.send(f'Hello! {ctx.author.name}')


@bot.command(name='echo')
async def echo_command(ctx, arg: str = f'Hello!, How are you?'):
    await ctx.send(arg)


@bot.tree.command(name='ping', description='Replies with Pong!')
async def ping_command(interaction):
    await interaction.response.send_message('Pong!')


@bot.tree.command(name='name')
@app_commands.describe(name=f'What is your name?')
async def name_command(interaction, name: str):
    await interaction.response.send_message(f'Hello!, {name}')


@bot.tree.command(name='help', description='Help commands')
async def help_command(interaction):
    embed = discord.Embed(title='Help', description='Help commands', color=discord.Color.green(),
                          timestamp=discord.utils.utcnow())
    embed.add_field(name='/ping', value='Ping command', inline=False)
    embed.add_field(name='/name', value='Name command', inline=False)
    embed.set_author(name='Author', url='https://www.linkedin.com/in/montheankul-k/', icon_url='')
    embed.set_thumbnail(url='')
    embed.set_image(url='')
    embed.set_footer(text='Help', icon_url='')
    await interaction.response.send_message(embed=embed)

def start_bot():
    if bot_token is None:
        raise ValueError('cannot get bot token form environment variable')
    bot.run(os.getenv('BOT_TOKEN'))

if __name__ == '__main__':
    start_bot()
