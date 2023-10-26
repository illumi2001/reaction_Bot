import discord
import toml

from dotenv import load_dotenv

# Parse config file for token and channel id
with open('config.toml', 'r') as f:
    config = toml.load(f)
    TOKEN = config['TOKEN']
    ROLE_CHANNEL_ID = config['ROLE_CHANNEL_ID']
    
# Dictionary that holds emote id to matching role
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
async def on_reaction_add(reaction, user):
    # Channel or Thread reaction was used
    channel = reaction.message.channel

    # Check if in role channel
    if channel.id != ROLE_CHANNEL_ID:
        return

    # Get id of reaction, check if in dict
    emoji_id = reaction.emoji.id
    role_id = emoji_role_dict.get(emoji_id)

    # Case where reaction added isnt an option
    if role_id is None: 
        return

    #Fetch role by id and grant user
    role = discord.utils.get(reaction.message.guild.roles, id=role_id)
    await user.add_roles(role)

client.run(TOKEN)

# Need to handle if user unreacts, add commands to add roles etc, , bot should react to it itself too maybe, change to async, 
# Change to checking reaction on a specific message instead of the whole channel