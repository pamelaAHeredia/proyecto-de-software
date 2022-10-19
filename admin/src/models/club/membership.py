from src.models.database import db


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

    @property
    def amount(self):
        for tariff in self.tariffs:
            if not tariff.date_to:
                return tariff.amount
