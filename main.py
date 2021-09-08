import random as rand
import time
import json
import discord
import requests
import bs4
from discord.ext import commands
from config import settings
from discord.utils import get
import sqlite3

client = commands.Bot(command_prefix = settings['prefix'])
client.remove_command('help')

hello_list = ['hello', 'hi', 'привет', 'здорова', 'здоров', 'ку', 'privet', 'ky', 'доров']
answer_words = ['узнать информацию о сервере', 'че как?', 'как сервер?', 'че скажешь?', 'команды', 'команды сервера']
goodbye_words = ['пока', 'пакеда', 'до связи', 'всем пока', 'всем добра', 'всем бобра', 'спокойной', 'спокойной ночи']
cards_words = ['я', 'I', 'my card', 'card', 'карточка']

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def get_anecdote():
    z = ''
    s = requests.get('http://anekdotme.ru/random')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    p = b.select('.anekdot_text')
    for x in p:
        s = (x.getText().strip())
        z = z + s + '\n\n'
    return s

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status = discord.Status.online, activity= discord.Game('Слушать и повиноваться'))

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        id INT,
        cash BIGINT,
        rep INT,
        lvl INT
    )""")

    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES (?, ?, 0, 0, 1)", (str(member), member.id))
            else:
                pass
    connection.commit()

@client.event # Добавление нового пользователя в БД
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES (?, ?, 0, 0, 1)", (str(member), member.id))
        print(member)
        connection.commit()
    else:
        print('Ничего')
        pass


@client.command(aliases = ['balance', 'cash', 'че_с_деньгами?', 'чё_с_деньгами?', 'че_с_деньгами', 'чё_с_деньгами'])
async def _balance(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed(
            description= f"""Баланс **{ctx.author}** = **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :leaves:**"""
        ))
    else:
        await ctx.send(embed=discord.Embed(
            description = f"""Баланс **{member}** = **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :leaves:**"""
        ))

@client.command(pass_context = True)
async def clear(ctx, amount = 2):
    await ctx.channel.purge(limit = amount)

@client.command(pass_context = True)
async def hello(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    author = ctx.message.author
    await ctx.send(f'Hello {author.mention}')

@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()

    if msg in answer_words:
        await  message.channel.send('Пропиши в чат команаду !help')
    if msg in goodbye_words:
        await  message.channel.send('Пока! Приходи ещё!')
    print('Message')

@client.command(pass_context = True)
async def help(ctx):
    emb = discord.Embed(title = 'Навигация по командам')
    emb.add_field(name = '{}clear #'.format(settings['prefix']), value='Очистка чата')
    emb.add_field(name = '{}hello'.format(settings['prefix']), value='Поздороваться с пользователем')
    emb.add_field(name = '{}join'.format(settings['prefix']), value='Присоединиться к голосовому каналу')
    emb.add_field(name = '{}leave'.format(settings['prefix']), value='Покинуть голосовой канал')
    emb.add_field(name = '{}heads_or_tails'.format(settings['prefix']), value='Подбросить монету')
    emb.add_field(name = '{}max'.format(settings['prefix']), value='Послушать анекдот от Максима Александровича')
    emb.add_field(name = '{}quote'.format(settings['prefix']), value='Послушать рандомную цитату')
    await ctx.send(embed = emb)

@client.command() #Присоединиться к голосовому каналу
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоединился к каналу:{channel}')

@client.command() #Покинуть голосовой канал
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'Бот отключился от канала:{channel}')

@client.command()
async def heads_or_tails(ctx):
    await ctx.send(f'Монета подбрасывается...')
    coin = rand.randint(1, 2)
    print(coin)
    time.sleep(1)
    if coin == 1:
        await ctx.send(f':full_moon: Выпал Орёл!')
    else:
        await ctx.send(f':new_moon: Выпал Решка!')

@client.command() #Цитата дня
async def quote(ctx):
    quote = get_quote()
    await ctx.send(quote)

@client.command() #Анекдот дня
async def max(ctx):
    anecdote = get_anecdote()
    await ctx.send(anecdote)

client.run(settings['token'])
