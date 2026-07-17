from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

app = Flask(__name__)

API_ID = 33159667
API_HASH = '5ec5f0d4bef6143e3549d925b3ee2c32'
BOT_OBJETIVO = '@KRONOS_VIP_BOT'

SESSION_FILE = "/tmp/sesion_string.txt"

if os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "r") as f:
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

    with open("/tmp/temp_login.py", "w") as f:
        f.write(f"""
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def main():
    client = TelegramClient(StringSession(), {API_ID}, '{API_HASH}')
    await client.connect()

    send = await client.send_code_request('{telefono}')

    with open('/tmp/phone_code_hash.txt', 'w') as fh:
        fh.write(send.phone_code_hash)

    print('OK')

asyncio.run(main())
""")

    os.system("python /tmp/temp_login.py")

    return "Codigo enviado a tu Telegram 💬. Usa /codigo?telefono=NUMERO&numero=CODIGO"


@app.route("/codigo")
def verificar_codigo():
    numero_codigo = request.args.get("numero", "").strip()
    telefono = request.args.get("telefono", "").strip()

    if not numero_codigo or not telefono:
        return "Faltan datos. Usa: /codigo?telefono=+51942978154&numero=12345"

    if not os.path.exists("/tmp/phone_code_hash.txt"):
        return "Error: No se encontro solicitud anterior."

    with open("/tmp/phone_code_hash.txt", "r") as f:
        phone_code_hash = f.read().strip()


    with open("/tmp/temp_verify.py", "w") as f:
        f.write(f"""
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def main():
    try:
        client = TelegramClient(StringSession(), {API_ID}, '{API_HASH}')

        await client.connect()

        await client.sign_in(
            '{telefono}',
            '{numero_codigo}',
            phone_code_hash='{phone_code_hash}'
        )

        string = client.session.save()

        with open('/tmp/sesion_string.txt','w') as fs:
            fs.write(string)

        print('OK')

    except Exception as e:
        with open('/tmp/error_verify.txt','w') as fe:
            fe.write(str(e))


asyncio.run(main())
""")

    os.system("python /tmp/temp_verify.py")


    if os.path.exists(SESSION_FILE):
        global CADENA_SESION

        with open(SESSION_FILE,"r") as fs:
            CADENA_SESION = fs.read().strip()

        return "¡CONECTADO EXITOSAMENTE! 🎉 Ya puedes usar /tel"


    error_msg = ""

    if os.path.exists("/tmp/error_verify.txt"):
        with open("/tmp/error_verify.txt","r") as fe:
            error_msg = fe.read().strip()

    return f"Error al verificar codigo: {error_msg}"


@app.route("/tel")
def buscar_telefono():

    numero = request.args.get("numero","").strip()

    if not numero:
        return jsonify({
            "status":"error",
            "mensaje":"Falta el numero"
        })


    if not CADENA_SESION:
        return jsonify({
            "status":"error",
            "mensaje":"No autorizado. Ve a /conectar primero."
        })


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


    try:

        client = TelegramClient(
            StringSession(CADENA_SESION),
            API_ID,
            API_HASH
        )

        loop.run_until_complete(client.connect())


        comando = f"/tel {numero}"

        loop.run_until_complete(
            client.send_message(
                BOT_OBJETIVO,
                comando
            )
        )


        loop.run_until_complete(
            asyncio.sleep(4)
        )


        mensajes = loop.run_until_complete(
            client.get_messages(
                BOT_OBJETIVO,
                limit=1
            )
        )


        respuesta_bot = mensajes[0].text if mensajes else "Sin respuesta"


        loop.run_until_complete(
            client.disconnect()
        )


        return jsonify({
            "status":"success",
            "numero":numero,
            "respuesta_del_bot":respuesta_bot
        })


    except Exception as e:

        return jsonify({
            "status":"error",
            "mensaje":str(e)
        })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
