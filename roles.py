import asyncio
import discord
import toml
import random 
import datetime
from discord.ext import commands
from dotenv import load_dotenv

with open('config.toml', 'r', encoding='utf-8') as f:
    config = toml.load(f)

for key, value in config.items():
    globals()[key] = value

safe_word = "joegrandma69"
typed_safe_word = False

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='$',intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    while True:
        today = datetime.date.today()
        for user in config["users"].values():
            name = user["name"]
            birthday = user["birthday"]
            birthday_calc = birthday.replace(birthday[0:4], str(today.year))
            if birthday and (datetime.date.fromisoformat(birthday_calc) - today).days == 7:
                channel = bot.get_channel(1120882608084111430) # links channel
                await channel.send(f"We got big BIRTHDAY COMING UP FOR, {name}!")
        await asyncio.sleep(86400)

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
    if (
        message.author.id in [users['matt']['id'], users['kevin']['id'], webhook_bot, kevin_bot] # Change to variables so recognizable
        and any(keyword in message.content for keyword in message_mapping)
    ):
        for keyword, channel_name in message_mapping.items():
            if keyword in message.content:
                boss_channel = bot.get_channel(BOSS_CHANNEL_ID)
                await boss_channel.edit(name=channel_name)
                break  # Stop searching after the first match
    if message.content == "stop3000":
        await bot.close()
        return
    if message.content in ("k", "K"):
        await message.reply("ys", mention_author=True)
    if message.author.id == users['sui']['id']:
        if typed_safe_word:
            return
        if message.content == safe_word:
            typed_safe_word = True
            matt_dm = await bot.fetch_user(users['matt']['id'])
            await matt_dm.send("siton escaped")
            return

        random_number = random.random()
        print(random_number)
        user = await bot.fetch_user(users['sui']['id'])

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
    if ctx.author.id == users['matt']['id']: 
        message = await ctx.channel.fetch_message(MESSAGE_ID)
        embed = message.embeds[0]
        # Add an example description for expected notation
        embed.add_field(name="",value=field_value,inline=False)
        await message.edit(embed=embed)
    else:
        await ctx.send("hahaHA")

@bot.command()
async def unjoe(ctx):
    if ctx.author.id != users['matt']['id']: # Check if the user has the appropriate permissions
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
    if ctx.author.id == users['matt']['id']:
        messages = []
        async for message in ctx.message.channel.history(limit=amount + 1):
            messages.append(message)
        for message in messages:
            await message.delete()
        await ctx.send(f"Deleted {amount} messages.")
    else:
        await ctx.send("plz stop troll")

@bot.command()
async def flip(ctx):
    flip_number = random.random()
    if flip_number < 0.01:
        await ctx.reply("Reply hazy, try again")
    elif flip_number < 0.51:
        await ctx.reply("Heads")
    else:
        await ctx.reply("Tails")
    
bot.run(TOKEN)