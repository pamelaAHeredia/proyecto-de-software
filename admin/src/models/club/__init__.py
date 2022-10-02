from src.models.database import db
from src.models.club.discipline import Discipline



def list_disciplines():
    """Función que retorna la lista de todos los Usuarios de la Base de Datos"""
    return Discipline.query.all()


def create_discipline(**kwargs):
    """Función que instancia un Usuario, lo agrega a la Base de Datos y lo retorna"""
    discipline = Discipline(**kwargs)
    db.session.add(discipline)
    db.session.commit()
    return discipline