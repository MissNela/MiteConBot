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
    return ctx.message.author.id == "470881108444053504, 342364288310312970"

def is_coo(ctx):
    return ctx.message.author.id == "503217704887386132"

def is_admin(ctx):
    return ctx.message.author.id == ""

def is_mod(ctx):
    return ctx.message.author.id == ""

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
        Zde jsou všechny help příkazy!
        ``/help``
        Ukáže tento message.
       `` /warn``
        Admin pouze! /warn @user Dúvod.
        ``/ban ``
        Zabanuje Uživatele. /ban @user.
        ``/unban``
        Odbanuje uživatele (Pokud není napsán odbanuje posledního v banlistu).
        ``/serverinfo``
        Zobrazí Info o serveru.
       `` /userinfo``
        Zobrazí info o hráči.
       
       `` Ping``
        Řekne :ping_pong: Pong!
        
        ``Scpbans``
        Ukáže ban list.
        """
        
        
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
        await client.say('**On/a je mod/admin a nemam pravomoce je/ho kicknout! ') 
        return
    
    try:
        await client.kick(user)
        await client.say(user.name+' Byl kicknutej! Papa :wave:   '+user.name+'!')
        await client.delete_message(ctx.message)

    except discord.Forbidden:
        await client.say('Permission denied.')
        return

    
@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True) 
@commands.check(is_coo, is_owner)
async def ban(ctx,user:discord.Member):

    if user.server_permissions.ban_members:
        await client.say('**On/a je Mod/Admin a jsem neoprávněn je zabanovat!**')
        return

    try:
        await client.ban(user)
        await client.say(user.name+'Byl zabanován!'+user.name+'!')

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
@commands.check(is_coo, is_owner)

async def unban(ctx):
    ban_list = await client.get_bans(ctx.message.server)

    # Show banned users
    await client.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))

    # Unban last banned user
    if not ban_list:
    	
        await client.say('Ban list je prázdný.')
        return
    try:
        await client.unban(ctx.message.server, ban_list[-1])
        await client.say('Unbanned user: `{}`'.format(ban_list[-1].name))
    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('unban selhal.')
        return		      	 		 		  


@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
@commands.check(is_coo, is_owner)
async def warn(ctx, userName: discord.User, *, message:str):
        await client.send_message(userName, "Byl jsi varován za: {}".format(message)) 
        await client.say("Varování {0} Byl varován! Dúvod : {1} ".format(userName,message))
        pass

@client.command(pass_context = True)
@commands.check(is_owner)
async def restart():
    await client.logout()

@client.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)   
@commands.check(is_coo, is_owner)
async def setnick(ctx, user: discord.Member, *, nickname):
    await client.change_nickname(user, nickname)
    await client.delete_message(ctx.message)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def bans(ctx):
    '''Gets A List Of Users Who Are No Longer With us'''
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List zabanovaných idiotů", description = x, color = 0xFFFFF)
    return await client.say(embed = embed)


client.run(os.getenv("BOT_TOKEN"))
