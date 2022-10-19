from src.models import auth
from src.services.utils import hash_pass
from src.services.member import MemberService
from src.services.discipline import DisciplineService
from src.services.user import UserService


def run():
    """Hacemos un seed de informacion en la BBDD"""

    service = DisciplineService()

    discipline = service.create_discipline(
        name="Basquet",
        category="Pre mini",
        instructor_first_name="Juan",
        instructor_last_name="De Los Palotes",
        days_and_schedules="Lunes 18 a 19 miercoles 18 a 19 jueves 18 a 19",
        registration_quota=50,
        amount=600.00,
        is_active=True
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

    perms = [
        "member_index",
        "member_create",
        "member_destroy",
        "member_update",
        "member_show",
        "discipline_index",
        "discipline_create",
        "discipline_destroy",
        "discipline_update",
        "discipline_show",
        "pays_index",
        "pays_show",
        "pays_import",
        "pays_destroy"
    ]

    member_perms = [service.create_permission(perm) for perm in perms]
    

    role_1 = service.create_role(name="Administrador")
    role_1.permissions = member_perms
    role_2 = service.create_role(name="Operador")
    role_3 = service.create_role(name="Socio")


    admin = service.create_user(
        email="admin@gmail.com",
        username="admin",
        password=hash_pass("admin"),
        first_name="José",
        last_name="Administrador",
        roles=[role_1],
    )

    user_1 = service.create_user(
        email="operador@mail.com",
        username="operador",
        password=hash_pass("operador"),
        first_name="Carlos",
        last_name="operador",
        roles=[role_2],
    )

    user_2 = service.create_user(
        email="socio@mail.com",
        username="socio",
        password=hash_pass("socio"),
        first_name="Eduardo",
        last_name="socio",
        roles=[role_2],
    )

    user_3 = service.create_user(
        email="socioperador@mail.com",
        username="socioperador",
        password=hash_pass("socioperador"),
        first_name="Nadia",
        last_name="Socioperador",
        roles=[role_2, role_3]
    )
