import discord
import toml
import random 

from dotenv import load_dotenv

with open('config.toml', 'r') as f:
    config = toml.load(f)

MESSAGE_ID = config['MESSAGE_ID']
TOKEN = config['TOKEN']
ROLE_CHANNEL_ID = config['ROLE_CHANNEL_ID']
emoji_role_dict = config['emoji_roles']
wins = config.get('wins')
losses = config.get('losses')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id != MESSAGE_ID: # Check if user reacted on role selector message
        return
    print("Reaction added")
    guild = client.get_guild(payload.guild_id) # Get the guild object
    if guild is None:
        print("Error setting guild")
        return
    try:
        role_id = emoji_role_dict[str(payload.emoji.id)] # Access role id from dict
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
    if payload.message_id != MESSAGE_ID:
        return
    print("Reaction removed")
    guild = client.get_guild(payload.guild_id)
    if guild is None:
        print("Error setting guild")
        return
    try:
        role_id = emoji_role_dict[str(payload.emoji.id)]
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

sui = 421002581330886666
message_options = ["A SUIIIIIIIIIIIII", "A SUIIIII AHAHAHA DOOOOONT KILL YOURSELF",
"A SUIIIII NO REALLLYYY DONT KYS AHAHAaAHA", "A SUIIIII HAHAHAA PLEAS EPLEASE PLEASEEEE", "A SUIIIII NOOOOO OOOOOOOOOO A SUIIIIII", 
"A SUIIIII A SUIIII AS UIIIIIIIIIIIIIIIII", "A SUIIIII SUII SUII SUII SUII", "A SUIIIII YOU MUSTA FORGOT AB THE TOOOOONE", 
"A SUIIIII SUII DOOOOOOOONT DO IT NOOOOOOOO", "A SUIIIII kys :3", "die",]

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.id == sui:
        random_number = random.random()
        print(random_number)
        if random_number < 0.4:
            wins += 1
            user = await client.fetch_user(sui)
            random_message = random.choice(message_options)
            await user.send(random_message)
        else:
            losses += 1
    if message.content in ("k", "K"):
        await message.reply("ys", mention_author=True)

# Update wins / losses tally
config['wins'] = wins
config['losses'] = losses
with open('config.toml', 'w') as f:
    toml.dump(config, f)

client.run(TOKEN)
# add commands to add roles etc, change to async, move message list, add command for sui to disable dms