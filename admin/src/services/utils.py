from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


def hash_pass(password):
    """Recibe un password de texto plano y lo retorna hasheado"""   
    return generate_password_hash(password)


def verify_pass(stored_password, provided_password):
    """Recibe un password hasheado y un password de texto plano y chequea si son iguales
    retornando un booleano"""   
    return check_password_hash(stored_password, provided_password)
