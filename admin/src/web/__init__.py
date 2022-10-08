from flask import Flask, render_template, request, flash

from src.web.helpers import handlers
from src.models import database
from src.models import seeds
from src.web.controllers.user import user_blueprint
from src.web.controllers.member import member_blueprint
from src.web.controllers.discipline import discipline_blueprint
from src.web.config import config



def create_app(env="development", static_folder="static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])

    app.secret_key = "secret key"

    database.init_app(app)

    # Define home
    @app.route("/")
    def home():
        contenido = "mundo"
        return render_template('index.html', contenido=contenido)

   
    # Registro de Blueprints
    app.register_blueprint(user_blueprint)
    app.register_blueprint(member_blueprint)
    app.register_blueprint(discipline_blueprint)

    # Handler Error
    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(500, handlers.internal_server_error)
    
    # Command Flask
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seeds")
    def seedsdb():
        seeds.run()
        
    return app