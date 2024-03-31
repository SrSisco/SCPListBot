import os
import string
import re
import discord
import requests
from discord import app_commands
from discord.ext import commands
bot = discord.Client(command_prefix="!",intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


# Comando para ver la lista de IDs de los servidores españoles más conocidos.
@tree.command(name="servidores")
async def servidores(ctx):
    await ctx.response.send_message("__**IDs de servidores españoles**__"
                                    "\n73339: [ES] - Unknow Place -"
                                    "\n72754: [ES] ZONA X"
                                    "\n74139: [ES] RadioLight #3[6.1.0]"
                                    "\n72846: [ES] Bachan Facility| ANARQUÍA"
                                    "\n68555: [ES] Bachan Facility| FF: OFF"
                                    "\n67001: [ES] SCP | World in Chaos #2"
                                    "\n67002: [ES] SCP | World in Chaos #1"
                                    "\n73262: Eternal Containment[ES]| Server #2"
                                    "\n61340: Eternal Containment PvP"
                                    "\n60360: Eternal Containment[ES]| Server #1"
                                    "\n44415: [ES] ★ InfernalBreach #1 ★"
                                    "\n45203: [ES] Neon Community - RolePlay"
                                    "\n45169: [ES] Neon Community - Normal"
                                    "\n74140: [ES] GAG-Server"
                                    "\n Otros...",ephemeral=True)


#Comando para obtener información sobre un server mediante su ID
@tree.command(name="buscar_server",description="Busca información de un server por su ID, puedes usar /servidores para verla")
async def buscar_server(ctx, server_id : int):


    # Busca información sobre un servidor de SCP:SL
    response = requests.get(f"https://api.scplist.kr/api/servers/{server_id}")

    #Comprueba que no haya ningún error en la solicitud
    if(response.status_code != 200):
       await ctx.send("Ha ocurrido un error, compruebe que los datos son correctos")
    else:
        # Pasa a json la info
        respuesta = response.json()

        #Crea el embed y le da el color y el "autor".
        embed = discord.Embed(title="INFORMACIÓN DEL SERVIDOR",
                         url=f"https://scplist.kr/servers/{server_id}",
                         colour=discord.Colour.random())
        embed.set_author(name="SCPList")


        #Apartado de nombre del servidor, se usa regex para eliminar los tags de HTML que pueda tener
        name = respuesta["info"]
        pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        name = re.sub(pattern, '', name)
        embed.add_field(name="Nombre:",
                   value=name,
                   inline=False)


        #Apartado de la IP del servidor
        embed.add_field(name="IP del servidor:",
                   value=respuesta["ip"]+":"+str(respuesta["port"]),
                   inline=False)


        #Apartado de friendlyfire del servidor
        ff = respuesta["friendlyFire"]
        ffTexto =""

        if ff:
            ffTexto = "Activado"
        else:
            ffTexto = "Desactivado"

        embed.add_field(name="Fuego amino",
                   value=ffTexto,
                   inline=False)


        #Apartado de conectividad del servidor y jugadores
        online = respuesta["online"]
        onlineTexto =""
        if online:
            onlineTexto = "Online"
        else:
            onlineTexto = "Offline"
        embed.add_field(name="Estado del Servidor:",
                   value=onlineTexto+", "+respuesta["players"]+ " jugadores",
                   inline=False)


        #Apartado técnico (framework si se usa)
        embed.add_field(name="Framework utilizado:",
                   value=respuesta["techList"][0]["name"]+" "+respuesta["techList"][0]["version"],
                   inline=False)

        embed.set_footer(text="Hecho por SrSisco")

        await ctx.response.send_message(embed=embed)


#Inicia el bot
@bot.event
async def on_ready():
   await tree.sync()
   print("El bot está online!")



bot.run("TOKEN")