from flask import Blueprint
from flask import jsonify
from flask_cors import cross_origin 

from src.services.discipline import DisciplineService
from src.services.settings import SettingsService
from src.services.member import MemberService


service = DisciplineService()
settings = SettingsService()
member_service = MemberService()
public_api_blueprint = Blueprint("club_api", __name__, url_prefix="/api/club")

# @cross_origin
@public_api_blueprint.get("/disciplines")
def discipline_list():
    disciplines = service.api_disciplines()
    return jsonify(disciplines), 200

@public_api_blueprint.get("/informacion")
def get_info():
    info = settings.get_contact_info()
    return jsonify({'contact_info':info}), 200

@public_api_blueprint.get("/members_by_gender")
def members_by_gender():
    quantitys = member_service.api_members_by_gender()
    return jsonify(quantitys), 200

@public_api_blueprint.get("/members_by_discipline")
def members_by_discipline():
    data = service.api_members_by_discipline()
    return jsonify(data), 200

@public_api_blueprint.get("/members_by_activated")
def members_by_activated():
    data = member_service.api_members_by_activated()
    return jsonify(data), 200