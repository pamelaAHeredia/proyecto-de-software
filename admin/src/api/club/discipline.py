from flask import Blueprint
from flask import jsonify

from src.services.discipline import DisciplineService


service = DisciplineService()
discipline_api_blueprint = Blueprint("dicipline_api", __name__, url_prefix="/api/club")


@discipline_api_blueprint.get("/disciplines")
def discipline_list():
    disciplines = service.api_get_disciplines()
    return jsonify(disciplines), 200
