import qrcode
import discord
import os
from discord.ext import commands
import requests
import wbgapi as wb
import random
import aiohttp
import asyncio
import aiohttp
from flask import Flask
from threading import Thread 




app = Flask('')
@app.route('/')
def home():
    return "Works"

def run():
    port = int(os.environ.get("PORT", 8080))  # DO NOT touch this block of code 
    print(f"Starting flask on {port}")
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()




intents = discord.Intents.default()
intents.message_content = True  # important bc it dont work if u dont set intent to true idk why

bot = commands.Bot(command_prefix='*', intents=intents)




def adding(a, b):
    return a + b

def division(a, b):
    return a / b

def multiple(a, b):
    return a*b

def remainder(a, b):
    return a % b

@bot.command()
async def makeqr(ctx, *, url): # makes a qr code from a url and sends it to the user
    file_path = "qrcode.png"

    img = qrcode.make(url)
    img.save(file_path)

    await ctx.author.send("The QR code you requested:", file=discord.File(file_path))
    await ctx.send("QR code sent in dms")

@bot.command()
async def ping(ctx): # responds with pong
    await ctx.send("Online")
    await ctx.send("🟢")



@bot.command()
async def talk(ctx): # sends a dm to the user
    await ctx.author.send('hi')

@bot.command()
async def sum(ctx, a: float, b: float): # adds two numbers
    result = adding(a, b)
    await ctx.send(f"sum {result}")

@bot.command()
async def div(ctx, a: float, b: float): # divides two numbers
    if b == 0:
        await ctx.send("Cannot divide by zero")
    else:
        result = division(a, b)
        await ctx.send(f"Answer: {result}")

@bot.command()
async def multiply(ctx, a: float, b:float): # multiplies two numbers
    result = multiple(a, b)
    await ctx.send(f"Answer: {result}")

@bot.command()
async def remain(ctx, a: int, b: int): # finds remainder
    result = remainder(a, b)
    await ctx.send(f"Remainder is {result}")



@bot.command()
async def convert(ctx, amount: float, from_currency: str, to_currency: str): # converts currency from one to another
    """
    Usage: *convert 100 USD EUR
    """
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency.upper()}&to={to_currency.upper()}"
    
    try:
        response = requests.get(url).json()
        converted_amount = list(response['rates'].values())[0]
        await ctx.send(f"{ctx.author.mention} {amount} {from_currency.upper()} = {converted_amount:.2f} {to_currency.upper()}")
    except Exception:
        await ctx.send(f"{ctx.author.mention} Something went wrong. Check your currency codes (USD, EUR, GBP, etc).")






@bot.command()
async def pokedex(ctx, name: str):
    """
    Usage: *pokedex <name>
    Fetches Pokémon details from PokéAPI
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        await ctx.send(f"Pokémon '{name}' not found!")
        return

    data = response.json()

    #details
    poke_name = data["name"].title()
    poke_id = data["id"]
    types = ", ".join([t["type"]["name"].title() for t in data["types"]])
    abilities = ", ".join([a["ability"]["name"].replace("-", " ").title() for a in data["abilities"]])
    stats = {s["stat"]["name"].title(): s["base_stat"] for s in data["stats"]}

    # Image
    image_url = data["sprites"]["front_default"]

    # embedding
    embed = discord.Embed(title=f"{poke_name} (#{poke_id})", color=discord.Color.blue())
    embed.set_thumbnail(url=image_url)
    embed.add_field(name="Type(s)", value=types, inline=True)
    embed.add_field(name="Abilities", value=abilities, inline=True)
    embed.add_field(name="Stats", value="\n".join([f"{k}: {v}" for k, v in stats.items()]), inline=False)

    await ctx.send(embed=embed)



@bot.command()
async def circum(ctx, radius):
    out = 2 * 3.14 * float(radius)
    await ctx.send(f"Circumference is {out}")



@bot.command()
async def holiday(ctx):
    respond = requests.get("https://date.nager.at/api/v3/publicholidays/2026/AT")
    holidays = respond.json()
    for holiday in holidays:
        await ctx.send(f"{holiday['date']}: {holiday['name']}")



@bot.command()
async def diction(ctx, word: str): 
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    #dont remove aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                
               
                name = data[0]['word']
                definition = data[0]['meanings'][0]['definitions'][0]['definition']
                
                await ctx.send(f"**{name}**: {definition}")
            
            elif response.status == 404:
                await ctx.send(f"cant find word |--{word}--|.")
            else:
                await ctx.send("dictionary isnt working rn")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = None):
    if member == ctx.author:
        await ctx.send("You cannot kick yourself.")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member} has been kicked. Reason: {reason or 'No reason provided.'}")
    except Exception as e:
        await ctx.send(f"❌ Could not kick {member}. {e}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = None):
    if member == ctx.author:
        await ctx.send("You cannot ban yourself.")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member} has been banned. Reason: {reason or 'No reason provided.'}")
    except Exception as e:
        await ctx.send(f"❌ Could not ban {member}. {e}")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount < 1:
        await ctx.send("Please provide a number greater than 0.")
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Deleted {len(deleted)-1} messages.", delete_after=5)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason: str = None):
    if member == ctx.author:
        await ctx.send("You cannot mute yourself.")
        return

    guild = ctx.guild
    muted_role = discord.utils.get(guild.roles, name="Muted")
    if muted_role is None:
        muted_role = await guild.create_role(name="Muted", reason="Create mute role")
        for channel in guild.channels:
            await channel.set_permissions(muted_role, send_messages=False, speak=False, add_reactions=False)

    try:
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"🔇 {member} has been muted.")
    except Exception as e:
        await ctx.send(f"❌ Could not mute {member}. {e}")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    muted_role = discord.utils.get(guild.roles, name="Muted")
    if muted_role is None:
        await ctx.send("No Muted role exists.")
        return

    if muted_role not in member.roles:
        await ctx.send(f"{member} is not muted.")
        return

    try:
        await member.remove_roles(muted_role)
        await ctx.send(f"🔈 {member} has been unmuted.")
    except Exception as e:
        await ctx.send(f"❌ Could not unmute {member}. {e}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🚫 You do not have permission to run this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗ Missing arguments. Use the command with the required arguments.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❗ Invalid argument type. Check mentions and ids.")
    else:
        await ctx.send("⚠️ An error occurred. Please check your command and try again.")
        raise error


bot.run(os.getenv("TOKEN"))


