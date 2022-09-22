from flask import Flask, render_template
from src.web.helpers import handlers

issues = [
    {
        "id": 1,
        "user": "José",
        "title": "Mi computadora no funciona.",
        "description": "Mi departamente me compró una nueva computadora y necesito configurarla con todos mis emails y documentos de mi vieja computadora.",
        "status": "new",
    },
    {
        "id": 2,
        "user": "María",
        "title": "No puedo obtener mis emails.",
        "description": "Estoy tratando de acceder a mi correo desde casa, pero no puedo obtenerlos. Estoy tratando con Outlook en mi casa pero en la oficina tengo Thunderbird.",
        "status": "in_progress",
    },
    {
        "id": 3,
        "user": "Rubén",
        "title": "No puedo imprimir",
        "description": "Cada vez que trato de imprimir mi presentación el programa se cierra. Esto sólo me pasa con PowerPoint en Word puedo imprimir. Ya me aseguré que la impresora está prendida. Tengo una HP LaserJet 5.",
        "status": "done",
    },
]


def create_app(static_folder="static"):
    app = Flask(__name__, static_folder=static_folder)

    # Define home
    @app.route("/")
    def home():
        contenido = "mundo"
        return render_template('index.html', contenido=contenido)

    @app.route("/personas")
    def personas():
        contenido = "personas"
        return render_template('index.html', contenido=contenido)

    @app.route("/personas/<string:nombre>")
    def persona(nombre):
        nombre = nombre.capitalize()
        contenido = nombre
        return render_template('index.html', contenido=contenido)

    @app.route("/issues/")
    def issues_index():
        return render_template("issues/index.html", issues=issues)

    # Handler Error
    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)

    return app