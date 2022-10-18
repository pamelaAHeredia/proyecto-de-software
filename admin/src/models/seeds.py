from src.models import auth
from src.services.utils import hash_pass
from src.services.member import MemberService
from src.services.discipline import DisciplineService
from src.services.user import UserService


def run():
    """Hacemos un seed de informacion en la BBDD"""

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
        "pays_destroy",
    ]

    members_perms = [auth.create_permission(perm) for perm in perms]

    role_1 = auth.create_role(name="Administrador")
    role_1.permissions = members_perms
    role_2 = auth.create_role(name="Operador")
    role_3 = auth.create_role(name="Socio")

    service = DisciplineService()

    # discipline = service.create_discipline(
    #     name="Basquet",
    #     category="Pre mini",
    #     instructor_first_name="Juan",
    #     instructor_last_name="De Los Palotes",
    #     days_and_schedules="Lunes 18 a 19 miercoles 18 a 19 jueves 18 a 19",
    #     registration_quota=50,
    #     amount=600.00,
    # )

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

    admin = service.create_user(
        email="admin@gmail.com",
        username="admin",
        password=hash_pass("admin"),
        is_active=True,
        first_name="José",
        last_name="Administrador",
        blocked=False,
        #roles=[role_1],
    )

    user_1 = service.create_user(
        email="carlos.solari@gmail.com",
        username="Indio49",
        password=hash_pass("carlos.solari@gmail.com"),
        is_active=True,
        first_name="Carlos",
        last_name="Solari",
        blocked=False,
        #roles=[role_1],
    )

    user_2 = service.create_user(
        email="skay.beili@gmail.com",
        username="Skay52",
        password=hash_pass("skay.beili@gmail.com"),
        is_active=True,
        first_name="Eduardo",
        last_name="Beilinson",
        blocked=False,
        #roles=[role_2],
    )

    user_3 = service.create_user(
        email="rockera75@gmail.com",
        username="Rocka75",
        password=hash_pass("rockera75@gmail.com"),
        is_active=False,
        first_name="Nadia",
        last_name="Benitez",
        blocked=False,
    )
#         roles=[role_2, role_3],