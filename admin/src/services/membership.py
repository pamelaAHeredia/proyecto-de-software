from decimal import Decimal
from typing import List, Optional
import datetime


from src.models.database import db
from src.models.club.suscription import Suscription
from src.services.discipline import DisciplineService
from src.errors import database


class MembershipService:
    """
    Clase que representa el servicio para el manejo de suscripciones.
    Implementa el patron singleton para que solo se instancie una vez en el sistema.
    """

    _instance = None
    _discipline_service = DisciplineService()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MembershipService, cls).__new__(cls)
        return cls._instance

    def membership_active(self, discipline_id):
        return self._discipline_service.active(discipline_id)

    def _membership(self, discipline_id):
        return self._discipline_service.membership(discipline_id)

    def member_is_enrolled(self, member_id, discipline_id):
        membership = self._membership(discipline_id)
        return membership.suscriptions.filter(
            Suscription.membership_id == membership.id,
            Suscription.member_id == member_id,
            Suscription.date_to == None,
        ).count()

    def available_quota(self, discipline_id):
        membership = self._membership(discipline_id)
        quota_left = membership.registration_quota - self.used_quota(discipline_id)
        return quota_left

    def used_quota(self, discipline_id):
        membership = self._membership(discipline_id)
        used_quota = membership.suscriptions.filter(Suscription.date_to == None).count()
        return used_quota
