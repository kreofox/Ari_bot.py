import discord
from discord.ext import commands

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addreaction(self, ctx, message_id: int, emoji: str):
        """Добавляет реакцию к сообщению с указанным ID"""
        try:
            message = await ctx.fetch_message(message_id)
            await message.add_reaction(emoji)
            await ctx.send(f'Reaction {emoji} added to message {message_id}')
        except discord.NotFound:
            await ctx.send('Message not found!')
        except Exception as e:
            await ctx.send(f'An error occurred: {e}')

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
