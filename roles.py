import discord
import toml

from dotenv import load_dotenv

# Parse config file for token and channel id
with open('config.toml', 'r') as f:
    config = toml.load(f)
    MESSAGE_ID = config['MESSAGE_ID']
    TOKEN = config['TOKEN']
    ROLE_CHANNEL_ID = config['ROLE_CHANNEL_ID']
    
# Dictionary that holds emote id to matching role
#Move to config, replace first field with game_emote_id, can also convert to PartialEmoji object
emoji_role_dict = {
    1166903222582124604: 1166946196892438538, # League
    1166902590693462117: 1166945937550229524 # Valorant
}

# Bot setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_raw_reaction_add(payload):
    print("Reaction added")
    # Check if user reacted on role selector message
    if payload.message_id != MESSAGE_ID:
        return
    
    # Get id of reaction, check if in dict
    emoji_id = payload.emoji.id
    # Convert this to try:except
    if emoji_id in emoji_role_dict:
        guild = client.get_guild(payload.guild_id)        # Get the guild object
        role_id = emoji_role_dict.get(emoji_id)           # Access role id from dict
        role = discord.utils.get(guild.roles, id=role_id) # Role object
        await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    print("Reaction removed")
    # Check if user reacted on role selector message
    if payload.message_id != MESSAGE_ID:
        return

    guild = client.get_guild(payload.guild_id)
    if guild is None:
        return

    try:
        role_id = emoji_role_dict[payload.emoji.id]
    except KeyError:
        return
    
    role = guild.get_role(role_id)
    if role is None:
        return

    # 'on_raw_reaction_remove' payload doesn't provide '.member'
    member = guild.get_member(payload.user_id)
    if member is None:
        return

    try:
        await member.remove_roles(role)
    except discord.HTTPException:
        print("ayo")
        return
    
client.run(TOKEN)
# add commands to add roles etc, , change to async, 