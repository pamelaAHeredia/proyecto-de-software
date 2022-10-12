from decimal import Decimal
from typing import List, Optional

from src.models.database import db
from src.models.club.discipline import Discipline
from src.errors import database
from src.services.paginator import Paginator


class DisciplineService:
    """
    Clase que representa el servicio para el manejo de disciplinas.
    Implementa el patron singleton para que solo se instancie una vez en el sistema.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DisciplineService, cls).__new__(cls)
        return cls._instance

    def list_disciplines(self) -> List[Discipline]:
        """Función que retorna la lista de todas las disciplinas cargadas en la Base de Datos

        Returns:
          Lista de disciplinas

        """
        return Discipline.query.all()

    def list_paginated_disciplines(
        self, page: int, items_per_page: int, endpoint: str
    ) -> Paginator:
        """Función que retorna el paginador con las disciplinas cargadas en el sistema.

        Args:
           page: Numero de pagina.
           items_per_page: cantidad de registros por página.
           endpoint: endpoint para el armado del url_for.

        Returns:
           Un paginador.
        """
        disciplines = Discipline.query
        return Paginator(disciplines, page, items_per_page, endpoint)

    def create_discipline(
        self,
        name: str,
        category: str,
        instructor_first_name: str,
        instructor_last_name: str,
        days_and_schedules: str,
        amount: Decimal,
    ) -> Discipline:
        """Función que instancia una Disciplina, la agrega a la Base de Datos y la retorna

        Args:
           name: Nombre de la disciplina.
           category: Categoria de la disciplina.
           instructor_first_name: Nombre del instructor que dicta la disciplina.
           instructor_last_name: Apellido del instructor que dicta la disciplina.
           days_and_schedule: Días y horarios en que se da la disciplina.
           amount: Monto a pagar por practicar la disciplina.

        Returns:
           Una disciplina.
        """

        if amount < 0:
            raise database.AmountValueError()

        discipline = self.find_discipline(name=name, category=category)
        if not discipline:
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
        else:
            raise database.ExistingData(message="ya existen en la base de datos")
        return discipline

    def find_discipline(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Discipline:
        """Función que busca una disciplina por id o nombre y categoria y la retorna.


        Args:
           id: Número identificador de la disciplina.
           name: Nombre de la disciplina a buscar.
           category: Categoria de la disciplina a buscar.

        Returns:
           Una disciplina.
        """
        if id:
            return Discipline.query.filter_by(id=id).first()
        return Discipline.query.filter_by(name=name, category=category).first()

    # def find_discipline(self, id: int) -> Discipline:
    #     """Función que busca una disciplina por id y la retorna.

    #     Args:
    #        id: Id de la disciplina a buscar.

    #     Returns:
    #        Una disciplina
    #     """
    #     return Discipline.query.filter_by(id=id).first()
