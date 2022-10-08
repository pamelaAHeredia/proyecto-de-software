from src.models import auth
from src.services.member import MemberService
from src.services.discipline import DisciplineService
from src.services.user import UserService


def run():
    """Hacemos un seed de informacion en la BBDD"""
    perms = [
        "member_index",
        "member_new",
        "member_destroy",
        "member_update",
        "member_show",
    ]

    members_perms = [auth.create_permission(perm) for perm in perms]

    role_1 = auth.create_role(name="Administrador")
    role_1.permissions = members_perms
    role_2 = auth.create_role(name="Operador")
    role_3 = auth.create_role(name="Socio")

    service = DisciplineService()

    discipline = service.create_discipline(
        name="Basquet",
        category="Pre mini",
        instructor_first_name="Juan",
        instructor_last_name="De Los Palotes",
        days_and_schedules="Lunes 18 a 19 miercoles 18 a 19 jueves 18 a 19",
        amount=600.00,
    )

    service = MemberService()

    member_1 = service.create_member(
        first_name="César",
        last_name="Amiconi",
        document_type="DNI",
        document_number="24953316",
        gender="M",
        address="La Plata",
    )

    service = UserService()

    user_1 = service.create_user(
        email="carlos.solari@gmail.com",
        username="Indio49",
        password="carlos.solari@gmail.com",
        first_name="Carlos",
        last_name="Solari",
        roles=[role_1],
    )

    user_2 = service.create_user(
        email="skay.beili@gmail.com",
        username="Skay52",
        password="skay.beili@gmail.com",
        first_name="Eduardo",
        last_name="Beilinson",
        roles=[role_2],
    )

    user_3 = auth.create_user(
        email="rockera75@gmail.com",
        username="Rocka75",
        password="rockera75@gmail.com",
        is_active=False,
        first_name="Nadia",
        last_name="Benitez",
        roles=[role_2, role_3],
    )
