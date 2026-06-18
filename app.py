from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession # <--- Cambiamos a sesión de texto
import asyncio

app = Flask(__name__)

API_ID = 33159667
API_HASH = '5ec5f0d4bef6143e3549d925b3ee2c32'
BOT_OBJETIVO = '@KRONOS_VIP_BOT'

# PEGA AQUÍ EL TEXTO LARGO QUE CONSEGUISTE EN EL PASO 1
# Debe quedar guardado dentro de las comillas simples
SESION_STRING = 'pega_aqui_todo_el_texto_largo_que_copiaste'

@app.route("/")
def hogar():
    return "Puente Userbot Activo ✅"

@app.route("/tel")
def buscar_telefono():
    numero = request.args.get("numero", "").strip()
    
    if not numero:
        return jsonify({"status": "error", "mensaje": "Falta el número de teléfono"})

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Iniciamos sesión directamente con el String sin pedir códigos
        client = TelegramClient(StringSession(SESION_STRING), API_ID, API_HASH)
        loop.run_until_complete(client.connect())
        
        comando = f"/tel {numero}"
        loop.run_until_complete(client.send_message(BOT_OBJETIVO, comando))
        
        # Esperamos 3 segundos la respuesta del bot de Kronos
        loop.run_until_complete(asyncio.sleep(3)) 
        
        mensajes = loop.run_until_complete(client.get_messages(BOT_OBJETIVO, limit=1))
        respuesta_bot = mensajes[0].text if mensajes else "Sin respuesta"
        
        loop.run_until_complete(client.disconnect())

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
    
