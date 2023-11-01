import discord
import toml

from dotenv import load_dotenv

# Parse config file for token and channel id
with open('config.toml', 'r') as f:
    config = toml.load(f)
    MESSAGE_ID = config['MESSAGE_ID']
    ROLE_CHANNEL_ID = config['ROLE_CHANNEL_ID']
    TOKEN = config['TOKEN']
    
# Bot setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    channel = client.get_channel(ROLE_CHANNEL_ID)
    # Select desired embed
    message = await channel.fetch_message(MESSAGE_ID) 

    # Emotes to react with
    emotes = [
        '<:valorant:1166902590693462117>',
        '<:league:1166903222582124604>',
        '<:case:1169395762690531478>',
        '<:battlerite:1169394236668526782>',
        '<:traitor:1169393487150587996>'
    ]

    # Add reactions to embed
    for emote in emotes:
        await message.add_reaction(emote)

client.run(TOKEN)