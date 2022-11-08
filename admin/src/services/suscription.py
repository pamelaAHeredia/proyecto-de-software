from decimal import Decimal
from typing import Dict, List, Optional
import datetime


from src.models.database import db
from src.errors.database import ExistingData
from src.models.club.member import Member
from src.models.club.membership import Membership
from src.models.club.suscription import Suscription
from src.models.club.member import Member

from src.services.membership import MembershipService
from src.services.movement import MovementService
from src.errors import database
from src.services.paginator import Paginator


class SuscriptionService:
    """
    Clase que representa el servicio para el manejo de suscripciones.
    Implementa el patron singleton para que solo se instancie una vez en el sistema.
    """

    _instance = None
    _membership_service = MembershipService()
    _movements_service = MovementService()

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

    def can_suscribe(self, member_id: int, discipline_id: int) -> Dict[str, bool]:
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
        member_defaulter = self._movements_service.is_defaulter(
            Member.query.filter_by(membership_number=member_id).first()
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
        can_member_suscribe = (
            member_active
            and not member_defaulter
            and member_enrolled
            and membership_active
            and membership_has_quota
        ) 

        result = {
            "can_suscribe": can_member_suscribe,
            "reason": {
                "member_active": member_active,
                "member_defaulter": not member_defaulter,
                "member_enrolled": member_enrolled,
                "membership_active": membership_active,
                "membership_has_quota": membership_has_quota,
            },
        }
        return result

    def _get_suscription(self, member_id: int, membership_id: int) -> Suscription:
        return Suscription.query.filter_by(
            member_id=member_id, membership_id=membership_id, date_to=None
        ).one()

    def leave(self, suscription_id: int) -> Suscription:
        """Baja de un socio a una suscripcion.

        Args:
            suscription_id (Suscription): Id de la suscripcion.

        Returns:
            Suscription: La suscripcion en cuestion.
        """
        suscription = Suscription.query.get(suscription_id)
        suscription.end_suscription()
        db.session.commit()
        return suscription

    def enroll(self, member: Member, membership: Membership) -> Dict:
        """Inscribe a un socio en una membresia.

        Si el socio no ya no se encuentra inscripto a la membresia y
        hay lugar en la membresia y ¿no tiene otras deudas?
        lo inscribe a la membresia.

        Args:
            member (Member): Un objeto socio
            membership (Membership): Un objeto membresia

        Returns:
            Dict: _description_
        """
        member_id = member.membership_number
        discipline_id = membership.discipline_id

        can_member_suscribe = self.can_suscribe(member_id, discipline_id)
        if not can_member_suscribe["can_suscribe"]:
            return can_member_suscribe

        suscription = Suscription(
            member_id=member.membership_number, membership_id=membership.id
        )

        debt_movement = self._movements_service.insert_movement(
            "D",
            membership.amount * -1,
            f"Cuota de {membership.name}",
            member,
        )
        credit_movement = self._movements_service.insert_movement(
            "C",
            membership.amount,
            f"Pago cuota de {membership.name}",
            member,
        )

        db.session.add_all([suscription, debt_movement, credit_movement])
        db.session.commit()
        return can_member_suscribe

    def associate_member(self, member: Member) -> Suscription:
        """Genera la inscripcion a la cuota societaria.

        Cuando un socio es creado llama a este método para
        darlo de alta en la membresia de la cuota societaria.

        Args:
            member_id (int): Id del socio.

        Returns:
            Suscription: La suscripcion del socio a la membresia cuota.
        """
        social_quota = Membership.query.get(1)
        suscription = Suscription(membership=social_quota, member=member)
        debt_movement = self._movements_service.insert_movement(
            "D",
            suscription.amount * -1,
            "Cuota Social Inicial",
            member,
        )
        credit_movement = self._movements_service.insert_movement(
            "C",
            suscription.amount,
            "Pago Cuota Social Inicial",
            member,
        )
        db.session.add_all([member, suscription, debt_movement, credit_movement])
        db.session.commit()
        return suscription
