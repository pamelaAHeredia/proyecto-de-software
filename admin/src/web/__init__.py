from flask import Flask, render_template
from flask_session import Session
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf


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
from src.api.club.public_api import public_api_blueprint
from src.api.club.private_api import private_api_blueprint
from src.web.controllers.license import license_blueprint

csrf = CSRFProtect()

def create_app(env="production", static_folder="static"):

    """Metodo de inicializacion de la aplicacion"""

    app = Flask(__name__, static_folder=static_folder)
    csrf.init_app(app)
      
    # Carga configuracion
    app.config.from_object(config[env])
    # CORS(app, origins=app.config["PORTAL_URL"])
    
    

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
    app.register_blueprint(public_api_blueprint)
    app.register_blueprint(private_api_blueprint)
    app.register_blueprint(license_blueprint)

    #Saco el csrf para el front de vue
    csrf.exempt(private_api_blueprint)

    # Handler Error
    # app.register_error_handler(400, handlers.bad_request)
    app.register_error_handler(401, handlers.unauthorized)
    app.register_error_handler(403, handlers.forbidden)
    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)

    # Jinja
    app.jinja_env.globals.update(is_authenticated=auth.is_authenticated)
    app.jinja_env.globals.update(is_administrator=auth.is_administrator_template)
    app.jinja_env.globals.update(is_member=auth.is_member_template)
    app.jinja_env.globals.update(is_operator=auth.is_operator_template)
    app.jinja_env.globals.update(is_admin=auth.is_admin)
    app.jinja_env.globals.update(can_do_it=auth.can_do_it)
    # app.jinja_env.globals.update(is_admin=auth.is_admin)

    # Jinja datetime formater
    @app.template_filter()
    def format_datetime(value, format="dmahm"):
        if format == "dmahm":
            format = "%d-%m-%Y %H:%M"
        elif format == "dma":
            format = "%d-%m-%Y"
        return value.strftime(format)

    @app.template_filter()
    def format_currency(value):
        currency = "${:,.2f}".format(value)
        return currency.replace(",", "~").replace(".", ",").replace("~", ".")

    @app.template_filter()
    def format_thousand(value):
        formato = format(int(value), ",")
        return formato.replace("," , ".")

    # Command Flask
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seeds")
    def seedsdb():
        seeds.run()

    # @app.after_request
    # def set_xsrf_cookie(response):
    #     response.set_cookie('csrf_token', generate_csrf())
    #     return response
    return app
