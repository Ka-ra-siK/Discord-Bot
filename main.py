import discord
from discord.ext import commands
from config import token
from config import prefix
from discord.utils import get

client = commands.Bot(command_prefix = prefix)
client.remove_command('help')

hello_list = ['hello', 'hi', 'привет', 'здорова', 'здоров', 'ку', 'privet', 'ky', 'доров']
answer_words = ['узнать информацию о сервере', 'че как?', 'как сервер?', 'че скажешь?', 'команды', 'команды сервера']
goodbye_words = ['пока', 'пакеда', 'до связи', 'всем пока', 'всем добра', 'всем бобра', 'спокойной', 'спокойной ночи']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status = discord.Status.online, activity= discord.Game('Слушать и повиноваться'))

# @client.command()
# async def play(ctx, url : str):
#     song_there = os.path.isfile("song.mp3")
#     try:
#         if song_there:
#             os.remove("song.mp3")
#     except PermissionError:
#         await ctx.send("Wait for the current playing music to end or use the 'stop' command")
#         return
#
#     voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
#     await voiceChannel.connect()
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#     for file in os.listdir("./"):
#         if file.endswith(".mp3"):
#             os.rename(file, "song.mp3")
#     voice.play(discord.FFmpegPCMAudio("song.mp3"))
#
#
# @client.command()
# async def leave(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice.is_connected():
#         await voice.disconnect()
#     else:
#         await ctx.send("The bot is not connected to a voice channel.")
#
#
# @client.command()
# async def pause(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice.is_playing():
#         voice.pause()
#     else:
#         await ctx.send("Currently no audio is playing.")
#
#
# @client.command()
# async def resume(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice.is_paused():
#         voice.resume()
#     else:
#         await ctx.send("The audio is not paused.")
#
#
# @client.command()
# async def stop(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     voice.stop()

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

    #if msg in hello_list:
      #  await message.channel.send('Привет! Как дела? Как сам?')
    if msg in answer_words:
        await  message.channel.send('Пропиши в чат команаду !help')
    if msg in goodbye_words:
        await  message.channel.send('Пока! Приходи ещё!')
    print('Message')

@client.command(pass_context = True)
async def help(ctx):
    emb = discord.Embed(title = 'Навигация по командам')
    emb.add_field(name = '{}clear #'.format(prefix), value='Очистка чата')
    emb.add_field(name = '{}hello'.format(prefix), value='Поздороваться с пользователем')
    emb.add_field(name = '{}join'.format(prefix), value='Присоединиться к голосовому каналу')
    emb.add_field(name = '{}leave'.format(prefix), value='Покинуть голосовой канал')
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

client.run(token)
