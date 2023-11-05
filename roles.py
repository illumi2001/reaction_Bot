import discord
import toml
import random 

from discord.ext import commands
from dotenv import load_dotenv

with open('config.toml', 'r') as f:
    config = toml.load(f)

MESSAGE_ID = config['MESSAGE_ID']
TOKEN = config['TOKEN']
ROLE_CHANNEL_ID = config['ROLE_CHANNEL_ID']
emoji_role_dict = config['emoji_roles']
wins = config[('wins')]
losses = config[('losses')]
message_options = config['message_options']

sui = 421002581330886666
matt = 77560540083265536 #testing
safe_word = "joegrandma69"
typed_safe_word = False

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='$',intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != MESSAGE_ID: # Check if user reacted on role selector message
        return
    print("Reaction added")
    guild = bot.get_guild(payload.guild_id) # Get the guild object
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

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != MESSAGE_ID:
        return
    print("Reaction removed")
    guild = bot.get_guild(payload.guild_id)
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

@bot.event
async def on_message(message):
    global typed_safe_word, wins, losses #BANDAID SORTA
    if message.author == bot.user:
        return
    if message.content.startswith('$'):
        await bot.process_commands(message)  # Let discord.py handle the commands
    if message.content == "stop3000":
        await bot.close()
        return
    if message.content in ("k", "K"):
        await message.reply("ys", mention_author=True)
    if message.author.id == sui:
        if message.content == safe_word:
            # Too sleepy to clean this up but can reuse matt var i think
            typed_safe_word = True
            matt_dm = await bot.fetch_user(matt)
            free_sui = "siton escaped"
            await matt_dm.send(free_sui)
            return
        if typed_safe_word:
            return

        random_number = random.random()
        print(random_number)
        user = await bot.fetch_user(sui)

        with open('config.toml', 'w') as f:
            toml.dump(config, f)

        if random_number < 0.01:
            wins += 1
            config['wins'] = wins
            await user.send(f'type safe word to stop dms: "{safe_word}"')
        elif random_number < 0.051:
            wins += 1
            config['wins'] = wins
            random_message = random.choice(message_options)
            await user.send(random_message)
        else:
            losses += 1
            config['losses'] = losses

@bot.command()
async def joe(ctx, field_value):
    # Check if the user has the appropriate permissions
    if ctx.author.id == matt: 
        print("hi ;3")
    else:
        await ctx.send("die")
        return

    message = await ctx.channel.fetch_message(MESSAGE_ID)
    embed = message.embeds[0]
        
    # Add an example description for expected notation
    embed.add_field(name="",value=field_value,inline=False)
    await message.edit(embed=embed)

@bot.command()
async def unjoe(ctx):
     # Check if the user has the appropriate permissions
    if ctx.author.id != matt:
        await ctx.send("die")
        return
    message = await ctx.channel.fetch_message(MESSAGE_ID)
    embed = message.embeds[0]
    embed.remove_field(len(embed.fields) - 1)
    await message.edit(embed=embed)

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def clean(ctx, amount: int):


bot.run(TOKEN)