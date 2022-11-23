import datetime

import jwt
from flask import Blueprint, current_app, jsonify, make_response, request
from flask_cors import cross_origin

from src.services.discipline import DisciplineService
from src.services.member import MemberService
from src.services.user import UserService
from src.services.movement import MovementService
from src.services.discipline import DisciplineService
from src.services.utils import verify_pass
from src.web.helpers.api import token_required

_member_service = MemberService()
_user_service = UserService()
_discipline_service = DisciplineService()
_movements_service = MovementService()

private_api_blueprint = Blueprint("private_api", __name__, url_prefix="/api")


@cross_origin
@private_api_blueprint.get("/me/disciplines/<int:id_member>")
@token_required
def discipline_list(current_user, id_member):
    disciplines = []

    member = _member_service.get_by_membership_number(id_member)
    if member.user==current_user:
        disciplines = _discipline_service.api_members_disciplines(member=member)
    else:
        return jsonify({"message": "El socio no pertenece al usuario"}), 401

    return jsonify(disciplines), 200


@cross_origin
@private_api_blueprint.get("")
@token_required
def member_movements(current_user, id_member):
    member = _member_service.get_by_membership_number(id_member)
    if member.user==current_user:
        movements = _movements_service.api_member_movements(member=member, movement_type="C")
    else:
        return jsonify({"message": "El socio no pertenece al usuario"}), 401

    return jsonify(movements), 200

@cross_origin
@private_api_blueprint.post("/auth")
def auth():
    auth_data = request.authorization

    if not auth_data or not auth_data.username or not auth_data.password:
        return make_response(
            {"message":"No se pudo verificar"},
            401,
            {"WWW-Authenticate": 'Basic realm="Login requerido!"'},
        )
    user = _user_service.find_user_byUsername(auth_data.username)

    if not user:
        return make_response(
            "Usuario incorrecto",
            401,
            {"WWW-Authenticate": 'Basic realm="Login requerido!"'},
        )
    if not user.is_active:
        return make_response(
            "Usuario inactivo",
            401,
            {"WWW-Authenticate": 'Basic realm="Login requerido!"'},
        )

    if verify_pass(user.password, auth_data.password):
        token = jwt.encode(
            {
                "user": user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            current_app.secret_key,
            algorithm="HS256",
        )
        return jsonify({"token": token})

    return make_response(
        "Contraseña incorrecta",
        401,
        {"WWW-Authenticate": 'Basic realm="Login requerido!"'},
    )

@cross_origin
@private_api_blueprint.post("/me/payment/<int:id_member>")
# @token_required
def member_pay(id_member):
    receipt = request.form.files('image')
    print(receipt)

@cross_origin
@private_api_blueprint.get("/me/user_jwt")
@token_required
def user_jwt(current_user):
    user_data = {
        "username": current_user.username,
        "email": current_user.email,
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
    }
    list_members = _user_service.api_list_members(current_user.id)
    user_data["members"] = list_members

    return jsonify(user_data), 200
