from src.models.database import db
from src.models.club.member import Member


def list_members():
    """Función que retorna la lista de todos los Socios de la Base de Datos"""
    return Member.query.all()

def create_member(**kwargs):
    """Función que instancia un Socio, lo agrega a la Base de Datos y lo retorna"""
    member = Member(**kwargs)
    db.session.add(member)
    db.session.commit()
    return member