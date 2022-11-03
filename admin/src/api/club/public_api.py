from flask import Blueprint
from flask import jsonify

from src.services.discipline import DisciplineService


service = DisciplineService()
club_api_blueprint = Blueprint("club_api", __name__, url_prefix="/api/club")


@club_api_blueprint.get("/disciplines")
def discipline_list():
    disciplines = service.api_get_disciplines()
    print(type(disciplines))
    return jsonify(disciplines), 200
