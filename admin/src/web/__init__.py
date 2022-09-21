from flask import Flask, render_template

def create_app(static_folder="static"):
    app = Flask(__name__)

    # Define home
    @app.route("/")
    def hello_world():
        contenido = "mundo!"
        return render_template('index.html', contenido=contenido)

    @app.route("/personas")
    def personas():
        contenido = "personas!"
        return render_template('index.html', contenido=contenido)

    @app.route("/personas/<string:nombre>")
    def persona(nombre):
        nombre = nombre.capitalize()
        contenido = nombre
        return render_template('index.html', contenido=contenido)

    return app
