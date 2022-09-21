from flask import Flask, render_template


def create_app(static_folder="static"):
    app = Flask(__name__)

    # Define home
    @app.route("/")
    def hello_world():
        return render_template('index.html')

    @app.route("/personas")
    def personas():
        mensaje = '<!DOCTYPE html>'
        mensaje += '<html lang="es"> '
        mensaje += '<head>'
        mensaje += '</head>'
        mensaje += '<body>'
        mensaje += 'Hola personas!'
        mensaje += '</body>'
        mensaje += '</html>'
        return mensaje

    @app.route("/personas/<string:nombre>")
    def persona(nombre):
        nombre = nombre.capitalize()
        mensaje = '<!DOCTYPE html>'
        mensaje += '<html lang="es"> '
        mensaje += '<head>'
        mensaje += '</head>'
        mensaje += '<body>'
        mensaje += f"Hola {nombre}"
        mensaje += '</body>'
        mensaje += '</html>'
        return mensaje

    return app
