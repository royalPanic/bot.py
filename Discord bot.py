import discord
import json
import tiquations
client = discord.Client()
ConfigLoc = 'config.json'
r=open(ConfigLoc,"r")
data=json.load(r)
ConfigJSON=list(data.values())
PREFIX=ConfigJSON[0]
TOKEN=ConfigJSON[1]
availableroles=[]
with open("roles.txt","r") as s:
    for x in s:
        if x == "":
            pass
        else:
            availableroles.append(x[:-1])


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    guild = message.guild
    PINGER=message.author.mention
    if message.author == client.user:
        return

    if message.author.id == 246297096595046401: # Eval can be very dangerous for the server hoster so it is only to be used by the bot owner
        if message.content.startswith(PREFIX+'eval'):
            cont=message.content.split("$$")
            cont=str(cont[1])
            if cont == None:
                print("Completed.")
            else:
                await message.channel.send(eval(cont))
        if message.content.startswith(PREFIX+'invite'):
            await message.channel.send("https://discordapp.com/api/oauth2/authorize?client_id=523203714794913802&permissions=8&scope=bot")

    if message.content.startswith(PREFIX+'hello'):
        await message.channel.send('Hello!')

    #THIS BOT WAS MADE FOR ONE SERVER ONLY. ANY COMMANDS AFTER THIS WILL NOT WORK IN ANY OTHER SERVER.

    if guild.id == 586587331654320152:
        pass
    else:
        return

    if message.content.startswith(PREFIX+'roles'):
        word=""
        with open("roles.txt","r") as s:
            for x in s:
                if x == "":
                    pass
                else:
                    word=word + x

            await message.channel.send("Available roles:")
            poo="```"+word+"```"
            await message.channel.send(poo)

    if message.content.startswith(PREFIX+'grant'):
        args=message.content.split(" ")
        if len(args)==1:
            await message.channel.send('**Usage:**\n```-grant ROLENAME```')
        else:
            go=args[1].capitalize()
            if go in availableroles:
                role = discord.utils.get(message.guild.roles, name=go)
                if role is None:
                    await message.channel.send("Role not found")
                else:
                    if str(role) in [y.name for y in message.author.roles]:
                        user=message.author
                        await user.remove_roles(role)
                        msg=PINGER," removed ",str(role)
                        strong =''.join(msg)
                        await message.channel.send(strong)
                    else:
                        user=message.author
                        await user.add_roles(role)
                        msg=PINGER," granted ",str(role)
                        strong =''.join(msg)
                        await message.channel.send(strong)
            else:
                print("This role hasn't been added using the bot")
                await message.channel.send("This role hasn't been added using the bot")


    if message.content.startswith(PREFIX+'addrole'):
         if "Moderators" in [role.name for role in message.author.roles] or "Administrators" in [role.name for role in message.author.roles]:
            args=message.content.split(" ")
            role = discord.utils.get(message.guild.roles, name=args[1])
            if len(args)==1:
                await message.channel.send('**Usage:**\n```-addrole ROLENAME```')
            else:

                namer=args[1]
                await guild.create_role(name=namer)
                with open('roles.txt', 'a') as the_file:
                    strang=str(namer)+'\n'
                    the_file.write(strang)
                    availableroles.append(namer)
                    print(availableroles)
                await message.channel.send('Success')

    if message.content.startswith(PREFIX+'delrole'):
            if "Moderators" in [role.name for role in message.author.roles] or "Administrators" in [role.name for role in message.author.roles]:
                args=message.content.split(" ")
                if len(args)==1:
                    await message.channel.send('**Usage:**\n```-delrole ROLENAME```')
                else:
                    role = discord.utils.get(message.guild.roles, name=args[1])
                    if role is None:
                        await message.channel.send("Role not found")
                    else:
                        await role.delete()
                        await message.channel.send("Role deleted")
                        availableroles.remove(args[1])
                        with open('roles.txt', 'w') as the_file:
                            for l in availableroles:
                                the_file.write(str(l)+'\n')




client.run(TOKEN)
