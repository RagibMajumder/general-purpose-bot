import qrcode
import discord
import os
from discord.ext import commands
import requests
import wbgapi as wb
import random
import aiohttp





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

    await ctx.author.send("Look at this qr get the joke rq and qr", file=discord.File(file_path))
    await ctx.send("Check your dms dumbass")

@bot.command()
async def ping(ctx): # responds with pong
    await ctx.send("Go away")
    await ctx.send("https://www.youtube.com/watch?v=IItSCWUndgM")

@bot.command()
async def inv(ctx): 
    await ctx.send("https://discord.gg/C3yxUpPQSS")

@bot.command()
async def talk(ctx): # sends a dm to the user
    await ctx.author.send('hi')

@bot.command()
async def sum(ctx, a: int, b: int): # adds two numbers
    result = adding(a, b)
    await ctx.send(f"Stupid {result}")

@bot.command()
async def div(ctx, a: int, b: int): # divides two numbers
    if b == 0:
        await ctx.send("Cannot divide by zero, dumbass")
    else:
        result = division(a, b)
        await ctx.send(f"Answer: {result}")

@bot.command()
async def multiply(ctx, a: int, b:int): # multiplies two numbers
    result = multiple(a, b)
    await ctx.send(f"Answer: {result}")

@bot.command()
async def remain(ctx, a: int, b: int): # finds remainder
    result = remainder(a, b)
    await ctx.send(f"Remainder is {result}")

@bot.command()
async def ghazi(ctx):
    ghaziid = 1275081834622881894
    await ctx.send(f'hi <@{ghaziid}> Pakistan zindabad')

@bot.command()
async def kyo(ctx):
    kyoid = 1211897276906344478
    await ctx.send(f"Kyo toaster bath <@{kyoid}>")

@bot.command()
async def kyonice(ctx):
    kyoid = 1211897276906344478
    await ctx.send(f"Kyo you are the sweetest most kindest person <@{kyoid}>")

@bot.command()
async def sally(ctx):
    sallyid = 1335651836455030934
    await ctx.send(f"Hi sally you are the bestest fr <@{sallyid}>")

@bot.command()
async def dingus(ctx):
    dingusid = 1405598042136252447
    await ctx.send(f"Dingus you are our favorite brazilian <@{dingusid}>")

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
async def anticommie(ctx): #names anticommunist leaders randomly
    anticom = ["Ronald Reagan (USA)",
    "Margaret Thatcher (UK)",
    "Konrad Adenauer (West Germany)",
    "Chiang Kai-shek (Taiwan/China)",
    "Lech Wałęsa (Poland)",
    "Pope John Paul II (Poland)",
    "Francisco Franco (Spain)",
    "Ferdinand Marcos (Philippines)",
    "Suharto (Indonesia)",
    "Helmut Kohl (Germany)",
    "Harry S. Truman (USA)",
    "Winston Churchill (UK)",
    "Nicolae Ceaușescus opponents (Romania)",
    "José Figueres Ferrer (Costa Rica)",
    "Syngman Rhee (South Korea)"]

    leader = random.choice(anticom)
    await ctx.send(f"{str(leader)}")


@bot.command()
async def commie(ctx): # names communist leaders randomly
    communistleaders = ["Karl Marx (Germany)",
    "Friedrich Engels (Germany)",
    "Vladimir Lenin (Soviet Union)",
    "Joseph Stalin (Soviet Union)",
    "Leon Trotsky (Soviet Union)",
    "Rosa Luxemburg (Germany/Poland)",
    "Che Guevara (Cuba/Argentina)",
    "Fidel Castro (Cuba)",
    "Salvador Allende (Chile)",
    "Hugo Chávez (Venezuela)",
    "Evo Morales (Bolivia)",
    "José Martí (Cuba)",
    "Mao Zedong (China)",
    "Ho Chi Minh (Vietnam)",
    "Kwame Nkrumah (Ghana)",
    "Antonio Gramsci (Italy)",
    "Jean Jaurès (France)",
    "Daniel Ortega (Nicaragua)",
    "Tomáš Masaryk (Czechoslovakia)",
    "Omar Torrijos (Panama)"]
    comleader = random.choice(communistleaders)
    await ctx.send(f"{str(comleader)}")

@bot.command()
async def helpme(ctx):
    helptext = {
        '!makeqr <url>': 'Generates a QR code from the provided URL and sends it to your DMs.',
        '!ping': 'Bot responds with a funny message.',
        '!inv': "Sends an invite link to the bot's server.",
        '!talk': 'Sends you a DM saying hi.',
        '!sum <a> <b>': 'Adds two numbers a and b.',
        '!div <a> <b>': 'Divides number a by number b.',
        '!multiply <a> <b>': 'Multiplies two numbers a and b.',
        '!remain <a> <b>': 'Finds the remainder when a is divided by b.',
        '!ghazi': 'Sends a special message to Ghazi.',
        '!kyo': 'Tells Kyo to kill himself.',
        '!kyonice': 'Sends a nice message to Kyo.',
        '!sally': 'Sends a special message to Sally.',
        '!convert <amount> <from_currency> <to_currency>': 'Converts amount from one currency to another.',
        '!gdp <country_code> <year>': 'Gets the GDP of a country for a specific year.',
        '!anticommie': 'Names a random anticommunist leader.',
        '!commie': 'Names a random communist leader.',
        '!pokedex <name>': 'Fetches details about a Pokémon from PokéAPI.'
    }

    # storage
    help_message = "\n".join(f"{cmd}: {desc}" for cmd, desc in helptext.items())
    
    # Sends the message
    await ctx.send(f"📜 **Bot Commands:**\n{help_message}")





@bot.command()
async def pokedex(ctx, name: str):
    """
    Usage: *pokedex <name>
    Fetches Pokémon details from PokéAPI
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        await ctx.send(f"❌ Pokémon '{name}' not found!")
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




bot.run(os.getenv("TOKEN"))


