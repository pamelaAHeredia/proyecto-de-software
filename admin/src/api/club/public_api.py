from flask import Blueprint
from flask import jsonify

from src.services.discipline import DisciplineService
from src.services.settings import SettingsService


service = DisciplineService()
settings = SettingsService()
public_api_blueprint = Blueprint("club_api", __name__, url_prefix="/api/club")


@public_api_blueprint.get("/disciplines")
def discipline_list():
    disciplines = service.api_disciplines()
    return jsonify(disciplines), 200

@public_api_blueprint.get("/informacion")
def get_info():
    info = settings.get_contact_info()
    return jsonify({'contact_info':info}), 200
