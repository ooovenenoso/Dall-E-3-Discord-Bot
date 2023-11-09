import discord
import openai
from discord.ext import commands
from discord import Option
import aiohttp
import io

# Configura la clave de la API de OpenAI directamente
openai.api_key = 'OPENAI_API_KEY'

# Crea un bot de Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.slash_command(name="imagine", description="Generates an image from a prompt using DALL·E 3")
async def imagine(ctx, prompt: Option(str, "Enter the prompt for the image:")):
    # Confirma que se recibió el comando
    await ctx.defer()

    try:
        # Utiliza la API de OpenAI para generar la imagen
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="url"
        )
        
        # Comprueba si se ha generado la imagen y envíala al canal
        if response.get('data'):
            image_url = response['data'][0]['url']
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status != 200:
                        return await ctx.followup.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await ctx.followup.send(file=discord.File(data, 'image.png'))
        else:
            await ctx.followup.send("No image was generated. Please try again.")
            
    except Exception as e:
        await ctx.followup.send(f"An error occurred: {e}")

# Ejecuta el bot con tu token de Discord
bot.run('DISCORD_BOT_TOKEN')
