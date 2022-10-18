from decimal import Decimal
from typing import List, Optional
import datetime


from src.models.database import db
from src.models.club.discipline import Discipline
from src.models.club.membership import Membership
from src.models.club.tariff import Tariff
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
        return Discipline.query.order_by(Discipline.id)

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
        disciplines = self.list_disciplines()
        return Paginator(disciplines, page, items_per_page, endpoint)

    def create_discipline(
        self,
        name: str,
        category: str,
        instructor: str,
        days_and_schedules: str,
        registration_quota: int,
        pays_per_year: int,
        amount: Decimal,
        is_active: bool,
    ) -> Discipline:
        """Función que instancia una Disciplina, la agrega a la Base de Datos y la retorna

        Args:
           name: Nombre de la disciplina.
           category: Categoria de la disciplina.
           instructor_first_name: Nombre del instructor que dicta la disciplina.
           instructor_last_name: Apellido del instructor que dicta la disciplina.
           days_and_schedule: Días y horarios en que se da la disciplina.
           amount: Monto a pagar por practicar la disciplina.
           is_active: ¿La disciplina esta activa?

        Returns:
           Una disciplina.
        """

        if 0 in [amount, pays_per_year]:
            raise database.MinValueValueError()

        if registration_quota < 0:
            raise database.MinValueValueError(
                message="El cupo no puede ser menor que 1"
            )

        discipline = self.find_discipline(name=name, category=category)
        
        
        if not discipline:
            tariff = Tariff(amount=amount)
            
            discipline = Discipline(
                name,
                category,
                instructor,
                days_and_schedules,
            )
            
            membership = Membership(is_active=is_active, registration_quota=registration_quota, pays_per_year=pays_per_year, discipline=discipline)
            tariff.membership = membership
            db.session.add_all([tariff, discipline, membership])
            db.session.commit()
        else:
            raise database.ExistingData(message="ya existen en la base de datos")
        return discipline

    def update_discipline(
        self,
        id: int,
        name: str,
        category: str,
        instructor: str,
        days_and_schedules: str,
        registration_quota: int,
        pays_per_year: int,
        amount: Decimal,
        is_active: bool,
    ) -> Discipline:
        """Función que instancia una Disciplina, la modifica en la Base de Datos y la retorna

        Args:
           id: Identificador unico de la disciplina.
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
            raise database.MinValueValueError()

        if registration_quota < 0:
            raise database.MinValueValueError(
                message="El cupo no puede ser menor que 1"
            )

        discipline_to_update = self.find_discipline(id=id)

        if (
            discipline_to_update.name != name
            or discipline_to_update.category != category
        ):
            discipline_in_db = self.find_discipline(name=name, category=category)
            if discipline_in_db:
                raise database.ExistingData(message="ya existen en la base de datos")

        discipline_to_update.name = name
        discipline_to_update.category = category
        discipline_to_update.instructor = instructor
        discipline_to_update.days_and_schedules = days_and_schedules
        discipline_to_update.pays_per_year = pays_per_year
        discipline_to_update.registration_quota = registration_quota
        discipline_to_update.is_active = is_active
        
        if discipline_to_update.amount!=amount:
            old_tarif = [t for t in discipline_to_update.membership.tariffs if t.date_to is None]
            if old_tarif:
                old_tarif[0].date_to = datetime.datetime.now()
            new_tarif = Tariff(amount=amount)
            new_tarif.membership = discipline_to_update.membership
        
        db.session.add_all([discipline_to_update, new_tarif])
        db.session.flush()
        db.session.commit()
        return discipline_to_update

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
            return Discipline.query.get(id)
        return Discipline.query.filter_by(name=name, category=category).first()
