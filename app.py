from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor funcionando ✅"

@app.route("/buscar")
def buscar():
    numero = request.args.get("numero", "")
    return jsonify({
        "ok": True,
        "numero": numero,
        "mensaje": "Consulta recibida"
    })

app.run(host="0.0.0.0", port=5000)
# actualizado
