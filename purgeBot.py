import discord
from discord.ext import commands
# Necessary for restart command
import subprocess
import asyncio
import sys

TOKEN="MTEzNjc5NTI3MTAwNzgzNDE3Mw.GGck8Q.onbbgw7waySgWvnaYAHMmGtmr1txZ9eJ2UWNAk"

client = commands.Bot(command_prefix="+", intents=discord.Intents.all(), status=discord.Status.online,
                     activity=discord.Activity(type=discord.ActivityType.listening, name="BEEP BOOP"))

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"{client.user} is ready")

@client.command()
async def test(ctx):
    await ctx.send("test")


@client.command()
async def restart(ctx):
    await ctx.send(f'{client.user} is now restarting, be patience')
    subprocess.Popen([sys.executable, "purgeBOT.py"])
    await asyncio.sleep(5)
    await ctx.send(f'{client.user} is back online')
    await client.close()



# serverIDlist=[]
# @client.command()
# async def serverIDs(ctx):
#     # Defines the array as global
#     global serverIDlist
#     # Clears the array's content so there are no repetitions if it's run several times
#     serverIDlist.clear()  
    
#     # Iterates trough the guilds(servers) the bot is in and adds them to the array
#     for server in client.guilds:
#         serverIDlist.append(server.id)
#     # Sends the array with all it's elements (DEBUGGING PURPOSES)
#     await ctx.send(serverIDlist)
    
# @client.command()
# async def purgeTarget(ctx, targetID:int):
#     # Checks if the invoker has permissions to delete messages
#     if not ctx.author.guild_permissions.manage_messages:
#         await ctx.send("I don't think you have the permissions to delete messages ")
#         return

#     deletedTotal = 0  # Counter for the total deleted messages
 
#     member= await client.fetch_user(targetID)

#     # Iterates trough all the servers the bot is in
#     for server_id in serverIDlist:
#         server = client.get_guild(server_id)
#         if server is not None:
#             try:
#                 # Iterate through all channels in the server
#                 for channel in server.text_channels:
#                     # The purge function will delete all the messages the specified member has sent
#                     deletedMessages = await channel.purge(limit=None, check=lambda msg: msg.author.id == targetID)
#                     deletedTotal += len(deletedMessages)
#             except discord.Forbidden:
#                 # The bot doesn't have permission to manage messages in this channel, skip it.
#                 continue

#     # Sends a message with the total deleted messages and the target member
#     await ctx.send(f'Deleted {deletedTotal} messages from {member} in all servers.')

serverIDlist=[]
@client.command()
async def serverIDs(ctx):
    # Defines the array as global
    global serverIDlist
    # Clears the array's content so there are no repetitions if it's run several times
    serverIDlist.clear()  
    
    # Iterates trough the guilds(servers) the bot is in and adds them to the array
    for server in client.guilds:
        serverIDlist.append(server.id)
    # Sends the array with all it's elements (DEBUGGING PURPOSES)
    await ctx.send(serverIDlist)
    
@client.command()
async def purgeTarget(ctx, targetID:int):

    await ctx.invoke(client.get_command('serverIDs'))
    # Checks if the invoker has permissions to delete messages
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("I don't think you have the permissions to delete messages ")
        return

    deletedTotal = 0  # Counter for the total deleted messages
 
    member= await client.fetch_user(targetID)

    # Iterates trough all the servers the bot is in
    for server_id in serverIDlist:
        server = client.get_guild(server_id)
        if server is not None:
            try:
                # Iterate through all channels in the server
                for channel in server.text_channels:
                    # The purge function will delete all the messages the specified member has sent
                    deletedMessages = await channel.purge(limit=None, check=lambda msg: msg.author.id == targetID)
                    deletedTotal += len(deletedMessages)
            except discord.Forbidden:
                # The bot doesn't have permission to manage messages in this channel, skip it.
                continue

    # Sends a message with the total deleted messages and the target member
    await ctx.send(f'Deleted {deletedTotal} messages from {member} in all servers.')


@client.command()
async def bonk(ctx, targetID:int,*,reason=None):
    # Invokes the function serverIDs
    await ctx.invoke(client.get_command('serverIDs'))

    # Defines member with the targetID
    member= await client.fetch_user(targetID)

    # Empty array that will store the servers the target will be banned for later usage
    serverBannedList=[]

    # If the invoker doesn't have the permissions to ban members it will send the error message and return nothing
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("MODS command only :P")
        return
    
    # If an unvalid ID has been input it will send an error message and return nothing
    if not member:
        await ctx.send("userID not found")
        return
        
    # Loops trough all the server IDs in the serverIDList array
    for server_id in serverIDlist:
        # Defines the server in which the bot will take action in this iteration
        server=client.get_guild(server_id)
        # This is basically impossible to be false but just in case
        if server:
            # Bans the specified member in the server the loop is iterating, if no reason was given it will default to none
            await server.ban(member,reason=reason)
            serverBannedList.append(server)
        else:
            await ctx.send("server not found")
    # Sends a messages with the member and the servers they've been banned
    banMessage=f"User {member} has been banned from: \n" + '\n'.join(str(x) for x in serverBannedList)
    await ctx.send (banMessage)

@client.tree.command (name="ping", description="Simple ping pong command")
async def ping (interaction:discord.Interaction):
    await interaction.response.send_message("PONG")


client.run(TOKEN)

# more modified stuff