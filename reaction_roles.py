import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_reactions = {
            '👍': 1266319527570833520,  # Замените на ID вашей роли
        }
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        
        if reaction.emoji in self.role_reactions:
            guild = reaction.message.guild
            role_id = self.role_reactions[reaction.emoji]
            role = discord.utils.get(guild.roles, id=role_id)
            
            if role:
                member = guild.get_member(user.id)
                if member:
                    await member.add_roles(role)
                    print(f'Added role {role.name} to {member.name}')
                else:
                    print('Member not found in guild')
            else:
                print('Role not found')
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user == self.bot.user:
            return
        
        if reaction.emoji in self.role_reactions:
            guild = reaction.message.guild
            role_id = self.role_reactions[reaction.emoji]
            role = discord.utils.get(guild.roles, id=role_id)
            
            if role:
                member = guild.get_member(user.id)
                if member:
                    await member.remove_roles(role)
                    print(f'Removed role {role.name} from {member.name}')
                else:
                    print('Member not found in guild')
            else:
                print('Role not found')

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
