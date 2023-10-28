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
wins = config[('wins')]
losses = config[('losses')]
sui = 421002581330886666
matt = 77560540083265536 #testing

message_options = [
"A SUIIIIIIIIIIIII", "A SUIIIII AHAHAHA DOOOOONT KILL YOURSELF", "A SUIIIII A SUIIIII A SUIIIII",
"A SUIIIII NO REALLLYYY DONT KYS AHAHAaAHA", "A SUIIIII HAHAHAA PLEAS EPLEASE PLEASEEEE", "A SUIIIII TOONE SUIII TOOO-O-ONE ALL SHE WANNA DO IS PARTY SUII TONE",
"A SUIIIII NOOOOO OOOOOOOOOO A SUIIIIII", "A SUIIIII FOR ME IS A TONE FOR THEEEE", "A SUIIIII PLEASEEEE MOLLY YOUR WHOLE TEAM IN A CLOSED SPACE",
"A SUIIIII PLEASEEE PLEASE PLEASEEEEE KEEP TALKING", "A SUIIIII YOURE SO SEXY NOOO DONT DO IT", "A SUIIIII AHAHAAHA NOOOOO WE WOULD MISS YOU TOO MUCH", 
"A SUIIIII PLEASEEEEE HAVE A LONG AND HAPPY LIFE PLEASEEEEEE", "A SUIIIII PLEASEEE PAY UP YOUR TWO BILLION DOLLARS", "A SUIIIII DONTTTT BE A PARRY ABUSER", 
"A SUIIIII MASSSSSA SUIIII", "A SUIIIII MASSA MASSA SUIIIIIII", "A SUIIIII PLEAAAAAAASE IS THIS SO CALLED COUNTRY OF YOURS IN THE ROOM WITH US?",
"A SUIIIII SUIII SUII I GOT SOMETHING TO TELL YOU YO SUI", "A SUIIIII DO YOU THINK WE WILL BE FRIENDS FOREVER", "A SUIIIII PLEEEEEEASE TRY NOT TO GAP THE OTHER TOP LANER SO HARD",
"A SUIIIII PLEASEEEEE GO ON YOUR STORY IS SO INTERESTING", "A SUIIIII YO I GOT A QUESTION", "A SUIIIII DO YOU HEAR THE VOICES", "A SUIIIII GIVE IN TO THE VOICES", "A SUIIIII IM IN YOUR WALLS",
"I WAS CRAZYYY ONCE", "CRAZY ?", "A RUBBER ROOM", "I WAS CRAZY ONCE", "A SUIIIII S)_D(GYHS)DGIBHLYUFCKTUXC", 
"A SUIIIII A SUIIII AS UIIIIIIIIIIIIIIIII", "A SUIIIII SUII SUII SUII SUII", "A SUIIIII YOU MUSTA FORGOT AB THE TOOOOONE", 
"A SUIIIII SUII DOOOOOOOONT DO IT NOOOOOOOO", "A SUIIIII kys :3", "die"]

intents = discord.Intents.all()
client = discord.Client(intents=intents)

safe_word = "joegrandma69"
typed_safe_word = False

def main():
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

    @client.event
    async def on_message(message):
        global typed_safe_word, wins, losses #BANDAID SORTA
        if message.author == client.user:
            return
        if message.author.id == sui:
            if message.content == safe_word:
                # Too sleepy to clean this up but can reuse matt var i think
                typed_safe_word = True
                matt_dm = await client.fetch_user(matt)
                free_sui = "siton escaped"
                await matt_dm.send(free_sui)
                return
            if typed_safe_word:
                return

            random_number = random.random()
            print(random_number)
            user = await client.fetch_user(sui)

            with open('config.toml', 'w') as f:
                toml.dump(config, f)

            if random_number < 0.01:
                wins += 1
                config['wins'] = wins
                await user.send(f'type safe word to stop dms: "{safe_word}"')
            elif random_number < 0.41:
                wins += 1
                config['wins'] = wins
                random_message = random.choice(message_options)
                await user.send(random_message)
            else:
                losses += 1
                config['losses'] = losses

        if message.content in ("k", "K"):
            await message.reply("ys", mention_author=True)

    client.run(TOKEN)
    
if __name__ == "__main__":
    main()
# add commands to add roles etc, change to async, move message list, add command for sui to disable dms
# add options for safe words, set reset timer 