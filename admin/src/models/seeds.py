from src.models import auth


def run():
    role_1 = auth.create_role(name='Administrador')
    role_2 = auth.create_role(name='Operador')
    role_3 = auth.create_role(name='Socio')
    
    user_1 = auth.create_user(
        email="carlos.solari@gmail.com",
        username="Indio49",
        password="carlos.solari@gmail.com",
        first_name="Carlos",
        last_name="Solari",
        roles=[role_1]
    )

    user_2 = auth.create_user(
        email="skay.beili@gmail.com",
        username="Skay52",
        password="skay.beili@gmail.com",
        first_name="Eduardo",
        last_name="Beilinson",
        roles=[role_2]
    )

    user_3 = auth.create_user(
        email="rockera75@gmail.com",
        username="Rocka75",
        password="rockera75@gmail.com",
        is_active=False,
        first_name="Nadia",
        last_name="Benitez",
        roles=[role_2, role_3]
    )
