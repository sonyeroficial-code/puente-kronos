from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio

app = Flask(__name__)

# Configura tus credenciales de Telegram (las sacas de my.telegram.org)
API_ID = 33159667         # Reemplaza con tu API ID (número)
API_HASH = '5ec5f0d4bef6143e3549d925b3ee2c32'  # Reemplaza con tu API Hash (letras y números)

# El nombre de usuario (@) del bot al que le vas a hacer la consulta
BOT_OBJETIVO = '@KRONOS_VIP_BOT' 

@app.route("/")
def hogar():
    return "Puente Userbot Activo ✅"

@app.route("/tel")
def buscar_telefono():
    numero = request.args.get("numero", "").strip()
    
    if not numero:
        return jsonify({"status": "error", "mensaje": "Falta el número de teléfono"})

    # Creamos un ciclo para manejar la petición asíncrona de Telegram dentro de Flask
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Iniciamos el cliente de Telegram (Userbot)
        client = TelegramClient('sesion_puente', API_ID, API_HASH)
        loop.run_until_complete(client.connect())
        
        # 1. Enviar el comando /tel al bot objetivo
        comando = f"/tel {numero}"
        loop.run_until_complete(client.send_message(BOT_OBJETIVO, comando))
        
        # 2. Esperar unos segundos a que el bot responda
        loop.run_until_complete(asyncio.sleep(3)) 
        
        # 3. Leer el último mensaje que nos mandó ese bot
        mensajes = loop.run_until_complete(client.get_messages(BOT_OBJETIVO, limit=1))
        respuesta_bot = mensajes[0].text if mensajes else "Sin respuesta"
        
        loop.run_until_complete(client.disconnect())

        # Devolvemos lo que el bot respondió textualmente
        return jsonify({
            "status": "success",
            "numero": numero,
            "respuesta_del_bot": respuesta_bot
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": f"Error en el puente: {str(e)}"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
