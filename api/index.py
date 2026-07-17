from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "123456"

@app.route("/")
def inicio():
    return "API activa ✅"

@app.route("/telefono/<numero>")
def telefono(numero):

    clave = request.headers.get("X-API-Key")

    if clave != API_KEY:
        return jsonify({
            "error": "API KEY incorrecta"
        }), 401

    return jsonify({
        "status": "ok",
        "numero": numero,
        "mensaje": "Consulta realizada"
    })

def handler(request):
    return app(request.environ, lambda status, headers: None)
