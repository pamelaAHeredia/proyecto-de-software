import datetime

import jwt
from flask import Blueprint, current_app, jsonify, make_response, request
from flask_cors import cross_origin

from src.services.discipline import DisciplineService
from src.services.member import MemberService
from src.services.user import UserService
from src.services.utils import verify_pass
from src.web.helpers.api import token_required

_member_service = MemberService()
_user_service = UserService()
_discipline_service = DisciplineService()
private_api_blueprint = Blueprint("private_api", __name__, url_prefix="/api")


@cross_origin
@private_api_blueprint.get("/me/disciplines")
@token_required
def discipline_list(current_user):
    disciplines = []
    members = current_user.members.all()
    disciplines = _discipline_service.api_members_disciplines(members=members)

    return jsonify(disciplines), 200


@cross_origin
@private_api_blueprint.post("/auth/")
def auth():
    auth_data = request.authorization

    print(auth_data)

    if not auth_data or not auth_data.username or not auth_data.password:
        return make_response(
            "No se pudo verificar",
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
@private_api_blueprint.get("/me/user_jwt")
@token_required
def user_jwt(current_user):
    user = {
        "username": current_user.username,
        "email": current_user.email,
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
    }
    return jsonify(user), 200
