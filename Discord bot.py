import discord
from discord.ext import commands
import json
import tiquations as tq
import ast

ConfigLoc = 'config.json'
r=open(ConfigLoc,"r")
data=json.load(r)
ConfigJSON=list(data.values())
PREFIX=ConfigJSON[0]
TOKEN=ConfigJSON[1]
WEATHERTOKEN=ConfigJSON[2]
availableroles=[]
client = commands.Bot(command_prefix=PREFIX)
with open("roles.txt","r") as s:
    for x in s:
        if x == "":
            pass
        else:
            availableroles.append(x[:-1])


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

async def check_if_server(ctx):
    #if await check_if_server(ctx):
    if message.guild.id == 586587331654320152:
        return True
    else:
        return False

async def check_if_moderator(ctx):
    #if await check_if_moderator(ctx):
    if "Moderators" in [role.name for role in ctx.message.author.roles] or "Administrators" in [role.name for role in ctx.message.author.roles]:
        return True
    else:
        return False

async def check_if_burnt(ctx):
    #if await check_if_burnt(ctx):
    if ctx.message.author.id == 246297096595046401:
        return True
    else:
        return False

@client.command(pass_context=True)
async def hello(ctx):
    await ctx.message.channel.send("Hello!")

@client.command(pass_context=True)
async def invite(ctx):
    await ctx.message.channel.send("https://discordapp.com/api/oauth2/authorize?client_id=523203714794913802&permissions=8&scope=bot")

#EVALUATION CODE
def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
@client.command()
async def evaluate(ctx, *, cmd):
    if await check_if_burnt(ctx):
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
#EVALUATION CODE END

@client.command(pass_context=True)
async def roles(ctx):
    word=""
    with open("roles.txt","r") as s:
        for x in s:
            if x == "":
                pass
            else:
                word=word + x

        await ctx.message.channel.send("Available roles:")
        poo="```"+word+"```"
        await ctx.message.channel.send(poo)

@client.command(pass_context=True)
async def role(ctx, rolename):
    go=rolename.capitalize()
    PINGER=ctx.message.author.mention
    if go in availableroles:
        role = discord.utils.get(ctx.message.guild.roles, name=go)
        if role is None:
            await ctx.message.channel.send("Role not found")
        else:
            if str(role) in [y.name for y in ctx.author.roles]:
                user=ctx.message.author
                await user.remove_roles(role)
                msg=PINGER," removed ",str(role)
                strong =''.join(msg)
                await ctx.message.channel.send(strong)
            else:
                user=ctx.message.author
                await user.add_roles(role)
                msg=PINGER," granted ",str(role)
                strong =''.join(msg)
                await ctx.message.channel.send(strong)
    else:
        print("This role hasn't been added using the bot")
        await ctx.message.channel.send("This role hasn't been added using the bot")

@client.command(pass_context=True)
async def addrole(ctx, rolename):
    if await check_if_moderator(ctx):
       role = discord.utils.get(ctx.message.guild.roles, name=rolename)
       await ctx.guild.create_role(name=rolename)#hi skid.I remade the bot 100% just making a check if user has the mod role stuff
       with open('roles.txt', 'a') as the_file:
           strang=str(rolename)+'\n'
           the_file.write(strang)
           availableroles.append(rolename)
           print(availableroles)
       await ctx.message.channel.send('Success')

@client.command(pass_context=True)
async def delrole(ctx, rolename):
     if await check_if_moderator(ctx):
         role = discord.utils.get(ctx.message.guild.roles, name=rolename)
         if role is None:
             await ctx.message.channel.send("Role not found")
         else:
             await role.delete()
             await ctx.message.channel.send("Role deleted")
             availableroles.remove(rolename)
             with open('roles.txt', 'w') as the_file:
                 for l in availableroles:
                     the_file.write(str(l)+'\n')

client.run(TOKEN)
