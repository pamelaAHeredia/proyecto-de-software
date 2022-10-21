from decimal import Decimal
from typing import List, Optional
import datetime


from src.models.database import db
from src.errors.database import ExistingData
from src.models.club.member import Member
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

    def list_suscriptions(self, discipline_id: int) -> List[Suscription]:
        """Lista las suscripciones de una disciplina

        Args:
            discipline_id (int): Id de la disciplina.

        Returns:
            List[Suscription]: Lista de todas las suscripciones 
              para esa disciplina.
        """        
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

    def can_suscribe(self, member_id: int, discipline_id: int) -> bool:
        """Verifica que se pueda inscribir a la disciplina.

        Metodo que verifica que el socio se pueda suscribir a la disciplina.
        Para un socio poder inscribirse a la disciplina debe garantizarse los siguintes
        puntos:
            1. El socio debe estar activo, sin deuda y ya no estar inscripto previamente.
            2. La disciplina debe estar activa y tener cupo.

        Args:
            member_id (int): Id del socio.
            discipline_id (int): Id de la disciplina.

        Returns:
            bool: True si se puede inscribir.
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

    def enroll(self, member: Member, membership: Membership) -> Suscription:
        """Inscribe a un socio en una membresia.

        Args:
            member (Member): Un objeto socio
            membership (Membership): Un objeto membresia

        Raises:
            ExistingData: Elsocio ya esta inscripto

        Returns:
            Suscription: La suscripcion del socio a la membresia.
        """        
        if not self._membership_service.member_is_enrolled(
            member.membership_number, membership.discipline_id
        ):
            raise ExistingData(message="El socio ya se encuentra inscripto.")

        suscription = Suscription(
            member_id=member.membership_number, membership_id=membership.id
        )
        db.session.add(suscription)
        db.session.commit()
        return suscription

    def associate_member(self, member_id: int) -> Suscription:
        """Genera la inscripcion a la cuota societaria.

        Cuando un socio es creado llama a este método para
        darlo de alta en la membresia de la cuota societaria.

        Args:
            member_id (int): Id del socio.

        Returns:
            Suscription: La suscripcion del socio a la membresia cuota.
        """        
        social_quota = Membership.query.get(
            1
        )  # Esto es una chanchada hay que mejorarlo
        member = Member.query.filter_by(membership_number=member_id).first()
        suscription = Suscription(membership=social_quota, member=member)
        db.session.add(suscription)
        db.session.commit()
        return suscription
