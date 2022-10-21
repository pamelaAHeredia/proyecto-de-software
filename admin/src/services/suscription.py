from decimal import Decimal
from typing import List, Optional
import datetime


from src.models.database import db
from src.models.club.membership import Membership
from src.models.club.suscription import Suscription

from src.services.membership import MembershipService
from src.errors import database
from src.services.paginator import Paginator


class SuscriptionService:
    """
    Clase que representa el servicio para el manejo de suscripciones.
    Implementa el patron singleton para que solo se instancie una vez en el sistema.
    """

    _instance = None
    _membership_service = MembershipService()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SuscriptionService, cls).__new__(cls)
        return cls._instance

    def list_suscriptions(self, discipline_id) -> List[Suscription]:
        suscriptions = self._membership_service.suscriptions(discipline_id)
        return suscriptions

    def list_paginated_suscriptions(
        self, discipline_id: int, page: int, items_per_page: int, endpoint: str
    ) -> Paginator:
        """Retorna un paginador con las suscripciones.

        Args:
            page (int): Numero de pagina.
            items_per_page (int): cantidad de registros por página.
            endpoint (str): endpoint para el armado del url_for.

        Returns:
            Paginator: Un paginador.
        """
        suscriptions = self.list_suscriptions(discipline_id)
        return Paginator(suscriptions, page, items_per_page, endpoint)

    def can_suscribe(self, member_id, discipline_id):
        """Verifica que se pueda inscribir a la disciplina.

        Metodo que verifica que el socio se pueda suscribir a la disciplina.
        Para un socio poder inscribirse a la disciplina debe garantizarse los siguintes
        puntos:
            1. El socio debe estar activo, sin deuda y ya no estar inscripto previamente.
            2. La disciplina debe estar activa y tener cupo.

        Args:
            member_id (_type_): _description_
            discipline_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        member_active = (
            Member.query.filter_by(membership_number=member_id).first().is_active
        )
        member_enrolled = (
            True
            if self._membership_service.member_is_enrolled(member_id, discipline_id)
            == 0
            else False
        )
        membership_active = self._membership_service.membership_active(discipline_id)
        membership_has_quota = (
            False
            if self._membership_service.available_quota(discipline_id) == 0
            else True
        )

        return (
            member_active
            and member_enrolled
            and membership_active
            and membership_has_quota
        )

    def enroll(self, member, membership):
        if not self._membership_service.member_is_enrolled(
            member.membership_number, membership.discipline_id
        ):
            print("Ya estaba")
            return False

        suscription = Suscription(
            member_id=member.membership_number, membership_id=membership.id
        )
        db.session.add(suscription)
        db.session.commit()
        return True
        # return self._membership_service.member_is_enrolled(member_id, discipline_id)

    def associate_member(self, member_id):
        social_quota = Membership.query.get(
            1
        )  # Esto es una chanchada hay que mejorarlo
        member = Member.query.filter_by(membership_number=member_id).first()
        suscription = Suscription(membership=social_quota, member=member)
        db.session.add(suscription)
        db.session.commit()
