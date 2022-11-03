from flask import Blueprint
from flask import jsonify

from src.services.member import MemberService
from src.services.discipline import DisciplineService


_member_service = MemberService()
_discipline_service = DisciplineService()
private_api_blueprint = Blueprint("private_api", __name__, url_prefix="/api")


@private_api_blueprint.get("/<user_id>/disciplines")
def discipline_list(user_id):
    disciplines = []
    members = _member_service.get_disciplines_subscribed(user_id)
    disciplines = _discipline_service.api_get_disciplines(members=members)

    return jsonify(disciplines), 200
