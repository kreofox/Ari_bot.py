import sqlite3
import discord
import logging

from config.config import Channels1
from config.config import level1, level2

# Инициализация база данных 
conn = sqlite3.connect('levels.db')
c = conn.cursor()

# Создание таблицы пользователей, если она не существует
c.execute('''CREATE TABLE IF NOT EXISTS users (
          user_id INTEGER PRIMARY KEY,
          username TEXT,
          level INTEGER,
          XP INTEGER
          )''')
conn.commit()

#определение уровня, не обходимого для повышения уровня
XP_PER_LEVEL = 100
LEVEL_UP_CHANNEL_ID = Channels1

#Соответствие уровни и ролей 
LEVEL_ROLES = {
    1: level1, # id ролей 
    2: level2
    # Добавьте дополнительные уровни и соответствующие роли здесь
}
async def update_level(member, bot):
    c.execute('SELECT * FROM users WHERE user_id = ?', (member.id,))
    user = c.fetchone()

    if user is None:
        c.execute('INSERT INTO users (user_id, username, level, xp) VALUES (?, ?, ?, ?)', 
                  (member.id, member.name, 1, 0))
        conn.commit()
        user = (member.id, member.name, 1, 0)

    user_id, username, level, xp = user
    xp += 10

    if xp >= XP_PER_LEVEL:
        level += 1
        xp -= XP_PER_LEVEL
        level_up_channel = bot.get_channel(LEVEL_UP_CHANNEL_ID)
        if level_up_channel:
            await level_up_channel.send(f'Поздравляем {username}! Вы достигли уровня {level}!')

        # Присвоение роли при достижении нового уровня
        if level in LEVEL_ROLES:
            role_id = LEVEL_ROLES[level]
            role = discord.utils.get(member.guild.roles, id=role_id)
            if role:
                # Удаление предыдущих ролей уровня
                roles_to_remove = [discord.utils.get(member.guild.roles, id=r) for r in LEVEL_ROLES.values() if r != role_id]
                await member.remove_roles(*roles_to_remove)

                # Присвоение новой роли
                await member.add_roles(role)
                if level_up_channel:
                    await level_up_channel.send(f'{username} получил роль {role.name} за достижение уровня {level}!')

    c.execute('UPDATE users SET level = ?, xp = ? WHERE user_id = ?', 
              (level, xp, user_id))
    conn.commit()
    logging.info(f'User {username} (ID: {user_id}) is now at level {level} with {xp} XP.')

def get_user_level_xp(user_id):
    c.execute('SELECT level, xp FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    if user:
        return user[0], user[1]
    else:
        return None, None