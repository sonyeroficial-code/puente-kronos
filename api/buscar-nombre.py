from flask import jsonify, request
import requests
import os

def buscar_nombre(request):

    numero = request.args.get("numero")

    if not numero:
        return jsonify({
            "ok": False,
            "mensaje": "Falta número"
        })

    url = f"https://distant-informative-settle-expense.trycloudflare.com/telefono/{numero}"

    headers = {
        "X-API-Key": os.environ.get("API_KEY")
    }

    respuesta = requests.get(url, headers=headers)

    return jsonify(respuesta.json())
