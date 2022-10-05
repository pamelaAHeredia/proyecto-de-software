from decimal import Decimal

from src.models.database import db
from src.models.club.discipline import Discipline
from src.errors import database


class DisciplineService:
    """Clase que representa el servicio para el manejo de disciplinas

    Returns:
        _type_: _description_
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DisciplineService, cls).__new__(cls)
        return cls._instance
    
    def list_disciplines(self):
        """Función que retorna la lista de todas las disciplinas cargadas en la Base de Datos"""
        return Discipline.query.all()

    def create_discipline(
        self,
        name,
        category,
        instructor_first_name,
        instructor_last_name,
        days_and_schedules,
        amount,
    ):
        """Función que instancia una Disciplina, la agrega a la Base de Datos y la retorna"""
        
        

        if Decimal(amount) < 0:
            raise database.AmountValueError()

        discipline = self.find_discipline(name, category)    
        if not discipline:
            discipline = Discipline(
                name,
                category,
                instructor_first_name,
                instructor_last_name,
                days_and_schedules,
                Decimal(amount)
            )
            db.session.add(discipline)
            db.session.commit()
        else:
            raise database.ExistingData(message="ya existen en la base de datos")
        


    def find_discipline(self, name, category):
        return Discipline.query.filter_by(
            name=name, category=category
        ).first()
