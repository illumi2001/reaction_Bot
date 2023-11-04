import discord
import toml

from dotenv import load_dotenv

# Parse config file for token and channel id
with open('config.toml', 'r') as f:
    config = toml.load(f)
    TOKEN = config['TOKEN']
    ROLE_CHANNEL_ID = config['ROLE_CHANNEL_ID']
    MESSAGE_ID = config['MESSAGE_ID']

# Bot setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Access embed by message id
    channel = client.get_channel(ROLE_CHANNEL_ID)
    message = await channel.fetch_message(MESSAGE_ID)

    # Update embed
    embed = message.embeds[0] # Message may contain multiple embeds
    embed.add_field(name="", value="<:case:1169395762690531478> = CS2",inline=False)
    embed.add_field(name="", value="<:battlerite:1169394236668526782> = Battlerite",inline=False)
    embed.add_field(name="", value="<:traitor:1169393487150587996> = Project Winter",inline=False)

    await message.edit(embed=embed) 


client.run(TOKEN)