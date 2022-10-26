from decimal import Decimal
from typing import List, Optional
import datetime
from src.models.database import db
from src.errors import database
from src.models.club.membership import Membership
from src.models.club.tariff import Tariff
from src.models.club.suscription import Suscription
from src.services.discipline import DisciplineService
from src.services.settings import SettingsService



class MembershipService:
    """
    Clase que representa el servicio para el manejo de suscripciones.
    Implementa el patron singleton para que solo se instancie una vez en el sistema.
    """

    _instance = None
    _discipline_service = DisciplineService()
    _settings_service = SettingsService()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MembershipService, cls).__new__(cls)
        return cls._instance

    def membership_active(self, discipline_id: int) -> bool:
        """Retorna si la membresia esta activa.

        Args:
            discipline_id (int): Id de la disciplina perteneciente al a membresia.

        Returns:
            bool: True si está activa.
        """
        return self._discipline_service.active(discipline_id)

    def membership(self, discipline_id):
        return self._discipline_service.membership(discipline_id)

    def suscriptions(self, discipline_id):
        membership = self.membership(discipline_id)
        return membership.active_suscriptions

    def member_is_enrolled(self, member_id: int, discipline_id: int) -> bool:
        """Verifica si un socio esta inscripto a una disciplina.

        Args:
            member_id (int): Id del socio.
            discipline_id (int): Id de la disciplina.

        Returns:
            bool: True si se puede inscribir.
        """
        membership = self.membership(discipline_id)
        cant = membership.suscriptions.filter(
            Suscription.membership_id == membership.id,
            Suscription.member_id == member_id,
            Suscription.date_to == None,
        ).count()
        return cant > 0

    def available_quota(self, discipline_id: int) -> int:
        """Retorna el cupo disponible

        Args:
            discipline_id (int): Id de la disciplina.

        Returns:
            int: Cantidad de cupos discponibles para inscripciones.
        """
        membership = self.membership(discipline_id)
        quota_left = membership.registration_quota - membership.used_quota
        return quota_left

    def used_quota(self, discipline_id: int) -> int:
        """Retorna la cantidad de inscriptos.

        Args:
            discipline_id (int): Id de la disciplina

        Returns:
            int: Cantidad de inscriptos
        """
        membership = self.membership(discipline_id)
        used_quota = membership.used_quota()
        return used_quota

    def create_social_membership(self) -> None:
        """Crea la cuota social inicial usada en el seeds."""
        social_membership = Membership(registration_quota=999999, pays_per_year=12)
        social_membership_tariff = Tariff(
            amount=self._settings_service.get_amount_monthly(),
            membership=social_membership,
        )
        db.session.add_all([social_membership, social_membership_tariff])
        db.session.commit()

    def update_social_membership(self, amount: Decimal) -> None:
        """Actualiza el valor de la cuota social.

        Args:
            amount (Decimal): Nuevo valor de la cuota.
        """
        old_tariff = Tariff.query.filter_by(membership_id=1, date_to=None).first()
        old_tariff.date_to = datetime.datetime.now()
        new_tariff = Tariff(membership_id=1, amount=amount)
        db.session.add_all([old_tariff, new_tariff])
        db.session.commit()
