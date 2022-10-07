from src.models import auth
from src.services.utils import hash_pass
from src.models import club
from src.services import discipline


def run(): 
    """Hacemos un seed de informacion en la BBDD"""
    
    discipline_service = discipline.DisciplineService()
    
    perms = [
        "member_index",
        "member_new",
        "member_destroy",
        "member_update",
        "member_show",
        "discipline_index",
        "discipline_new",
        "discipline_destroy",
        "discipline_update",
        "discipline_show",
    ]

    members_perms = [auth.create_permission(perm) for perm in perms]

    role_1 = auth.create_role(name="Administrador")
    role_1.permissions = members_perms
    role_2 = auth.create_role(name="Operador")
    role_3 = auth.create_role(name="Socio")

    user_1 = auth.create_user(
        email="carlos.solari@gmail.com",
        username="Indio49",
        password=hash_pass("carlos.solari@gmail.com"),
        first_name="Carlos",
        last_name="Solari",
        roles=[role_1],
    )

    user_2 = auth.create_user(
        email="skay.beili@gmail.com",
        username="Skay52",
        password=hash_pass("skay.beili@gmail.com"),
        first_name="Eduardo",
        last_name="Beilinson",
        roles=[role_2],
    )

    user_3 = auth.create_user(
        email="rockera75@gmail.com",
        username="Rocka75",
        password=hash_pass("rockera75@gmail.com"),
        is_active=False,
        first_name="Nadia",
        last_name="Benitez",
        roles=[role_2, role_3],
    )
    discipline_service.create_discipline(
        name="Basquet",
        category="Pre mini",
        instructor_first_name = "Juan",
        instructor_last_name = "De Los Palotes",
        days_and_schedules = "Lunes 18 a 19 miercoles 18 a 19 jueves 18 a 19",
        amount = 600.00
    )