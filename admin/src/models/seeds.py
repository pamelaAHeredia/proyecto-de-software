from src.models import auth
from src.services.utils import hash_pass
from src.services.member import MemberService
from src.services.membership import MembershipService
from src.services.discipline import DisciplineService
from src.services.settings import SettingsService
from src.services.user import UserService


def run():
    """Hacemos un seed de informacion en la BBDD"""

   
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
        "pays_destroy",
        "suscription_index",
        "suscription_create",
        "suscription_destroy",
        "suscription_update",
        "suscription_show",
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
        roles=[role_2, role_3],
    )

    service = SettingsService()
    service.load_settings(5, True, "Correo", "pagos", 600, 10)
    service = MembershipService()
    service.create_social_membership()

    service = MemberService()

    member_1 = service.create_member(
        first_name="César",
        last_name="Amiconi",
        document_type="DNI",
        document_number="24953316",
        gender="M",
        address="La Plata",
    )

    member_3 = service.create_member(
        first_name="Nemo",
        last_name="Nobody",
        document_type="DNI",
        document_number="87654321",
        gender="M",
        address="La Plata",
    )
