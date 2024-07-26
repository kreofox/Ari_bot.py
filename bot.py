import discord
import config.config
import logging
import asyncio

from reaction_roles import ReactionRoles
from discord.ext import commands, tasks
from logging_config import setup_logging
from roly import on_member_join
from logging_config import loggin
from checks import is_in_allowed_channel , is_in_allowed_channel_admin
from music_handler import YTDLSource
from level_system import update_level, get_user_level_xp
from shop_system import get_user_balance, update_user_balance, buy_role, list_available_roles, increment_user_xp, get_user_level, add_role_to_db

#Вызов функций 
setup_logging()
loggin()

# Установите намерения для бота
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
intents.guilds = True
intents.messages = True

# Создайте экземпляр бота с префиксом команд "!"
bot = commands.Bot(command_prefix='!', intents=intents)
# Событие, которое выполняется при готовности бота
@bot.event
async def on_ready():
    print("<===========================================>")
    print(f'Bot {bot.user.name} has connected to Discord!')
    print("<===========================================>")

# Команда "!hello"
@bot.command(name='hello')
@is_in_allowed_channel()
async def hello(ctx, member: discord.Member = None):
    user = ctx.author.name
    await ctx.send(f'Hello, {user}!')
# Команда "!info"
@bot.command(name="info")
@is_in_allowed_channel()
async def info(ctx, member: discord.Member = None):
    try:
        # Если участник не указан, используем того, кто вызвал команду
        if member is None:
            member = ctx.author

        # Получение информации о пользователе
        embed = discord.Embed(title="Информация о участнике!", color=discord.Color.blurple())
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Имя", value=f"{member.name}", inline=False)
        embed.add_field(name="ID", value=f"{member.id}", inline=False)
        embed.add_field(name="Заход",value=f"{member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}", inline=False)
        embed.add_field(name="Статус", value=f"{member.status}", inline=False)
        embed.add_field(name="Role", value=f"{member.top_role.name}", inline=False)

        # Отправка информации о пользователе в канал
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f'Error in userinfo command: {e}')
        await ctx.send('При получении информации о пользователе произошла ошибка.')
# Команда "!command"
@bot.command(name="command")
@is_in_allowed_channel()
async def help(ctx):
    await ctx.send("Разработка")
#Команда "!creator"
@bot.command(name="creator")
@is_in_allowed_channel()
async def creator(ctx, member: discord.Member = None ):
    guild = ctx.guild 
    owner = guild.owner
    embed = discord.Embed(title="Информация о создатете бота", color=discord.Color.dark_blue())
    embed.set_thumbnail(url=owner.avatar.url)
    embed.add_field(name="Имя:", value=f"{owner.name}", inline=False)
    embed.add_field(name="ID:", value=owner.id, inline=False)
    embed.add_field(name ="Написать", value=f"{owner.mention}", inline=False)
    #embed.add_field(name="", inline=False)
    await ctx.send(embed=embed)
#Подключение к голосову каналу 
@bot.command(name="join", help="Присоединиться к голосовому каналу")
@is_in_allowed_channel()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f"{ctx.message.author.name} не в голосовому канале.")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
#Отключение от голосового канала
@bot.command(name="leave", help="Покинуть голосовой канал")
@is_in_allowed_channel()
async def leave(ctx):
    if not ctx.voice_client:
        await ctx.send("Бот не подлючен к голосовому каналу.")
        return
    await ctx.voice_client.disconnect()
#Проигрывание музыки 
@bot.command(name="play", help="Проигрывать музыку")
@is_in_allowed_channel()
async def play(ctx, url):
    if not ctx.voice_client:
        await ctx.send("Бот не подлючен к голосову каналу.")
        return
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print(f"Ошибка игрока: {e}") if e else None)

    await ctx.send(f"Проигрываю:{player.title}")
#Пауза вопроизведения 
@bot.command(name="pause", help="Возобновить вопроизведение")
@is_in_allowed_channel()
async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Музыка возобновлена.")
#Остановка воспроизведения
@bot.command(name="stop", help="Возбновить вопроизведение") 
@is_in_allowed_channel()
async def resume(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Вопроизвдение остановлено.") 
#Обратка сообщений для обновлления !level
@bot.event
async def on_level(message):
    if not message.author.bot:
        leveled_up, new_level = increment_user_xp(message.author.id)
        if leveled_up:
            await handle_level_up(message.author, new_level)
        await bot.process_commands(message)
#обратока повышения уровня
async def handle_level_up(member, new_level):
    role_name = f"Level {new_level}"
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await member.send(f'Поздравляю! Вы достигли {new_level} уровня и получили роль {role_name}.')
    else:
        await member.send(f'Поздравляю! Вы достигли {new_level} уровня, но роль {role_name} не найдена.')
#Команда !level 
@bot.command(name="level")
@is_in_allowed_channel()
async def level(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    user_id = member.id
    username = member.name
    level, xp = get_user_level_xp(user_id)
    if level is not None:
        await ctx.send(f'{username}, ваш текущий уровень: {level}, ваш текущий XP: {xp}.')
    else:
        await ctx.send(f'{username}, вас нет в базе данных. Начните активность, чтобы получить уровень!')
# Команда для проверки баланса пользователя
@bot.command(name='balance')
@is_in_allowed_channel()
async def balance(ctx):
    user_id = ctx.author.id
    balance = get_user_balance(user_id)
    await ctx.send(f'{ctx.author.name}, ваш баланс: {balance} монет.')
# Команда для покупки роли
@bot.command(name='buy')
@is_in_allowed_channel()
async def buy(ctx, role_name: str):
    user_id = ctx.author.id
    success = buy_role(user_id, role_name, ctx.author)
    if success:
        await ctx.send(f'{ctx.author.name}, вы успешно купили роль {role_name}!')
    else:
        await ctx.send(f'{ctx.author.name}, не удалось купить роль {role_name}. Возможно, у вас недостаточно монет или роль не найдена.')
# Команда для отображения доступных товаров
@bot.command(name='shop')
@is_in_allowed_channel()
async def shop(ctx):
    try:
        roles = list_available_roles()
        logging.info(f"Available roles: {roles}")
        if roles:
            embed = discord.Embed(title="Магазин ролей", color=discord.Color.blue())
            for role_info in roles:
                role_name, price = role_info
                embed.add_field(name=role_name, value=f'{price} монет', inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('В магазине нет доступных товаров.')
    except Exception as e:
        logging.error(f"Error in shop command: {e}")
        await ctx.send('Произошла ошибка при получении данных из магазина.')
# Задача для начисления монет каждые 10 минут
@tasks.loop(minutes=10)
async def award_coins():
    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:
                update_user_balance(member.id, 10)  # Добавление 10 монет
@bot.command(name='add_role')
@commands.has_permissions(administrator=True)
@is_in_allowed_channel_admin()
async def add_role(ctx, role_name: str, role_id: int, price: int):
    if add_role_to_db(role_name, role_id, price):
        await ctx.send(f'Роль {role_name} успешно добавлена в базу данных.')
    else:
        await ctx.send(f'Не удалось добавить роль {role_name} в базу данных.')
# Обработка сообщений
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'hi' in message.content.lower():
     await message.channel.send(f'Hello, {message.author.name}!')

    await bot.process_commands(message)
# Обратко исключениий команд
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Извините, я не понимаю эту команду.")
    else:
        logging.error(f"Произошла ошибка: {error}")
        await ctx.send("При обработке вашей команды произошла ошибка.")
# Подлючаем обратчик события on_member_join
bot.event(on_member_join)

# Загрузка расширения
bot.load_extension('reaction_roles')
bot.load_extension('admin_commands')
# Запуск бота
bot.run(config.config.TOKEN)