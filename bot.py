import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import platform
import colorsys
import random
import os
import time
from discord.voice_client import VoiceClient
from discord import Game, Embed, Color, Status, ChannelType







client = commands.Bot(command_prefix = '/')
client.remove_command('help')

@client.event
async def on_ready():
    print("The bot is online and connected with Discord!")

def is_owner(ctx):
    return ctx.message.author.id == "

def is_admin(ctx):
    return ctx.message.author.id == "

def is_mod(ctx):
    return ctx.message.author.id == "

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content.startswith('Ping'):
        await client.send_message(message.channel, ":ping_pong: Pong!")

@client.command(pass_context = True)
async def help():
    embed = discord.Embed(
        title = "Help",
        description= """
        Here are all cmds!
        ``Scphelp``
        Shows this message.
       `` Scpwarn``
        Admin only/Warns a user.
        ``Scpban ``
        Bans a user. Admin perms.
        ``Scpunban``
        Unbans a use if not specified (unbans last user)
        ``Scpserverinfo``
        Shows Info about server.
       `` Scpuserinfo``
        Shows Info about user.
       
       `` Ping``
        Says :ping_pong: Pong!
        ``Scpmakemod``
        Makes a mod. Usage ``Scpmakemod @user``
        ``Scpremovemod``
        Removes mod. Usage: ``Scpremovemod @user``
        ``Scppoll``
        Makes a poll. Usage: ``Scppoll <Question>``
        ``Scpbans``
        Shows a ban list
        ``Scpsetnick``
        Sets someone's nick. Usage: ``Scpsetnick @user <Nick>""",
        
        color = discord.Color.orange()
)
    await client.say(embed=embed)

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)     
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)

@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     
@commands.check(is_mod)
async def kick(ctx,user:discord.Member):

    if user.server_permissions.kick_members:
        await client.say('**He is mod/admin and i am unable to kick him/her**')
        return
    
    try:
        await client.kick(user)
        await client.say(user.name+' was kicked. Good bye '+user.name+'!')
        await client.delete_message(ctx.message)

    except discord.Forbidden:
        await client.say('Permission denied.')
        return

    
@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True) 
@commands.check(is_admin)
async def ban(ctx,user:discord.Member):

    if user.server_permissions.ban_members:
        await client.say('**He is mod/admin and i am unable to ban him/her**')
        return

    try:
        await client.ban(user)
        await client.say(user.name+' was banned. Good bye '+user.name+'!')

    except discord.Forbidden:

        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('ban failed.')
        return		 

@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     

async def serverinfo(ctx):
    '''Displays Info About The Server!'''

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await client.say(embed = join);


@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)     
@commands.check(is_admin)

async def unban(ctx):
    ban_list = await client.get_bans(ctx.message.server)

    # Show banned users
    await client.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))

    # Unban last banned user
    if not ban_list:
    	
        await client.say('Ban list is empty.')
        return
    try:
        await client.unban(ctx.message.server, ban_list[-1])
        await client.say('Unbanned user: `{}`'.format(ban_list[-1].name))
    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('unban failed.')
        return		      	 		 		  


@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
@commands.check(is_mod)
async def warn(ctx, userName: discord.User, *, message:str):
        await client.send_message(userName, "You have been warned for: {}".format(message)) 
        await client.say("warning {0} Has Been Warned! Warning Reason : {1} ".format(userName,message))
        pass

@client.command(pass_context = True)
@commands.check(is_owner)
async def restart():
    await client.logout()

@client.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member, *, nickname):
    await client.change_nickname(user, nickname)
    await client.delete_message(ctx.message)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def bans(ctx):
    '''Gets A List Of Users Who Are No Longer With us'''
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of The Banned Idiots", description = x, color = 0xFFFFF)
    return await client.say(embed = embed)

client.run(os.getenv("BOT_TOKEN")
