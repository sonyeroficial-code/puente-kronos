from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio

app = Flask(__name__)

API_ID = 33159667
API_HASH = '5ec5f0d4bef6143e3549d925b3ee2c32'
BOT_OBJETIVO = '@KRONOS_VIP_BOT'

# Cliente global temporal para guardar el proceso de inicio de sesión
client = None

@app.route("/")
def hogar():
    return "Puente Activo ✅ Usa /conectar para iniciar sesion."

# 1. PASO UNO: Enviar el número de teléfono
@app.route("/conectar")
def conectar():
    global client
    telefono = request.args.get("telefono", "").strip()
    if not telefono:
        return "Falta el telefono. Usa: /conectar?telefono=+51942978154"
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        client = TelegramClient('sesion_puente', API_ID, API_HASH)
        loop.run_until_complete(client.connect())
        
        # Enviamos el código a tu Telegram
        loop.run_until_complete(client.send_code_request(telefono))
        return "Codigo enviado a tu Telegram 💬. Ahora usa la ruta /codigo?numero=TU_CODIGO"
    except Exception as e:
        return f"Error enviando codigo: {str(e)}"

# 2. PASO DOS: Meter el código de 5 dígitos que te mandó Telegram
@app.route("/codigo")
def verificar_codigo():
    global client
    numero_codigo = request.args.get("numero", "").strip()
    if not numero_codigo:
        return "Falta el codigo. Usa: /codigo?numero=12345"
    if client is None:
        return "Primero debes enviar tu telefono en /conectar"
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(client.sign_in(code=numero_codigo))
        return "¡CONECTADO EXITOSAMENTE! 🎉 Tu cuenta ya es el puente. Ya puedes usar /tel"
    except Exception as e:
        return f"Error al verificar codigo: {str(e)}"

# 3. PASO TRES: Buscar el número en el bot Kronos
@app.route("/tel")
def buscar_telefono():
    numero = request.args.get("numero", "").strip()
    if not numero:
        return jsonify({"status": "error", "mensaje": "Falta el número de teléfono"})
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        local_client = TelegramClient('sesion_puente', API_ID, API_HASH)
        loop.run_until_complete(local_client.connect())
        
        if not loop.run_until_complete(local_client.is_user_authorized()):
            return jsonify({"status": "error", "mensaje": "No autorizado. Ve a /conectar primero."})
        
        comando = f"/tel {numero}"
        loop.run_until_complete(local_client.send_message(BOT_OBJETIVO, comando))
        
        loop.run_until_complete(asyncio.sleep(3)) 
        
        mensajes = loop.run_until_complete(local_client.get_messages(BOT_OBJETIVO, limit=1))
        respuesta_bot = mensajes[0].text if mensajes else "Sin respuesta"
        
        loop.run_until_complete(local_client.disconnect())

        return jsonify({
            "status": "success",
            "numero": numero,
            "respuesta_del_bot": respuesta_bot
        })
    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error en el puente: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
