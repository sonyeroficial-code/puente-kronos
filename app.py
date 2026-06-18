from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

app = Flask(__name__)

API_ID = 33159667
API_HASH = '5ec5f0d4bef6143e3549d925b3ee2c32'
BOT_OBJETIVO = '@KRONOS_VIP_BOT'

if os.path.exists("sesion_string.txt"):
    with open("sesion_string.txt", "r") as f:
        CADENA_SESION = f.read().strip()
else:
    CADENA_SESION = ""

@app.route("/")
def hogar():
    if CADENA_SESION:
        return "Puente Userbot Activo ✅ Listo para usar /tel"
    return "Puente Activo ⚠️ Ve a /conectar para registrar tu cuenta."

@app.route("/conectar")
def conectar():
    telefono = request.args.get("telefono", "").strip()
    if not telefono:
        return "Falta el telefono. Usa: /conectar?telefono=+51942978154"
    
    with open("temp_login.py", "w") as f:
        f.write(f"""
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def main():
    client = TelegramClient(StringSession(), {API_ID}, '{API_HASH}')
    await client.connect()
    send = await client.send_code_request('{telefono}')
    with open('phone_code_hash.txt', 'w') as fh:
        fh.write(send.phone_code_hash)
    print('OK')

asyncio.run(main())
""")
    os.system("python temp_login.py")
    return "Codigo enviado a tu Telegram 💬. En cuanto te llegue, usa la ruta /codigo mandando telefono y numero."

@app.route("/codigo")
def verificar_codigo():
    numero_codigo = request.args.get("numero", "").strip()
    telefono = request.args.get("telefono", "").strip()
    
    if not numero_codigo or not telefono:
        return "Faltan datos. Usa: /codigo?telefono=+51942978154&numero=12345"
    
    if not os.path.exists("phone_code_hash.txt"):
        return "Error: No se encontro la solicitud anterior. Primero ve a /conectar"
    
    with open("phone_code_hash.txt", "r") as f:
        phone_code_hash = f.read().strip()

    with open("temp_verify.py", "w") as f:
        f.write(f"""
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def main():
    try:
        client = TelegramClient(StringSession(), {API_ID}, '{API_HASH}')
        await client.connect()
        await client.sign_in('{telefono}', '{numero_codigo}', phone_code_hash='{phone_code_hash}')
        string = client.session.save()
        with open('sesion_string.txt', 'w') as fs:
            fs.write(string)
        print('OK')
    except Exception as e:
        with open('error_verify.txt', 'w') as fe:
            fe.write(str(e))

asyncio.run(main())
""")
    os.system("python temp_verify.py")
    
    if os.path.exists("sesion_string.txt"):
        global CADENA_SESION
        with open("sesion_string.txt", "r") as fs:
            CADENA_SESION = fs.read().strip()
        return "¡CONECTADO EXITOSAMENTE! 🎉 Tu cuenta ya es el puente. Ya puedes usar /tel"
    else:
        error_msg = ""
        if os.path.exists("error_verify.txt"):
            with open("error_verify.txt", "r") as fe:
                error_msg = fe.read().strip()
        return f"Error al verificar el codigo: {error_msg}. Intentalo de nuevo pidiendo otro codigo."

@app.route("/tel")
def buscar_telefono():
    numero = request.args.get("numero", "").strip()
    if not numero:
        return jsonify({"status": "error", "mensaje": "Falta el numero"})
    
    if not CADENA_SESION:
        return jsonify({"status": "error", "mensaje": "No autorizado. Ve a /conectar primero."})
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        client = TelegramClient(StringSession(CADENA_SESION), API_ID, API_HASH)
        loop.run_until_complete(client.connect())
        
        comando = f"/tel {numero}"
        loop.run_until_complete(client.send_message(BOT_OBJETIVO, comando))
        
        loop.run_until_complete(asyncio.sleep(4)) 
        
        mensajes = loop.run_until_complete(client.get_messages(BOT_OBJETIVO, limit=1))
        respuesta_bot = mensajes[0].text if mensajes else "Sin respuesta"
        
        loop.run_until_complete(client.disconnect())

        return jsonify({
            "status": "success",
            "numero": numero,
            "respuesta_del_bot": respuesta_bot
        })
    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
