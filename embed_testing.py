import discord
import toml

from dotenv import load_dotenv

# Parse config file for token and channel id
with open('config.toml', 'r') as f:
    config = toml.load(f)
    TOKEN = config['TOKEN']
    ROLE_CHANNEL_ID = config['ROLE_CHANNEL_ID']

# Embed setup
embed = discord.Embed(
    title="Game Options", 
    description="React to be pingable for corresponding game", 
    color=discord.Color.dark_blue()
    )
embed.add_field(name="", value="",inline=True)
embed.add_field(name="", value="<:valorant:1166902590693462117> = Valorant",inline=False)
embed.add_field(name="", value="<:league:1166903222582124604> = League of Legends", inline=False)

# Bot setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(ROLE_CHANNEL_ID)
    await channel.send(embed=embed)

client.run(TOKEN)