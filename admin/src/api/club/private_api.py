import datetime
from flask import current_app, Blueprint
from flask import jsonify, request, make_response
from flask_cors import cross_origin 
import jwt
 

from src.services.utils import verify_pass
from src.services.member import MemberService
from src.services.user import UserService
from src.services.discipline import DisciplineService
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
@private_api_blueprint.post("/auth")
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
            "No se pudo verificar",
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
        "No se pudo verificar",
        401,
        {"WWW-Authenticate": 'Basic realm="Login requerido!"'},
    )

@cross_origin
@private_api_blueprint.get("/me/payments")
@token_required
def payments_list(current_user):
    #payments = []
    #members = current_user.members.all()
    #disciplines = _discipline_service.api_members_disciplines(members=members)

    return jsonify(current_user), 200