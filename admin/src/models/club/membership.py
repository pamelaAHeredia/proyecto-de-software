from typing import List
from decimal import Decimal
from src.models.database import db
from src.models.club.suscription import Suscription
from src.models.club.tariff import Tariff

class Membership(db.Model):
    """
    Clase usada para representar una Membresia

    Atributos
    ---------
    is_active : Boolean
        Indica si la disciplina esta activa para la inscripción.
    registration_quota : Integer
        Indica el cupo total de inscripciones.
    pays_per_year : Integer
        Indica la periodicidad de los pagos.
        Ejemplos:
            1 -> Anual.
            2 -> Bimestral.
            3 -> Trimestral.
            4 -> Cuatrimestral.
            6 -> Semestral.
            12 -> Mensual.
    discipline_id : Integer
        Es el Id de la disciplina asociada a la membresia.
    discipline : Discipline
        Es el objeto disciplina que contiene la relación.
    """

    __tablename__ = "membership"
    __table_args__ = (
        db.UniqueConstraint("discipline_id", name="unique_discipline_id"),
    )
    id = db.Column(db.Integer, primary_key=True, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    registration_quota = db.Column(db.Integer, nullable=False)
    pays_per_year = db.Column(db.Integer, default=12)
    discipline_id = db.Column(db.Integer, db.ForeignKey("discipline.id"))
    discipline = db.relationship("Discipline", back_populates="membership")

    tariffs = db.relationship("Tariff", back_populates="membership")
    suscriptions = db.relationship(
        "Suscription", back_populates="membership", lazy="dynamic"
    )

    @property
    def amount(self) -> Decimal:
        """Retorna el costo de la membresia

        Returns:
            Decimal: Valor de la membresia
        """
        for tariff in self.tariffs:
            if not tariff.date_to:
                return tariff.amount

    @property
    def used_quota(self) -> int:
        """Retorna la cantidad de inscriptos.

        Returns:
            int: Cantidad de inscriptos.
        """
        return self.suscriptions.filter(Suscription.date_to == None).count()

    @property
    def name(self):
        if not self.discipline:
            return 'Cuota Social'
        return self.discipline.discipline_name

    @property
    def has_quota(self) -> bool:
        """Verifica si hay lugar para una inscripcion nueva.

        Returns:
            bool: True si hay lugar para inscribirse.
        """
        return self.registration_quota > self.used_quota

    @property
    def active_suscriptions(self) -> List[Suscription]:
        return self.suscriptions.filter(Suscription.date_to == None)

    def __repr__(self):
        return f"Membresia {self.id}"
