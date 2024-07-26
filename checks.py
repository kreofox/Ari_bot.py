from discord.ext import commands
from config.config import Channels , Channels_admin

#Id канала, в котором разрешено выполнять команды 
allowed_channel_id = Channels
allowed_channel_id_Admin = Channels_admin


def is_in_allowed_channel():
    async def predicate(ctx):
        if ctx.channel.id != allowed_channel_id:
            await ctx.send(f"{ctx.author.mention},Пожалуйста, используйте команды только в указанном канале.")
            return False
        return True
    return commands.check(predicate)
def is_in_allowed_channel_admin():
    async def predicate(ctx):
        if ctx.channel.id != allowed_channel_id_Admin:
            await ctx.send(f"{ctx.author.mention},Пожалуйста, используйте команды только в указанном канале.")
            return False
        return True
    return commands.check(predicate)