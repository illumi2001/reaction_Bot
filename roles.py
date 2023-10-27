import discord
import toml

from dotenv import load_dotenv

with open('config.toml', 'r') as f:
    config = toml.load(f)

MESSAGE_ID = config['MESSAGE_ID']
TOKEN = config['TOKEN']
ROLE_CHANNEL_ID = config['ROLE_CHANNEL_ID']
emoji_role_dict = config['emoji_roles']
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_raw_reaction_add(payload):
    print("Reaction added")
    if payload.message_id != MESSAGE_ID: # Check if user reacted on role selector message
        return
    guild = client.get_guild(payload.guild_id) # Get the guild object
    if guild is None:
        print("Error setting guild")
        return
    try:
        role_id = emoji_role_dict[payload.emoji.id] # Access role id from dict
    except KeyError:
        print(f'Error: No role matching emoji id {payload.emoji.id}')
        return
    role = guild.get_role(role_id) # Role object
    if role is None:
        print(f'Error: Role with ID {role_id} does not exist')
        return
    try:
        await payload.member.add_roles(role)
    except discord.HTTPException:
        print(f'Error: Adding role {role.name} to user {payload.member.name} failed')
        return

@client.event
async def on_raw_reaction_remove(payload):
    print("Reaction removed")
    if payload.message_id != MESSAGE_ID:
        return
    guild = client.get_guild(payload.guild_id)
    if guild is None:
        print("Error setting guild")
        return
    try:
        role_id = emoji_role_dict[payload.emoji.id]
    except KeyError:
        print(f'Error: No role matching emoji id {payload.emoji.id}')
        return
    role = guild.get_role(role_id)
    if role is None:
        print(f'Error: Role with ID {role_id} does not exist')
        return
    # 'on_raw_reaction_remove' payload doesn't provide '.member'
    member = guild.get_member(payload.user_id)
    if member is None:
        return
    try:
        await member.remove_roles(role)
    except discord.HTTPException:
        print(f'Error: Adding role {role.name} to user {member.name} failed')
        return
    
client.run(TOKEN)
# add commands to add roles etc, , change to async, 