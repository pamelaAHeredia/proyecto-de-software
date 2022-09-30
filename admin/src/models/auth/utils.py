from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


def hash_pass(password):

    return generate_password_hash(password) 


def verify_pass(stored_password, provided_password):

    return check_password_hash(stored_password, provided_password)

