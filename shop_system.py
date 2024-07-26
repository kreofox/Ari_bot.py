import sqlite3
import logging

# Создание подключения к базе данных
connection = sqlite3.connect('shop.db')
cursor = connection.cursor()

# Создание таблиц, если они не существуют
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS roles (
    name TEXT PRIMARY KEY,
    role_id INTEGER,
    price INTEGER
)
''')

connection.commit()

def get_user_balance(user_id):
    cursor.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 0

def update_user_balance(user_id, amount):
    cursor.execute('INSERT OR IGNORE INTO users (id, balance) VALUES (?, 0)', (user_id,))
    cursor.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))
    connection.commit()

def increment_user_xp(user_id):
    cursor.execute('INSERT OR IGNORE INTO users (id, xp) VALUES (?, 0)', (user_id,))
    cursor.execute('UPDATE users SET xp = xp + 1 WHERE id = ?', (user_id,))
    connection.commit()
    cursor.execute('SELECT xp, level FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    xp, level = row
    new_level = xp // 100 + 1
    if new_level > level:
        cursor.execute('UPDATE users SET level = ? WHERE id = ?', (new_level, user_id))
        connection.commit()
        return True, new_level
    return False, level

def get_user_level(user_id):
    cursor.execute('SELECT level, xp FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    return (row[0], row[1]) if row else (1, 0)

async def buy_role(user_id, role_name, member):
    cursor.execute('SELECT price, role_id FROM roles WHERE name = ?', (role_name,))
    row = cursor.fetchone()
    if row:
        price, role_id = row
        balance = get_user_balance(user_id)
        if balance >= price:
            update_user_balance(user_id, -price)
            role = member.guild.get_role(role_id)
            if role:
                await member.add_roles(role)
                return True
    return False

def list_available_roles():
    cursor.execute('SELECT name, price FROM roles')
    roles = cursor.fetchall()
    logging.info(f"Queried roles: {roles}")
    return roles

def add_role_to_db(role_name, role_id, price):
    try:
        cursor.execute('INSERT INTO roles (name, role_id, price) VALUES (?, ?, ?)', 
                       (role_name, role_id, price))
        connection.commit()
        return True
    except sqlite3.IntegrityError as e:
        logging.error(f"Error adding role to DB: {e}")
        return False
