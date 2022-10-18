from src.models.database import db


class Membership(db.Model):
    """
    Clase usada para representar una Membresia

    Atributos
    ---------
    name : str

    is_active : Boolean
        Indica si la disciplina esta activa para la inscripción.
    deleted : Boolean
        Indica si la disciplina se sigue dando o no.
    """
    __tablename__ = "membership"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    registration_quota = db.Column(db.Integer, nullable=False)
    pays_per_year = db.Column(db.Integer, default=12)
    discipline = db.relationship("Discipline", back_populates="membership", uselist=False)
    tariffs = db.relationship("Tariff", back_populates="membership")
    