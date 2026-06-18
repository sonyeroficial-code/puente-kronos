from flask import Flask, request, jsonify

app = Flask(__name__)

BASE = {
    "942978154": "prueba,
    "999999999": "Juan "
}

@app.route("/")
def home():
    return "Servidor funcionando ✅"

@app.route("/buscar")
def buscar():
    numero = request.args.get("numero", "").strip()

    titular = BASE.get(numero)

    if titular:
        return jsonify({
            "ok": True,
            "numero": numero,
            "titular": titular
        })

    return jsonify({
        "ok": False,
        "numero": numero,
        "mensaje": "No encontrado"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
