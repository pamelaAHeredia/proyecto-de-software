from decimal import Decimal
from typing import List, Optional
import datetime

from src.models.database import db
from src.models.club.discipline import Discipline, DisciplineSchema
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
    _discipline_schema = DisciplineSchema()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DisciplineService, cls).__new__(cls)
        return cls._instance

    def api_disciplines(self):

        disciplines = (
            Discipline.query.filter(Discipline.membership.has(is_active=True))
            .order_by(Discipline.id)
            .all()
        )

        return self._discipline_schema.dump(disciplines, many=True)

    def api_members_disciplines(self, member):
        disciplines = []
        data = dict()
        for suscription in member.active_suscriptions:
            if suscription.membership_id!=1:
                disciplines.append(suscription.membership.discipline)
            data["disciplines"] = self._discipline_schema.dump(disciplines, many=True)
        return data

    def active(self, discipline_id):
        discipline = self.find_discipline(id=discipline_id)
        return discipline.is_active

    def membership(self, discipline_id):
        discipline = self.find_discipline(id=discipline_id)
        return discipline.membership

    def list_disciplines(self) -> List[Discipline]:
        """Retorna todas las disciplinas

        Retorna todas las disciplinas cargadas en la Base de Datos.

        Returns:
            List[Discipline]: Una lista con todas las disciplinas
        """
        return Discipline.query.filter_by(deleted=False).order_by(Discipline.id)

    def list_paginated_disciplines(
        self, page: int, items_per_page: int, endpoint: str
    ) -> Paginator:
        """Retorna un paginador con las disciplinas.

        Args:
            page (int): Numero de pagina.
            items_per_page (int): cantidad de registros por página.
            endpoint (str): endpoint para el armado del url_for.

        Returns:
            Paginator: Un paginador.
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
        """Crea una disciplina.

        Método que instancia una Disciplina, la agrega a la Base de Datos y la retorna

        Args:
            name (str): Nombre de la disciplina.
            category (str): Categoria de la disciplina.
            instructor (str): Nombre/s de el/los instructor/es que dicta/n la disciplina.
            days_and_schedules (str): Días y horarios en que se da la disciplina.
            registration_quota (int): Cupo máximo de inscripciones.
            pays_per_year (int): Cantidad de cuotas a pagar por año.
            amount (Decimal): Monto a pagar por practicar la disciplina.
            is_active (bool): True si la disciplina esta activa.

        Raises:
            database.MinValueValueError: Los pagos por año son menores a 0.
            database.MinValueValueError: El cupo es menor a 0.
            database.MinValueValueError: El monto es menor a 0.
            database.ExistingData: La disciplina ya existe.

        Returns:
            Discipline: Una disciplina.
        """

        if pays_per_year <= 0:
            raise database.MinValueValueError(
                message="Los pagos por año deben ser mayores a 0."
            )

        if registration_quota <= 0:
            raise database.MinValueValueError(message="El cupo debe ser mayor a 0.")

        if amount <= 0:
            raise database.MinValueValueError(message="El monto debe ser mayor a 0.")

        discipline = self.find_discipline(name=name, category=category)

        if not discipline or discipline.deleted:
            tariff = Tariff(amount=amount)

            discipline = Discipline(
                name,
                category,
                instructor,
                days_and_schedules,
            )

            membership = Membership(
                is_active=is_active,
                registration_quota=registration_quota,
                pays_per_year=pays_per_year,
                discipline=discipline,
            )
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
        """Modifica una disciplina

        Método que instancia una Disciplina, la modifica en la Base de Datos y la retorna

        Args:
            id (int): Id de la disciplina a modificar.
            name (str): Nombre de la disciplina.
            category (str): Categoria de la disciplina.
            instructor (str): Nombre/s de el/los instructor/es que dicta/n la disciplina.
            days_and_schedules (str): Días y horarios en que se da la disciplina.
            registration_quota (int): Cupo máximo de inscripciones.
            pays_per_year (int): Cantidad de cuotas a pagar por año.
            amount (Decimal): Monto a pagar por practicar la disciplina.
            is_active (bool): True si la disciplina esta activa.

        Raises:
            database.MinValueValueError: Los pagos por año son menores a 0.
            database.MinValueValueError: El cupo es menor a 0.
            database.MinValueValueError: El monto es menor a 0.
            database.ExistingData: La disciplina ya existe.
            database.MinValueValueError: El nuevo cupo maximo es menor a la
              cantidad actual de registros.

        Returns:
            Discipline: Una disciplina.
        """
        discipline_to_update = self.find_discipline(id=id)

        if pays_per_year <= 0:
            raise database.MinValueValueError(
                message="Los pagos por año deben ser mayores a 0."
            )

        if registration_quota <= 0:
            raise database.MinValueValueError(message="El cupo debe ser mayor a 0.")

        if amount <= 0:
            raise database.MinValueValueError(message="El monto debe ser mayor a 0.")

        if (
            discipline_to_update.name != name
            or discipline_to_update.category != category
        ):
            discipline_in_db = self.find_discipline(name=name, category=category)
            if discipline_in_db and discipline_in_db.deleted is False:
                raise database.ExistingData(message="ya existen en la base de datos")

        if not discipline_to_update.membership.used_quota <= registration_quota:
            raise database.MinValueValueError(
                message="La cantidad de inscripciones activas son mayores al cupo nuevo"
            )

        if (
            discipline_to_update.membership.used_quota > 0
            and discipline_to_update.is_active
            and not is_active
        ):
            raise database.UpdateError(
                message="La disciplina tiene inscriptos. No se puede desactivar."
            )

        discipline_to_update.is_active = is_active
        discipline_to_update.name = name
        discipline_to_update.category = category
        discipline_to_update.instructor = instructor
        discipline_to_update.days_and_schedules = days_and_schedules
        discipline_to_update.pays_per_year = pays_per_year
        discipline_to_update.registration_quota = registration_quota

        if discipline_to_update.amount != amount:
            old_tarif = [
                t for t in discipline_to_update.membership.tariffs if t.date_to is None
            ]
            if old_tarif:
                old_tarif[0].date_to = datetime.datetime.now()
            new_tarif = Tariff(amount=amount)
            new_tarif.membership = discipline_to_update.membership
            db.session.add(new_tarif)

        # db.session.add(discipline_to_update)
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

    def delete_discipline(self, discipline_id):
        discipline = self.find_discipline(discipline_id)
        for suscription in discipline.membership.active_suscriptions:
            suscription.date_to = datetime.datetime.now()

        discipline.membership.is_active = False
        discipline.deleted = True
        db.session.commit()
        return discipline

    def api_members_by_discipline(self):

        disciplines = (
            Discipline.query.filter(Discipline.membership.has(is_active=True))
            .order_by(Discipline.name, Discipline.category)
            .all()
        )
        data = []
        for disciplina in disciplines:
            info = {
                "name": disciplina.discipline_name,
                "enrolled": disciplina.membership.used_quota,
            }
            data.append(info)
            info = {}
        return data
