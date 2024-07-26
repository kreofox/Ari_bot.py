import logging
import discord

async def on_member_join(member):
    role_id = 1265611684043817021 # id роли участника 
    
    role = member.guild.get_role(role_id)

    if role:
        await member.add_roles(role)
        logging.info(f"Назначенная роль '{role.name}' на {member.name}")
    else:
        logging.warning(f"Роль с идентификатором '{role_id}' не найден")
