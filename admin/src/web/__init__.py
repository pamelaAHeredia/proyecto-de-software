from flask import Flask, render_template
from flask_session import Session

from src.web.helpers import handlers
from src.web.helpers import auth
from src.models import database
from src.models import seeds
from src.web.controllers.user import user_blueprint
from src.web.controllers.member import member_blueprint
from src.web.controllers.discipline import discipline_blueprint
from src.web.controllers.settings import settings_blueprint
from src.web.controllers.suscription import suscription_blueprint
from src.web.controllers.movement import movement_blueprint
from src.web.config import config
from src.web.controllers.auth import auth_blueprint
from src.api.club.discipline import discipline_api_blueprint


def create_app(env="development", static_folder="static"):

    """Metodo de inicializacion de la aplicacion"""

    app = Flask(__name__, static_folder=static_folder)
   
    # Carga configuracion
    app.config.from_object(config[env])

    # app.secret_key = "secret key"

    # Inicia base de datos
    database.init_app(app)
    
    # Configura sesion de backend
    Session(app)

    # Define home
    @app.route("/")
    def home():
        contenido = "mundo"
        return render_template("index.html", contenido=contenido)

    # Registro de Blueprints
    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(member_blueprint)
    app.register_blueprint(discipline_blueprint)
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(suscription_blueprint)
    app.register_blueprint(movement_blueprint)
    app.register_blueprint(discipline_api_blueprint)

    # Handler Error
    app.register_error_handler(401, handlers.unauthorized)
    app.register_error_handler(403, handlers.forbidden)
    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)

    # Jinja
    app.jinja_env.globals.update(is_authenticated=auth.is_authenticated)
    app.jinja_env.globals.update(is_administrator=auth.is_administrator_template)
    app.jinja_env.globals.update(is_operator=auth.is_operator_template)

    #Jinja datetime formater    
    @app.template_filter()
    def format_datetime(value, format='dma'):
        if format == 'dmahm':
            format="%d-%m-%Y %H:%M"
        elif format == 'dma':
            format="%d-%m-%Y"
        return value.strftime(format)

    # Command Flask
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seeds")
    def seedsdb():
        seeds.run()

    return app