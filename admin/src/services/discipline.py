from src.models.database import db
from src.models.club.discipline import Discipline


class DisciplineService:
    @classmethod
    def list_disciplines(cls):
        """Función que retorna la lista de todos los Usuarios de la Base de Datos"""
        return Discipline.query.all()

    @classmethod
    def create_discipline(
        cls,
        name,
        category,
        instructor_first_name,
        instructor_last_name,
        days_and_schedules,
        amount,
    ):
        """Función que instancia un Usuario, lo agrega a la Base de Datos y lo retorna"""
        discipline = Discipline(
            name,
            category,
            instructor_first_name,
            instructor_last_name,
            days_and_schedules,
            amount,
        )
        db.session.add(discipline)
        db.session.commit()

    @classmethod
    def find_discipline(cls, name, category):
        return Discipline.query.filter_by(name=name, category=category, deleted=False).first()
