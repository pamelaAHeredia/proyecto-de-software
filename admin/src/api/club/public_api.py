from flask import Blueprint
from flask import jsonify

from src.services.discipline import DisciplineService


service = DisciplineService()
public_api_blueprint = Blueprint("club_api", __name__, url_prefix="/api/club")


@public_api_blueprint.get("/disciplines")
def discipline_list():
    disciplines = service.api_disciplines()
    return jsonify(disciplines), 200
