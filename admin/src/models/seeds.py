import email
from src.models import auth


def run():
    user1= auth.create_user(
        email="carlos.solari@gmail.com",
        username="Indio49",
        password="carlos.solari@gmail.com",
        first_name="Carlos",
        last_name="Solari"
    )
    user1= auth.create_user(
        email="skay.beili@gmail.com",
        username="Skay52",
        password="skay.beili@gmail.com",
        first_name="Eduardo",
        last_name="Beilinson"
    )
    user1= auth.create_user(
        email="rockera75@gmail.com",
        username="Rocka75",
        password="rockera75@gmail.com",
        is_active=False,
        first_name="Nadia",
        last_name="Benitez"
    )
