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

                                ## VERY IMPORTANT ##
# when deploying on render make sure to clear build cache and deploy through manual deploy
# or else it will send out double the code



                                #####################


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
async def sum(ctx, a: int, b: int): # adds two numbers
    result = adding(a, b)
    await ctx.send(f"sum {result}")

@bot.command()
async def div(ctx, a: int, b: int): # divides two numbers
    if b == 0:
        await ctx.send("Cannot divide by zero")
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


GOOGLE_APPS_SCRIPT_URL = os.getenv("GOOGLE_APPS_SCRIPT_URL")

@bot.command()
async def montecarlo(ctx, shares_mean: float = None, shares_stddev: float = None, 
                     price_mean: float = None, price_stddev: float = None, threshold: float = 150000):
    """
    Usage: *montecarlo [shares_mean] [shares_stddev] [price_mean] [price_stddev] [threshold]
    Example: *montecarlo 7 0 67 5 150000
    """
    try:
        
        params = {}
        if shares_mean is not None:
            params["shares_mean"] = shares_mean
        if shares_stddev is not None:
            params["shares_stddev"] = shares_stddev
        if price_mean is not None:
            params["price_mean"] = price_mean
        if price_stddev is not None:
            params["price_stddev"] = price_stddev
        if threshold is not None:
            params["threshold"] = threshold
        
        # loading screen
        loading = await ctx.send("Running Monte Carlo simulation... (10-15 seconds)")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(GOOGLE_APPS_SCRIPT_URL, json=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if not data.get("success", False):
                            await loading.edit(content=f"Error: {data.get('error', 'Unknown error')}")
                            return
                        
                        results = data.get("results", {})
                        chart_url = data.get("chartUrl")
                        
                        #Dashboard
                        embed = discord.Embed(
                            title="Monte Carlo Simulation Results",
                            description="1000 trial simulation complete",
                            color=discord.Color.blue()
                        )
                        
                        embed.add_field(name="Average Revenue", value=f"${results.get('Average Revenue', 'N/A')}", inline=True)
                        embed.add_field(name="Worst Case (5%)", value=f"${results.get('Worst Case (5%)', 'N/A')}", inline=True)
                        embed.add_field(name="Best Case (95%)", value=f"${results.get('Best Case (95%)', 'N/A')}", inline=True)
                        embed.add_field(name="Probability > Threshold", value=results.get("Probability > $150k", "N/A"), inline=True)
                        
                        inputs = results.get("Input Parameters", {})
                        params_text = "\n".join([f"**{k}:** {v}" for k, v in inputs.items()])
                        embed.add_field(name="Inputs", value=params_text or "Default", inline=False)
                        
                        if chart_url:
                            embed.set_image(url=chart_url)
                        
                        embed.set_footer(text="Monte Carlo Simulation")
                        
                        await loading.delete()
                        await ctx.send(embed=embed)
                    
                    else:
                        error_text = await response.text()
                        await loading.edit(content=f"❌ Error {response.status}")
            
            except asyncio.TimeoutError:
                await loading.edit(content="Simulation timed out. Try again.")
            except Exception as e:
                await loading.edit(content=f"❌ Failed: {str(e)[:100]}")
    
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")




bot.run(os.getenv("TOKEN"))


